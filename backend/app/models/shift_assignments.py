from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id", ondelete="SET NULL"), nullable=True)
    date = Column(Date, nullable=False)

    # Unique constraint: each employee can have only one shift per day
    __table_args__ = (UniqueConstraint('employee_id', 'date', name='uq_employee_shift_date'),)

    # Relationships
    employee = relationship("Employee", back_populates="shift_assignments")
    shift = relationship("Shift", back_populates="shift_assignments")
