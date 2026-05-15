import customtkinter as ctk
from PIL import Image
import mysql.connector
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from utils.resource_path import resource_path


class UsersPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            width=1200,
            height=700
        )

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

        # ------------------------------------------------ #
        # BACKGROUND IMAGE
        # ------------------------------------------------ #

        bg_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path("assets/images/vireon_common.png")
            ),
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
        # PAGE TITLE
        # ------------------------------------------------ #

        title = ctk.CTkLabel(
            self,
            text="User Management",
            font=("Georgia", 42, "bold"),
            text_color="#5B6FB8",
            fg_color="#EEF3FF"
        )

        title.place(
            x=420,
            y=40
        )

        # ------------------------------------------------ #
        # USERS OUTER FRAME
        # ------------------------------------------------ #

        users_frame = ctk.CTkFrame(
            self,
            width=1000,
            height=480,
            fg_color="#E9EDF7",
            corner_radius=6,
            border_width=2,
            border_color="#B8C4E4"
        )

        users_frame.place(
            x=100,
            y=120
        )

        # ------------------------------------------------ #
        # SCROLLABLE INNER FRAME
        # ------------------------------------------------ #

        scroll_frame = ctk.CTkScrollableFrame(
            users_frame,
            width=940,
            height=400,
            fg_color="#E9EDF7"
        )

        scroll_frame.place(
            x=20,
            y=50
        )

        # ------------------------------------------------ #
        # TABLE HEADERS
        # ------------------------------------------------ #

        headers = [
            "Username",
            "Role",
            "Linked ID",
            "Created At"
        ]

        x_positions = [
            40,
            280,
            500,
            720
        ]

        for i in range(len(headers)):

            header = ctk.CTkLabel(
                users_frame,
                text=headers[i],
                font=("Georgia", 20, "bold"),
                text_color="#4D63B3"
            )

            header.place(
                x=x_positions[i],
                y=20
            )

        # ------------------------------------------------ #
        # FETCH USERS
        # ------------------------------------------------ #

        self.cursor.execute(
            """
            SELECT
            username,
            role,
            linked_id,
            created_at

            FROM users
            """
        )

        users = self.cursor.fetchall()

        # ------------------------------------------------ #
        # DISPLAY USERS
        # ------------------------------------------------ #

        for user in users:

            row_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color="transparent"
            )

            row_frame.pack(
                fill="x",
                pady=8,
                padx=10
            )

            username = ctk.CTkLabel(
                row_frame,
                text=user[0],
                width=220,
                anchor="w",
                font=("Georgia", 16),
                text_color="#243B7C"
            )

            username.pack(
                side="left",
                padx=(10, 20)
            )

            role = ctk.CTkLabel(
                row_frame,
                text=user[1],
                width=180,
                anchor="w",
                font=("Georgia", 16),
                text_color="#243B7C"
            )

            role.pack(
                side="left",
                padx=(10, 20)
            )

            linked_id = ctk.CTkLabel(
                row_frame,
                text=str(user[2]),
                width=180,
                anchor="w",
                font=("Georgia", 16),
                text_color="#243B7C"
            )

            linked_id.pack(
                side="left",
                padx=(10, 20)
            )

            created_at = ctk.CTkLabel(
                row_frame,
                text=str(user[3]),
                width=250,
                anchor="w",
                font=("Georgia", 16),
                text_color="#243B7C"
            )

            created_at.pack(
                side="left",
                padx=(10, 20)
            )

        # ------------------------------------------------ #
        # BACK BUTTON
        # ------------------------------------------------ #

        back_button = ctk.CTkButton(
            self,
            text="Back",
            width=180,
            height=45,
            corner_radius=2,
            fg_color="#8792AE",
            hover_color="#7280A0",
            font=("Georgia", 22),
            command=self.go_back
        )

        back_button.place(
            x=630,
            y=605
        )
    
        # ------------------------------------------------ #
        # EXPORT BUTTON
        # ------------------------------------------------ #

        export_button = ctk.CTkButton(
            self,
            text="Export CSV",
            width=180,
            height=45,
            corner_radius=2,
            fg_color="#8792AE",
            hover_color="#7280A0",
            font=("Georgia", 22),
            command=self.export_users_csv
        )

        export_button.place(
            x=420,
            y=605
        )

    # ------------------------------------------------ #
    # GO BACK
    # ------------------------------------------------ #

    def go_back(self):

        self.destroy()

        from ui.dashboards.admin_dashboard import (
            AdminDashboard
        )

        dashboard = AdminDashboard(
            self.master
        )

        dashboard.pack(
            fill="both",
            expand=True
        )
    
    # ------------------------------------------------ #
    # EXPORT USERS CSV
    # ------------------------------------------------ #

    def export_users_csv(self):

        try:

            self.cursor.execute(
                """
                SELECT
                username,
                role,
                linked_id,
                created_at

                FROM users
                """
            )

            data = self.cursor.fetchall()

            df = pd.DataFrame(
                data,
                columns=[
                    "Username",
                    "Role",
                    "Linked ID",
                    "Created At"
                ]
            )

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Users Report"
            )

            if file_path:

                df.to_csv(
                    file_path,
                    index=False
                )

                messagebox.showinfo(
                    "Export Success",
                    "Users CSV exported successfully!"
                )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )