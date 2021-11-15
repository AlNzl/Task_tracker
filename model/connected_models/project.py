from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ("low", "Low"),
    ("important", "Important"),
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
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")
    worker_ids = fields.Many2many(comodel_name="hr.employee", string="Team")
    team_lead_id = fields.Many2one(comodel_name="hr.employee", string="Team Lead",
                                   domain=[("position_ids.name", "=", "Team Lead")])
    project_manager_id = fields.Many2one(comodel_name="hr.employee", string="Project Manager",
                                         domain=[("position_ids.name", "=", "Project Manager")])
    task_ids = fields.One2many(comodel_name="task", inverse_name="project_id", string="Tasks")
    project_line_ids = fields.One2many(comodel_name="project.line", inverse_name="project_id", string="Workers")
    task_count = fields.Integer(string="Number of task", compute="_compute_count")

    def _compute_count(self):
        for record in self:
            record.task_count = self.env["task"].search_count([("project_id", "=", self.id)])

    @api.onchange("team_lead_id")
    def _onchange_auto_select_team_lead(self):
        for record in self:
            record.worker_ids = [(4, record.team_lead_id.id)]

    @api.onchange("project_manager_id")
    def _onchange_auto_select_project_manager(self):
        for record in self:
            record.worker_ids = [(4, record.project_manager_id.id)]

    def _go_to_tasks(self):
        return {"name": "Tasks",
                "view_mode": "kanban",
                "res_model": "task",
                "type": "ir.actions.act_window",
                "domain": [("project_id", "in", self.ids)]
                }


class ProjectLine(models.Model):
    _name = "project.line"
    _description = "Project Line"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    sold = fields.Float(string="Sold")
    project_id = fields.Many2one(comodel_name="project", string="Worker")
