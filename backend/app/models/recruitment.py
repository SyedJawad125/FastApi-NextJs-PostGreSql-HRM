# from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime

# class Recruitment(Base):
#     __tablename__ = "recruitments"

#     id = Column(Integer, primary_key=True, index=True)
#     job_title = Column(String, nullable=False)
#     description = Column(String)
#     posted_date = Column(Date)
#     deadline = Column(Date)
#     department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
#     created_by_employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

#     # Audit fields
#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     updated_by_user_id = Column(Integer, ForeignKey("users.id"))

#     creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_recruitments")
#     updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_recruitments")

#     department = relationship("Department", back_populates="recruitments")
#     created_by_employee = relationship("Employee", back_populates="created_recruitments")
#     candidates = relationship("Candidate", back_populates="recruitment", cascade="all, delete-orphan")



from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, DateTime, Boolean,
    Text, Enum as SqlEnum, Numeric
)
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

# === ENUMS ===
class JobType(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"
    freelance = "freelance"

class JobLevel(enum.Enum):
    entry = "entry"
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    manager = "manager"
    director = "director"
    executive = "executive"

class JobStatus(enum.Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    closed = "closed"
    cancelled = "cancelled"

class WorkMode(enum.Enum):
    onsite = "onsite"
    remote = "remote"
    hybrid = "hybrid"

# === MODEL ===
class Recruitment(Base):
    __tablename__ = "recruitments"

    id = Column(Integer, primary_key=True, index=True)

    # Core job info
    job_title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    requirements = Column(Text)
    responsibilities = Column(Text)

    # Job attributes
    job_type = Column(SqlEnum(JobType), nullable=False, default=JobType.full_time)
    job_level = Column(SqlEnum(JobLevel), nullable=False, default=JobLevel.mid)
    work_mode = Column(SqlEnum(WorkMode), nullable=False, default=WorkMode.onsite)
    status = Column(SqlEnum(JobStatus), nullable=False, default=JobStatus.draft, index=True)

    # Location & pay
    location = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    salary_min = Column(Numeric(10, 2))
    salary_max = Column(Numeric(10, 2))
    currency = Column(String(3), default="USD")

    # Experience & education
    min_experience_years = Column(Integer, default=0)
    max_experience_years = Column(Integer)
    education_level = Column(String(100))

    # Application settings
    max_applicants = Column(Integer)
    auto_close_when_full = Column(Boolean, default=False)
    application_instructions = Column(Text)

    # Skills & tags
    required_skills = Column(Text)
    preferred_skills = Column(Text)
    tags = Column(Text)

    # Dates
    posted_date = Column(Date, index=True)
    deadline = Column(Date, index=True)
    last_activity_date = Column(Date)

    # Contact info
    contact_email = Column(String(255))
    contact_phone = Column(String(20))

    # Flags
    is_urgent = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_confidential = Column(Boolean, default=False)
    allow_remote_candidates = Column(Boolean, default=True)
    requires_visa_sponsorship = Column(Boolean, default=False)

    # Analytics
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)

    # SEO / external
    slug = Column(String(255), unique=True, index=True)
    meta_description = Column(String(160))
    external_job_boards = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    closed_at = Column(DateTime)

    # Foreign Keys
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    created_by_employee_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    hiring_manager_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    department = relationship("Department", back_populates="recruitments")
    created_by_employee = relationship(
        "Employee", 
        foreign_keys=[created_by_employee_id],
        back_populates="created_recruitments"
    )
    hiring_manager = relationship(
        "Employee",
        foreign_keys=[hiring_manager_id],
        back_populates="managed_recruitments"
    )
    creator = relationship("User", foreign_keys=[created_by_user_id])
    updater = relationship("User", foreign_keys=[updated_by_user_id])

    candidates = relationship("Candidate", back_populates="recruitment", cascade="all, delete-orphan")
    # applications = relationship("Application", back_populates="recruitment", cascade="all, delete-orphan")
    # interviews = relationship("Interview", back_populates="recruitment")

    def __repr__(self):
        return f"<Recruitment(id={self.id}, title='{self.job_title}', status='{self.status.value}')>"

    @property
    def is_active(self):
        return (
            self.status == JobStatus.active and 
            (self.deadline is None or self.deadline >= datetime.now().date())
        )

    @property
    def days_until_deadline(self):
        if self.deadline:
            delta = self.deadline - datetime.now().date()
            return delta.days
        return None

    @property
    def salary_range_display(self):
        if self.salary_min and self.salary_max:
            return f"{self.currency} {float(self.salary_min):,.0f} - {float(self.salary_max):,.0f}"
        elif self.salary_min:
            return f"{self.currency} {float(self.salary_min):,.0f}+"
        return "Salary not specified"