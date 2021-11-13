from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Important'),
]


class Project(models.Model):
    _name = "project"
    _description = "Project"

    name = fields.Char(string="Project name", required="True")
    description = fields.Text(string="Description")
    date_of_registration = fields.Datetime(string="Date", default=lambda self: fields.datetime.now())
    currency_id = fields.Many2one(comodel_name="res.currency", string="currency")
    total_price = fields.Monetary(string="Total Price")
    time = fields.Float(string="General time")
    priority = fields.Selection(AVAILABLE_PRIORITIES, select=True)
    worker_ids = fields.Many2many(comodel_name="hr.employee", string="Workers")
    team_lead_id = fields.Many2one(comodel_name="hr.employee", string="Team Lead")
    project_manager_id = fields.Many2one(comodel_name="hr.employee", string="Project Manager")
    task_ids = fields.One2many(comodel_name="task", inverse_name="project_id", string="Tasks")
    project_line_ids = fields.One2many(comodel_name="project.line", inverse_name="project_id", string="Workers")


class ProjectLine(models.Model):
    _name = "project.line"
    _description = "Project Line"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    sold = fields.Float(string="Sold")
    project_id = fields.Many2one(comodel_name="project", string="Worker")