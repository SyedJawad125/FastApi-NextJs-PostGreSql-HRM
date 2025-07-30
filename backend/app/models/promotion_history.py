from sqlalchemy import Column, Integer, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PromotionHistory(Base):
    __tablename__ = "promotion_histories"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    previous_rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=True)
    new_rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False)
    promotion_date = Column(Date, nullable=False, default=datetime.utcnow)
    remarks = Column(Text, nullable=True)

    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # === Relationships ===
    employee = relationship("Employee", back_populates="promotion_histories")
    previous_rank = relationship("Rank", foreign_keys=[previous_rank_id])
    new_rank = relationship("Rank", foreign_keys=[new_rank_id])

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_promotion_histories")
    updater = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_promotion_histories")
