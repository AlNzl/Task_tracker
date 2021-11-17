from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_coefficient = fields.Float(string="Employee coefficient", help="Coefficient must more than 0 !")
    currency_id = fields.Many2one("res.currency", string="Currency")
    employee_hour = fields.Monetary(string="Employee hour")

    task_ids = fields.One2many(comodel_name="task", inverse_name="worker_id", string="Tasks")
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="worker_id", string="Worker")

    position_ids = fields.Many2many(comodel_name="reference.book", string="Job Position")

    @api.constrains("employee_coefficient")
    def _constrains_employee_coefficient(self):
        """Checks coefficient for non-negativity"""
        for record in self:
            if record.employee_coefficient < 0:
                raise ValidationError(_("Your coefficient '%s' less than 0" % record.employee_coefficient))
