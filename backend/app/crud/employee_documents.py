from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app import models
import shutil
from pathlib import Path
import uuid
from datetime import datetime

# File storage directory
DOCUMENT_UPLOAD_DIR = Path("uploads/employees_documents")
DOCUMENT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Max file size (10MB for example)
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_DOC_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png"}

def save_uploaded_document(file: UploadFile) -> str:
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_DOC_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    file_id = uuid.uuid4().hex
    new_filename = f"{file_id}_{file.filename}"
    file_path = DOCUMENT_UPLOAD_DIR / new_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)

# def create_employee_documents(db: Session, doc_data: dict, file: UploadFile):
#     file_path = save_uploaded_document(file)
#     doc_data["document_path"] = file_path
#     doc_data["uploaded_at"] = datetime.utcnow()

#     doc = models.EmployeeDocument(**doc_data)
#     db.add(doc)
#     db.commit()
#     db.refresh(doc)
#     return doc

def create_employee_documents(db: Session, doc_data: dict, file: UploadFile):
    file_path = save_uploaded_document(file)

    doc_data["document_path"] = file_path
    doc_data["uploaded_at"] = datetime.utcnow()

    doc = models.EmployeeDocument(**doc_data)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_employee_documents(db: Session, employee_id: int):
    return db.query(models.EmployeeDocument).filter_by(employee_id=employee_id).all()

def get_employee_document_by_id(db: Session, document_id: int):
    return db.query(models.EmployeeDocument).filter_by(id=document_id).first()

def update_employee_document(db: Session, document_id: int, update_data: dict, file: UploadFile = None):
    doc = get_employee_document_by_id(db, document_id)
    if not doc:
        return None

    if file:
        new_path = save_uploaded_document(file)
        update_data["document_path"] = new_path

    for key, value in update_data.items():
        setattr(doc, key, value)

    db.commit()
    db.refresh(doc)
    return doc

def delete_employee_document(db: Session, document_id: int):
    doc = get_employee_document_by_id(db, document_id)
    if doc:
        try:
            Path(doc.document_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete file: {e}")
        db.delete(doc)
        db.commit()
