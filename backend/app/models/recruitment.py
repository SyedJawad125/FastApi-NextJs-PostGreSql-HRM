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




# from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Boolean, Text, Enum, Numeric
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime
# import enum

# class JobType(enum.Enum):
#     FULL_TIME = "full_time"
#     PART_TIME = "part_time"
#     CONTRACT = "contract"
#     INTERNSHIP = "internship"
#     FREELANCE = "freelance"

# class JobLevel(enum.Enum):
#     ENTRY = "entry"
#     JUNIOR = "junior"
#     MID = "mid"
#     SENIOR = "senior"
#     LEAD = "lead"
#     MANAGER = "manager"
#     DIRECTOR = "director"
#     EXECUTIVE = "executive"

# class JobStatus(enum.Enum):
#     DRAFT = "draft"
#     ACTIVE = "active"
#     PAUSED = "paused"
#     CLOSED = "closed"
#     CANCELLED = "cancelled"

# class WorkMode(enum.Enum):
#     ONSITE = "onsite"
#     REMOTE = "remote"
#     HYBRID = "hybrid"

# class Recruitment(Base):
#     __tablename__ = "recruitments"

#     id = Column(Integer, primary_key=True, index=True)
#     job_title = Column(String(255), nullable=False, index=True)
#     description = Column(Text)
#     requirements = Column(Text)  # Job requirements and qualifications
#     responsibilities = Column(Text)  # Job responsibilities
    
#     # Job details
#     job_type = Column(Enum(JobType), nullable=False, default=JobType.FULL_TIME)
#     job_level = Column(Enum(JobLevel), nullable=False, default=JobLevel.MID)
#     work_mode = Column(Enum(WorkMode), nullable=False, default=WorkMode.ONSITE)
#     status = Column(Enum(JobStatus), nullable=False, default=JobStatus.DRAFT, index=True)
    
#     # Location and compensation
#     location = Column(String(255))
#     city = Column(String(100))
#     country = Column(String(100))
#     salary_min = Column(Numeric(10, 2))
#     salary_max = Column(Numeric(10, 2))
#     currency = Column(String(3), default="USD")  # ISO currency code
    
#     # Experience and education
#     min_experience_years = Column(Integer, default=0)
#     max_experience_years = Column(Integer)
#     education_level = Column(String(100))  # Bachelor's, Master's, PhD, etc.
    
#     # Application settings
#     max_applicants = Column(Integer)  # Maximum number of applications
#     auto_close_when_full = Column(Boolean, default=False)
#     application_instructions = Column(Text)
    
#     # Skills and tags
#     required_skills = Column(Text)  # JSON or comma-separated skills
#     preferred_skills = Column(Text)  # Nice-to-have skills
#     tags = Column(Text)  # For categorization and search
    
#     # Dates
#     posted_date = Column(Date, index=True)
#     deadline = Column(Date, index=True)
#     last_activity_date = Column(Date)  # Last time job was updated or got application
    
#     # Contact information
#     contact_email = Column(String(255))
#     contact_phone = Column(String(20))
#     hiring_manager_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    
#     # Relationships
#     department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
#     created_by_employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    
#     # Flags and settings
#     is_urgent = Column(Boolean, default=False)
#     is_featured = Column(Boolean, default=False)
#     is_confidential = Column(Boolean, default=False)  # Hide company name
#     allow_remote_candidates = Column(Boolean, default=True)
#     requires_visa_sponsorship = Column(Boolean, default=False)
    
#     # Analytics fields
#     view_count = Column(Integer, default=0)
#     application_count = Column(Integer, default=0)
    
#     # SEO and external posting
#     slug = Column(String(255), unique=True, index=True)  # URL-friendly version
#     meta_description = Column(String(160))  # For SEO
#     external_job_boards = Column(Text)  # JSON list of where job is posted
    
#     # Timestamps
#     created_at = Column(DateTime, default=datetime.utcnow, index=True)
#     updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
#     published_at = Column(DateTime, nullable=True)  # When job went live
#     closed_at = Column(DateTime, nullable=True)  # When job was closed
    
#     # Audit fields
#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     updated_by_user_id = Column(Integer, ForeignKey("users.id"))

#     # Relationships
#     creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_recruitments")
#     updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_recruitments")
    
#     department = relationship("Department", back_populates="recruitments")
#     created_by_employee = relationship("Employee", foreign_keys=[created_by_employee_id], back_populates="created_recruitments")
#     hiring_manager = relationship("Employee", foreign_keys=[hiring_manager_id], back_populates="managed_recruitments")
    
#     candidates = relationship("Candidate", back_populates="recruitment", cascade="all, delete-orphan")
#     applications = relationship("Application", back_populates="recruitment", cascade="all, delete-orphan")
#     interviews = relationship("Interview", back_populates="recruitment")
    
#     def __repr__(self):
#         return f"<Recruitment(id={self.id}, title='{self.job_title}', status='{self.status}')>"
    
#     @property
#     def is_active(self):
#         """Check if recruitment is currently active and accepting applications"""
#         return (self.status == JobStatus.ACTIVE and 
#                 (self.deadline is None or self.deadline >= datetime.now().date()))
    
#     @property
#     def days_until_deadline(self):
#         """Calculate days remaining until deadline"""
#         if self.deadline:
#             delta = self.deadline - datetime.now().date()
#             return delta.days
#         return None
    
#     @property
#     def salary_range_display(self):
#         """Format salary range for display"""
#         if self.salary_min and self.salary_max:
#             return f"{self.currency} {self.salary_min:,.0f} - {self.salary_max:,.0f}"
#         elif self.salary_min:
#             return f"{self.currency} {self.salary_min:,.0f}+"
#         return "Salary not specified"