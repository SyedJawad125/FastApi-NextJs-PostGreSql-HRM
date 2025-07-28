from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class HealthCheckUp(Base):
    __tablename__ = "health_checkups"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    checkup_date = Column(Date, nullable=False)
    blood_pressure = Column(String(20))
    heart_rate = Column(String(10))
    diagnosis = Column(String(255))
    remarks = Column(String(255))

    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="health_checkups")
    department = relationship("Department", back_populates="health_checkups")

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_health_checkups")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_health_checkups")
