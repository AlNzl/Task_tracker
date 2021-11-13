from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Important'),
]


class Task(models.Model):
    _name = "task"
    _description = "Task"

    def _get_default_stage_id(self):
        stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        return stage_id

    name = fields.Char(string="Task")
    description = fields.Text(string="Description")
    priority = fields.Selection(AVAILABLE_PRIORITIES, select=True)
    total_time = fields.Float(string="Total time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id)

    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project")
    time_ids = fields.One2many(comodel_name="time.tracker", inverse_name="task_id", string="Time tracker")


