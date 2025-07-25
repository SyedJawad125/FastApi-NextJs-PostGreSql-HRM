# user schemas
from .user import (
    UserBase,
    UserCreate,
    LoginRequest,
    UserUpdate,
    UserOut,
    Token,
    TokenData,
    TokenResponse
)

# employee schemas
from .employee import (
    Employee,
    EmployeeCreate,
    PaginatedEmployees,
    EmployeeListResponse,
    EmployeeUpdate
)

# department schemas
from .department import (
    DepartmentBase,
    DepartmentCreate,
    Department,
    DepartmentUpdate,
    PaginatedDepartments,
    DepartmentListResponse
)
from .rank import (
    RankBase,
    RankCreate,
    Rank,
    RankUpdate,
    PaginatedRanks,
    RankListResponse
)
from .attendance import (
    AttendanceBase,
    AttendanceCreate,
    Attendance,
    AttendanceUpdate,
    PaginatedAttendances,
    AttendanceListResponse
)
from .timesheet import (
    TimesheetBase,
    TimesheetCreate,
    Timesheet,
    TimesheetUpdate,
    PaginatedTimesheets,
    TimesheetListResponse
)

from .leave import (
    LeaveStatus,
    LeaveType,
    LeaveBase,
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse,
    CreateLeaveResponse,
    LeaveList,
    GetAllLeaveListResponse,
    LeaveListResult,
    MyLeaveListResponse
)

from .permission import (
    PermissionBase,
    PermissionCreate,
    PermissionUpdate,
    Permission,
    PaginatedPermissions,
    PermissionListResponse
)
from .role import (
    RoleBase,
    RoleCreate,
    RoleUpdate,
    Role,
    PaginatedRoles,
    RoleListResponse
)

