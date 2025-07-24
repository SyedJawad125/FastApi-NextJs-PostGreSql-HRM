# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime
# from app.models.permission import Permission, user_permission
# from app.models.shift_assignments import ShiftAssignment

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

#     created_shifts = relationship("Shift", back_populates="creator")
#     created_shift_assignments = relationship("ShiftAssignment", back_populates="creator")
#     updated_shift_assignments = relationship("ShiftAssignment", foreign_keys=[ShiftAssignment.updated_by_user_id])



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.models.permission import Permission, user_permission
from app.models.shift_assignments import ShiftAssignment

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users", foreign_keys=[role_id])

    created_roles = relationship("Role", back_populates="creator", foreign_keys="Role.created_by_user_id")
    created_departments = relationship("Department", back_populates="creator")
    created_permissions = relationship("Permission", back_populates="creator")
    created_ranks = relationship("Rank", back_populates="creator")

    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
    permissions = relationship("Permission", secondary=user_permission, back_populates="users")

    created_employee_salaries = relationship("EmployeeSalary", back_populates="creator")
    created_salary_structures = relationship("SalaryStructure", back_populates="creator")
    created_salary_histories = relationship("SalaryHistory", back_populates="creator")

    created_payslips = relationship("Payslip", back_populates="creator", foreign_keys="Payslip.created_by_user_id")
    approved_payslips = relationship("Payslip", back_populates="approver", foreign_keys="Payslip.approved_by_user_id")

    created_shifts = relationship("Shift", back_populates="creator")

    # ✅ Explicit foreign keys for shift assignments
    created_shift_assignments = relationship(
        "ShiftAssignment",
        foreign_keys="[ShiftAssignment.created_by_user_id]",
        back_populates="creator"
    )

    updated_shift_assignments = relationship(
        "ShiftAssignment",
        foreign_keys="[ShiftAssignment.updated_by_user_id]"
    )
