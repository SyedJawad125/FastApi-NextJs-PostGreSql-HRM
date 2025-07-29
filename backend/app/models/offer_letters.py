from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import date, datetime
from app.database import Base
import enum

class OfferStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class OfferLetter(Base):
    __tablename__ = "offer_letters"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False)
    recruitment_id = Column(Integer, ForeignKey("recruitments.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=True)

    job_title = Column(String, nullable=False)
    offer_date = Column(Date, default=date.today)
    joining_date = Column(Date, nullable=False)
    salary_package = Column(String, nullable=False)
    benefits = Column(Text)
    status = Column(SqlEnum(OfferStatusEnum), default=OfferStatusEnum.pending)
    issued_by = Column(String, nullable=False)
    offer_body = Column(Text, nullable=True)
    pdf_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    candidate = relationship("Candidate", back_populates="offer_letters")
    job_application = relationship("JobApplication", back_populates="offer_letters")
    recruitment = relationship("Recruitment", back_populates="offer_letters")
    interview = relationship("Interview", back_populates="offer_letters")

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_offer_letters")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_offer_letters")
