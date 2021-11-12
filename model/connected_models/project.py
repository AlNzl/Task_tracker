from odoo import models, fields, api


class Project(models.Model):
    _name = "project"
    _description = "Project"

    name = fields.Char(string="Project name")
    description = fields.Text(string="Description")
    currency_id = fields.Many2one(comodel_name="res.currency", string="currency")
    total_price = fields.Monetary(string="Total Price")
    time = fields.Float(string="General time")
    worker_ids = fields.Many2many(comodel_name="hr.employee", string="Workers")
    team_lead = fields.Many2one(comodel_name="hr.employee", string="Team Lead")
    project_manager = fields.Many2one(comodel_name="hr.employee", string="Project manager")
    #price_for_hour = fields.Float(string="Price for hour")  # TODO make compute field
    task_ids = fields.One2many(comodel_name="task", inverse_name="project_id", string="Tasks")
    project_line_ids = fields.One2many(comodel_name="project.line", inverse_name="project_id", string="Workers")

class ProjectLine(models.Model):
    _name = "project.line"
    _description = "Project Line"

    employee_id = fields.Many2one(comodel_name="hr.employee",string="Employee")
    sold = fields.Float(string="Sold")
    project_id = fields.Many2one(comodel_name="project",string="Worker")