from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Important'),
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
    priority = fields.Selection(AVAILABLE_PRIORITIES)
    ba_time = fields.Float(string="BA time")
    total_time = fields.Float(string="Total time", compute="_compute_total_time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id,
                               track_visibility="onchange")

    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker", domain=[("position_ids.name", "=", "Developer")])
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project", ondelete="cascade")
    time_ids = fields.One2many(comodel_name="time.tracker", inverse_name="task_id", string="Time tracker")
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="task_id", string="Time tracker")

    @api.onchange("project_id")
    def _onchange_get_responsible_person(self):
        for record in self:
            record.responsible_id = record.project_id.team_lead_id.id

    def _compute_total_time(self):
        for record in self:
            record.total_time = record.ba_time * record.worker_id.employee_coefficient


class TimeTrackerLine(models.Model):
    _name = 'time.tracker.line'

    task_id = fields.Many2one(comodel_name='task', string='Time Tracker')
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")

    description = fields.Text(string='Description')
    date = fields.Date(string='Date')
    time = fields.Float(string='Time spent')





