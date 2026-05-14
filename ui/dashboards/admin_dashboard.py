import customtkinter as ctk
from PIL import Image
from ui.dashboards.student_page import StudentsPage
from ui.dashboards.analytics_page import AnalyticsPage
from ui.dashboards.faculty_page import FacultyPage
from ui.dashboards.users import UsersPage
from ui.dashboards.audit_log_page import AuditLogPage


class AdminDashboard(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(width=1200, height=700)

        # ---------------- BACKGROUND IMAGE ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open("assets/images/vireon_admindashboard.png"),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(
            self,
            image=bg_image,
            text=""
        )

        bg_label.place(x=0, y=0)

        self.bg_image = bg_image



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
            font=("Georgia", 16)
        )

        logout_button.place(x=105, y=600)


        # ---------------- DASHBOARD CARDS ---------------- #

        cards = [
            ("520", "Students", 330),
            ("48", "Faculty", 530),
            ("92%", "Attendance", 730),
            ("12", "Alerts", 930)
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

            value_label.place(relx=0.5, rely=0.38, anchor="center")

            text_label = ctk.CTkLabel(
                card,
                text=label,
                text_color="#6E7FA5",
                font=("Georgia", 15),
                fg_color="transparent"
            )

            text_label.place(relx=0.5, rely=0.72, anchor="center")

        # ---------------- ANALYTICS PANEL ---------------- #

        analytics_panel = ctk.CTkFrame(
            self,
            width=420,
            height=210,
            fg_color="#EDF3FF",
            corner_radius=10
        )

        analytics_panel.place(x=310, y=420)

        analytics_title = ctk.CTkLabel(
            analytics_panel,
            text="Performance Analytics",
            text_color="#5976BA",
            font=("Georgia", 22),
            fg_color="transparent"
        )

        analytics_title.place(x=25, y=20)

        analytics_placeholder = ctk.CTkLabel(
            analytics_panel,
            text="Graph area",
            text_color="#8A9CC2",
            font=("Georgia", 16),
            fg_color="transparent"
        )

        analytics_placeholder.place(relx=0.5, rely=0.55, anchor="center")

        # ---------------- TOP PERFORMERS PANEL ---------------- #

        leaderboard_panel = ctk.CTkFrame(
            self,
            width=320,
            height=210,
            fg_color="#EDF3FF",
            corner_radius=10
        )

        leaderboard_panel.place(x=780, y=420)

        leaderboard_title = ctk.CTkLabel(
            leaderboard_panel,
            text="Top Performers",
            text_color="#5976BA",
            font=("Georgia", 22),
            fg_color="transparent"
        )

        leaderboard_title.place(x=25, y=20)

        performers = [
            ("Aarav", "98%"),
            ("Diya", "96%"),
            ("Vihaan", "95%"),
            ("Meera", "94%")
        ]

        y = 70

        for name, score in performers:

            name_label = ctk.CTkLabel(
                leaderboard_panel,
                text=name,
                text_color="#4F648F",
                font=("Georgia", 16),
                fg_color="transparent"
            )

            name_label.place(x=35, y=y)

            score_label = ctk.CTkLabel(
                leaderboard_panel,
                text=score,
                text_color="#5976BA",
                font=("Georgia", 16, "bold"),
                fg_color="transparent"
            )

            score_label.place(x=235, y=y)

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
        
if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")
    app.title("Vireon")
    app.resizable(False, False)

    dashboard = AdminDashboard(app)
    dashboard.pack(fill="both", expand=True)

    app.mainloop()