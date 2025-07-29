from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import models, schemas, database, oauth2
from app.utils import filter_company_announcements, paginate_data  # optional: use if you have pagination utility

router = APIRouter(
    prefix="/company-announcements",
    tags=["Company Announcements"]
)

# ✅ GET all announcements with filtering and pagination
@router.get("/", response_model=schemas.CompanyAnnouncementListResponse)
def get_announcements(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.CompanyAnnouncement).order_by(models.CompanyAnnouncement.created_at.desc())

        # ✅ Apply filters
        query = filter_company_announcements(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized = [schemas.CompanyAnnouncementOut.from_orm(a) for a in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ POST create announcement
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CompanyAnnouncementOut)
def create_announcement(
    announcement: schemas.CompanyAnnouncementCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = announcement.dict()
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_announcement = models.CompanyAnnouncement(**data)
        db.add(new_announcement)
        db.commit()
        db.refresh(new_announcement)

        return new_announcement

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET single announcement by ID
@router.get("/{id}", response_model=schemas.CompanyAnnouncementOut)
def get_announcement_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    announcement = db.query(models.CompanyAnnouncement).filter(models.CompanyAnnouncement.id == id).first()

    if not announcement:
        raise HTTPException(status_code=404, detail=f"Announcement with id {id} not found")

    return announcement


# ✅ PATCH update announcement
@router.patch("/{id}", response_model=schemas.CompanyAnnouncementOut)
def update_announcement(
    id: int,
    announcement_update: schemas.CompanyAnnouncementUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        announcement = db.query(models.CompanyAnnouncement).filter(models.CompanyAnnouncement.id == id).first()

        if not announcement:
            raise HTTPException(status_code=404, detail=f"Announcement with id {id} not found")

        update_dict = announcement_update.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(announcement, key, value)

        db.commit()
        db.refresh(announcement)

        return announcement

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ DELETE announcement
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_announcement(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    announcement_query = db.query(models.CompanyAnnouncement).filter(models.CompanyAnnouncement.id == id)
    announcement = announcement_query.first()

    if not announcement:
        raise HTTPException(status_code=404, detail=f"Announcement with id {id} not found")

    announcement_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "CompanyAnnouncement deleted successfully"}
