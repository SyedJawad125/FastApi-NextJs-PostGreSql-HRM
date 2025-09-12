from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)               # Policy title
    description = Column(Text, nullable=True)                 # Full description / policy body
    category = Column(String(100), nullable=True)             # e.g. "HR", "Finance", "Security"
    effective_date = Column(DateTime, nullable=False)         # When policy takes effect
    expiry_date = Column(DateTime, nullable=True)             # Optional expiry
    version = Column(String(50), default="1.0")               # Versioning for updates
    is_active = Column(Boolean, default=True)                 # Quick activation/deactivation flag

    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    department = relationship("Department", back_populates="policies")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_policies")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_policies")

    # acknowledgements = relationship("PolicyAcknowledgement", back_populates="policy", cascade="all, delete-orphan")
    # attachments = relationship("PolicyAttachment", back_populates="policy", cascade="all, delete-orphan")
