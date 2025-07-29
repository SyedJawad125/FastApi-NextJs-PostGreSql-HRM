# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime
# from app.models.permission import Permission, user_permission
# from app.models.shift_assignments import ShiftAssignment
# from app.models.shift import Shift  # ✅ Needed to reference foreign_keys on Shift

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True, nullable=True)
#     email = Column(String, unique=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, server_default='TRUE', nullable=False)
#     is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

#     role_id = Column(Integer, ForeignKey("roles.id"))
#     role = relationship("Role", back_populates="users", foreign_keys=[role_id])

#     created_roles = relationship("Role", back_populates="creator", foreign_keys="Role.created_by_user_id")
#     created_departments = relationship("Department", back_populates="creator")
#     created_permissions = relationship("Permission", back_populates="creator")
#     created_ranks = relationship("Rank", back_populates="creator")
#     notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
#     permissions = relationship("Permission", secondary=user_permission, back_populates="users")

#     created_employee_salaries = relationship("EmployeeSalary", back_populates="creator")
#     created_salary_structures = relationship("SalaryStructure", back_populates="creator")
#     created_salary_histories = relationship("SalaryHistory", back_populates="creator")

#     created_payslips = relationship("Payslip", back_populates="creator", foreign_keys="Payslip.created_by_user_id")
#     approved_payslips = relationship("Payslip", back_populates="approver", foreign_keys="Payslip.approved_by_user_id")

#     # ✅ Explicit relationships to Shift using foreign keys
#     created_shifts = relationship(
#         "Shift",
#         foreign_keys=[Shift.created_by_user_id],
#         back_populates="creator"
#     )

#     updated_shifts = relationship(
#         "Shift",
#         foreign_keys=[Shift.updated_by_user_id],
#         back_populates="updater"
#     )

#     # ✅ ShiftAssignment relationships (already correct)
#     created_shift_assignments = relationship(
#         "ShiftAssignment",
#         foreign_keys=[ShiftAssignment.created_by_user_id],
#         back_populates="creator"
#     )

#     updated_shift_assignments = relationship(
#         "ShiftAssignment",
#         foreign_keys=[ShiftAssignment.updated_by_user_id]
#     )
#     created_recruitments = relationship("Recruitment", foreign_keys='Recruitment.created_by_user_id', back_populates="creator")
#     updated_recruitments = relationship("Recruitment", foreign_keys='Recruitment.updated_by_user_id', back_populates="updater")

#     created_candidates = relationship("Candidate", foreign_keys='Candidate.created_by_user_id', back_populates="creator")
#     updated_candidates = relationship("Candidate", foreign_keys='Candidate.updated_by_user_id', back_populates="updater")

#         # reviews where user is the reviewer
#     reviews_given = relationship("PerformanceReview", foreign_keys="PerformanceReview.reviewer_id",
#         back_populates="reviewer")

#     # reviews where user is the creator
#     created_reviews = relationship("PerformanceReview", foreign_keys="PerformanceReview.created_by_user_id",
#         back_populates="creator")

#     # reviews where user is the updater
#     updated_reviews = relationship("PerformanceReview", foreign_keys="PerformanceReview.updated_by_user_id",
#         back_populates="updater")

#     trainings_given = relationship("Training", foreign_keys="Training.trainer_id", back_populates="trainer")

#     created_trainings = relationship("Training", foreign_keys="Training.created_by_user_id", back_populates="creator")

#     updated_trainings = relationship("Training", foreign_keys="Training.updated_by_user_id", back_populates="updater")

#     created_participations = relationship(
#     "TrainingParticipant",
#     foreign_keys="TrainingParticipant.created_by_user_id",
#     back_populates="creator"
#     )

#     updated_participations = relationship(
#     "TrainingParticipant",
#     foreign_keys="TrainingParticipant.updated_by_user_id",
#     back_populates="updater"
#     )

