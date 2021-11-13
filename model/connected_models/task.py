from odoo import models, fields, api


class Task(models.Model):
    _name = "task"
    _description = "Task"

    name = fields.Char(string="Task")
    description = fields.Text(string="Description")
    priority = fields.Selection(selection=[('a', '1'), ('b', '2'), ('c', '3'), ('d', '4'), ('e', '5')])
    total_time = fields.Float(string="Total time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project")
    time_ids = fields.One2many(comodel_name="time.tracker", inverse_name="task_id", string="Time tracker")

    def create_time_tracker(self):
        if self.env['task'].search([('total_time', '=', self.total_time)]):
            self.name = 'The task already exists '
        else:
            info = {
                'total_time': self.total_time,
                'task_id': self.time_ids
            }
            self.env['time.tracker'].create(info)
