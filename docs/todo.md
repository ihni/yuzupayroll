add to dict for easier access in templates
```python
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date_worked': self.date_worked.isoformat(),
            'hours_worked': self.hours_worked,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

also first validate in routers layer if data is valid too before passing it to services to process

update services update function especially when checking fields(just check dict if value is changed so logging is shorter---loop it!)