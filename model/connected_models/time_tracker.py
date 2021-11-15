from odoo import models, fields, api


class TimeTracker(models.Model):
    """Model time tracker"""
    _name = "time.tracker"
    _description = "Time Tracker"

    date = fields.Date(string="Date")
    description = fields.Text(string="Description")

    time = fields.Float(string="Time spent")

    task_id = fields.Many2one(comodel_name="task", string="Task")
