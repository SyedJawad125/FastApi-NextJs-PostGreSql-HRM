from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import database, models, oauth2
from app.utils import paginate_data
from app.utils import filter_image_categories
from app.schemas.image_category import (
    ImageCategory,
    ImageCategoryCreate,
    ImageCategoryUpdate,
    ImageCategoryListResponse,
)

router = APIRouter(
    prefix="/image_categories",
    tags=['ImageCategory']
)



@router.get("/", response_model=ImageCategoryListResponse)
def get_image_categories(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.ImageCategory)
        query = filter_image_categories(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [ImageCategory.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ImageCategory)
def create_image_category(
    image_category: ImageCategoryCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        category_data = image_category.dict()
        category_data["created_by_user_id"] = current_user.id

        new_category = models.ImageCategory(**category_data)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=ImageCategory)
def get_image_category(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    category = db.query(models.ImageCategory).filter(models.ImageCategory.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Image Category with id {id} not found")
    return category


@router.patch("/{id}", response_model=ImageCategory)
def patch_update_image_category(
    id: int,
    updated_category: ImageCategoryUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    category_instance = db.query(models.ImageCategory).filter(models.ImageCategory.id == id).first()

    if not category_instance:
        raise HTTPException(status_code=404, detail=f"Image Category with id {id} not found")

    update_data = updated_category.dict(exclude_unset=True)
    update_data["updated_by_user_id"] = current_user.id

    for key, value in update_data.items():
        setattr(category_instance, key, value)

    db.commit()
    db.refresh(category_instance)

    return category_instance


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_image_category(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    category_query = db.query(models.ImageCategory).filter(models.ImageCategory.id == id)
    category = category_query.first()

    if not category:
        raise HTTPException(status_code=404, detail=f"Image Category with id {id} not found")

    category_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Image Category deleted successfully"}
