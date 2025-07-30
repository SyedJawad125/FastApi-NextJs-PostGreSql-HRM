from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class DisciplinaryActionStatus(enum.Enum):
    pending = "pending"
    reviewed = "reviewed"
    action_taken = "action_taken"
    resolved = "resolved"
    closed = "closed"

class DisciplinaryAction(Base):
    __tablename__ = "disciplinary_actions"

    id = Column(Integer, primary_key=True, index=True)

    # Relationships
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    employee = relationship("Employee", back_populates="disciplinary_actions")
    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_disciplinary_actions")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_disciplinary_actions")

    # Core Fields
    reason = Column(Text, nullable=False)
    action = Column(Text)
    status = Column(SqlEnum(DisciplinaryActionStatus), default=DisciplinaryActionStatus.pending)
    issued_by = Column(String, nullable=False)
    issued_date = Column(DateTime, default=datetime.utcnow)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
