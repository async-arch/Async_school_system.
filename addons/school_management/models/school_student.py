from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Registration'
    _order = 'name'

    regno = fields.Char(string='Registration Number', required=True, copy=False, readonly=True, default=lambda self: ('New'))
    name = fields.Char(string='Full Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')

    guardian_name = fields.Char(string='Parent / Guardian Name', required=True)
    guardian_phone = fields.Char(string='Guardian Phone', required=True)

    class_id = fields.Many2one('school.class', string='Grade / Class', required=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.age = relativedelta(today, rec.date_of_birth).years if rec.date_of_birth else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('regno', 'New') == 'New':
                vals['regno'] = self.env['ir.sequence'].next_by_code('school.student') or 'New'
        return super().create(vals_list)