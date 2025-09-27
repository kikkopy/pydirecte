# pydirecte/__init__.py

"""
pydirecte - A Python API wrapper for EcoleDirecte
"""

from .index import (
    # Exceptions
    BadCredentials,
    DoubleAuthRequired,
    InvalidVersion,
    SessionTokenRequired,
    BadDoubleAuth,
    
    # Session & Auth
    Session,
    DoubleAuth,
    DoubleAuthChallenge,
    login,
    refresh,
    set_access_token,
    init_double_auth,
    check_double_auth,
    
    # Student API
    student_grades,
    student_homeworks,
    student_coming_homeworks,
    set_homework_state,
    student_attendance,
    student_cantine,
    student_documents,
    student_timetable,
    student_timeline,
    student_homepage_timeline,
    student_workspace,
    student_visios,
    student_received_messages,
    read_message,
    
    # Account API
    account_edforms,
    
    # Files
    get_file,
    build_file_download_url,
    
    # Models
    Account,
    Grade,
    GradeValue,
    Homework,
    ComingHomework,
    ClassSubject,
    Document,
    TimetableItem,
    TimelineItem,
    HomepageTimelineItem,
    ReceivedMessage,
    AttendanceItem,
    Period,
    SubjectOverview,
    PeriodOverview,
    CantineReservations,
    CantineBarcode,
    WorkspaceItem,
    Skill,
    Subject,
    
    # Enums
    AccountKind,
    GradeKind,
    FileKind,
    DocumentKind,
    AttendanceItemKind,
    TimetableItemKind,
    TimelineItemKind,
    WorkspaceItemKind,
    
    # Request/Response classes
    Request,
    Response,
)

__all__ = [
    # Exceptions
    "BadCredentials",
    "DoubleAuthRequired",
    "InvalidVersion",
    "SessionTokenRequired",
    "BadDoubleAuth",
    
    # Session & Auth
    "Session",
    "DoubleAuth",
    "DoubleAuthChallenge",
    "login",
    "refresh",
    "set_access_token",
    "init_double_auth",
    "check_double_auth",
    
    # Student API
    "student_grades",
    "student_homeworks",
    "student_coming_homeworks",
    "set_homework_state",
    "student_attendance",
    "student_cantine",
    "student_documents",
    "student_timetable",
    "student_timeline",
    "student_homepage_timeline",
    "student_workspace",
    "student_visios",
    "student_received_messages",
    "read_message",
    
    # Account API
    "account_edforms",
    
    # Files
    "get_file",
    "build_file_download_url",
    
    # Models
    "Account",
    "Grade",
    "GradeValue",
    "Homework",
    "ComingHomework",
    "ClassSubject",
    "Document",
    "TimetableItem",
    "TimelineItem",
    "HomepageTimelineItem",
    "ReceivedMessage",
    "AttendanceItem",
    "Period",
    "SubjectOverview",
    "PeriodOverview",
    "CantineReservations",
    "CantineBarcode",
    "WorkspaceItem",
    "Skill",
    "Subject",
    
    # Enums
    "AccountKind",
    "GradeKind",
    "FileKind",
    "DocumentKind",
    "AttendanceItemKind",
    "TimetableItemKind",
    "TimelineItemKind",
    "WorkspaceItemKind",
    
    # Request/Response classes
    "Request",
    "Response",
]

__version__ = "1.0.3"
__author__ = "kikkopy"
__license__ = "GPL-3.0-or-later"