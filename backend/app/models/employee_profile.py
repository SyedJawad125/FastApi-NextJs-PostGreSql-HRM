from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Text
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
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    marital_status = Column(String, nullable=True)
    nationality = Column(String, nullable=False)
    national_id = Column(String(50), unique=True, nullable=False)
    passport_number = Column(String(50), unique=True, nullable=True)
    passport_expiry = Column(Date, nullable=True)
    personal_email = Column(String(100), nullable=True)

    # Contact Information
    emergency_contact_name = Column(String(100), nullable=False)
    emergency_contact_relationship = Column(String(50), nullable=False)
    emergency_contact_phone = Column(String(20), nullable=False)
    current_address = Column(String(200), nullable=False)
    permanent_address = Column(String(200), nullable=True)

    # Education & Professional
    highest_education = Column(String(100), nullable=True)
    field_of_study = Column(String(100), nullable=True)
    institution = Column(String(100), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    professional_certifications = Column(Text, nullable=True)  # Store as comma-separated string
    skills = Column(Text, nullable=True)  # Store as comma-separated string

    # Banking Information
    bank_name = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_branch = Column(String(100), nullable=True)
    swift_code = Column(String(50), nullable=True)

    # Additional Information
    blood_group = Column(String(10), nullable=True)
    medical_conditions = Column(Text, nullable=True)
    dietary_restrictions = Column(Text, nullable=True)
    languages = Column(Text, nullable=True)  # Comma-separated
    hobbies = Column(Text, nullable=True)    # Comma-separated

    # System Fields
    created_by_user_id = Column(Integer, nullable=True)
    updated_by_user_id = Column(Integer, nullable=True)

    # Optional timestamps (if using `sqlalchemy.sql.func.now()`)
    created_at = Column(Date, nullable=True)
    updated_at = Column(Date, nullable=True)

    # Relationship
    employee = relationship("Employee", back_populates="profile", uselist=False)
