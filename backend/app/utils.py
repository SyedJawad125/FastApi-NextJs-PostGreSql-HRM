from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from app import models
from sqlalchemy.orm import Query
from app import models, schemas 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fastapi import Query
from sqlalchemy.orm import Query as SAQuery
from sqlalchemy import or_
from typing import Mapping
from app.models import PerformanceReview

from fastapi import Query as FastAPIQuery
from starlette.datastructures import QueryParams
from app import models

 # ✅ Keep this if enums are in the same schemas file


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def paginate_data(data, request):
    try:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end], len(data)
    except:
        return data, len(data)
    
from fastapi.responses import JSONResponse
def create_response(data, message, status_code):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": message,
            "result": data
        }
    )
from app import models

def filter_departments(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Department.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query



def filter_employees(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Employee.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query

def filter_ranks(params, query):
    title = params.get("title")
    if title:
        query = query.filter(models.Rank.title.ilike(f"%{title}%"))
    # Add more filters as needed
    return query

def filter_attendances(params, query):
    is_present = params.get("is_present")
    date = params.get("date")
    employee_id = params.get("employee_id")

    # Handle is_present filter
    if is_present is not None:
        is_present = is_present.lower()
        if is_present in ["true", "1"]:
            query = query.filter(models.Attendance.is_present == True)
        elif is_present in ["false", "0"]:
            query = query.filter(models.Attendance.is_present == False)

    # Handle date filter
    if date:
        try:
            # Optional: Validate the date format
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")  # Will raise ValueError if invalid
            query = query.filter(models.Attendance.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Handle employee_id filter
    if employee_id:
        try:
            query = query.filter(models.Attendance.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    return query


def filter_timesheets(params, query):
    date = params.get("date")
    employee_id = params.get("employee_id")
    attendance_id = params.get("attendance_id")

    if date:
        try:
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")
            query = query.filter(models.Timesheet.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if employee_id:
        try:
            query = query.filter(models.Timesheet.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if attendance_id:
        try:
            query = query.filter(models.Timesheet.attendance_id == int(attendance_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="attendance_id must be an integer.")

    return query
    


def filter_leave(params: dict, query: Query):
    status = params.get("status")
    leave_type = params.get("leave_type")
    employee_id = params.get("employee_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if status:
        if status not in [s.value for s in schemas.LeaveStatus]:  # ✅ Use schemas.LeaveStatus
            raise HTTPException(status_code=400, detail="Invalid leave status.")
        query = query.filter(models.Leave.status == status)

    if leave_type:
        if leave_type not in [lt.value for lt in schemas.LeaveType]:  # ✅ Use schemas.LeaveType
            raise HTTPException(status_code=400, detail="Invalid leave type.")
        query = query.filter(models.Leave.leave_type == leave_type)

    if employee_id:
        try:
            query = query.filter(models.Leave.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Leave.start_date >= start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(models.Leave.end_date <= end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

    return query



def filter_employee_salaries(params, query):
    employee_id = params.get("employee_id")
    salary_month = params.get("salary_month")  # Format: YYYY-MM
    payment_status = params.get("payment_status")
    department_id = params.get("department_id")
    rank_id = params.get("rank_id")

    # Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.EmployeeSalary.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # Filter by salary_month (YYYY-MM)
    if salary_month:
        try:
            salary_month_date = datetime.strptime(salary_month, "%Y-%m")
            query = query.filter(models.EmployeeSalary.salary_month == salary_month_date.date())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid salary_month format. Use YYYY-MM.")

    # Filter by payment_status
    if payment_status:
        allowed_statuses = ["pending", "paid", "cancelled"]
        if payment_status.lower() in allowed_statuses:
            query = query.filter(models.EmployeeSalary.payment_status == payment_status.lower())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid payment_status. Allowed: {allowed_statuses}")

    # Filter by department_id
    if department_id:
        try:
            query = query.filter(models.EmployeeSalary.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # Filter by rank_id
    if rank_id:
        try:
            query = query.filter(models.EmployeeSalary.rank_id == int(rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rank_id. Must be an integer.")

    return query


from app.models.salary_history import ChangeType  # adjust this path if needed

def filter_salary_histories(params, query: Query):
    employee_id = params.get("employee_id")
    department_id = params.get("department_id")
    previous_rank_id = params.get("previous_rank_id")
    new_rank_id = params.get("new_rank_id")
    change_type = params.get("change_type")  # promotion, annual_raise, etc.
    effective_date = params.get("effective_date")  # format: YYYY-MM-DD

    # Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.SalaryHistory.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # Filter by department_id
    if department_id:
        try:
            query = query.filter(models.SalaryHistory.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # Filter by previous_rank_id
    if previous_rank_id:
        try:
            query = query.filter(models.SalaryHistory.previous_rank_id == int(previous_rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid previous_rank_id. Must be an integer.")

    # Filter by new_rank_id
    if new_rank_id:
        try:
            query = query.filter(models.SalaryHistory.new_rank_id == int(new_rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid new_rank_id. Must be an integer.")

    # Filter by change_type
    if change_type:
        valid_types = [e.value for e in ChangeType]
        if change_type.lower() in valid_types:
            query = query.filter(models.SalaryHistory.change_type == change_type.lower())
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid change_type. Allowed: {valid_types}"
            )

    # Filter by effective_date
    if effective_date:
        try:
            parsed_date = datetime.strptime(effective_date, "%Y-%m-%d").date()
            query = query.filter(models.SalaryHistory.effective_date == parsed_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid effective_date format. Use YYYY-MM-DD."
            )

    return query


from app.models.payslip import PayslipStatus

def filter_payslips(params, query: Query):
    payslip_number = params.get("payslip_number")
    employee_id = params.get("employee_id")
    department_id = params.get("department_id")
    rank_id = params.get("rank_id")
    status = params.get("status")
    payment_method = params.get("payment_method")
    pay_period_start = params.get("pay_period_start")  # format: YYYY-MM-DD
    pay_period_end = params.get("pay_period_end")      # format: YYYY-MM-DD
    payment_date = params.get("payment_date")          # format: YYYY-MM-DD

    # Filter by payslip_number
    if payslip_number:
        query = query.filter(models.Payslip.payslip_number.ilike(f"%{payslip_number}%"))

    # Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.Payslip.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # Filter by department_id
    if department_id:
        try:
            query = query.filter(models.Payslip.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # Filter by rank_id
    if rank_id:
        try:
            query = query.filter(models.Payslip.rank_id == int(rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rank_id. Must be an integer.")

    # Filter by status (DRAFT, GENERATED, etc.)
    if status:
        valid_statuses = [e.value for e in PayslipStatus]
        if status.lower() in valid_statuses:
            query = query.filter(models.Payslip.status == status.lower())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {valid_statuses}")

    # Filter by payment method
    if payment_method:
        query = query.filter(models.Payslip.payment_method.ilike(f"%{payment_method}%"))

    # Filter by pay_period_start (exact match)
    if pay_period_start:
        try:
            date_obj = datetime.strptime(pay_period_start, "%Y-%m-%d").date()
            query = query.filter(models.Payslip.pay_period_start == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid pay_period_start format. Use YYYY-MM-DD.")

    # Filter by pay_period_end (exact match)
    if pay_period_end:
        try:
            date_obj = datetime.strptime(pay_period_end, "%Y-%m-%d").date()
            query = query.filter(models.Payslip.pay_period_end == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid pay_period_end format. Use YYYY-MM-DD.")

    # Filter by payment_date (exact match)
    if payment_date:
        try:
            date_obj = datetime.strptime(payment_date, "%Y-%m-%d").date()
            query = query.filter(models.Payslip.payment_date == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payment_date format. Use YYYY-MM-DD.")

    return query


from app.models.salary_structure import PaymentFrequency

def filter_salary_structures(params, query: Query):
    employee_id = params.get("employee_id")
    rank_id = params.get("rank_id")
    department_id = params.get("department_id")
    payment_frequency = params.get("payment_frequency")
    effective_date = params.get("effective_date")  # format: YYYY-MM-DD
    end_date = params.get("end_date")              # format: YYYY-MM-DD

    # ✅ Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.SalaryStructure.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # ✅ Filter by rank_id
    if rank_id:
        try:
            query = query.filter(models.SalaryStructure.rank_id == int(rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rank_id. Must be an integer.")

    # ✅ Filter by department_id
    if department_id:
        try:
            query = query.filter(models.SalaryStructure.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # ✅ Filter by payment_frequency
    if payment_frequency:
        valid_frequencies = [f.value for f in PaymentFrequency]
        if payment_frequency.lower() in valid_frequencies:
            query = query.filter(models.SalaryStructure.payment_frequency == payment_frequency.lower())
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid payment_frequency. Allowed: {valid_frequencies}"
            )

    # ✅ Filter by effective_date (exact match)
    if effective_date:
        try:
            date_obj = datetime.strptime(effective_date, "%Y-%m-%d").date()
            query = query.filter(models.SalaryStructure.effective_date == date_obj)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid effective_date format. Use YYYY-MM-DD."
            )

    # ✅ Filter by end_date (exact match)
    if end_date:
        try:
            date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(models.SalaryStructure.end_date == date_obj)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid end_date format. Use YYYY-MM-DD."
            )

    return query


from starlette.datastructures import QueryParams
from app.models.image_category import ImageCategory


def filter_image_categories(query_params: QueryParams, query: Query) -> Query:
    category = query_params.get("category")
    created_by_user_id = query_params.get("created_by_user_id")
    updated_by_user_id = query_params.get("updated_by_user_id")

    if category:
        query = query.filter(ImageCategory.category.ilike(f"%{category}%"))

    if created_by_user_id:
        try:
            query = query.filter(ImageCategory.created_by_user_id == int(created_by_user_id))
        except ValueError:
            pass

    if updated_by_user_id:
        try:
            query = query.filter(ImageCategory.updated_by_user_id == int(updated_by_user_id))
        except ValueError:
            pass

    return query

from sqlalchemy.orm import Session
from app.models.image import Image
from typing import List, Optional


def filter_images(
    db: Session,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    created_by_user_id: Optional[int] = None,
    mime_type: Optional[str] = None
) -> List[Image]:
    query = db.query(Image)

    if name:
        query = query.filter(Image.name.ilike(f"%{name}%"))
    if category_id:
        query = query.filter(Image.category_id == category_id)
    if created_by_user_id:
        query = query.filter(Image.created_by_user_id == created_by_user_id)
    if mime_type:
        query = query.filter(Image.mime_type == mime_type)

    return query.all()

from typing import Any
from fastapi import Request
from sqlalchemy.orm import Query
from app.models.image import Image  # make sure this import is correct

def filter_images_all(query_params: dict[str, Any], query: Query) -> Query:
    """
    Dynamically filter images based on query parameters.
    Supported filters: name, category_id, created_by_user_id, mime_type
    """
    name = query_params.get("name")
    category_id = query_params.get("category_id")
    created_by_user_id = query_params.get("created_by_user_id")
    mime_type = query_params.get("mime_type")

    if name:
        query = query.filter(Image.name.ilike(f"%{name}%"))
    if category_id:
        try:
            query = query.filter(Image.category_id == int(category_id))
        except ValueError:
            pass  # Skip invalid category_id
    if created_by_user_id:
        try:
            query = query.filter(Image.created_by_user_id == int(created_by_user_id))
        except ValueError:
            pass
    if mime_type:
        query = query.filter(Image.mime_type == mime_type)

    return query


def filter_shifts(query_params, query):
    if "name" in query_params:
        query = query.filter(models.Shift.name.ilike(f"%{query_params['name']}%"))
    if "start_time" in query_params:
        query = query.filter(models.Shift.start_time == query_params["start_time"])
    if "end_time" in query_params:
        query = query.filter(models.Shift.end_time == query_params["end_time"])
    return query


def filter_shift_assignments(query_params, query):
    if "employee_id" in query_params:
        query = query.filter(models.ShiftAssignment.employee_id == int(query_params["employee_id"]))
    if "shift_id" in query_params:
        query = query.filter(models.ShiftAssignment.shift_id == int(query_params["shift_id"]))
    if "date" in query_params:
        query = query.filter(models.ShiftAssignment.date == query_params["date"])
    return query


def filter_candidates(params, query):
    if "name" in params:
        query = query.filter(models.Candidate.name.ilike(f"%{params['name']}%"))
    if "email" in params:
        query = query.filter(models.Candidate.email.ilike(f"%{params['email']}%"))
    if "recruitment_id" in params:
        query = query.filter(models.Candidate.recruitment_id == int(params["recruitment_id"]))
    return query

def filter_recruitments(params, query):
    if "job_title" in params:
        query = query.filter(models.Recruitment.job_title.ilike(f"%{params['job_title']}%"))
    if "department_id" in params:
        query = query.filter(models.Recruitment.department_id == int(params["department_id"]))
    if "posted_date" in params:
        query = query.filter(models.Recruitment.posted_date == params["posted_date"])
    return query


def filter_performance_reviews(query_params: Mapping[str, str], query: SAQuery) -> SAQuery:
    if "employee_id" in query_params:
        query = query.filter(PerformanceReview.employee_id == int(query_params["employee_id"]))

    if "reviewer_id" in query_params:
        query = query.filter(PerformanceReview.reviewer_id == int(query_params["reviewer_id"]))

    if "rating" in query_params:
        query = query.filter(PerformanceReview.rating == int(query_params["rating"]))

    if "min_rating" in query_params:
        query = query.filter(PerformanceReview.rating >= int(query_params["min_rating"]))

    if "max_rating" in query_params:
        query = query.filter(PerformanceReview.rating <= int(query_params["max_rating"]))

    if "start_date" in query_params:
        query = query.filter(PerformanceReview.review_date >= query_params["start_date"])

    if "end_date" in query_params:
        query = query.filter(PerformanceReview.review_date <= query_params["end_date"])

    if "comment_contains" in query_params:
        query = query.filter(PerformanceReview.comments.ilike(f"%{query_params['comment_contains']}%"))

    return query




def filter_trainings(query_params: QueryParams, query: Query) -> Query:
    if "employee_id" in query_params:
        query = query.filter_by(employee_id=query_params.get("employee_id"))

    if "trainer_id" in query_params:
        query = query.filter_by(trainer_id=query_params.get("trainer_id"))

    if "department_id" in query_params:
        query = query.filter_by(department_id=query_params.get("department_id"))

    if "training_date" in query_params:
        query = query.filter_by(training_date=query_params.get("training_date"))

    if "from_date" in query_params:
        query = query.filter(models.Training.training_date >= query_params.get("from_date"))

    if "to_date" in query_params:
        query = query.filter(models.Training.training_date <= query_params.get("to_date"))

    if "training_title" in query_params:
        query = query.filter(models.Training.training_title.ilike(f"%{query_params.get('training_title')}%"))

    if "description" in query_params:
        query = query.filter(models.Training.description.ilike(f"%{query_params.get('description')}%"))

    return query


def filter_training_participants(query_params: QueryParams, query: Query) -> Query:
    if "training_id" in query_params:
        query = query.filter(models.TrainingParticipant.training_id == query_params.get("training_id"))

    if "employee_id" in query_params:
        query = query.filter(models.TrainingParticipant.employee_id == query_params.get("employee_id"))

    if "created_by_user_id" in query_params:
        query = query.filter(models.TrainingParticipant.created_by_user_id == query_params.get("created_by_user_id"))

    if "updated_by_user_id" in query_params:
        query = query.filter(models.TrainingParticipant.updated_by_user_id == query_params.get("updated_by_user_id"))

    return query

def filter_audit_logs(params, query):
    if action := params.get("action"):
        query = query.filter(models.AuditLog.action.ilike(f"%{action}%"))
    if table := params.get("table_name"):
        query = query.filter(models.AuditLog.table_name.ilike(f"%{table}%"))
    if performed_by := params.get("performed_by_user_id"):
        query = query.filter(models.AuditLog.performed_by_user_id == int(performed_by))
    if logged_by := params.get("logged_by_user_id"):
        query = query.filter(models.AuditLog.logged_by_user_id == int(logged_by))
    if record_id := params.get("record_id"):
        query = query.filter(models.AuditLog.record_id == int(record_id))
    return query

def filter_education_experiences(params: dict, query):
    if "degree" in params:
        query = query.filter(models.EducationExperience.degree.ilike(f"%{params['degree']}%"))
    if "institution_name" in params:
        query = query.filter(models.EducationExperience.institution_name.ilike(f"%{params['institution_name']}%"))
    if "field_of_study" in params:
        query = query.filter(models.EducationExperience.field_of_study.ilike(f"%{params['field_of_study']}%"))
    if "employee_id" in params:
        query = query.filter(models.EducationExperience.employee_id == int(params["employee_id"]))
    return query


from typing import Dict
from sqlalchemy.orm import Query
from app import models


def filter_employee_experiences(params: Dict, query: Query):
    if employee_id := params.get("employee_id"):
        query = query.filter(models.EmployeeExperience.employee_id == int(employee_id))

    if job_title := params.get("job_title"):
        query = query.filter(models.EmployeeExperience.job_title.ilike(f"%{job_title}%"))

    if company_name := params.get("company_name"):
        query = query.filter(models.EmployeeExperience.company_name.ilike(f"%{company_name}%"))

    if start_date := params.get("start_date"):
        query = query.filter(models.EmployeeExperience.start_date >= start_date)

    if end_date := params.get("end_date"):
        query = query.filter(models.EmployeeExperience.end_date <= end_date)

    return query



def filter_permissions(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Permission.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query


def filter_roles(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Role.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query



def get_first_error_message(exc: RequestValidationError, default_message="Invalid input"):
    try:
        first_error = exc.errors()[0]
        loc = first_error.get("loc", [])
        msg = first_error.get("msg", default_message)

        if loc:
            field = loc[-1]  # the field name (e.g., job_title)
            return f"{field}: {msg}"
        return msg
    except Exception:
        return default_message



import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email_notification(to_email: str, subject: str, message: str):
    sender_email = os.getenv("EMAIL_USER", "default@gmail.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "")
    email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port = int(os.getenv("EMAIL_PORT", 465))

    print(f"Preparing to send email to: {to_email}")
    print(f"SMTP Server: {email_host}:{email_port}, From: {sender_email}")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(email_host, email_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"[SUCCESS] Email sent to {to_email}")
    except Exception as e:
        print("[ERROR] Failed to send email:", str(e))

import os
from datetime import datetime

LOG_FILE_PATH = "app/logs/leave_actions.log"  # You can customize the path

def log_action(message: str):
    print("📄 Writing log:", message)  # TEMP
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, "a") as log_file:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")


# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "syedjawadali92@gmail.com"
# EMAIL_HOST_PASSWORD = "ctpgxfclwyucweni"


# app/utils/redis_client.py

import redis
from redis.exceptions import RedisError
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()  # Try connecting to Redis
    print("✅ Redis connected successfully.")
except RedisError as e:
    print("❌ Redis connection failed:", e)
    redis_client = None

from fastapi import HTTPException
from sqlalchemy.orm import Query

def get_object_or_404(query: Query, id: int, name: str = "Object"):
    obj = query.filter_by(id=id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{name} with id {id} not found")
    return obj
