from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .project import AVAILABLE_PRIORITIES
from datetime import datetime, timedelta


class Task(models.Model):
    _name = "task"
    _description = "Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_stage_id(self):
        stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        return stage_id

    name = fields.Char(string="Task name", required=True)
    description = fields.Text(string="Description")
    ba_time = fields.Float(string="BA time")
    total_time = fields.Float(string="Total time", compute="_compute_total_time")
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id,
                               track_visibility="onchange", group_expand="_read_group_stage_ids")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker",
                                domain=lambda self: [
                                    ("position_ids.id", "=", self.env.ref("Task_tracker.reference_book_developer").id)])
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person",
                                     domain=lambda self: [("position_ids.id", "=",
                                                           self.env.ref("Task_tracker.reference_book_team_lead").id)])
    project_id = fields.Many2one(comodel_name="project", string="Project", ondelete="cascade")
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="task_id",
                                            string="Time tracker")
    timer = fields.Datetime(string="Timer")

    def create_stage_dct(self):
        """
        Create dict with stages
        """
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
            test: {"previous": review, "next": done}
        }
        return stage_dct

    @api.model
    def change_stage(self):
        """
        Change stage on tree view if currents stages the same
        """
        stage_dct = self.create_stage_dct()
        acceptance_criteria = [len(self.stage_id) == 1,
                               self.stage_id.id in stage_dct,
                               self.stage_id.id != self.env.ref("Task_tracker.task_stage_done").id
                               ]
        if all(acceptance_criteria):
            stage_id = stage_dct[self.stage_id.id]["next"]
            self.env["task"].browse(self._context.get("active_ids")).update({"stage_id": stage_id})
        else:
            raise UserError(_("The stage can't be changed."))

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """
        Group stage_ids default
        """
        stage_ids = self.env["stage"].search([])
        return stage_ids

    @api.onchange("project_id")
    def _onchange_project_id(self):
        """
        Inserts a value from team_lead_id to responsible_id
        """
        for record in self:
            record.responsible_id = record.project_id.team_lead_id.id

    def _compute_total_time(self):
        """
        Calculates total time
        """
        for record in self:
            record.total_time = record.ba_time * record.worker_id.employee_coefficient

    @api.constrains("stage_id")
    def check_stage(self):
        """
        Here we check the stage, if it is in 'In progress', we start the timer
        """
        if self.stage_id.id == self.env.ref("Task_tracker.task_stage_progress").id:
            timer = datetime.now() + timedelta(hours=self.total_time, days=1)
            self.timer = timer
            return timer

    def check_stages(self, vals, method_name):
        bl_stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        ready_stage_id = self.env.ref("Task_tracker.task_stage_ready").id

        if method_name == "write":
            check_stage = self.stage_id.id == bl_stage_id or self.stage_id.id == ready_stage_id

        elif method_name == "create":
            check_stage = vals.get("stage_id") == bl_stage_id and vals.get("stage_id") == ready_stage_id

        if not check_stage:
            if not self.timer or self.timer > datetime.now():
                return True
            else:
                raise UserError(_("You can no longer change Time tracker"))
        else:
            if "time_tracker_line_ids" in vals:
                raise UserError(_("You can edit Time tracker only after stage 'Ready'"))
            else:
                return True

        # if not check_stage:
        #     if not self.timer or self.timer > datetime.now():
        #         res = super(Task, self).create(vals)
        #         return res
        #     else:
        #         raise UserError(_(error_time))
        # else:
        #     if "time_tracker_line_ids" in vals:
        #         raise UserError(_(error_stage))
        #     else:
        #         return res

    @api.model
    def create(self, vals):
        """
        If datetime now < timer, we are not allowed to change
        """
        self.check_stages(vals, "create")
        if self.check_stages:
            res = super(Task, self).create(vals)
            return res

        # bl = self.env.ref("Task_tracker.task_stage_backlog").id
        # ready = self.env.ref("Task_tracker.task_stage_ready").id
        # if vals.get("stage_id") != bl and vals.get("stage_id") != ready:
        #     if not self.timer or self.timer > datetime.now():
        #         res = super(Task, self).create(vals)
        #         return res
        #     else:
        #         raise UserError(_("You can no longer change Time tracker"))
        # else:
        #     if "time_tracker_line_ids" in vals:
        #         raise UserError(_("You can edit Time tracker only after stage 'Ready'"))
        #     else:
        #         res = super(Task, self).create(vals)
        #         return res

    def write(self, vals):
        """
        If datetime now < timer, we are not allowed to change
        """
        self.check_stages(vals, "write")
        if self.check_stages:
            res = super(Task, self).write(vals)
            return res
        # bl = self.env.ref("Task_tracker.task_stage_backlog").id
        # ready = self.env.ref("Task_tracker.task_stage_ready").id
        # if self.stage_id.id != bl and self.stage_id.id != ready:
        #     if not self.timer or self.timer > datetime.now():
        #         res = super(Task, self).write(vals)
        #         return res
        #     else:
        #         raise UserError(_("You can no longer change Time tracker"))
        # else:
        #     if "time_tracker_line_ids" in vals:
        #         raise UserError(_("You can edit Time tracker only after stage 'Ready'"))
        #     else:
        #         res = super(Task, self).write(vals)
        #         return res


class TimeTrackerLine(models.Model):
    _name = "time.tracker.line"

    task_id = fields.Many2one(comodel_name="task", string="Time Tracker")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")

    description = fields.Text(string="Description")
    date = fields.Date(string="Date")
    time = fields.Float(string="Time spent")
