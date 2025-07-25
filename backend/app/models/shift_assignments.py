# from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from app.database import Base

# class ShiftAssignment(Base):
#     __tablename__ = "shift_assignments"

#     id = Column(Integer, primary_key=True)
#     employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
#     shift_id = Column(Integer, ForeignKey("shifts.id", ondelete="SET NULL"), nullable=True)
#     date = Column(Date, nullable=False)

#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_shift_assignments")

#     updated_by_user_id = Column(Integer, ForeignKey("users.id"))
#     updater = relationship("User", foreign_keys=[updated_by_user_id])

#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

#     __table_args__ = (
#         UniqueConstraint('employee_id', 'date', name='uq_employee_shift_date'),
#     )

#     employee = relationship("Employee", back_populates="shift_assignments")
#     shift = relationship("Shift", back_populates="shift_assignments")




from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id", ondelete="SET NULL"), nullable=True)
    date = Column(Date, nullable=False)

    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    creator = relationship(
        "User", 
        foreign_keys=[created_by_user_id], 
        back_populates="created_shift_assignments"
    )
    
    updater = relationship(
        "User", 
        foreign_keys=[updated_by_user_id], 
        back_populates="updated_shift_assignments",
        overlaps="updater"
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', name='uq_employee_shift_date'),
    )

    employee = relationship("Employee", back_populates="shift_assignments")
    shift = relationship("Shift", back_populates="shift_assignments")