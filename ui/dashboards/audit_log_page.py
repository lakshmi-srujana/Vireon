import customtkinter as ctk
from PIL import Image
import mysql.connector
import pandas as pd

from tkinter import filedialog
from utils.resource_path import resource_path
from tkinter import messagebox


class AuditLogPage(ctk.CTkFrame):

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
            light_image=Image.open(resource_path("assets/images/vireon_common.png")),
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
            text="Audit Logs",
            font=("Georgia", 42, "bold"),
            text_color="#5B6FB8",
            fg_color="#EEF3FF"
        )

        title.place(
            x=470,
            y=40
        )

        # ------------------------------------------------ #
        # OUTER FRAME
        # ------------------------------------------------ #

        logs_frame = ctk.CTkFrame(
            self,
            width=1000,
            height=480,
            fg_color="#E9EDF7",
            corner_radius=6,
            border_width=2,
            border_color="#B8C4E4"
        )

        logs_frame.place(
            x=100,
            y=120
        )

        # ------------------------------------------------ #
        # SCROLLABLE FRAME
        # ------------------------------------------------ #

        scroll_frame = ctk.CTkScrollableFrame(
            logs_frame,
            width=940,
            height=400,
            fg_color="#E9EDF7"
        )

        scroll_frame.place(
            x=20,
            y=50
        )

        # ------------------------------------------------ #
        # HEADERS
        # ------------------------------------------------ #

        headers = [
            "Log ID",
            "Action",
            "Student Roll",
            "Performed By",
            "Action Time"
        ]

        x_positions = [
            20,
            160,
            340,
            560,
            760
        ]

        for i in range(len(headers)):

            header = ctk.CTkLabel(
                logs_frame,
                text=headers[i],
                font=("Georgia", 18, "bold"),
                text_color="#4D63B3"
            )

            header.place(
                x=x_positions[i],
                y=20
            )

        # ------------------------------------------------ #
        # FETCH LOGS
        # ------------------------------------------------ #

        self.cursor.execute(
            """
            SELECT
            log_id,
            action_type,
            student_roll,
            performed_by,
            action_time

            FROM audit_logs

            ORDER BY action_time DESC
            """
        )

        logs = self.cursor.fetchall()

        # ------------------------------------------------ #
        # DISPLAY LOGS
        # ------------------------------------------------ #

        for log in logs:

            row_frame = ctk.CTkFrame(
                scroll_frame,
                fg_color="transparent"
            )

            row_frame.pack(
                fill="x",
                pady=8,
                padx=10
            )

            widths = [100, 140, 180, 180, 250]

            for i in range(5):

                label = ctk.CTkLabel(
                    row_frame,
                    text=str(log[i]),
                    width=widths[i],
                    anchor="w",
                    font=("Georgia", 15),
                    text_color="#243B7C"
                )

                label.pack(
                    side="left",
                    padx=(10, 10)
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
            fg_color="#5B6FB8",
            hover_color="#4A5AA3",
            font=("Georgia", 22),
            command=self.export_logs_csv
        )

        export_button.place(
            x=420,
            y=605
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
    # EXPORT LOGS CSV
    # ------------------------------------------------ #

    def export_logs_csv(self):

        try:

            self.cursor.execute(
                """
                SELECT log_id,
                action_type,
                student_roll,
                performed_by,
                action_time
                FROM audit_logs
                """
            )

            data = self.cursor.fetchall()

            df = pd.DataFrame(
                data,
                columns=[
                    "Log ID",
                    "Action Type",
                    "Student Roll",
                    "Performed By",
                    "Action Time"
                ]
            )

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Audit Logs"
            )

            if file_path:

                df.to_csv(
                    file_path,
                    index=False
                )

                messagebox.showinfo(
                    "Export Success",
                    "Audit logs exported successfully!"
                )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
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
