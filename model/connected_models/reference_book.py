from odoo import models, fields, api


class ReferenceBook(models.Model):
    _name = "reference.book"
    _description = "Reference Book"

    name = fields.Char(string="Profession name", required=True)

    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")



