from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# Enable SQLAlchemy logging
import logging

from app.models import performance_review
from app.utils import get_first_error_message
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Import Base and engine from database (use absolute import)
from app.database import engine, Base

# Import all models explicitly (make sure these use Base from database.py)
from app.models.user import User
from app.models.department import Department
from app.models.role import Role
from app.models.permission import Permission
from app.models.rank import Rank
from app.models.attendance import Attendance
from app.models.timesheet import Timesheet
from app.models.leave import Leave
from app.models.notification import Notification
from app.models.employee_salary import EmployeeSalary
from app.models.salary_structure import SalaryStructure
from app.models.payslip import Payslip
from app.models.salary_history import SalaryHistory
from app.models.image_category import ImageCategory
from app.models.image import Image
from app.models.employee_profile import EmployeeProfile
from app.models.employee_documents import EmployeeDocument
from app.models.holiday_calendar import HolidayCalendar
from app.models.shift import Shift
from app.models.shift_assignments import ShiftAssignment
from app.models.candidate import Candidate
from app.models.recruitment import Recruitment
from app.models.performance_review import PerformanceReview
from app.models.training import Training
from app.models.training_participant import TrainingParticipant
from app.models.audit_logs import AuditLog
from app.models.education_experience import EducationExperience
from app.models.employee_experiences import EmployeeExperience

# Import routers
from app.routers import (
    employee, department, auth, user, 
    role, permission, rank, attendance, 
    timesheet, leave, notification, employee_salary,
    salary_structure, payslip, salary_history, 
    image_category,
    image, 
    employee_profile,
    employee_documents,
    holiday_calendar, shift , shift_assignments, 
    candidate, recruitment, performance_review, training, training_participant,
    audit_logs, education_experience, employee_experiences
)

app = FastAPI(
    title="HRM System",
    version="1.0.0",
    description="An API for managing HRM features",
    openapi_tags=[
        {
            "name": "Departments",
            "description": "Operations related to leave creation, approval, and management"
        },
        {
            "name": "Employees",
            "description": "Employee profile management"
        },
        {
            "name": "Users",
            "description": "User login and registration"
        },
        {
            "name": "Ranks",
            "description": "Rank profile management"
        },
        {
            "name": "Roles",
            "description": "Roles profile management"
        },
        {
            "name": "Notifications",
            "description": "User notifications management"
        },
        {
            "name": "Image Categories",
            "description": "Image categories management"
        }
    ]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = get_first_error_message(exc)
    return JSONResponse(
        status_code=422,
        content={"detail": message}
    )

# CORS settings to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.staticfiles import StaticFiles
import os
# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}
    
# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(rank.router)
app.include_router(attendance.router)
app.include_router(timesheet.router)
app.include_router(leave.router)
app.include_router(notification.router)
app.include_router(employee_salary.router)
app.include_router(salary_structure.router)
app.include_router(payslip.router)
app.include_router(salary_history.router)
app.include_router(image_category.router)
app.include_router(image.router)
app.include_router(employee_profile.router)
app.include_router(employee_documents.router)
app.include_router(holiday_calendar.router)
app.include_router(shift.router)
app.include_router(shift_assignments.router)
app.include_router(candidate.router)
app.include_router(recruitment.router)
app.include_router(performance_review.router)
app.include_router(training.router)
app.include_router(training_participant.router)
app.include_router(audit_logs.router)
app.include_router(education_experience.router)
app.include_router(employee_experiences.router)












@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    print(f"Engine URL: {engine.url}")
    print(f"Tables in metadata: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


@app.get("/")
def root():
    return {"message": "Welcome to HRM API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"status": "working"}
