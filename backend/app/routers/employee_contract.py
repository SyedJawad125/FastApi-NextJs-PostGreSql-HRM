from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from .. import database, schemas, models, oauth2
from app.utils import paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/contracts",
    tags=["Employee Contracts"]
)


@router.get("/", response_model=schemas.EmployeeContractListResponse)
def get_contracts(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeContract)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.EmployeeContractOut.from_orm(contract) for contract in paginated_data]

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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeContractOut)
def create_contract(
    contract: schemas.EmployeeContractCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        contract_data = contract.dict()
        contract_data["created_by_user_id"] = current_user.id
        contract_data["updated_by_user_id"] = None

        new_contract = models.EmployeeContract(**contract_data)
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)

        return new_contract

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=schemas.EmployeeContractOut)
def get_contract(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    contract = db.query(models.EmployeeContract).filter(models.EmployeeContract.id == id).first()

    if not contract:
        raise HTTPException(status_code=404, detail=f"Contract with id {id} not found")

    return contract


@router.patch("/{id}", response_model=schemas.EmployeeContractOut)
def update_contract(
    id: int,
    updated_data: schemas.EmployeeContractUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        contract_instance = db.query(models.EmployeeContract).filter(models.EmployeeContract.id == id).first()

        if not contract_instance:
            raise HTTPException(status_code=404, detail=f"Contract with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        for key, value in update_dict.items():
            setattr(contract_instance, key, value)

        db.commit()
        db.refresh(contract_instance)

        return contract_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_contract(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    contract_query = db.query(models.EmployeeContract).filter(models.EmployeeContract.id == id)
    contract = contract_query.first()

    if not contract:
        raise HTTPException(status_code=404, detail=f"Contract with id {id} not found")

    contract_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Contract deleted successfully"}
