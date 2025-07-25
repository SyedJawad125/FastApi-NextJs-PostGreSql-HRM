from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Training(Base):
    """Stores training records for employees."""
    __tablename__ = "trainings"

    __table_args__ = (
        CheckConstraint('training_date <= CURRENT_DATE', name='check_training_date_not_future'),
        CheckConstraint('description IS NULL OR LENGTH(description) >= 10', name='check_description_length'),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    trainer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    training_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    training_date = Column(Date, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    employee = relationship("Employee", back_populates="trainings")
    department = relationship("Department", back_populates="trainings")

    participants = relationship(
    "TrainingParticipant",
    back_populates="training",
    cascade="all, delete-orphan"
    )

    trainer = relationship(
        "User",
        foreign_keys=[trainer_id],
        back_populates="trainings_given"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by_user_id],
        back_populates="created_trainings"
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by_user_id],
        back_populates="updated_trainings"
    )
