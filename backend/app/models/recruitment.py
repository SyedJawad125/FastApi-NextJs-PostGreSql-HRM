from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Recruitment(Base):
    __tablename__ = "recruitments"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    description = Column(String)
    posted_date = Column(Date)
    deadline = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    created_by_employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Audit fields
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_recruitments")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_recruitments")

    department = relationship("Department", back_populates="recruitments")
    created_by_employee = relationship("Employee", back_populates="created_recruitments")
    candidates = relationship("Candidate", back_populates="recruitment", cascade="all, delete-orphan")
