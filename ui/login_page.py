import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from utils.auth import login_user
from ui.dashboards.admin_dashboard import AdminDashboard


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # ---------------- BACKGROUND IMAGE ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open("assets/images/vireon.png"),
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

    # ---------------- LOGIN FUNCTION ---------------- #

    def handle_login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(username, password)

        if user:

            role = user['role']

            messagebox.showinfo(
                "Login Success",
                f"Welcome {username}!\nRole: {role}"
            )

            self.destroy()

            dashboard = AdminDashboard(self.master)
            dashboard.pack(fill="both", expand=True)

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )