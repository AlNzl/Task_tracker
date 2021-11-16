from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReferenceBook(models.Model):
    _name = "reference.book"
    _description = "Reference Book"

    name = fields.Char(string="Profession name", required=True)

    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")

    @api.onchange("name")
    def _onchange_name(self):
        """When creating a duplicate calls UserError"""
        if self.env["reference.book"].search([("name", "=", self.name)]):
            raise UserError(_("%s already exists!!!" % (self.name)))

    @api.constrains("employee_ids")
    def _pass_tl_to_developer(self):
        """When adding a team lead, pass it to developers """
        if self.name == self.env.ref("Task_tracker.reference_book_team_lead").name:
            team_leads = self.env["hr.employee"].search(
                [("position_ids", "=", self.env.ref("Task_tracker.reference_book_team_lead").name)])
            for team_lead in team_leads:
                team_lead.position_ids = [(4, self.env.ref("Task_tracker.reference_book_developer").id)]
