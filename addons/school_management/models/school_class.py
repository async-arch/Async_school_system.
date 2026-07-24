from odoo import models, fields # type: ignore

class SchoolClass(models.Model):
    _name = 'school.class'  # <-- MUST MATCH XML res_model
    _description = 'School Class'