from .notification import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    Notification,
    NotificationResponse,
    PaginatedNotifications,
    NotificationListResponse
)
from .employee_salary import (
    EmployeeSalaryBase,
    EmployeeSalaryCreate,
    EmployeeSalaryUpdate,
    EmployeeSalaryOut,
    EmployeeSalaryListResponse
)
from .salary_structure import (
    PaymentFrequency,
    SalaryStructureBase,
    SalaryStructureCreate,
    SalaryStructureUpdate,
    SalaryStructureOut,
    SalaryStructureListResponse
) 
from .payslip import (
    PayslipStatus,
    PayslipBase,
    PayslipCreate,
    PayslipUpdate,
    PayslipOut,
    PayslipListResponse
)
from .salary_history import (
    ChangeType,
    SalaryHistoryBase,
    SalaryHistoryCreate,
    SalaryHistoryUpdate,
    SalaryHistoryOut,
    SalaryHistoryListResponse
)
from .image_category import (
    ImageCategoryBase,
    ImageCategoryCreate,
    ImageCategoryUpdate,
    PaginatedImageCategory,
    ImageCategoryListResponse
)       
from .image import (
    ImageBase,
    ImageCreate,    
    ImageUpdate,
    ImageOut,
)
from .employee_profile import (
    EmployeeProfileBase,
    EmployeeProfileCreate,
    EmployeeProfileUpdate,
    EmployeeProfileOut,
    PaginatedEmployeeProfiles,
    EmployeeProfileListResponse
)
from .employee_documents import (
    DocumentType,
    EmployeeDocumentBase,
    EmployeeDocumentCreate,
    EmployeeDocumentUpdate,
    EmployeeDocumentOut
)
from .holiday_calendar import (
    HolidayCalendarBase,
    HolidayCalendarCreate,
    HolidayCalendarUpdate,
    HolidayCalendarOut
)  
from .shift import (
    ShiftBase,
    ShiftCreate,
    ShiftUpdate,
    ShiftOut,
    PaginatedShifts,
    ShiftListResponse
)
from .shift_assignments import (
    ShiftAssignmentBase,
    ShiftAssignmentCreate,
    ShiftAssignmentUpdate,
    ShiftAssignmentOut, 
    PaginatedShiftAssignments,
    ShiftAssignmentListResponse
)
from .candidate import (
    CandidateBase,
    CandidateCreate,
    CandidateUpdate,
    CandidateOut,
    PaginatedCandidates,
    CandidateListResponse
)
from .recruitment import (
    RecruitmentBase,
    RecruitmentCreate,
    RecruitmentUpdate,
    RecruitmentOut,
    PaginatedRecruitments,
    RecruitmentListResponse
)
from .performance_review import (
    PerformanceReviewBase,
    PerformanceReviewCreate,
    PerformanceReviewUpdate,
    PerformanceReviewOut,
    PaginatedPerformanceReviews,
    PerformanceReviewListResponse   
)
from .training import (
    TrainingBase,
    TrainingCreate,
    TrainingUpdate,
    TrainingOut,
    PaginatedTrainings,
    TrainingListResponse    
)
from .training_participant import (
    TrainingParticipantBase,
    TrainingParticipantCreate,
    TrainingParticipantUpdate,
    TrainingParticipantOut,
    PaginatedTrainingParticipants,
    TrainingParticipantListResponse     
)
from .audit_logs import (
    AuditLogBase,
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogOut,
    PaginatedAuditLogs,
    AuditLogListResponse
)   
from .education_experience import (
    EducationExperienceBase,
    EducationExperienceCreate,
    EducationExperienceUpdate,
    EducationExperienceOut,
    PaginatedEducationExperiences,
    EducationExperienceListResponse 
)
from .employee_experiences import (
    EmployeeExperienceBase,
    EmployeeExperienceCreate,
    EmployeeExperienceUpdate,
    EmployeeExperienceOut,
    PaginatedEmployeeExperiences,
    EmployeeExperienceListResponse  
)
# define what will be exported on `from schemas import *`
__all__ = [
    'UserBase', 'UserCreate', 'LoginRequest', 'UserUpdate', 'UserOut',
    'Token', 'TokenData', 'TokenResponse',
    'Employee', 'EmployeeCreate','PaginatedEmployees','EmployeeListResponse','EmployeeUpdate',
    'DepartmentBase', 'DepartmentCreate', 'Department', 'DepartmentUpdate',
    'PaginatedDepartments', 'DepartmentListResponse',
    'RankBase', 'RankCreate', 'Rank', 'RankUpdate', 'PaginatedRanks', 'RankListResponse',
    'AttendanceBase', 'AttendanceCreate', 'Attendance', 'AttendanceUpdate', 'PaginatedAttendances', 'AttendanceListResponse',
    'TimesheetBase', 'TimesheetCreate', 'Timesheet', 'TimesheetUpdate', 'PaginatedTimesheets', 'TimesheetListResponse',
    'LeaveStatus', 'LeaveType', 'LeaveBase', 'LeaveCreate', 'LeaveUpdate', 'LeaveResponse', 'CreateLeaveResponse',
    'LeaveList', 'GetAllLeaveListResponse',
    'LeaveListResult', 'MyLeaveListResponse',   
    'PermissionBase', 'PermissionCreate' ,'PermissionUpdate','Permission', 'PaginatedPermissions', 'PermissionListResponse',
    'RoleBase', 'RoleCreate', 'RoleUpdate', 'Role', 'PaginatedRoles', 'RoleListResponse',
    'NotificationBase', 'NotificationCreate', 'NotificationUpdate', 'Notification', 'NotificationResponse', 'PaginatedNotifications', 'NotificationListResponse',
    'EmployeeSalaryBase', 'EmployeeSalaryCreate', 'EmployeeSalaryUpdate', 'EmployeeSalaryOut', 'EmployeeSalaryListResponse',
    'PaymentFrequency', 'SalaryStructureBase', 'SalaryStructureCreate', 'SalaryStructureUpdate', 'SalaryStructureOut', 'SalaryStructureListResponse',
    'PayslipStatus', 'PayslipBase', 'PayslipCreate', 'PayslipUpdate', 'PayslipOut', 'PayslipListResponse',
    'ChangeType', 'SalaryHistoryBase', 'SalaryHistoryCreate', 'SalaryHistoryUpdate', 'SalaryHistoryOut', 'SalaryHistoryListResponse',
    'ImageCategoryBase', 'ImageCategoryCreate', 'ImageCategoryUpdate', 'PaginatedImageCategory', 'ImageCategoryListResponse',
    'ImageBase', 'ImageCreate', 'ImageUpdate', 'ImageOut',
    'EmployeeProfileBase', 'EmployeeProfileCreate', 'EmployeeProfileUpdate', 'EmployeeProfileOut', 'PaginatedEmployeeProfiles', 'EmployeeProfileListResponse',
    'DocumentType', 'EmployeeDocumentBase', 'EmployeeDocumentCreate', 'EmployeeDocumentUpdate', 'EmployeeDocumentOut',
    'HolidayCalendarBase', 'HolidayCalendarCreate', 'HolidayCalendarUpdate', 'HolidayCalendarOut', 'PaginatedHolidayCalendars', 'HolidayCalendarListResponse',
    'ShiftBase', 'ShiftCreate', 'ShiftUpdate', 'ShiftOut', 'PaginatedShifts', 'ShiftListResponse',
    'ShiftAssignmentBase', 'ShiftAssignmentCreate', 'ShiftAssignmentUpdate', 'ShiftAssignmentOut','PaginatedShiftAssignments' , 'ShiftAssignmentListResponse',
    'CandidateBase', 'CandidateCreate', 'CandidateUpdate', 'CandidateOut', 'PaginatedCandidates', 'CandidateListResponse',
    'RecruitmentBase', 'RecruitmentCreate', 'RecruitmentUpdate', 'RecruitmentOut', 'PaginatedRecruitments', 'RecruitmentListResponse',
    'PerformanceReviewBase', 'PerformanceReviewCreate', 'PerformanceReviewUpdate', 'PerformanceReviewOut', 'PaginatedPerformanceReviews', 'PerformanceReviewListResponse',
    'TrainingBase', 'TrainingCreate', 'TrainingUpdate', 'TrainingOut', 'PaginatedTrainings', 'TrainingListResponse',
    'TrainingParticipantBase', 'TrainingParticipantCreate', 'TrainingParticipantUpdate', 'TrainingParticipantOut', 'PaginatedTrainingParticipants', 'TrainingParticipantListResponse',
    'AuditLogBase', 'AuditLogCreate', 'AuditLogUpdate', 'AuditLogOut', 'PaginatedAuditLogs', 'AuditLogListResponse',
    'EducationExperienceBase', 'EducationExperienceCreate', 'EducationExperienceUpdate', 'EducationExperienceOut', 'PaginatedEducationExperiences', 'EducationExperienceListResponse',
    'EmployeeExperienceBase', 'EmployeeExperienceCreate', 'EmployeeExperienceUpdate', 'EmployeeExperienceOut', 'PaginatedEmployeeExperiences', 'EmployeeExperienceListResponse',
    ]

