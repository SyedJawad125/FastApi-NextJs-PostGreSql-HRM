# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime

# class AuditLog(Base):
#     __tablename__ = "audit_logs"

#     id = Column(Integer, primary_key=True, index=True)
#     action = Column(String(50))
#     table_name = Column(String)
#     record_id = Column(Integer)
#     description = Column(String)
    
#     # ForeignKey relationships for users
#     performed_by_user_id = Column(Integer, ForeignKey("users.id"))
#     logged_by_user_id = Column(Integer, ForeignKey("users.id"))

#     created_by_user_id = Column(Integer)
#     updated_by_user_id = Column(Integer)

#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

#     # Define the relationship back to the User model
#     performed_by = relationship("User", foreign_keys=[performed_by_user_id], back_populates="performed_audits")
#     logged_by = relationship("User", foreign_keys=[logged_by_user_id], back_populates="logged_audits")




from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from typing import Dict, Any

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(50), nullable=False)  # Actions like CREATE, UPDATE, DELETE
    table_name = Column(String(100), nullable=False)  # Name of the affected table
    record_id = Column(Integer, nullable=False)  # ID of the affected record
    description = Column(Text)  # Detailed description of the change
    
    # ForeignKey relationships for users
    performed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who performed the action
    logged_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who logged the action

    # Additional tracking fields
    created_by_user_id = Column(Integer, nullable=False)
    updated_by_user_id = Column(Integer)
    
    # Old and new values for changes (stored as JSON strings)
    old_values = Column(Text)
    new_values = Column(Text)
    
    # Additional context fields
    ip_address = Column(String(45))  # IPv4 or IPv6 address
    user_agent = Column(Text)  # Browser/device info
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    performed_by = relationship(
        "User", 
        foreign_keys=[performed_by_user_id], 
        back_populates="performed_audits"
    )
    logged_by = relationship(
        "User", 
        foreign_keys=[logged_by_user_id], 
        back_populates="logged_audits"
    )

    def as_dict(self) -> Dict[str, Any]:
        """Convert the AuditLog instance to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the audit log
        """
        return {
            "id": self.id,
            "action": self.action,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "description": self.description,
            "performed_by_user_id": self.performed_by_user_id,
            "logged_by_user_id": self.logged_by_user_id,
            "created_by_user_id": self.created_by_user_id,
            "updated_by_user_id": self.updated_by_user_id,
            "old_values": self.old_values,
            "new_values": self.new_values,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "performed_by": {
                "id": self.performed_by.id,
                "username": self.performed_by.username
            } if self.performed_by else None,
            "logged_by": {
                "id": self.logged_by.id,
                "username": self.logged_by.username
            } if self.logged_by else None
        }

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', table_name='{self.table_name}', record_id={self.record_id})>"