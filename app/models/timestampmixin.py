from datetime import datetime, timezone
from app.extensions import db
from functools import partial

utc_now = partial(datetime.now, timezone.utc)

class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=utc_now)
    updated_at = db.Column(db.DateTime(timezone=True), default=utc_now, onupdate=utc_now)