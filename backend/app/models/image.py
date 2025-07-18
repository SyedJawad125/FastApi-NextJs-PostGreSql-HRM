# from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime

# class Image(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True, index=True)
#     # Image file related fields
#     image_path = Column(String, nullable=False)  # Path where image is stored (e.g., 'hotel_images/image1.jpg')
#     original_filename = Column(String, nullable=True)  # Original filename of the uploaded image
#     file_size = Column(Integer, nullable=True)  # Size of the file in bytes
#     mime_type = Column(String, nullable=True)  # MIME type of the image (e.g., 'image/jpeg')
    
#     # Metadata fields
#     name = Column(String(30), nullable=True)
#     description = Column(Text(500), nullable=True)
#     bulletsdescription = Column(Text, nullable=True)
#     upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
#     # Foreign Keys
#     category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
#     created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#     updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

#     # Relationships
#     category = relationship("Category", back_populates="images")
#     creator = relationship("User", foreign_keys=[created_by_user_id], backref="images_created")
#     updater = relationship("User", foreign_keys=[updated_by_user_id], backref="images_updated") 




# app/models/image.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)

    name = Column(String(30), nullable=True)
    description = Column(Text, nullable=True)
    bulletsdescription = Column(Text, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="images", lazy="joined")
    creator = relationship("User", foreign_keys=[created_by_user_id], backref="images_created")
    updater = relationship("User", foreign_keys=[updated_by_user_id], backref="images_updated")
