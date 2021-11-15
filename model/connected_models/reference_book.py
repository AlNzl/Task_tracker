from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReferenceBook(models.Model):
    _name = "reference.book"
    _description = "Reference Book"

    name = fields.Char(string="Profession name", required=True)

    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")

    @api.onchange('name')
    def check_duplicate_name(self):
        if self.env["reference.book"].search([("name", '=', self.name)]):
            raise UserError(_(f"{self.name} already exists!!!"))



