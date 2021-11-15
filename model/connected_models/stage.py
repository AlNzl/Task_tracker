from odoo import models, fields, api


class Stage(models.Model):
    """Model stage"""
    _name = "stage"
    _description = "Stage"

    name = fields.Char(string="Stage")
    
    task_ids = fields.One2many(comodel_name="task", inverse_name="stage_id", string="Task")

