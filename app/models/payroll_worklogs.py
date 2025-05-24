from app.extensions import db

class PayrollWorklog(db.Model):
    __tablename__ = "payroll_worklogs"

    id = db.Column(db.Integer, primary_key=True)

    payroll_id = db.Column(
        db.Integer,
        db.ForeignKey("payroll.id"),
        nullable=False
    )
    worklog_id = db.Column(
        db.Integer,
        db.ForeignKey("worklogs.id"),
        nullable=False
    )

    hours_recorded = db.Column(db.Numeric(5, 2), nullable=False)
    snapshot_locked = db.Column(db.Boolean, nullable=False, server_default=db.text("0"))

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )

    payroll = db.relationship("Payroll", backref="payroll_worklogs")
    worklog = db.relationship("Worklog", backref="payroll_worklogs")
