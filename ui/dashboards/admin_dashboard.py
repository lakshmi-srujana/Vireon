import customtkinter as ctk
from PIL import Image
from ui.dashboards.student_page import StudentsPage
from ui.dashboards.analytics_page import AnalyticsPage
from ui.dashboards.faculty_page import FacultyPage
from ui.dashboards.users import UsersPage
from ui.dashboards.audit_log_page import AuditLogPage
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
from utils.resource_path import resource_path
import matplotlib.pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)


class AdminDashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(width=1200, height=700)

        # ---------------- BACKGROUND IMAGE ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/images/vireon_admindashboard.png")),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(
            self,
            image=bg_image,
            text=""
        )

        bg_label.place(x=0, y=0)

        self.bg_image = bg_image

        # ------------------------------------------------ #
        # MYSQL CONNECTION
        # ------------------------------------------------ #

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        self.cursor = self.connection.cursor()

        # ---------------- SIDEBAR ITEMS ---------------- #

        sidebar_items = [
            "Dashboard",
            "Students",
            "Analytics",
            "Users",
            "Faculty",
            "Audit Log",
            "Export CSV"
        ]

        y = 155

        for text in sidebar_items:

            if text == "Students":
                button_command = self.open_students
            elif text == "Analytics":
                button_command = self.open_analytics
            elif text == "Faculty":
                button_command = self.open_faculty_page
            elif text == "Users":
                button_command = self.open_users_page
            elif text == "Audit Log":
                button_command = self.open_audit_logs
            elif text == "Dashboard":  
                button_command = self.open_dashboard
            elif text == "Export CSV":
                button_command = self.open_export_center
            else:
                button_command = None

            item = ctk.CTkButton(
                self,
                text=text,
                width=105,
                height=30,
                corner_radius=2,
                fg_color="#bfcbe2",
                hover_color="#c9d5eb",
                text_color="#5976BA",
                border_width=0,
                font=("Georgia", 14),
                anchor="center",
                cursor="hand2",
                command=button_command
            )

            item.place(x=135, y=y)

            y += 65

        # ---------------- LOGOUT BUTTON ---------------- #

        logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=118,
            height=32,
            corner_radius=5,
            fg_color="#8792AE",
            hover_color="#7380A3",
            text_color="#F5F8F9",
            border_width=0,
            font=("Georgia", 16),
            command=self.logout
        )

        logout_button.place(x=105, y=600)

        # ------------------------------------------------ #
        # PERFORMANCE ANALYTICS GRAPH
        # ------------------------------------------------ #

        graph_frame = ctk.CTkFrame(
            self,
            width=400,
            height=250,
            fg_color="#EDF3FF",
            corner_radius=1
        )

        graph_frame.place(
            x=310,
            y=390
        )

        graph_title = ctk.CTkLabel(
            graph_frame,
            text="Department Analytics",
            text_color="#5976BA",
            font=("Georgia", 24),
            fg_color="transparent"
        )

        graph_title.place(
            x=25,
            y=15
        )

        # ------------------------------------------------ #
        # FETCH GRAPH DATA
        # ------------------------------------------------ #

        self.cursor.execute(
            """
            SELECT
            department,
            average_attendance

            FROM department_summary
            """
        )

        graph_data = self.cursor.fetchall()

        departments = []
        attendance = []

        for row in graph_data:

            departments.append(row[0])
            attendance.append(float(row[1]))

        # ------------------------------------------------ #
        # CREATE MATPLOTLIB GRAPH
        # ------------------------------------------------ #

        fig, ax = plt.subplots(
            figsize=(4.6, 2.5),
            dpi=100
        )

        fig.patch.set_facecolor("#EDF3FF")

        ax.set_facecolor("#EDF3FF")

        ax.plot(
            departments,
            attendance,
            marker="o",
            linewidth=2
        )

        ax.set_title(
            "Average Attendance"
        )

        # ------------------------------------------------ #
        # EMBED GRAPH
        # ------------------------------------------------ #

        canvas = FigureCanvasTkAgg(
            fig,
            master=graph_frame
        )

        canvas.draw()
        plt.close(fig)

        canvas.get_tk_widget().place(
            x=15,
            y=60
        )
        # ------------------------------------------------ #
        # TOP PERFORMERS PANEL
        # ------------------------------------------------ #

        leaderboard_panel = ctk.CTkFrame(
            self,
            width=360,
            height=220,
            fg_color="#EDF3FF",
            corner_radius=1
        )

        leaderboard_panel.place(
            x=780,
            y=420
        )

        leaderboard_title = ctk.CTkLabel(
            leaderboard_panel,
            text="Top Performers",
            text_color="#5976BA",
            font=("Georgia", 24),
            fg_color="transparent"
        )

        leaderboard_title.place(
            x=35,
            y=20
        )

        # ------------------------------------------------ #
        # FETCH DASHBOARD STATS
        # ------------------------------------------------ #

        # Total Students
        self.cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        total_students = self.cursor.fetchone()[0]

        # Total Faculty
        self.cursor.execute(
            "SELECT COUNT(*) FROM faculty"
        )

        total_faculty = self.cursor.fetchone()[0]

        # Average Attendance
        self.cursor.execute(
            """
            SELECT ROUND(AVG(attendance), 0)
            FROM students
            """
        )

        average_attendance = self.cursor.fetchone()[0]

        # Attendance Alerts
        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM attendance_alerts
            """
        )

        total_alerts = self.cursor.fetchone()[0]

        # ------------------------------------------------ #
        # DASHBOARD CARDS
        # ------------------------------------------------ #

        cards = [
            (str(total_students), "Students", 330),
            (str(total_faculty), "Faculty", 530),
            (f"{average_attendance}%", "Attendance", 730),
            (str(total_alerts), "Alerts", 930)
        ]

        for value, label, x in cards:

            card = ctk.CTkFrame(
                self,
                width=170,
                height=115,
                fg_color="#EDF3FF",
                corner_radius=1
            )

            card.place(x=x, y=250)

            value_label = ctk.CTkLabel(
                card,
                text=value,
                text_color="#19325F",
                font=("Georgia", 34, "bold"),
                fg_color="transparent"
            )

            value_label.place(
                relx=0.5,
                rely=0.38,
                anchor="center"
            )

            text_label = ctk.CTkLabel(
                card,
                text=label,
                text_color="#6E7FA5",
                font=("Georgia", 15),
                fg_color="transparent"
            )

            text_label.place(
                relx=0.5,
                rely=0.72,
                anchor="center"
            )

        # ------------------------------------------------ #
        # TOP PERFORMERS
        # ------------------------------------------------ #

        self.cursor.execute(
            """
            SELECT
            full_name,
            attendance

            FROM students

            ORDER BY attendance DESC

            LIMIT 4
            """
        )

        performers = self.cursor.fetchall()

        y = 70

        for name, score in performers:

            name_label = ctk.CTkLabel(
                leaderboard_panel,
                text=name,
                text_color="#4F648F",
                font=("Georgia", 16),
                fg_color="transparent"
            )

            name_label.place(
                x=35,
                y=y
            )

            score_label = ctk.CTkLabel(
                leaderboard_panel,
                text=f"{score}%",
                text_color="#5976BA",
                font=("Georgia", 16, "bold"),
                fg_color="transparent"
            )

            score_label.place(
                x=235,
                y=y
            )

            y += 32

    # ---------------- OPEN STUDENT PAGE ---------------- #

    def open_students(self):

        student_window = ctk.CTkToplevel(self)

        student_window.geometry("1200x700+160+70")
        student_window.title("Vireon")
        student_window.resizable(False, False)

        page = StudentsPage(student_window)
        page.pack(fill="both", expand=True)

        self.master.withdraw()

        def on_close():
            student_window.destroy()
            self.master.deiconify()

        student_window.protocol("WM_DELETE_WINDOW", on_close)
    def open_analytics(self):

        analytics_window = ctk.CTkToplevel(self)

        analytics_window.geometry("1200x700+160+70")

        analytics_window.title("Vireon Analytics")

        analytics_window.resizable(False, False)

        page = AnalyticsPage(analytics_window)

        page.pack(fill="both", expand=True)

        analytics_window.focus_force()

        analytics_window.grab_set()
    def open_faculty_page(self):

        faculty_window = ctk.CTkToplevel(self)

        faculty_window.geometry("1200x700+160+70")
        faculty_window.title("Vireon")
        faculty_window.resizable(False, False)

        page = FacultyPage(faculty_window)
        page.pack(fill="both", expand=True)

        self.master.withdraw()

        def on_close():
            faculty_window.destroy()
            self.master.deiconify()
        faculty_window.protocol("WM_DELETE_WINDOW", on_close)
    def open_users_page(self):
        self.destroy()

        users_page = UsersPage(
            self.master
        )

        users_page.pack(
            fill="both",
            expand=True
        )
    def open_audit_logs(self):

        self.destroy()

        page = AuditLogPage(
            self.master
        )

        page.pack(
            fill="both",
            expand=True
        )
    def logout(self):

        try:

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="vireon"
            )

            cursor = connection.cursor()

            query = """
            INSERT INTO audit_logs
            (
                action_type,
                performed_by
            )

            VALUES
            (
                %s,
                %s
            )
            """

            cursor.execute(
                query,
                (
                    "LOGOUT",
                    "admin"
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

        except Exception as e:

            print(
                "Logout Audit Error:",
                e
            )

        self.destroy()

        from ui.login_page import LoginPage

        login_page = LoginPage(
            self.master
        )

        login_page.pack(
            fill="both",
            expand=True
        )
    def open_dashboard(self):

        self.destroy()

        dashboard = AdminDashboard(
            self.master
        )

        dashboard.pack(
            fill="both",
            expand=True
        )
    # ------------------------------------------------ #
    # EXPORT CENTER
    # ------------------------------------------------ #

    def open_export_center(self):

        export_window = ctk.CTkToplevel(self)

        export_window.title("Vireon Export Center")

        export_window.geometry(
            "500x420+500+200"
        )

        export_window.configure(
            fg_color="#EEF3FF"
        )

        export_window.grab_set()

        # ------------------------------------------------ #
        # TITLE
        # ------------------------------------------------ #

        title = ctk.CTkLabel(
            export_window,
            text="Export Center",
            font=("Georgia", 32, "bold"),
            text_color="#4D63B3"
        )

        title.pack(
            pady=(30, 20)
        )

        # ------------------------------------------------ #
        # EXPORT STUDENTS
        # ------------------------------------------------ #

        students_button = ctk.CTkButton(
            export_window,
            text="Export Students CSV",
            width=300,
            height=50,
            fg_color="#5B6FB8",
            hover_color="#445AA8",
            font=("Georgia", 20),
            command=lambda:self.export_table_csv("students")
        )

        students_button.pack(
            pady=12
        )

        # ------------------------------------------------ #
        # EXPORT FACULTY
        # ------------------------------------------------ #

        faculty_button = ctk.CTkButton(
            export_window,
            text="Export Faculty CSV",
            width=300,
            height=50,
            fg_color="#5B6FB8",
            hover_color="#445AA8",
            font=("Georgia", 20),
            command=lambda: self.export_table_csv("faculty")
        )

        faculty_button.pack(
            pady=12
        )

        # ------------------------------------------------ #
        # EXPORT USERS
        # ------------------------------------------------ #

        users_button = ctk.CTkButton(
            export_window,
            text="Export Users CSV",
            width=300,
            height=50,
            fg_color="#5B6FB8",
            hover_color="#445AA8",
            font=("Georgia", 20),
            command=lambda:self.export_table_csv("users")
        )

        users_button.pack(
            pady=12
        )

        # ------------------------------------------------ #
        # EXPORT AUDIT LOGS
        # ------------------------------------------------ #

        logs_button = ctk.CTkButton(
            export_window,
            text="Export Audit Logs CSV",
            width=300,
            height=50,
            fg_color="#5B6FB8",
            hover_color="#445AA8",
            font=("Georgia", 20),
            command=lambda:self.export_table_csv("audit_logs")
        )

        logs_button.pack(
            pady=12
        )
    # ------------------------------------------------ #
    # EXPORT FUNCTION
    # ------------------------------------------------ #

    def export_table_csv(self, table_name):

        try:

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="vireon"
            )

            cursor = connection.cursor()

            cursor.execute(
                f"SELECT * FROM {table_name}"
            )

            data = cursor.fetchall()

            columns = [
                column[0]
                for column in cursor.description
            ]

            df = pd.DataFrame(
                data,
                columns=columns
            )

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[
                    ("CSV files", "*.csv")
                ],
                title=f"Save {table_name} CSV"
            )

            if file_path:

                df.to_csv(
                    file_path,
                    index=False
                )

                messagebox.showinfo(
                    "Export Success",
                    f"{table_name} exported successfully!"
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )
            
if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")
    app.title("Vireon")
    app.resizable(False, False)

    dashboard = AdminDashboard(app)
    dashboard.pack(fill="both", expand=True)

    app.mainloop()