# app/routers/image.py

from fastapi import APIRouter, Depends, UploadFile, File,Form, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.image import ImageCreate, ImageOut, ImageUpdate, ImageListResponse
from app.crud.image import create_image, get_all_images, get_image, update_image, delete_image
from app import oauth2, models
from app.utils import paginate_data
from typing import Optional
from app.schemas.image import ImageUpdate, ImageOut
from app.crud.image import update_image , save_image_file
from app.schemas.image import ImageCreate
from app.crud.image import update_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("/", response_model=ImageOut)
def upload_image(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # 1. First save the file and get its path
        file_info = save_image_file(file)
        if not file_info or not file_info.get("image_path"):
            raise HTTPException(
                status_code=400, 
                detail="Failed to save image file"
            )

        # 2. Prepare complete image data including the path
        image_data = {
            "name": name,
            "description": description,
            "category_id": category_id,
            "image_path": file_info["image_path"],  # Include the saved path
            "created_by_user_id": current_user.id,
            "updated_by_user_id": current_user.id,
        }

        # 3. Create the image record
        db_image = models.Image(**image_data)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        # 4. Optionally store additional file metadata if needed
        # You could update the record here with:
        # db_image.original_filename = file_info.get("original_filename")
        # db_image.file_size = file_info.get("file_size")
        # db.commit()

        return db_image

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        # Clean up the saved file if database operation failed
        if 'file_info' in locals() and file_info.get("image_path"):
            try:
                Path(file_info["image_path"]).unlink(missing_ok=True)
            except Exception:
                pass
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to upload image: {str(e)}"
        )


@router.get("/", response_model=ImageListResponse)
def read_all_images(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        data = get_all_images(db)
        paginated_data, count = paginate_data(data, request)
        
        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": paginated_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=ImageOut)
def read_image(
    image_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        image = get_image(db, image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi import UploadFile, File, Form, HTTPException
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import logging
from datetime import datetime

# Import your models and schemas
from app import models, oauth2
from app.database import get_db
from app.schemas.image import ImageOut, ImageUpdate
from app.crud.image import save_image_file

logger = logging.getLogger(__name__)

@router.patch("/{image_id}", response_model=ImageOut)
def update_image_route(
    image_id: int,
    file: Optional[UploadFile] = File(None),
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        logger.info(f"Attempting to update image with ID: {image_id}")
        
        # Verify the image exists
        db_image = db.query(models.Image).filter(models.Image.id == image_id).first()
        if not db_image:
            logger.error(f"Image with ID {image_id} not found in database")
            raise HTTPException(
                status_code=404, 
                detail=f"Image with ID {image_id} not found"
            )
            
        # Prepare update data based on model fields
        update_data = {
            "name": name,
            "description": description,
            "category_id": category_id,
            "updated_by_user_id": current_user.id,
        }

        # Handle file upload if provided
        old_image_path = None
        if file:
            file_info = save_image_file(file)
            update_data["image_path"] = file_info["image_path"]
            old_image_path = db_image.image_path  # Save old path for cleanup

        # Filter out None values and create update object
        clean_data = {k: v for k, v in update_data.items() if v is not None}
        
        # Update only the fields that were provided
        for field, value in clean_data.items():
            setattr(db_image, field, value)
        
        # Update the modification timestamp
        db_image.upload_date = datetime.utcnow()
        
        db.commit()
        db.refresh(db_image)

        # Clean up old file if new one was uploaded
        if old_image_path and file:
            try:
                old_path = Path(old_image_path)
                if old_path.exists():
                    old_path.unlink()
                    logger.info(f"Successfully deleted old image: {old_image_path}")
            except Exception as e:
                logger.warning(f"Failed to delete old image {old_image_path}: {str(e)}")

        return db_image

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the image: {str(e)}"
        )


@router.delete("/{image_id}")
def delete_existing_image(
    image_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        if delete_image(db, image_id):
            return {"status": "SUCCESSFUL", "message": "Image deleted successfully"}
        raise HTTPException(status_code=404, detail="Image not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
