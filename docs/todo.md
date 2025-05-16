jsonify services and routes for proper api responses

example:
```python
    if not success:
        return jsonify({'error': 'Delete failed or already deleted'}), 400
    return jsonify({'message': 'Work log deleted'}), 200
```

also serialize data in the models:
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