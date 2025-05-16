from datetime import datetime, timezone
from app.extensions import db

def utc_now():
    return datetime.now(timezone.utc)

class SoftDeleteMixin:
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), default=None, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = utc_now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None

    @classmethod
    def query_not_deleted(cls):
        return cls.query.filter_by(is_deleted=False)