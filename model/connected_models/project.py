from odoo import models, fields, api, _
from odoo.exceptions import UserError

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
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    total_price = fields.Monetary(string="Total Price")
    time = fields.Float(string="General time")
    priority = fields.Selection(AVAILABLE_PRIORITIES, string="Priority")
    worker_ids = fields.Many2many(comodel_name="hr.employee", string="Team")
    team_lead_id = fields.Many2one(comodel_name="hr.employee", string="Team Lead",
                                   domain=lambda self: [("position_ids.id", "=",
                                                         self.env.ref("Task_tracker.reference_book_team_lead").id)],
                                   required=True)
    project_manager_id = fields.Many2one(comodel_name="hr.employee", string="Project Manager",
                                         domain=lambda self: [("position_ids.id", "=", self.env.ref(
                                             "Task_tracker.reference_book_project_manager").id)])
    task_ids = fields.One2many(comodel_name="task", inverse_name="project_id", string="Tasks")
    project_line_ids = fields.One2many(comodel_name="project.line", inverse_name="project_id", string="Workers")

    task_count = fields.Integer(string="Number of task", compute="_compute_count")
    project_profit = fields.Float(string="Profit for project", compute="_compute_project_profit", store=True)

    @api.depends("total_price", "task_ids.time_tracker_line_ids")
    def _compute_project_profit(self):
        """Count the project profit"""
        for record in self:
            record.project_profit = record.total_price - sum(record.task_ids.mapped("employees_salary"))

    def _compute_count(self):
        """Counts the number of tasks in the project"""
        for record in self:
            record.task_count = self.env["task"].search_count([("project_id", "=", self.id)])

    @api.onchange("name")
    def _onchange_name(self):
        """Func check duplicate in project name"""
        if self.env["project"].search([("name", "=", self.name)]):
            raise UserError(_("Project with the same name already exists"))

    @api.onchange("team_lead_id")
    def _onchange_team_lead_id(self):
        """Link worker with TL"""
        for record in self:
            record.worker_ids = [(4, record.team_lead_id.id)]

    @api.onchange("project_manager_id")
    def _onchange_project_manager_id(self):
        """Link worker with PM"""
        for record in self:
            record.worker_ids = [(4, record.project_manager_id.id)]

    def action_to_tasks(self):
        """In tree view the server activity , action to tasks of only the selected projects"""
        action = {
            "name": _("Tasks"),
            "view_mode": "kanban",
            "res_model": "task",
            "type": "ir.actions.act_window",
            "domain": [("project_id", "in", self.ids)]
        }
        return action


class ProjectLine(models.Model):
    _name = "project.line"
    _description = "Project Line"

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        """Does not add the employee to the project.line if it already exists"""
        for record in self:
            employee_ids = record.project_id.project_line_ids.employee_id.ids
            employee_ids.extend([record.project_id.team_lead_id.id, record.project_id.project_manager_id.id])
            return {"domain": {
                "employee_id": [("id", "not in", employee_ids)]}}

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    position = fields.Char(related="employee_id.position_ids.name", string="Profession")
    sold = fields.Float(string="Sold")
    project_id = fields.Many2one(comodel_name="project", string="Project")

    employee_profit = fields.Float(string="Profit", compute="_compute_total_profit", store=True)

    @api.depends("employee_id.time_tracker_line_ids.time")
    def _compute_total_profit(self):
        """Compute total profit for project from employee"""
        for record in self:
            person_time = sum(record.employee_id.time_tracker_line_ids.mapped("time"))
            task_time = record.employee_id.task_ids.total_time
            record.employee_profit = record.sold * task_time - record.employee_id.employee_hour * person_time

    @api.constrains("sold")
    def _constrains_sold(self):
        """Checks sold for non-negativity"""
        for record in self:
            if record.sold < 0:
                raise UserError(_("Selling price '%s' less than 0" % record.sold))
