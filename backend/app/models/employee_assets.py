from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class EmployeeAsset(Base):
    __tablename__ = "employee_assets"

    id = Column(Integer, primary_key=True, index=True)
    
    asset_name = Column(String(100), nullable=False)
    asset_type = Column(String(50), nullable=False)  # e.g. Laptop, Phone, Chair
    brand = Column(String(50), nullable=True)
    model = Column(String(100), nullable=True)
    serial_number = Column(String(100), unique=True, nullable=True)

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    issued_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    condition_issued = Column(String(100), nullable=True)
    condition_returned = Column(String(100), nullable=True)
    remarks = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,  nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_assets")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_assets")

    # Relationships
    employee = relationship("Employee", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id])
