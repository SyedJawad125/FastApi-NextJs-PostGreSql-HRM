# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
# from enum import Enum


# # ----------- Enum for Document Type -----------
# class DocumentType(str, Enum):
#     resume = "resume"
#     certificate = "certificate"
#     id_proof = "id_proof"
#     other = "other"


# # ----------- Base Schema -----------
# class EmployeeDocumentBase(BaseModel):
#     employee_id: int
#     document_type: DocumentType
#     document_name: str
#     description: Optional[str] = None


# # ----------- Create Schema (frontend does not send document_path) -----------
# class EmployeeDocumentCreate(EmployeeDocumentBase):
#     pass


# # ----------- Update Schema (frontend does not send document_path) -----------
# class EmployeeDocumentUpdate(BaseModel):
#     document_type: Optional[DocumentType] = None
#     document_name: Optional[str] = None
#     description: Optional[str] = None


# # ----------- Output Schema (response includes document_path) -----------
# class EmployeeDocumentOut(EmployeeDocumentBase):
#     id: int
#     document_path: str  # ✅ Only shown in the response
#     uploaded_at: datetime

#     class Config:
#         from_attributes = True  # Replaces orm_mode in Pydantic v2



# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional
# from enum import Enum


# # ----------- Enum for Document Type -----------
# class DocumentType(str, Enum):
#     resume = "resume"
#     certificate = "certificate"
#     id_proof = "id_proof"
#     other = "other"


# # ----------- Base Schema -----------
# class EmployeeDocumentBase(BaseModel):
#     employee_id: int
#     document_type: DocumentType
#     document_name: str
#     description: Optional[str] = None


# # ----------- Create Schema (frontend does not send document_path) -----------
# class EmployeeDocumentCreate(EmployeeDocumentBase):
#     pass


# # ----------- Update Schema (frontend does not send document_path) -----------
# class EmployeeDocumentUpdate(BaseModel):
#     document_type: Optional[DocumentType] = None
#     document_name: Optional[str] = None
#     description: Optional[str] = None


# # ----------- Output Schema (response includes document_path) -----------
# class EmployeeDocumentOut(EmployeeDocumentBase):
#     id: int
#     document_path: str  # ✅ Only shown in the response
#     uploaded_at: datetime

#     class Config:
#         from_attributes = True  # Replaces orm_mode in Pydantic v2



from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class DocumentType(str, Enum):
    resume = "resume"
    certificate = "certificate"
    id_proof = "id_proof"
    other = "other"

class EmployeeDocumentBase(BaseModel):
    employee_id: int
    document_type: DocumentType
    document_name: str
    description: Optional[str] = None

    @field_validator('document_type', mode='before')
    def validate_document_type(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            try:
                return DocumentType(v)
            except ValueError:
                pass
        raise ValueError(f"Invalid document type. Valid types are: {[e.value for e in DocumentType]}")

class EmployeeDocumentCreate(EmployeeDocumentBase):
    pass

class EmployeeDocumentUpdate(BaseModel):
    document_type: Optional[DocumentType] = None
    document_name: Optional[str] = None
    description: Optional[str] = None

    @field_validator('document_type', mode='before')
    def validate_document_type(cls, v):
        if v is None:
            return v
        return EmployeeDocumentBase.validate_document_type(v)

class EmployeeDocumentOut(EmployeeDocumentBase):
    id: int
    document_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True