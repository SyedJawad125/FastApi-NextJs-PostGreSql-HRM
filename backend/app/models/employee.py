from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from app.models import User

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone_number = Column(String(20))
    hire_date = Column(Date, nullable=False)
    job_title = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    @hybrid_property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    department = relationship("Department", back_populates="employees")
    # ✅ Foreign key column
    rank_id = Column(Integer, ForeignKey("ranks.id"))

    # ✅ Relationship back to Rank
    rank = relationship("Rank", back_populates="employees")
    
    # Add relationships for attendance and timesheet
    attendances = relationship("Attendance", back_populates="employee")
    timesheets = relationship("Timesheet", back_populates="employee")
    
    # Add relationships for salary management
    salaries = relationship("EmployeeSalary", back_populates="employee")
    salary_structures = relationship("SalaryStructure", back_populates="employee")
    salary_histories = relationship("SalaryHistory", back_populates="employee")
    
    # Add relationship for payslips
    payslips = relationship("Payslip", back_populates="employee")
    
    # Add one-to-one relationship with EmployeeProfile
    profile = relationship("EmployeeProfile", back_populates="employee", uselist=False)

    documents = relationship("EmployeeDocument", back_populates="employee", cascade="all, delete-orphan")

    # Add this in Employee class:
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    shift = relationship("Shift", back_populates="employees")
    
    shift_assignments = relationship("ShiftAssignment", back_populates="employee", cascade="all, delete-orphan")
    created_recruitments = relationship("Recruitment", back_populates="created_by_employee")

    performance_reviews = relationship("PerformanceReview", back_populates="employee", cascade="all, delete-orphan")

    trainings = relationship("Training", back_populates="employee", cascade="all, delete")

    trainings_attended = relationship(
    "TrainingParticipant",
    back_populates="employee",
    cascade="all, delete-orphan"
    )

    educations = relationship("EducationExperience", back_populates="employee", cascade="all, delete-orphan")

    experiences = relationship("EmployeeExperience", back_populates="employee", cascade="all, delete-orphan")
    
    assets = relationship("EmployeeAsset", back_populates="employee")

    # Inside Employee class
    contracts = relationship("EmployeeContract", back_populates="employee")

    # Inside Employee model
    health_checkups = relationship("HealthCheckUp", back_populates="employee")
