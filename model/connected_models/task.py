from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Important'),
]


class Task(models.Model):
    _name = "task"
    _description = "Task"

    name = fields.Char(string="Task")
    description = fields.Text(string="Description")
    priority = fields.Selection(AVAILABLE_PRIORITIES, select=True)
    total_time = fields.Float(string="Total time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project")
    time_ids = fields.One2many(comodel_name="time.tracker", inverse_name="task_id", string="Time tracker")
