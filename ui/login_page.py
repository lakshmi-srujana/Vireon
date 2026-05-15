import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from utils.auth import login_user
from ui.dashboards.admin_dashboard import AdminDashboard
from ui.dashboards.student_dashboard import StudentDashboard
from ui.dashboards.faculty_dashboard import FacultyDashboard
from utils.audit import log_audit
from utils.resource_path import resource_path


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # ---------------- BACKGROUND IMAGE ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/images/vireon.png")),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(self, image=bg_image, text="")
        bg_label.place(x=0, y=0)

        # Keep image alive
        self.image = bg_image

        # ---------------- ROLE MENU ---------------- #

        self.role_menu = ctk.CTkOptionMenu(
            self,
            values=["Admin", "Faculty", "Student"],
            width=300,
            height=22,
            fg_color="#A3BEDD",
            button_color="#A3BEDD",
            button_hover_color="#A3BEDD",
            dropdown_fg_color="#EDF3FF",
            dropdown_hover_color="#D1DDF8",
            dropdown_text_color="#19325F",
            text_color="#19325F",
            font=("Georgia", 14),
            corner_radius=15,
            anchor="w"
        )

        self.role_menu.place(x=680, y=310)

        # ---------------- USERNAME ENTRY ---------------- #

        self.username_entry = ctk.CTkEntry(
            self,
            width=300,
            height=22,
            corner_radius=25,
            fg_color="#A3BEDD",
            border_width=0,
            text_color="#19325F",
            font=("Georgia", 14)
        )

        self.username_entry.place(x=680, y=390)

        # ---------------- PASSWORD ENTRY ---------------- #

        self.password_entry = ctk.CTkEntry(
            self,
            width=300,
            height=22,
            corner_radius=25,
            fg_color="#A3BEDD",
            border_width=0,
            text_color="#19325F",
            show="•",
            font=("Georgia", 14)
        )

        self.password_entry.place(x=680, y=470)

        # ---------------- FORGOT PASSWORD ---------------- #

        forgot_password = tk.Label(
            self,
            text="Forgot Password?",
            fg="#7D88A8",
            bg="#EAF1FB",
            cursor="hand2",
            font=("Georgia", 13)
        )

        forgot_password.place(x=1190, y=635)

        forgot_password.bind(
            "<Button-1>",
            lambda e:
            self.show_forgot_password_message()
        )

        # ---------------- LOGIN BUTTON ---------------- #

        login_button = ctk.CTkButton(
            self,
            text="Login",
            width=220,
            height=48,
            corner_radius=30,
            fg_color="#8792AE",
            text_color="#F5F8F9",
            border_width=0,
            font=("Georgia", 30),
            command=self.handle_login,
        )

        login_button.place(x=760, y=545)

    def show_forgot_password_message(self):

        selected_role = self.role_menu.get()

        if selected_role.lower() == "admin":

            messagebox.showinfo(
                "Admin Password Recovery",
                "Admin password recovery is\nhandled directly through MySQL."
            )

        else:

            messagebox.showinfo(
                "Forgot Password",
                "Please contact the administrator\nfor password reset."
            )

    # ---------------- LOGIN FUNCTION ---------------- #

    def handle_login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()

        selected_role = self.role_menu.get()

        user = login_user(username, password)

        if user:

            role = user["role"]

            # ---------- ROLE VALIDATION ---------- #

            if role.lower() != selected_role.lower():

                messagebox.showerror(
                    "Role Error",
                    f"This account is not registered as {selected_role}"
                )

                return

            messagebox.showinfo(
                "Login Success",
                f"Welcome {username}!\nRole: {role}"
            )

            self.destroy()
            log_audit(
                "LOGIN",
                username,
                username,
                role
            )

            # ---------- ADMIN DASHBOARD ---------- #

            if role.lower() == "admin":

                dashboard = AdminDashboard(self.master)

                dashboard.pack(
                    fill="both",
                    expand=True
                )

            # ---------- STUDENT DASHBOARD ---------- #

            elif role.lower() == "student":

                dashboard = StudentDashboard(
                    self.master,
                    user["linked_id"]
                )

                dashboard.pack(
                    fill="both",
                    expand=True
                )

            # ---------- FACULTY DASHBOARD ---------- #

            elif role.lower() == "faculty":

                dashboard = FacultyDashboard(
                    self.master,
                    user["linked_id"]
                )

                dashboard.pack(
                    fill="both",
                    expand=True
                )

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )
            log_audit(
                "FAILED LOGIN",
                username,
                username,
                "unknown"
            )