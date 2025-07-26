from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(50))
    table_name = Column(String)
    record_id = Column(Integer)
    description = Column(String)
    
    # ForeignKey relationships for users
    performed_by_user_id = Column(Integer, ForeignKey("users.id"))
    logged_by_user_id = Column(Integer, ForeignKey("users.id"))

    created_by_user_id = Column(Integer)
    updated_by_user_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the relationship back to the User model
    performed_by = relationship("User", foreign_keys=[performed_by_user_id], back_populates="performed_audits")
    logged_by = relationship("User", foreign_keys=[logged_by_user_id], back_populates="logged_audits")
