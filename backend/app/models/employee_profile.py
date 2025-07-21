from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MaritalStatus(str, enum.Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"

class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"

    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    marital_status = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=False)
    
    # Contact Information
    emergency_contact_name = Column(String(100), nullable=False)
    emergency_contact_relationship = Column(String(50), nullable=False)
    emergency_contact_phone = Column(String(20), nullable=False)
    current_address = Column(String(200), nullable=False)
    permanent_address = Column(String(200), nullable=True)
    
    # Government IDs
    national_id = Column(String(50), unique=True, nullable=False)
    passport_number = Column(String(50), unique=True, nullable=True)
    tax_id = Column(String(50), unique=True, nullable=True)
    
    # Education and Skills
    education_level = Column(String(100), nullable=True)
    field_of_study = Column(String(100), nullable=True)
    skills = Column(String(500), nullable=True)  # Comma-separated list of skills
    
    # One-to-One relationship with Employee
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    employee = relationship("Employee", back_populates="profile", uselist=False) 