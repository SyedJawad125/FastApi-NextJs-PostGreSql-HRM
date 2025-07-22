# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import os, shutil

# from app import models
# from app.database import get_db
# from app.schemas.employee_documents import EmployeeDocumentOut
# from app.crud.employee_documents import (
#     create_employee_documents,
#     get_employee_documents,
#     update_employee_document,
#     delete_employee_document,
#     get_employee_document_by_id,
# )

# from app import schemas, crud, database
# router = APIRouter(prefix="/employee-documents", tags=["Employee Documents"])

# UPLOAD_DIR = "uploads/employees_documents"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # -------------------- Upload Multiple Documents --------------------
# @router.post("/upload-multiple/", response_model=List[schemas.EmployeeDocumentOut])
# async def upload_multiple_documents(
#     employee_id: int = Form(...),
#     document_types: List[str] = Form(...),
#     descriptions: List[str] = Form(...),
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(database.get_db)
# ):
#     if len(files) != len(document_types) or len(files) != len(descriptions):
#         raise HTTPException(status_code=400, detail="Files and metadata count mismatch.")

#     saved_docs = []

#     for i in range(len(files)):
#         file = files[i]
#         doc_data = {
#             "employee_id": employee_id,
#             "document_type": document_types[i],
#             "document_name": file.filename,
#             "description": descriptions[i]
#         }
#         saved_doc = crud.create_employee_documents(db=db, doc_data=doc_data, file=file)
#         saved_docs.append(saved_doc)

#     return saved_docs


# # -------------------- Get Documents for Employee --------------------
# @router.get("/{employee_id}", response_model=List[EmployeeDocumentOut])
# def get_documents_by_employee(employee_id: int, db: Session = Depends(get_db)):
#     return get_employee_documents(db, employee_id)


# # -------------------- Update Document Metadata --------------------

# @router.patch("/{document_id}", response_model=EmployeeDocumentOut)
# async def patch_document(
#     document_id: int,
#     document_type: Optional[str] = Form(None),
#     description: Optional[str] = Form(None),
#     file: Optional[UploadFile] = File(None),
#     db: Session = Depends(get_db),
# ):
#     # Fetch existing document
#     existing_doc = get_employee_document_by_id(db, document_id)
#     if not existing_doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     update_data = {}

#     # Update type and description
#     if document_type:
#         update_data["document_type"] = document_type
#     if description:
#         update_data["description"] = description

#     # If a new file is uploaded
#     if file:
#         # Delete old file from storage
#         if existing_doc.document_path and os.path.exists(existing_doc.document_path):
#             os.remove(existing_doc.document_path)

#         # Save new file
#         upload_dir = os.path.join(UPLOAD_DIR, str(existing_doc.employee_id))
#         os.makedirs(upload_dir, exist_ok=True)

#         file_path = os.path.join(upload_dir, file.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         update_data["document_name"] = file.filename
#         update_data["document_path"] = file_path

#     # Update DB record
#     updated_doc = update_employee_document(db, document_id, update_data)
#     return updated_doc



# # -------------------- Delete Document --------------------
# @router.delete("/{document_id}", status_code=204)
# def delete_document(document_id: int, db: Session = Depends(get_db)):
#     doc = get_employee_document_by_id(db, document_id)
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     # Also remove file from disk
#     if doc.document_path and os.path.exists(doc.document_path):
#         os.remove(doc.document_path)

#     delete_employee_document(db, document_id)
#     return







# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import os
# import shutil

# from app import models
# from app.database import get_db
# from app.schemas.employee_documents import EmployeeDocumentOut
# from app.crud.employee_documents import (
#     create_employee_documents,
#     get_employee_documents,
#     update_employee_document,
#     delete_employee_document,
#     get_employee_document_by_id,
# )

# router = APIRouter(prefix="/employee-documents", tags=["Employee Documents"])

# UPLOAD_DIR = "uploads/employees_documents"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # -------------------- Upload Multiple Documents --------------------
# @router.post("/upload-multiple/", response_model=List[EmployeeDocumentOut])
# async def upload_multiple_documents(
#     employee_id: int = Form(...),
#     document_types: List[str] = Form(...),
#     descriptions: List[str] = Form(...),
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     if len(files) != len(document_types) or len(files) != len(descriptions):
#         raise HTTPException(status_code=400, detail="Files and metadata count mismatch.")

#     saved_docs = []

#     for i in range(len(files)):
#         file = files[i]

