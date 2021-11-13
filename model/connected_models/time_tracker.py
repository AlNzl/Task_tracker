from odoo import models, fields, api


class TimeTracker(models.Model):
    _name = "time.tracker"
    _description = "Time Tracker"

    total_time = fields.Float(string='Total task time')
    description = fields.Text(string="Description")
    data = fields.Date(string="Date")
    time = fields.Float(string="Time spent")

    task_id = fields.Many2one(comodel_name="task", string="Task")
