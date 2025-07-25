from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    resume = Column(String)  # File path or URL
    applied_date = Column(Date)

    recruitment_id = Column(Integer, ForeignKey("recruitments.id", ondelete="CASCADE"))
    recruitment = relationship("Recruitment", back_populates="candidates")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_candidates")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_candidates")
