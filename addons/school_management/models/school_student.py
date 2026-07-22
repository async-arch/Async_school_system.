import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Registration'
    _order = 'name'

    regno = fields.Char(string='Registration Number', required=True, copy=False, readonly=True, default='New')
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

    registration_status = fields.Selection([
        ('draft', 'Draft'),
        ('incomplete', 'Incomplete'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Registration Status', default='draft')
    registration_date = fields.Date(string='Registration Date', default=lambda self: fields.Date.context_today(self), required=True)
    responsible_staff_id = fields.Many2one('res.users', string='Responsible Staff', default=lambda self: self.env.user)
    previous_school = fields.Char(string='Previous School')
    notes = fields.Text(string='Notes')

    birth_certificate = fields.Binary(string='Birth Certificate', attachment=True)
    birth_certificate_filename = fields.Char(string='Birth Certificate Filename')
    previous_grade_document = fields.Binary(string='Previous Grade Document', attachment=True)
    previous_grade_document_filename = fields.Char(string='Previous Grade Document Filename')

    class_id = fields.Many2one('school.class', string='Grade / Class', required=True)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('regno_unique', 'unique(regno)', 'Registration number must be unique.'),
    ]

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.age = relativedelta(today, rec.date_of_birth).years if rec.date_of_birth else 0

    def _validate_submission_requirements(self):
        missing = []
        if not self.name:
            missing.append('Full Name')
        if not self.date_of_birth:
            missing.append('Date of Birth')
        if not self.guardian_name:
            missing.append('Parent / Guardian Name')
        if not self.guardian_phone or len(re.sub(r'\D', '', self.guardian_phone)) < 7:
            missing.append('Guardian Phone (must contain at least 7 digits)')
        if not self.class_id:
            missing.append('Grade / Class')
        if not self.birth_certificate:
            missing.append('Birth Certificate')
        if not self.previous_grade_document:
            missing.append('Previous Grade Document')
        return missing

    @api.constrains('registration_status', 'name', 'date_of_birth', 'guardian_name',
                     'guardian_phone', 'class_id', 'birth_certificate', 'previous_grade_document')
    def _check_required_fields_for_submission(self):
        for rec in self:
            if rec.registration_status not in ('submitted', 'approved'):
                continue
            missing = rec._validate_submission_requirements()
            if missing:
                raise ValidationError(
                    "Cannot mark the student as %s while the following required fields are missing: %s"
                    % (rec.registration_status.title(), ', '.join(missing))
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('regno', 'New') == 'New':
                vals['regno'] = self.env['ir.sequence'].next_by_code('school.student') or 'New'
        return super().create(vals_list)

    def action_mark_submitted(self):
        for rec in self:
            missing = rec._validate_submission_requirements()
            if missing:
                raise ValidationError(
                    "Cannot submit: missing %s" % ', '.join(missing)
                )
            rec.registration_status = 'submitted'

    def action_mark_approved(self):
        for rec in self:
            if rec.registration_status != 'submitted':
                raise ValidationError("Only submitted registrations can be approved.")
            rec.registration_status = 'approved'