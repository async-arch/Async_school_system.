from odoo import models, fields # type: ignore

class SchoolStudent(models.Model):
    _name = 'school.student'  # <--- MUST match res_model in XML exactly!
    _description = 'School Student'

    name = fields.Char(string='Name', required=True)