#         # Save file to disk
#         upload_dir = os.path.join(UPLOAD_DIR, str(employee_id))
#         os.makedirs(upload_dir, exist_ok=True)
#         file_path = os.path.join(upload_dir, file.filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Prepare DB data
#         doc_data = {
#             "employee_id": employee_id,
#             "document_type": document_types[i],
#             "document_name": file.filename,
#             "document_path": file_path,
#             "description": descriptions[i]
#         }

#         # Save to DB
#         saved_doc = create_employee_documents(db=db, doc_data=doc_data)
#         saved_docs.append(saved_doc)

#     return saved_docs


# # -------------------- Get Documents for Employee --------------------
# @router.get("/{employee_id}", response_model=List[EmployeeDocumentOut])
# def get_documents_by_employee(employee_id: int, db: Session = Depends(get_db)):
#     return get_employee_documents(db, employee_id)


# # -------------------- Update Document Metadata --------------------
# @router.patch("/{document_id}", response_model=EmployeeDocumentOut)
# async def patch_document(
#     document_id: int,
#     document_type: Optional[str] = Form(None),
#     description: Optional[str] = Form(None),
#     file: Optional[UploadFile] = File(None),
#     db: Session = Depends(get_db),
# ):
#     existing_doc = get_employee_document_by_id(db, document_id)
#     if not existing_doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     update_data = {}

#     if document_type:
#         update_data["document_type"] = document_type
#     if description:
#         update_data["description"] = description

#     if file:
#         # Delete old file
#         if existing_doc.document_path and os.path.exists(existing_doc.document_path):
#             os.remove(existing_doc.document_path)

#         # Save new file
#         upload_dir = os.path.join(UPLOAD_DIR, str(existing_doc.employee_id))
#         os.makedirs(upload_dir, exist_ok=True)
#         file_path = os.path.join(upload_dir, file.filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         update_data["document_name"] = file.filename
#         update_data["document_path"] = file_path

#     updated_doc = update_employee_document(db, document_id, update_data)
#     return updated_doc


# # -------------------- Delete Document --------------------
# @router.delete("/{document_id}", status_code=204)
# def delete_document(document_id: int, db: Session = Depends(get_db)):
#     doc = get_employee_document_by_id(db, document_id)
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     if doc.document_path and os.path.exists(doc.document_path):
#         os.remove(doc.document_path)

#     delete_employee_document(db, document_id)






import mimetypes
from django.http import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union
import os
import shutil
from pathlib import Path
import uuid
from datetime import datetime

from app import models
from app.database import get_db
from app.schemas.employee_documents import DocumentType, EmployeeDocumentOut
from app.crud.employee_documents import (
    create_employee_documents,
    get_employee_documents,
    update_employee_document,
    delete_employee_document,
    get_employee_document_by_id,
)

router = APIRouter(prefix="/employee-documents", tags=["Employee Documents"])

# Configuration
UPLOAD_DIR = Path("uploads/employees_documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "jpeg", "png", "txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(file: UploadFile):
    """Validate file size and extension"""
    extension = Path(file.filename).suffix[1:].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{extension}' not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size {file_size} exceeds maximum allowed size {MAX_FILE_SIZE}"
        )

def save_document_file(file: UploadFile, employee_id: int) -> str:
    """Save document to disk and return the file path"""
    validate_file(file)
    
    # Create employee-specific directory
    emp_dir = UPLOAD_DIR / str(employee_id)
    emp_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    unique_id = uuid.uuid4().hex[:8]
    file_ext = Path(file.filename).suffix
    new_filename = f"{unique_id}_{file.filename}"
    file_path = emp_dir / new_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)

