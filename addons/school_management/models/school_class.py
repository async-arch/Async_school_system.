from odoo import fields, models  # type: ignore


class SchoolClass(models.Model):
    _name = 'school.class'  # MUST MATCH XML res_model
    _description = 'School Grade / Class'
    _order = 'name, section, academic_year'

    name = fields.Char(string='Grade / Class', required=True)
    section = fields.Char(string='Section')
    academic_year = fields.Char(string='Academic Year', required=True)
    student_ids = fields.One2many('school.student', 'class_id', string='Students')

    _sql_constraints = [
        (
            'class_section_year_unique',
            'unique(name, section, academic_year)',
            'This class/section already exists for this academic year.',
        ),
    ]