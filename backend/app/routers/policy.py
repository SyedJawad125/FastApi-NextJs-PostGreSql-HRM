from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.dependencies.permission import require
from .. import database, schemas, models, oauth2
from app.utils import paginate_data, create_response, filter_permissions

router = APIRouter(
    prefix="/policies",
    tags=['Policies']
)


# === GET all policies (with pagination) ===
@router.get("/", response_model=schemas.PolicyListResponse)
def get_policies(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    try:
        query = db.query(models.Policy)
        query = filter_permissions(request.query_params, query)
        data = query.all()
        paginated_data, count = paginate_data(data, request)

        serialized_data = [schemas.PolicyOut.from_orm(policy) for policy in paginated_data]

        response_data = {
            "count": count,
            "data": serialized_data
        }

        return {
            "status": "SUCCESSFUL",
            "result": response_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === GET policy by ID ===
@router.get("/{id}", response_model=schemas.PolicyOut, dependencies=[require("read_policy")])
def get_policy(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    policy = db.query(models.Policy).filter(models.Policy.id == id).first()
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"Policy with id {id} not found")
    return policy


# === CREATE policy ===
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PolicyOut, dependencies=[require("create_policy")])
def create_policy(
    policy: schemas.PolicyCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        policy_data = policy.dict()
        policy_data["created_by_user_id"] = current_user.id

        new_policy = models.Policy(**policy_data)
        db.add(new_policy)
        db.commit()
        db.refresh(new_policy)

        return new_policy

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === UPDATE policy (PATCH) ===
@router.patch("/{id}", response_model=schemas.PolicyOut, dependencies=[require("update_policy")])
def update_policy(
    id: int,
    updated_policy: schemas.PolicyUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        policy_instance = db.query(models.Policy).filter(models.Policy.id == id).first()

        if not policy_instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Policy with id {id} not found"
            )

        update_data = updated_policy.dict(exclude_unset=True)
        update_data["updated_by_user_id"] = current_user.id

        for key, value in update_data.items():
            setattr(policy_instance, key, value)

        db.commit()
        db.refresh(policy_instance)

        return policy_instance

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the policy: {str(e)}"
        )


# === DELETE policy ===
@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_policy")])
def delete_policy(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    policy_query = db.query(models.Policy).filter(models.Policy.id == id)
    policy = policy_query.first()

    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy with id {id} not found"
        )

    policy_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Policy deleted successfully"}
