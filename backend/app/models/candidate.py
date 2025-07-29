# from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime


# class Candidate(Base):
#     __tablename__ = "candidates"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     phone = Column(String)
#     resume = Column(String)  # File path or URL
#     applied_date = Column(Date)

#     recruitment_id = Column(Integer, ForeignKey("recruitments.id", ondelete="CASCADE"))
#     recruitment = relationship("Recruitment", back_populates="candidates")

    # created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

#     # Audit fields
#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     updated_by_user_id = Column(Integer, ForeignKey("users.id"))

#     creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_candidates")
#     updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_candidates")




from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(Text, nullable=True)
    
    # Resume & portfolio
    resume = Column(String, nullable=True)  # file path or URL
    resume_url = Column(String(500), nullable=True)  # Optional extra field
    portfolio_url = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)

    # Professional info
    skills = Column(Text, nullable=True)  # Can store comma-separated or JSON
    experience_years = Column(Integer, default=0)
    education = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    
    applied_date = Column(Date)

    # Foreign keys
    recruitment_id = Column(Integer, ForeignKey("recruitments.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional: if candidate is also a registered user
    
    # Relationships
    recruitment = relationship("Recruitment", back_populates="candidates")
    job_applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")

    
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_candidates")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_candidates")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
