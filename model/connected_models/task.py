from datetime import datetime, timedelta
from odoo.exceptions import UserError

from odoo import models, fields, api

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Important'),
]


class Task(models.Model):
    _name = "task"
    _description = "Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_default_stage_id(self):
        stage_id = self.env.ref("Task_tracker.task_stage_backlog").id
        return stage_id

    name = fields.Char(string="Task name", required=True)
    description = fields.Text(string="Description")
    priority = fields.Selection(AVAILABLE_PRIORITIES)
    total_time = fields.Float(string="Total time")

    stage_id = fields.Many2one(comodel_name="stage", string="Stage", default=_get_default_stage_id,
                               track_visibility="onchange")

    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")
    responsible_id = fields.Many2one(comodel_name="hr.employee", string="Responsible person")
    project_id = fields.Many2one(comodel_name="project", string="Project", ondelete="cascade")
    time_tracker_line_ids = fields.One2many(comodel_name="time.tracker.line", inverse_name="task_id",
                                            string="Time tracker")
    timer = fields.Datetime(store=True)

    @api.constrains("stage_id")
    def check_stage(self):
        """
        Here we check the stage, if it is in 'In progress', we start the timer
        :return: Timer(type: datetime)
        """
        if self.stage_id.name == "In progress":
            timer = datetime.now() + timedelta(hours=self.total_time, days=1)
            self.timer = timer
            return print(self.timer)

    def write(self, vals):
        """
        If datetime now < timer, we are not allowed to change
        :param vals: info Time tracker
        :return: if: error else: vals
        """
        if self.timer < datetime.now():
            raise UserError("You can no longer change Time tracker")
        else:
            res = super(Task, self).write(vals)
            return res


class TimeTrackerLine(models.Model):
    _name = "time.tracker.line"

    task_id = fields.Many2one(comodel_name="task", string="Time Tracker")
    worker_id = fields.Many2one(comodel_name="hr.employee", string="Worker")

    description = fields.Text(string="Description")
    date = fields.Date(string="Date")
    time = fields.Float(string="Time spent")