#     performed_audits = relationship("AuditLog", foreign_keys="[AuditLog.performed_by_user_id]", back_populates="performed_by")
#     logged_audits = relationship("AuditLog", foreign_keys="[AuditLog.logged_by_user_id]", back_populates="logged_by")
#     created_candidates = relationship("AuditLog", foreign_keys="[AuditLog.created_by_user_id]", back_populates="creator")
#     updated_candidates = relationship("AuditLog", foreign_keys="[AuditLog.updated_by_user_id]", back_populates="updater")



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.models.permission import Permission, user_permission
from app.models.shift_assignments import ShiftAssignment
from app.models.shift import Shift
from app.models.education_experience import EducationExperience


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    # Role relationships
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    created_roles = relationship("Role", back_populates="creator", foreign_keys="Role.created_by_user_id")

    # Department relationships
    created_departments = relationship("Department", foreign_keys="[Department.created_by_user_id]", back_populates="creator")
    updated_departments = relationship("Department", foreign_keys="[Department.updated_by_user_id]", back_populates="updater")


    # Permission relationships
    created_permissions = relationship("Permission", back_populates="creator")
    permissions = relationship("Permission", secondary=user_permission, back_populates="users")

    # Rank relationships
    created_ranks = relationship("Rank", back_populates="creator")

    # Notification relationships
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")

    # Salary relationships
    created_employee_salaries = relationship("EmployeeSalary", back_populates="creator")
    created_salary_structures = relationship("SalaryStructure", back_populates="creator")
    created_salary_histories = relationship("SalaryHistory", back_populates="creator")

    # Payslip relationships
    created_payslips = relationship("Payslip", back_populates="creator", foreign_keys="Payslip.created_by_user_id")
    approved_payslips = relationship("Payslip", back_populates="approver", foreign_keys="Payslip.approved_by_user_id")

    # Shift relationships
    created_shifts = relationship(
        "Shift",
        foreign_keys=[Shift.created_by_user_id],
        back_populates="creator"
    )
    updated_shifts = relationship(
        "Shift",
        foreign_keys=[Shift.updated_by_user_id],
        back_populates="updater"
    )

    # ShiftAssignment relationships - CORRECTED VERSION
    created_shift_assignments = relationship(
        "ShiftAssignment",
        foreign_keys=[ShiftAssignment.created_by_user_id],
        back_populates="creator"
    )
    updated_shift_assignments = relationship(
        "ShiftAssignment",
        foreign_keys=[ShiftAssignment.updated_by_user_id],
        back_populates="updater",
        overlaps="updater"
    )

    # Recruitment relationships
    created_recruitments = relationship(
        "Recruitment",
        foreign_keys="[Recruitment.created_by_user_id]",
        backref="created_by_user"
    )

    updated_recruitments = relationship(
        "Recruitment",
        foreign_keys="[Recruitment.updated_by_user_id]",
        backref="updated_by_user"
    )


    # Candidate relationships
    created_candidates = relationship(
        "Candidate",
        foreign_keys='Candidate.created_by_user_id',
        back_populates="creator"
    )
    updated_candidates = relationship(
        "Candidate",
        foreign_keys='Candidate.updated_by_user_id',
        back_populates="updater"
    )

    # Performance Review relationships
    reviews_given = relationship(
        "PerformanceReview", 
        foreign_keys="PerformanceReview.reviewer_id",
        back_populates="reviewer"
    )
    created_reviews = relationship(
        "PerformanceReview", 
        foreign_keys="PerformanceReview.created_by_user_id",
        back_populates="creator"
    )
    updated_reviews = relationship(
        "PerformanceReview", 
        foreign_keys="PerformanceReview.updated_by_user_id",
        back_populates="updater"
    )

    # Training relationships
    trainings_given = relationship(
        "Training", 
        foreign_keys="Training.trainer_id", 
        back_populates="trainer"
    )
    created_trainings = relationship(
        "Training", 
        foreign_keys="Training.created_by_user_id", 
        back_populates="creator"
    )
    updated_trainings = relationship(
        "Training", 
        foreign_keys="Training.updated_by_user_id", 
        back_populates="updater"
    )

    # Training Participant relationships
    created_participations = relationship(
        "TrainingParticipant",
        foreign_keys="TrainingParticipant.created_by_user_id",
        back_populates="creator"
    )
    updated_participations = relationship(
        "TrainingParticipant",
        foreign_keys="TrainingParticipant.updated_by_user_id",
        back_populates="updater"
    )

    # Relationships in User model
    performed_audits = relationship(
        "AuditLog", 
        foreign_keys="AuditLog.performed_by_user_id", 
        back_populates="performed_by"
    )
    logged_audits = relationship(
        "AuditLog", 
        foreign_keys="AuditLog.logged_by_user_id", 
        back_populates="logged_by"
    )
    
    created_educations = relationship(
    "EducationExperience",
    foreign_keys=[EducationExperience.created_by_user_id],
    back_populates="creator"
    )

    updated_educations = relationship(
    "EducationExperience",
    foreign_keys=[EducationExperience.updated_by_user_id],
    back_populates="updater"
    )

    created_experiences = relationship("EmployeeExperience",
        foreign_keys="[EmployeeExperience.created_by_user_id]", back_populates="creator")
    updated_experiences = relationship("EmployeeExperience", 
        foreign_keys="[EmployeeExperience.updated_by_user_id]", back_populates="updater")
    
    created_assets = relationship("EmployeeAsset",
                                       foreign_keys="[EmployeeAsset.created_by_user_id]", back_populates="creator")
    updated_assets = relationship("EmployeeAsset",
                                       foreign_keys="[EmployeeAsset.updated_by_user_id]", back_populates="updater")
    
    # Inside User class
    created_employee_contracts = relationship("EmployeeContract",
    foreign_keys="[EmployeeContract.created_by_user_id]",
    back_populates="creator"
    )

    updated_employee_contracts = relationship("EmployeeContract",
    foreign_keys="[EmployeeContract.updated_by_user_id]",
    back_populates="updater"
    )

    # ✅ Relationships for HealthCheckUp
    created_health_checkups = relationship(
        "HealthCheckUp",
        foreign_keys="[HealthCheckUp.created_by_user_id]",
        back_populates="creator"
    )
    
    updated_health_checkups = relationship(
        "HealthCheckUp",
        foreign_keys="[HealthCheckUp.updated_by_user_id]",
        back_populates="updater"
    )

    created_advanced_salaries = relationship("AdvancedSalary", back_populates="creator",
        foreign_keys="[AdvancedSalary.created_by_user_id]"
    )

    updated_advanced_salaries = relationship("AdvancedSalary", back_populates="updater",
        foreign_keys="[AdvancedSalary.updated_by_user_id]"
    )

    company_announcements_created = relationship(
        "CompanyAnnouncement",
        foreign_keys="[CompanyAnnouncement.created_by_user_id]",
        back_populates="creator"
    )

    company_announcements_updated = relationship(
        "CompanyAnnouncement",
        foreign_keys="[CompanyAnnouncement.updated_by_user_id]",
        back_populates="updater"
    )


    created_job_applications = relationship("JobApplication", foreign_keys='JobApplication.created_by_user_id', back_populates="creator")
    updated_job_applications = relationship("JobApplication", foreign_keys='JobApplication.updated_by_user_id', back_populates="updater")

    created_interviews = relationship("Interview", foreign_keys="[Interview.created_by_user_id]", back_populates="creator")
    updated_interviews = relationship("Interview", foreign_keys="[Interview.updated_by_user_id]", back_populates="updater")
