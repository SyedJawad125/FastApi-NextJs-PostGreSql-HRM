from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil

from app import models
from app.database import get_db
from app.schemas.employee_documents import EmployeeDocumentOut
from app.crud.employee_documents import (
    create_employee_documents,
    get_employee_documents,
    update_employee_document,
    delete_employee_document,
    get_employee_document_by_id,
)

router = APIRouter(prefix="/employee-documents", tags=["Employee Documents"])

UPLOAD_DIR = "uploads/employees"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------- Upload Multiple Documents --------------------
@router.post("/upload-multiple/", response_model=List[EmployeeDocumentOut])
async def upload_multiple_documents(
    employee_id: int = Form(...),
    document_types: List[str] = Form(...),
    descriptions: List[str] = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    if len(files) != len(document_types) or len(files) != len(descriptions):
        raise HTTPException(status_code=400, detail="Files and metadata count mismatch.")

    upload_dir = os.path.join(UPLOAD_DIR, str(employee_id))
    os.makedirs(upload_dir, exist_ok=True)

    saved_docs = []
    for i in range(len(files)):
        file = files[i]
        doc_type = document_types[i]
        desc = descriptions[i]

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_data = {
            "employee_id": employee_id,
            "document_type": doc_type,
            "document_name": file.filename,
            "document_path": file_path,
            "description": desc
        }

        saved_doc = create_employee_documents(db=db, doc_data=doc_data)
        saved_docs.append(saved_doc)

    return saved_docs


# -------------------- Get Documents for Employee --------------------
@router.get("/{employee_id}", response_model=List[EmployeeDocumentOut])
def get_documents_by_employee(employee_id: int, db: Session = Depends(get_db)):
    return get_employee_documents(db, employee_id)


# -------------------- Update Document Metadata --------------------

@router.patch("/{document_id}", response_model=EmployeeDocumentOut)
async def patch_document(
    document_id: int,
    document_type: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Fetch existing document
    existing_doc = get_employee_document_by_id(db, document_id)
    if not existing_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    update_data = {}

    # Update type and description
    if document_type:
        update_data["document_type"] = document_type
    if description:
        update_data["description"] = description

    # If a new file is uploaded
    if file:
        # Delete old file from storage
        if existing_doc.document_path and os.path.exists(existing_doc.document_path):
            os.remove(existing_doc.document_path)

        # Save new file
        upload_dir = os.path.join(UPLOAD_DIR, str(existing_doc.employee_id))
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        update_data["document_name"] = file.filename
        update_data["document_path"] = file_path

    # Update DB record
    updated_doc = update_employee_document(db, document_id, update_data)
    return updated_doc



# -------------------- Delete Document --------------------
@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = get_employee_document_by_id(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Also remove file from disk
    if doc.document_path and os.path.exists(doc.document_path):
        os.remove(doc.document_path)

    delete_employee_document(db, document_id)
    return
