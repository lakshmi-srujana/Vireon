"""
Vireon - Student Performance Analyzer

Final application entry point.

The project is organized into modules under ui/, utils/, and database/.
This file launches the complete application and keeps the public imports in
one place for submission and packaging.
"""

import customtkinter as ctk

from database.db_connection import get_connection
from ui.dashboards.admin_dashboard import AdminDashboard
from ui.dashboards.analytics_page import AnalyticsPage
from ui.dashboards.audit_log_page import AuditLogPage
from ui.dashboards.faculty_dashboard import FacultyDashboard
from ui.dashboards.faculty_page import FacultyPage
from ui.dashboards.student_dashboard import StudentDashboard
from ui.dashboards.student_page import StudentsPage
from ui.dashboards.users import UsersPage
from ui.login_page import LoginPage
from ui.splash_screen import SplashScreen
from utils.audit import log_audit
from utils.auth import login_user
from utils.resource_path import resource_path


APP_TITLE = "Vireon"
APP_GEOMETRY = "1200x700+160+70"


def show_login(app, splash):

    splash.pack_forget()

    login = LoginPage(app)

    login.pack(
        fill="both",
        expand=True
    )


def create_app():

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry(APP_GEOMETRY)

    app.title(APP_TITLE)

    app.resizable(False, False)

    splash = SplashScreen(
        app,
        lambda: show_login(app, splash)
    )

    splash.pack(
        fill="both",
        expand=True
    )

    return app


def main():

    app = create_app()

    app.mainloop()


if __name__ == "__main__":

    main()


__all__ = [
    "AdminDashboard",
    "AnalyticsPage",
    "AuditLogPage",
    "FacultyDashboard",
    "FacultyPage",
    "LoginPage",
    "SplashScreen",
    "StudentDashboard",
    "StudentsPage",
    "UsersPage",
    "create_app",
    "get_connection",
    "log_audit",
    "login_user",
    "main",
    "resource_path",
    "show_login",
]
