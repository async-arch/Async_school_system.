from odoo import fields, models


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Grade / Class'
    name = fields.Char(string='Grade / Class', required=True)
    section = fields.Char(string='Section')
    academic_year = fields.Char(string='Academic Year', required=True)

    _sql_constraints = [
        ('class_section_year_unique', 'unique(name, section, academic_year)',
         'This class/section already exists for this academic year.'),
    ]