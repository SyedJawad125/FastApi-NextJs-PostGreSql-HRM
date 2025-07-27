from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, oauth2
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
@router.post("/", response_model=List[EmployeeAssetOut])
def create_employee_assets(
    items: Union[EmployeeAssetCreate, List[EmployeeAssetCreate]] = Body(...),
    db: Session = Depends(get_db),
    created_by_user_id: Optional[int] = 1
):
    # Wrap single item into a list
    if isinstance(items, EmployeeAssetCreate):
        items = [items]

    created = []
    for item in items:
        asset = models.EmployeeAsset(**item.dict())
        asset.created_by_user_id = created_by_user_id
        db.add(asset)
        created.append(asset)
    db.commit()
    for asset in created:
        db.refresh(asset)
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
@router.patch("/{asset_id}", response_model=EmployeeAssetOut)
def update_employee_asset(
    asset_id: int,
    update_data: EmployeeAssetUpdate,
    db: Session = Depends(get_db),
    updated_by_user_id: Optional[int] = 1
):
    asset = db.query(models.EmployeeAsset).filter_by(id=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Employee asset not found")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(asset, key, value)

    asset.updated_by_user_id = updated_by_user_id
    db.commit()
    db.refresh(asset)
    return asset

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
