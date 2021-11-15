from odoo import models, fields, api
from odoo.exceptions import UserError

AVAILABLE_PRIORITIES = [
    ('low', 'Low'),
    ('important', 'Important'),
]


class Task(models.Model):
    _name = "task"
    _description = "Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_stage_id(self):
        stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        return stage_id

    name = fields.Char(string="Task name", required=True)
    description = fields.Text(string="Description")
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")
    total_time = fields.Float(string="Total time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id,
                               track_visibility="onchange", group_expand="_read_group_stage_ids")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project", ondelete="cascade")
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="task_id", string="Time tracker")

    @api.model
    def _change_stage(self):
        if len(self.stage_id) == 1 and self.stage_id.id < self.env.ref("Task_tracker.task_stage_done").id:
            stage_id = self.stage_id.id + 1
            self.env["task"].browse(self._context.get("active_ids")).update({"stage_id": stage_id})
        else:
            raise UserError("The stage can't be changed.")

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['stage'].search([])
        return stage_ids


class TimeTrackerLine(models.Model):
    _name = 'time.tracker.line'

    task_id = fields.Many2one(comodel_name='task', string='Time Tracker')
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")

    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    time = fields.Float(string='Time spent')



