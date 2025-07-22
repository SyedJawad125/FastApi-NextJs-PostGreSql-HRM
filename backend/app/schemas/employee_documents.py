from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


# ----------- Enum for Document Type -----------
class DocumentType(str, Enum):
    resume = "resume"
    certificate = "certificate"
    id_proof = "id_proof"
    other = "other"


# ----------- Shared Base Schema -----------
class EmployeeDocumentBase(BaseModel):
    employee_id: int
    document_type: DocumentType
    document_name: str
    document_path: str
    description: Optional[str] = None


# ----------- Create Schema (used for internal validation, not directly for FastAPI file upload) -----------
class EmployeeDocumentCreate(EmployeeDocumentBase):
    pass


# ----------- Patch Schema (for internal update logic) -----------
class EmployeeDocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    document_name: Optional[str] = None
    document_path: Optional[str] = None
    description: Optional[str] = None


# ----------- Output Schema -----------
class EmployeeDocumentOut(EmployeeDocumentBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
