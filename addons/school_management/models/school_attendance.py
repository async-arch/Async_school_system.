from odoo import fields, models  # type: ignore


class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "Student Attendance"
    _order = "date desc"

    student_id = fields.Many2one(
        "school.student",
        string="Student",
        required=True
    )

    class_id = fields.Many2one(
        "school.class",
        string="Class",
        related="student_id.class_id",
        store=True
    )

    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today
    )

    status = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
            ("late", "Late"),
        ],
        string="Status",
        required=True,
        default="present"
    )

    note = fields.Text(
        string="Remarks"
    )

    _sql_constraints = [
        (
            "student_date_unique",
            "unique(student_id, date)",
            "Attendance already exists for this student on this date."
        )
    ]