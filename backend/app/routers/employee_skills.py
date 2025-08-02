from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Any, List

from .. import database, schemas, models, oauth2
from app.utils import filter_employee_skills, paginate_data
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/employee-skills",
    tags=["Employee Skills"]
)

# ✅ Get all employee skills with filtering + pagination
@router.get("/", response_model=schemas.EmployeeSkillListResponse)
def get_employee_skills(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        query = db.query(models.EmployeeSkill).options(joinedload(models.EmployeeSkill.skill))
        query = filter_employee_skills(request.query_params, query)

        all_data = query.all()
        paginated_data, count = paginate_data(all_data, request)

        serialized_data = [schemas.EmployeeSkillOut.from_orm(emp_skill) for emp_skill in paginated_data]

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

# ✅ Create new employee skill
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EmployeeSkillOut)
def create_employee_skill(
    employee_skill: schemas.EmployeeSkillCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
) -> Any:
    try:
        # Verify employee exists
        employee = db.query(models.Employee).filter(models.Employee.id == employee_skill.employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with id {employee_skill.employee_id} not found")


        # Verify skill exists
        skill = db.query(models.Skill).filter(models.Skill.id == employee_skill.skill_id).first()
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill with id {employee_skill.skill_id} not found")

        # Check if employee already has this skill
        existing_emp_skill = db.query(models.EmployeeSkill).filter(
            models.EmployeeSkill.employee_id == employee_skill.employee_id,
            models.EmployeeSkill.skill_id == employee_skill.skill_id
        ).first()
        
        if existing_emp_skill:
            raise HTTPException(
                status_code=400, 
                detail=f"Employee already has this skill assigned"
            )

        emp_skill_data = employee_skill.dict(exclude_unset=True)
        emp_skill_data["created_by_user_id"] = current_user.id
        emp_skill_data["updated_by_user_id"] = None

        new_employee_skill = models.EmployeeSkill(**emp_skill_data)
        db.add(new_employee_skill)
        db.commit()
        db.refresh(new_employee_skill)

        return new_employee_skill

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single employee skill by ID
@router.get("/{id}", response_model=schemas.EmployeeSkillOut)
def get_employee_skill(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    employee_skill = db.query(models.EmployeeSkill).options(
        joinedload(models.EmployeeSkill.skill)
    ).filter(models.EmployeeSkill.id == id).first()

    if not employee_skill:
        raise HTTPException(status_code=404, detail=f"Employee skill with id {id} not found")

    return employee_skill

# ✅ Update employee skill
@router.patch("/{id}", response_model=schemas.EmployeeSkillOut)
def update_employee_skill(
    id: int,
    updated_data: schemas.EmployeeSkillUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        emp_skill_instance = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.id == id).first()

        if not emp_skill_instance:
            raise HTTPException(status_code=404, detail=f"Employee skill with id {id} not found")

        update_dict = updated_data.dict(exclude_unset=True)
        update_dict["updated_by_user_id"] = current_user.id

        # If updating employee_id or skill_id, check for conflicts
        if "employee_id" in update_dict or "skill_id" in update_dict:
            new_employee_id = update_dict.get("employee_id", emp_skill_instance.employee_id)
            new_skill_id = update_dict.get("skill_id", emp_skill_instance.skill_id)
            
            existing_conflict = db.query(models.EmployeeSkill).filter(
                models.EmployeeSkill.employee_id == new_employee_id,
                models.EmployeeSkill.skill_id == new_skill_id,
                models.EmployeeSkill.id != id
            ).first()
            
            if existing_conflict:
                raise HTTPException(
                    status_code=400, 
                    detail="This employee-skill combination already exists"
                )

        for key, value in update_dict.items():
            setattr(emp_skill_instance, key, value)

        db.commit()
        db.refresh(emp_skill_instance)

        return emp_skill_instance

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete employee skill
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee_skill(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    emp_skill_query = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.id == id)
    emp_skill = emp_skill_query.first()

    if not emp_skill:
        raise HTTPException(status_code=404, detail=f"Employee skill with id {id} not found")

    emp_skill_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Employee skill deleted successfully"}

# ✅ Get all skills for a specific employee
@router.get("/employee/{employee_id}", response_model=schemas.EmployeeWithSkills)
def get_employee_skills(
    employee_id: int,
    is_active: bool = True,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Verify employee exists
    employee = db.query(models.User).filter(models.User.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")

    query = db.query(models.EmployeeSkill).options(
        joinedload(models.EmployeeSkill.skill)
    ).filter(models.EmployeeSkill.employee_id == employee_id)
    
    if is_active is not None:
        query = query.filter(models.EmployeeSkill.is_active == is_active)
    
    employee_skills = query.all()

    return {
        "employee_id": employee_id,
        "employee_name": getattr(employee, 'name', None) or getattr(employee, 'username', None),
        "skills": employee_skills
    }

# ✅ Bulk assign skills to employee
@router.post("/employee/{employee_id}/bulk-assign", status_code=status.HTTP_201_CREATED)
def bulk_assign_skills_to_employee(
    employee_id: int,
    skill_assignments: List[schemas.EmployeeSkillCreate],
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    try:
        # Verify employee exists
        employee = db.query(models.User).filter(models.User.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")

        created_skills = []
        
        for skill_assignment in skill_assignments:
            # Ensure employee_id matches the path parameter
            if skill_assignment.employee_id != employee_id:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Employee ID in payload ({skill_assignment.employee_id}) doesn't match path parameter ({employee_id})"
                )

            # Check if skill exists
            skill = db.query(models.Skill).filter(models.Skill.id == skill_assignment.skill_id).first()
            if not skill:
                raise HTTPException(status_code=404, detail=f"Skill with id {skill_assignment.skill_id} not found")

            # Check if employee already has this skill
            existing_emp_skill = db.query(models.EmployeeSkill).filter(
                models.EmployeeSkill.employee_id == employee_id,
                models.EmployeeSkill.skill_id == skill_assignment.skill_id
            ).first()
            
            if existing_emp_skill:
                continue  # Skip duplicates instead of raising error

            emp_skill_data = skill_assignment.dict(exclude_unset=True)
            emp_skill_data["created_by_user_id"] = current_user.id
            emp_skill_data["updated_by_user_id"] = None

            new_employee_skill = models.EmployeeSkill(**emp_skill_data)
            db.add(new_employee_skill)
            created_skills.append(new_employee_skill)

        db.commit()
        
        for skill in created_skills:
            db.refresh(skill)

        return {
            "message": f"Successfully assigned {len(created_skills)} skills to employee",
            "assigned_skills": len(created_skills)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))