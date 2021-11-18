from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .project import AVAILABLE_PRIORITIES
from datetime import datetime, timedelta


class Task(models.Model):
    _name = "task"
    _description = "Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_stage_id(self):
        """Get default stage id"""
        stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        return stage_id

    name = fields.Char(string="Task name", required=True)
    description = fields.Text(string="Description")
    time_left = fields.Float(string="Time left", compute="_compute_time_left", store=True)
    ba_time = fields.Float(string="BA time")
    total_time = fields.Float(string="Total time", compute="_compute_total_time", store=True)
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id,
                               track_visibility="onchange", group_expand="_read_group_stage_ids")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker",
                                domain=lambda self: [
                                    ("position_ids.id", "=", self.env.ref("Task_tracker.reference_book_developer").id)])
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person",
                                     domain=lambda self: [("position_ids.id", "=",
                                                           self.env.ref("Task_tracker.reference_book_team_lead").id)])
    project_id = fields.Many2one(comodel_name="project", string="Project", ondelete="cascade", required=True)
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="task_id",
                                            string="Time tracker")
    timer = fields.Datetime(string="Timer")

    task_progress = fields.Float(string="Progress", compute="_compute_task_progress")

    @api.depends("time_tracker_line_ids.time", "total_time")
    def _compute_time_left(self):
        """Calculates how much time left to complete the task"""
        for record in self:
            record.time_left = record.total_time - sum(record.time_tracker_line_ids.mapped("time"))

    def _compute_task_progress(self):
        """Calculates the percentage of completion of the task"""
        for record in self:
            try:
                record.task_progress = sum(record.time_tracker_line_ids.mapped("time")) * 100 / record.total_time
            except ZeroDivisionError:
                pass
            if record.task_progress >= 100:
                record.task_progress = 100

    def create_stage_dct(self):
        """Create dict with stages"""
        back = self.env.ref("Task_tracker.task_stage_backlog").id
        ready = self.env.ref("Task_tracker.task_stage_ready").id
        progress = self.env.ref("Task_tracker.task_stage_progress").id
        review = self.env.ref("Task_tracker.task_stage_review").id
        test = self.env.ref("Task_tracker.task_stage_test").id
        done = self.env.ref("Task_tracker.task_stage_done").id

        stage_dct = {
            back: {"next": ready},
            ready: {"previous": back, "next": progress},
            progress: {"previous": ready, "next": review},
            review: {"previous": test, "next": progress},
            test: {"previous": review, "next": done},
            done: {"previous": test},
        }
        return stage_dct

    @api.model
    def change_stage(self):
        """Change stage on tree view if currents stages the same"""
        stage_dct = self.create_stage_dct()
        task_done_id = self.env.ref("Task_tracker.task_stage_done").id
        if len(self.stage_id) == 1 and self.stage_id.id in stage_dct and self.stage_id.id != task_done_id:
            stage_id = stage_dct[self.stage_id.id]["next"]
            for record in self:
                record.stage_id = stage_id
        else:
            raise UserError(_("The stage can't be changed."))

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """Group stage_ids default"""
        stage_ids = self.env["stage"].search([])
        return stage_ids

    @api.depends("ba_time", "worker_id.employee_coefficient")
    def _compute_total_time(self):
        """Calculates total time"""
        for record in self:
            record.total_time = record.ba_time * record.worker_id.employee_coefficient

    @api.constrains("stage_id")
    def check_stage(self):
        """Here we check the stage, if it is in 'In progress', we start the timer"""
        if self.stage_id.id == self.env.ref("Task_tracker.task_stage_progress").id:
            timer = datetime.now() + timedelta(hours=self.total_time, days=1)
            self.timer = timer

    @api.constrains("stage_id")
    def _constrains_stage_id(self):
        """Here we check the stage, if it is in 'Review', pass Team Lead in responsible_id"""
        for record in self:
            if record.stage_id.id == self.env.ref("Task_tracker.task_stage_review").id:
                record.responsible_id = record.project_id.team_lead_id.id

    @api.onchange("stage_id")
    def _onchange_stage_id(self):
        """Changing stage only to next or previous"""
        stage_dct = self.create_stage_dct()
        origin_id = self._origin.stage_id.id
        current_id = self.stage_id.id
        if origin_id in stage_dct:
            is_next = stage_dct[origin_id].get("next") == current_id
            is_previous = stage_dct[origin_id].get("previous") == current_id
            if not is_previous and not is_next:
                raise UserError(_("The stage can't be changed."))
        self._onchange_stage_to_review(origin_id, current_id)

    @api.onchange("stage_id")
    def _onchange_stage_to_review(self, origin_id=None, current_id=None):
        """Put responsible on the task when changing stage from 'in progress' to 'review'"""
        progress_id = self.env.ref("Task_tracker.task_stage_progress").id
        review_id = self.env.ref("Task_tracker.task_stage_review").id
        if origin_id == progress_id and current_id == review_id:
            self.responsible_id = self.project_id.team_lead_id.id

    def check_stages(self, vals, method_name):
        """Checking stage and is it allowed to create and write"""
        bl_stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        ready_stage_id = self.env.ref("Task_tracker.task_stage_ready").id
        check_timer_id = not self.timer or self.timer > datetime.now()

        if method_name == "write":
            check_stage = self.stage_id.id == bl_stage_id or self.stage_id.id == ready_stage_id
            check_info = "time_tracker_line_ids" in vals

        elif method_name == "create":
            check_stage = vals.get("stage_id") == bl_stage_id or vals.get("stage_id") == ready_stage_id
            check_info = vals.get("time_tracker_line_ids")

        if not check_stage and not check_timer_id:
            raise UserError(_("You can no longer change Time tracker"))
        elif check_stage and check_info:
            raise UserError(_("You can edit Time tracker only after stage 'Ready'"))

    @api.model
    def create(self, vals):
        """Check in check_stages and if everything is ok create"""
        self.check_stages(vals, "create")
        res = super(Task, self).create(vals)
        return res

    def write(self, vals):
        """Check in check_stages and if everything is ok write"""
        self.check_stages(vals, "write")
        res = super(Task, self).write(vals)
        return res


class TimeTrackerLine(models.Model):
    _name = "time.tracker.line"

    task_id = fields.Many2one(comodel_name="task", string="Time Tracker")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")

    description = fields.Text(string="Description")
    date = fields.Date(string="Date")
    time = fields.Float(string="Time spent")

    @api.model
    def create(self, vals):
        """When add new worker, hiw name pass to chatter"""
        res = super(TimeTrackerLine, self).create(vals)
        msg = _("New worker: %s" % res.worker_id.name)
        res.task_id.message_post(body=msg)
        return res
