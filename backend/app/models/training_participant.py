from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class TrainingParticipant(Base):
    __tablename__ = "training_participants"

    id = Column(Integer, primary_key=True, index=True)

    training_id = Column(Integer, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    training = relationship("Training", back_populates="participants")
    employee = relationship("Employee", back_populates="trainings_attended")

    creator = relationship(
        "User",
        foreign_keys=[created_by_user_id],
        back_populates="created_participations"
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by_user_id],
        back_populates="updated_participations"
    )
