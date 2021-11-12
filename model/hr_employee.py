from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_coefficient = fields.Float(string="Employee coefficient")
    currency_id = fields.Many2one("res.currency", string="currency")
    employee_hour = fields.Monetary(string="Employee hour")
    position = fields.Selection(selection=[('team_lead', 'Team Lead'), ('pm', 'PM'), ('developer', 'Developer'), ('ba', 'BA')])

    worker_ids = fields.One2many(comodel_name="task", inverse_name="worker_id", string="Workers")
