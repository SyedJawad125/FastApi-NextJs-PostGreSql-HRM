# app/models/__init__.py or app/models/events.py
from sqlalchemy import event
from sqlalchemy.orm import Session
from app.utils import create_audit_log_entry
from app import models
from sqlalchemy.ext.declarative import DeclarativeMeta


def setup_model_event_hooks(Base: DeclarativeMeta):

    def after_insert(mapper, connection, target):
        db = Session(bind=connection)
        create_audit_log_entry(
            db=db,
            action="INSERT",
            table_name=target.__tablename__,
            record_id=target.id,
            description=f"Inserted record into {target.__tablename__} with ID {target.id}",
            performed_by_user_id=getattr(target, 'created_by_user_id', None),
            logged_by_user_id=getattr(target, 'created_by_user_id', None),
            created_by_user_id=getattr(target, 'created_by_user_id', None)
        )
        db.flush()

    def after_update(mapper, connection, target):
        db = Session(bind=connection)
        create_audit_log_entry(
            db=db,
            action="UPDATE",
            table_name=target.__tablename__,
            record_id=target.id,
            description=f"Updated record in {target.__tablename__} with ID {target.id}",
            performed_by_user_id=getattr(target, 'updated_by_user_id', None),
            logged_by_user_id=getattr(target, 'updated_by_user_id', None),
            created_by_user_id=getattr(target, 'created_by_user_id', None)
        )
        db.flush()

    def after_delete(mapper, connection, target):
        db = Session(bind=connection)
        create_audit_log_entry(
            db=db,
            action="DELETE",
            table_name=target.__tablename__,
            record_id=target.id,
            description=f"Deleted record from {target.__tablename__} with ID {target.id}",
            performed_by_user_id=None,
            logged_by_user_id=None,
            created_by_user_id=None
        )
        db.flush()

    for cls in Base.__subclasses__():
        if cls.__tablename__ != "audit_logs":  # Avoid self-logging
            event.listen(cls, 'after_insert', after_insert)
            event.listen(cls, 'after_update', after_update)
            event.listen(cls, 'after_delete', after_delete)
