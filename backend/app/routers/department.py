from fastapi import (
    APIRouter, Depends, status, Request,
    HTTPException, Query, UploadFile, File
)
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from io import StringIO, BytesIO
import pandas as pd
import re

from app import database, models, oauth2
from app.database import get_db
from app.oauth2 import get_current_user  # ✅ Correct import
from app.dependencies.permission import permission_required, require
from app.utils import paginate_data, create_response, filter_departments
from app import schemas  # ✅ Import schemas correctly

router = APIRouter(
    prefix="/departments",
    tags=['Departments']
)

@router.get("/", response_model=schemas.DepartmentListResponse, dependencies=[require("read_department")])
def get_departments(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        query = db.query(models.Department)
        query = filter_departments(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.Department.from_orm(dept) for dept in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Department, dependencies=[require("create_department")])
# @router.post("/", status_code=201, response_model=schemas.Department)

def create_department(
    request: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        print("Request received:", request)
        new_department = models.Department(**request.model_dump())
        new_department.created_by_user_id = current_user.id
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        print("Created department:", new_department)
        return new_department
    except Exception as e:
        print("ERROR in create_department:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.get("/download-departments", dependencies=[require("read_department")])
def download_departments(
    format: str = Query("csv"),
    download: bool = Query(False),
    db: Session = Depends(get_db)
):
    departments = db.query(models.Department).all()
    data = [{"id": d.id, "name": d.name, "location": d.location} for d in departments]
    df = pd.DataFrame(data)

    if format == "csv":
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=departments.csv",
            "Access-Control-Expose-Headers": "Content-Disposition"
        } if download else {}
        return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)

    elif format == "xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Departments")
        output.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=departments.xlsx",
            "Access-Control-Expose-Headers": "Content-Disposition"
        } if download else {}
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

    raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'xlsx'.")


@router.get("/{id}", response_model=schemas.Department, dependencies=[require("read_department")])
def get_department(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    department = db.query(models.Department).filter(models.Department.id == id).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")
    return department


@router.patch("/{id}", response_model=schemas.Department, dependencies=[require("update_department")])
def patch_update_department(
    id: int,
    updated_department: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        department_instance = db.query(models.Department).filter(models.Department.id == id).first()
        if not department_instance:
            raise HTTPException(status_code=404, detail=f"Department with id {id} not found")

        update_data = updated_department.dict(exclude_unset=True)
        update_data["updated_by_user_id"] = current_user.id

        for key, value in update_data.items():
            setattr(department_instance, key, value)

        db.commit()
        db.refresh(department_instance)
        return department_instance

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating department: {str(e)}")


@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_department")])
def delete_department(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    department_query = db.query(models.Department).filter(models.Department.id == id)
    department = department_query.first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with id {id} not found")

    department_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Department deleted successfully"}


def is_valid_name(value):
    return isinstance(value, str) and value.strip() and re.match(r'^[a-zA-Z\s]+$', value.strip())

def is_valid_location(value):
    return isinstance(value, str) and value.strip() and not value.strip().isdigit()


@router.post("/upload-departments", dependencies=[require("create_department")])
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        elif file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            raise HTTPException(status_code=400, detail="Only .xlsx and .csv files are supported.")

        added_count = 0
        skipped_rows = []

        for i, row in df.iterrows():
            try:
                name = row.get("name")
                location = row.get("location")
                if not is_valid_name(name) or not is_valid_location(location):
                    skipped_rows.append(i + 2)
                    continue

                department = models.Department(name=name.strip(), location=location.strip())
                db.add(department)
                added_count += 1
            except Exception:
                skipped_rows.append(i + 2)

        db.commit()

        return {
            "status": "PARTIAL_SUCCESS" if skipped_rows else "SUCCESS",
            "message": f"{added_count} departments added.",
            "Total skipped Rows": len(skipped_rows),
            "skipped_rows": skipped_rows or None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/test")
def test_route():
    return {"message": "Department router is working"}
