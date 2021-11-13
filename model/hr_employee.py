from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_coefficient = fields.Float(string="Employee coefficient")
    currency_id = fields.Many2one("res.currency", string="currency")
    employee_hour = fields.Monetary(string="Employee hour")
    # position = fields.Selection(selection=[('team_lead', 'Team Lead'), ('pm', 'PM'), ('developer', 'Developer'), ('ba', 'BA'), ('dev_tl', 'Developer or Team Lead')])

    task_ids = fields.One2many(comodel_name="task", inverse_name="worker_id", string="Tasks")  # Tut taski dolzni bit'

    position_ids = fields.Many2many(comodel_name="reference.book", string="Positions")


