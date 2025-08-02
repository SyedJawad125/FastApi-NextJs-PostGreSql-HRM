from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from .. import database, schemas, models, oauth2
from app.utils import filter_skills, paginate_data  # You'll need to create filter_skills utility
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

# ✅ Get all skills with filtering + pagination
@router.get("/", response_model=schemas.SkillListResponse)
def get_skills(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.Skill)
        # Apply filters if filter_skills utility exists
        query = filter_skills(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.SkillOut.from_orm(skill) for skill in paginated_data]

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

# ✅ Create new skill
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SkillOut)
def create_skill(
    skill: schemas.SkillCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Check if skill with same name already exists
        existing_skill = db.query(models.Skill).filter(models.Skill.name == skill.name).first()
        if existing_skill:
            raise HTTPException(status_code=400, detail=f"Skill with name '{skill.name}' already exists")

        skill_data = skill.dict(exclude_unset=True)
        skill_data["created_by_user_id"] = current_user.id
        skill_data["updated_by_user_id"] = None

        new_skill = models.Skill(**skill_data)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)

        return new_skill

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single skill by ID
@router.get("/{id}", response_model=schemas.SkillOut)
def get_skill(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    skill = db.query(models.Skill).filter(models.Skill.id == id).first()

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill with id {id} not found")

    return skill

# ✅ Update skill
@router.patch("/{id}", response_model=schemas.SkillOut)
def update_skill(
    id: int,
    updated_data: schemas.SkillUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        skill_instance = db.query(models.Skill).filter(models.Skill.id == id).first()

        if not skill_instance:
            raise HTTPException(status_code=404, detail=f"Skill with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        # Check for name conflicts if name is being updated
        if "name" in update_dict:
            existing_skill = db.query(models.Skill).filter(
                models.Skill.name == update_dict["name"],
                models.Skill.id != id
            ).first()
            if existing_skill:
                raise HTTPException(status_code=400, detail=f"Skill with name '{update_dict['name']}' already exists")

        for key, value in update_dict.items():
            setattr(skill_instance, key, value)

        db.commit()
        db.refresh(skill_instance)

        return skill_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete skill
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_skill(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    skill_query = db.query(models.Skill).filter(models.Skill.id == id)
    skill = skill_query.first()

    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill with id {id} not found")

    # Check if skill is being used by any employee
    employee_skills_count = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.skill_id == id).count()
    if employee_skills_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete skill. It is assigned to {employee_skills_count} employee(s)"
        )

    skill_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Skill deleted successfully"}

# ✅ Get skill with all employees who have this skill
@router.get("/{id}/employees", response_model=schemas.SkillWithEmployees)
def get_skill_with_employees(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    skill = db.query(models.Skill).filter(models.Skill.id == id).first()
    
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill with id {id} not found")
    
    employee_skills = db.query(models.EmployeeSkill).filter(
        models.EmployeeSkill.skill_id == id,
        models.EmployeeSkill.is_active == True
    ).all()
    
    return {  
        "skill": skill,
        "employees": employee_skills
    }