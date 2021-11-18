from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReferenceBook(models.Model):
    _name = "reference.book"
    _description = "Reference Book"

    name = fields.Char(string="Profession", required=True)
    employee_ids_group = fields.Char(string="Name", compute="compute_employee_name", store=True)

    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")

    @api.depends("employee_ids")
    def compute_employee_name(self):
        """Get name from employee_ids and add to employee_ids_group"""
        for record in self:
            if record.employee_ids:
                tag_group = ",".join([p.name for p in record.employee_ids])
            else:
                tag_group = ""
            record.employee_ids_group = tag_group

    @api.onchange("name")
    def _onchange_name(self):
        """When creating a duplicate calls UserError"""
        if self.env["reference.book"].search([("name", "=", self.name)]):
            raise UserError(_("%s already exists!!!" % self.name))

    @api.constrains("employee_ids")
    def _constrains_employee_ids(self):
        """When adding a team lead, pass it to developers """
        tl_id = self.env.ref("Task_tracker.reference_book_team_lead").id
        if self.id == tl_id:
            team_lead_ids = self.env["hr.employee"].search([("position_ids", "=", tl_id)])
            for team_lead_id in team_lead_ids:
                team_lead_id.position_ids = [(4, self.env.ref("Task_tracker.reference_book_developer").id)]
