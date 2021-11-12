from odoo import models, fields, api


class TimeTracker(models.Model):
    _name = "time.tracker"
    _description = "TimeTracker"

    description = fields.Text(string="Description")
    data = fields.Date(string="Date")
    time = fields.Float(string="Time")  # TODO check field

    task_id = fields.Many2one(comodel_name="task", string="Task")
