from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import database, schemas, models, oauth2
from app.utils import paginate_data  # If you want filters, you can create a filter_offers utility

router = APIRouter(
    prefix="/offer-letters",
    tags=["Offer Letters"]
)

# ✅ Get all offer letters (with pagination)
@router.get("/", response_model=schemas.OfferLetterListResponse)
def get_offer_letters(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.OfferLetter)

        # Optionally, add filtering logic here like filter_offer_letters(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.OfferLetterOut.from_orm(item) for item in paginated_data]

        return {
            "status": "SUCCESSFUL",
            "result": {
                "count": count,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Create a new offer letter
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.OfferLetterOut)
def create_offer_letter(
    offer: schemas.OfferLetterCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        data = offer.dict(exclude_unset=True)
        data["created_by_user_id"] = current_user.id
        data["updated_by_user_id"] = None

        new_offer = models.OfferLetter(**data)
        db.add(new_offer)
        db.commit()
        db.refresh(new_offer)

        return new_offer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get an offer letter by ID
@router.get("/{id}", response_model=schemas.OfferLetterOut)
def get_offer_letter_by_id(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    offer = db.query(models.OfferLetter).filter(models.OfferLetter.id == id).first()

    if not offer:
        raise HTTPException(status_code=404, detail=f"Offer letter with ID {id} not found")

    return offer


# ✅ Update an offer letter
@router.patch("/{id}", response_model=schemas.OfferLetterOut)
def update_offer_letter(
    id: int,
    updated_data: schemas.OfferLetterUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        offer = db.query(models.OfferLetter).filter(models.OfferLetter.id == id).first()

        if not offer:
            raise HTTPException(status_code=404, detail=f"Offer letter with ID {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(offer, key, value)

        db.commit()
        db.refresh(offer)

        return offer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete an offer letter
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_offer_letter(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    offer_query = db.query(models.OfferLetter).filter(models.OfferLetter.id == id)
    offer = offer_query.first()

    if not offer:
        raise HTTPException(status_code=404, detail=f"Offer letter with ID {id} not found")

    offer_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Offer letter deleted successfully"}
