from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    performed_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    logged_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    performed_by = relationship("User", foreign_keys=[performed_by_user_id], back_populates="performed_audits")
    logged_by = relationship("User", foreign_keys=[logged_by_user_id], back_populates="logged_audits")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_candidates")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_candidates")
