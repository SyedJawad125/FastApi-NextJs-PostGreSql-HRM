from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, oauth2, schemas
from app import database
from app.schemas.employee_assets import (
    EmployeeAssetCreate,
    EmployeeAssetUpdate,
    EmployeeAssetOut,
    PaginatedEmployeeAssets,
)
from app.database import get_db
from app.utils import filter_employee_assets, paginate_data

from fastapi import Body
from typing import Union

router = APIRouter(
    prefix="/employee-assets",
    tags=["Employee Assets"]
)

# -------------------- Create One or Many --------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.EmployeeAssetOut])
def create_employee_assets(
    items: Union[schemas.EmployeeAssetCreate, List[schemas.EmployeeAssetCreate]] = Body(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Wrap single item into a list
    if isinstance(items, schemas.EmployeeAssetCreate):
        items = [items]

    created = []
    errors = []
    
    for item in items:
        # Check for existing asset with same serial number
        existing_asset = db.query(models.EmployeeAsset).filter(
            models.EmployeeAsset.serial_number == item.serial_number
        ).first()
        
        if existing_asset:
            errors.append({
                "serial_number": item.serial_number,
                "error": f"Asset with serial number {item.serial_number} already exists"
            })
            continue
            
        try:
            asset = models.EmployeeAsset(
                **item.dict(),
                created_by_user_id=current_user.id,
                updated_by_user_id=None
            )
            db.add(asset)
            created.append(asset)
        except Exception as e:
            db.rollback()
            errors.append({
                "serial_number": item.serial_number,
                "error": str(e)
            })
    
    if errors and not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": errors}
        )
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "employee_assets_serial_number_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate serial number detected during commit"
            )
        raise

    for asset in created:
        db.refresh(asset)

    if errors:
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={
                "created": [schemas.EmployeeAssetOut.from_orm(a).dict() for a in created],
                "errors": errors
            }
        )
    
    return created

# -------------------- Get All with Pagination --------------------
@router.get("/", response_model=PaginatedEmployeeAssets)
def get_all_employee_assets(
    request: Request,
    db: Session = Depends(get_db)
):
    query = db.query(models.EmployeeAsset)
    params = dict(request.query_params)

    # Remove pagination params
    params.pop("page", None)
    params.pop("page_size", None)

    query = filter_employee_assets(params, query)
    all_results = query.all()

    paginated_data, total = paginate_data(all_results, request)

    return {
        "count": total,
        "data": paginated_data
    }
# -------------------- Get by Employee ID --------------------
@router.get("/employee/{employee_id}", response_model=List[EmployeeAssetOut])
def get_assets_by_employee(employee_id: int, db: Session = Depends(get_db)):
    results = db.query(models.EmployeeAsset).filter_by(employee_id=employee_id).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No assets found for employee {employee_id}"
        )
    return results

# -------------------- Update Asset --------------------
@router.patch("/{asset_id}", response_model=schemas.EmployeeAssetOut)
def update_employee_asset(
    asset_id: int,
    update_data: schemas.EmployeeAssetUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    asset = db.query(models.EmployeeAsset).filter_by(id=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Employee asset not found")

    # Check if serial number is being updated to one that already exists
    if update_data.serial_number is not None and update_data.serial_number != asset.serial_number:
        existing_asset = db.query(models.EmployeeAsset).filter(
            models.EmployeeAsset.serial_number == update_data.serial_number,
            models.EmployeeAsset.id != asset_id
        ).first()
        
        if existing_asset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with serial number {update_data.serial_number} already exists"
            )

    update_dict = update_data.dict(exclude_unset=True)
    
    try:
        for key, value in update_dict.items():
            setattr(asset, key, value)
        
        asset.updated_by_user_id = current_user.id
        db.commit()
        db.refresh(asset)
        return asset
    except IntegrityError as e:
        db.rollback()
        if "employee_assets_serial_number_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate serial number detected"
            )
        raise

# -------------------- Delete Asset --------------------
@router.delete("/{asset_id}", status_code=status.HTTP_200_OK)
def delete_employee_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # Optional: if needed for authentication
):
    asset_query = db.query(models.EmployeeAsset).filter(models.EmployeeAsset.id == asset_id)
    asset = asset_query.first()

    if not asset:
        raise HTTPException(status_code=404, detail=f"Employee asset with id {asset_id} not found")

    asset_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Employee asset deleted successfully"}