# -------------------- Upload Documents (Single or Multiple) --------------------
@router.post("/upload/", response_model=List[EmployeeDocumentOut])
async def upload_documents(
    employee_id: int = Form(...),
    document_type: Union[List[str], str] = Form(...),
    description: Union[List[str], str] = Form(...),
    files: Union[List[UploadFile], UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload one or multiple documents for an employee.
    """
    try:
        # Normalize inputs to lists
        files = [files] if not isinstance(files, list) else files
        document_type = [document_type] if not isinstance(document_type, list) else document_type
        description = [description] if not isinstance(description, list) else description

        # Validate array lengths
        if not (len(files) == len(document_type) == len(description)):
            raise HTTPException(
                status_code=400,
                detail="Number of files, document types, and descriptions must match"
            )

        # Process each file
        saved_docs = []
        for i, file in enumerate(files):
            try:
                # Clean and validate document type
                try:
                    dt = document_type[i].strip().lower()
                    document_type[i] = DocumentType(dt).value  # Convert to enum then get value
                except ValueError:
                    valid_types = [e.value for e in DocumentType]
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid document type '{dt}'. Valid types: {', '.join(valid_types)}"
                    )

                # Save file and create record
                file_path = save_document_file(file, employee_id)
                doc_data = {
                    "employee_id": employee_id,
                    "document_type": document_type[i],
                    "document_name": file.filename,
                    "document_path": file_path,
                    "description": description[i],
                    "uploaded_at": datetime.utcnow()
                }
                saved_doc = create_employee_documents(db, doc_data)
                saved_docs.append(saved_doc)

            except HTTPException:
                raise
            except Exception as e:
                if 'file_path' in locals() and Path(file_path).exists():
                    Path(file_path).unlink()
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process {file.filename}: {str(e)}"
                )

        return saved_docs

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during upload: {str(e)}"
        )
# -------------------- Get Documents for Employee --------------------
@router.get("/{employee_id}", response_model=List[EmployeeDocumentOut])
def get_documents_by_employee(
    employee_id: int, 
    document_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all documents for an employee, optionally filtered by document type
    """
    query = db.query(models.EmployeeDocument).filter_by(employee_id=employee_id)
    
    if document_type:
        query = query.filter(models.EmployeeDocument.document_type == document_type)
    
    documents = query.order_by(models.EmployeeDocument.uploaded_at.desc()).all()
    
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No documents found for employee {employee_id}"
        )
    
    return documents

# -------------------- Download Document --------------------

import os
import mimetypes
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

@router.get("/download/{document_id}")
def download_document(document_id: int, db: Session = Depends(get_db)):
    """
    Download an employee document by ID with enhanced security and error handling.
    """
    try:
        # 1. Get document from database
        document = get_employee_document_by_id(db, document_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found in database"
            )

        # 2. Validate and construct file path
        try:
            file_path = Path(document.document_path)
            if not file_path.is_absolute():
                file_path = UPLOAD_DIR / str(document.employee_id) / file_path.name
            
            # Convert Path object to string
            file_path_str = str(file_path.resolve())
            
            # Security check - prevent directory traversal
            if not file_path.resolve().is_relative_to(UPLOAD_DIR.resolve()):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access to requested file is forbidden"
                )
        except (ValueError, RuntimeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file path: {str(e)}"
            )

        # 3. Verify file exists and is accessible
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found at path: {file_path}"
            )
        
        if not os.access(file_path, os.R_OK):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to read the file"
            )

        # 4. Determine content type
        content_type, _ = mimetypes.guess_type(document.document_name)
        if not content_type:
            ext = Path(document.document_name).suffix[1:].lower()
            if ext in {'jpg', 'jpeg'}:
                content_type = 'image/jpeg'
            elif ext == 'png':
                content_type = 'image/png'
            elif ext == 'pdf':
                content_type = 'application/pdf'
            else:
                content_type = 'application/octet-stream'

        # 5. Return file response
        return FileResponse(
    str(file_path.resolve()),  # ✅ pass as positional argument
    filename=document.document_name,
    media_type=content_type,
    headers={
        'Content-Disposition': f'attachment; filename="{document.document_name}"',
        'Cache-Control': 'no-cache'
    }
)


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download document: {str(e)}"
        )
# -------------------- Update Document Metadata --------------------
@router.patch("/{document_id}", response_model=EmployeeDocumentOut)
async def update_document(
    document_id: int,
    document_type: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    """
    Update document metadata and/or replace the file
    """
    existing_doc = get_employee_document_by_id(db, document_id)
    if not existing_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    update_data = {}
    
    if document_type:
        update_data["document_type"] = document_type
    if description:
        update_data["description"] = description
    
    if file:
        try:
            # Save new file
            new_path = save_document_file(file, existing_doc.employee_id)
            
            # Delete old file
            if existing_doc.document_path and os.path.exists(existing_doc.document_path):
                os.remove(existing_doc.document_path)
            
            update_data.update({
                "document_name": file.filename,
                "document_path": new_path
            })
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update file: {str(e)}"
            )
    
    updated_doc = update_employee_document(db, document_id, update_data)
    return updated_doc

# -------------------- Delete Document --------------------
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """
    Delete a document and its associated file
    """
    doc = get_employee_document_by_id(db, document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Delete file
        if doc.document_path and os.path.exists(doc.document_path):
            os.remove(doc.document_path)
        
        # Delete database record
        delete_employee_document(db, document_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document: {str(e)}"
        )