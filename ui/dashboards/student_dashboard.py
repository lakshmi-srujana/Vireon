import customtkinter as ctk
import mysql.connector

from PIL import Image

from tkinter import filedialog
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage
)

from reportlab.lib.styles import getSampleStyleSheet

import tempfile
import os
from utils.resource_path import resource_path


class StudentDashboard(ctk.CTkFrame):

    def __init__(self, parent, student_roll_no):

        super().__init__(parent)

        self.student_roll_no = student_roll_no

        self.configure(
            width=1200,
            height=700
        )

        # ------------------------------------------------ #
        # DATABASE CONNECTION
        # ------------------------------------------------ #

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        self.cursor = self.connection.cursor()

        # ------------------------------------------------ #
        # FETCH STUDENT DATA
        # ------------------------------------------------ #

        query = """
        SELECT
        roll_no,
        full_name,
        department,
        year,
        cgpa,
        attendance,
        email
        FROM students
        WHERE roll_no = %s
        """

        self.cursor.execute(
            query,
            (self.student_roll_no,)
        )

        student = self.cursor.fetchone()

        self.roll_no = student[0]
        self.full_name = student[1]
        self.department = student[2]
        self.year = student[3]
        self.cgpa = student[4]
        self.attendance = student[5]
        self.email = student[6]

        # ------------------------------------------------ #
        # PERFORMANCE STATUS
        # ------------------------------------------------ #

        if self.cgpa >= 9:

            self.performance = "Excellent Performance"

        elif self.cgpa >= 8:

            self.performance = "Very Good Performance"

        else:

            self.performance = "Needs Improvement"

        # ------------------------------------------------ #
        # BACKGROUND IMAGE
        # ------------------------------------------------ #

        self.bg_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path("assets/images/vireon_studentdash.png")
            ),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(
            self,
            image=self.bg_image,
            text=""
        )

        bg_label.place(x=0, y=0)

        # ------------------------------------------------ #
        # VISUAL THEME
        # ------------------------------------------------ #

        navy = "#1F3763"
        slate = "#51617D"
        muted = "#7A89A6"
        panel = "#F7FAFF"
        card = "#FFFFFF"
        soft_blue = "#E8F0FF"
        line = "#C9D6F2"
        accent = "#2F80ED"
        mid_blue = "#4F8DEB"
        deep_blue = "#2559B8"
        soft_button = "#6F86B8"

        # ------------------------------------------------ #
        # MAIN SURFACE
        # ------------------------------------------------ #

        shell = ctk.CTkFrame(
            self,
            width=1080,
            height=580,
            fg_color=panel,
            corner_radius=18,
            border_width=1,
            border_color="#D7E1F3"
        )

        shell.place(x=60, y=80)

        # ------------------------------------------------ #
        # HEADER
        # ------------------------------------------------ #

        header = ctk.CTkFrame(
            shell,
            width=1020,
            height=90,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        header.place(x=30, y=25)

        title = ctk.CTkLabel(
            header,
            text="Student Analytics",
            font=("Georgia", 32, "bold"),
            text_color=navy
        )

        title.place(x=28, y=16)

        subtitle = ctk.CTkLabel(
            header,
            text=f"{self.full_name}  |  {self.department} - Year {self.year}",
            font=("Segoe UI", 15),
            text_color=slate
        )

        subtitle.place(x=31, y=58)

        status_badge = ctk.CTkLabel(
            header,
            text=self.performance,
            width=230,
            height=36,
            fg_color=soft_blue,
            corner_radius=18,
            font=("Segoe UI", 14, "bold"),
            text_color=accent
        )

        status_badge.place(x=760, y=27)

        # ------------------------------------------------ #
        # QUICK STATS
        # ------------------------------------------------ #

        stat_data = [
            ("CGPA", f"{self.cgpa}", "out of 10", accent),
            ("Attendance", f"{self.attendance}%", "current record", mid_blue),
            ("Roll No", f"{self.roll_no}", "student id", deep_blue)
        ]

        for index, (label, value, caption, color) in enumerate(stat_data):

            stat_card = ctk.CTkFrame(
                shell,
                width=255,
                height=92,
                fg_color=card,
                corner_radius=12,
                border_width=1,
                border_color="#E1E8F6"
            )

            stat_card.place(x=30 + (index * 300), y=135)

            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Segoe UI", 13, "bold"),
                text_color=muted
            ).place(x=18, y=14)

            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Georgia", 28, "bold"),
                text_color=color
            ).place(x=18, y=36)

            ctk.CTkLabel(
                stat_card,
                text=caption,
                font=("Segoe UI", 12),
                text_color=muted
            ).place(x=145, y=51)

        # ------------------------------------------------ #
        # PROFILE CARD
        # ------------------------------------------------ #

        profile_card = ctk.CTkFrame(
            shell,
            width=330,
            height=275,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        profile_card.place(x=30, y=250)

        profile_title = ctk.CTkLabel(
            profile_card,
            text="Profile",
            font=("Georgia", 22, "bold"),
            text_color=navy
        )

        profile_title.place(x=22, y=18)

        details = [
            f"Roll Number : {self.roll_no}",
            f"Name : {self.full_name}",
            f"Department : {self.department}",
            f"Year : {self.year}",
            f"CGPA : {self.cgpa}",
            f"Attendance : {self.attendance}%",
            f"Email : {self.email}"
        ]

        for index, detail in enumerate(details):

            label_name, label_value = detail.split(" : ", 1)

            label = ctk.CTkLabel(
                profile_card,
                text=label_name.upper(),
                font=("Segoe UI", 11, "bold"),
                text_color=muted,
                anchor="w"
            )

            label.place(
                x=22,
                y=58 + index * 29
            )

            value = ctk.CTkLabel(
                profile_card,
                text=label_value,
                font=("Segoe UI", 14),
                text_color=navy,
                anchor="w"
            )

            value.place(
                x=138,
                y=55 + index * 29
            )

        # ------------------------------------------------ #
        # GRAPH CARD
        # ------------------------------------------------ #

        graph_card = ctk.CTkFrame(
            shell,
            width=420,
            height=275,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        graph_card.place(x=380, y=250)

        graph_title = ctk.CTkLabel(
            graph_card,
            text="Performance Analytics",
            font=("Georgia", 22, "bold"),
            text_color=navy
        )

        graph_title.place(x=22, y=18)

        graph_caption = ctk.CTkLabel(
            graph_card,
            text="Attendance and CGPA on a 100-point scale.",
            font=("Segoe UI", 12),
            text_color=muted
        )

        graph_caption.place(x=24, y=48)

        # ------------------------------------------------ #
        # GRAPH
        # ------------------------------------------------ #

        subjects = [
            "Attendance",
            "CGPA"
        ]

        values = [
            self.attendance,
            self.cgpa * 10
        ]

        self.fig = plt.Figure(
            figsize=(3.75, 1.9),
            dpi=100
        )

        ax = self.fig.add_subplot(111)

        ax.bar(
            subjects,
            values,
            color=[mid_blue, deep_blue],
            width=0.45,
            edgecolor="#FFFFFF",
            linewidth=1.5
        )

        ax.set_ylim(0, 100)
        ax.grid(
            axis="y",
            color="#DDE6F7",
            linewidth=0.8
        )

        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(line)
        ax.spines["bottom"].set_color(line)
        ax.tick_params(
            colors=slate,
            labelsize=9
        )

        self.fig.patch.set_facecolor(card)

        ax.set_facecolor(card)

        self.fig.tight_layout(
            pad=1.2
        )

        canvas = FigureCanvasTkAgg(
            self.fig,
            master=graph_card
        )

        canvas.draw()

        canvas.get_tk_widget().place(
            x=18,
            y=70
        )

        # ------------------------------------------------ #
        # PERFORMANCE LABEL
        # ------------------------------------------------ #

        performance_label = ctk.CTkLabel(
            graph_card,
            text=self.performance,
            font=("Segoe UI", 15, "bold"),
            text_color=accent,
            fg_color=soft_blue,
            corner_radius=16,
            width=240,
            height=34
        )

        performance_label.place(
            x=90,
            y=226
        )

        # ------------------------------------------------ #
        # DOWNLOAD BUTTON
        # ------------------------------------------------ #

        export_button = ctk.CTkButton(
            shell,
            text="Download Report",
            width=220,
            height=44,
            corner_radius=10,
            fg_color=accent,
            hover_color="#226BC7",
            font=("Segoe UI", 15, "bold"),
            command=self.export_report
        )

        export_button.place(
            x=590,
            y=530
        )

        # ---------- ANALYTICS FRAME ---------- #

        self.analytics_frame = ctk.CTkFrame(
            shell,
            width=220,
            height=275,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        self.analytics_frame.place(
            x=830,
            y=250
        )

        self.analytics_frame.pack_propagate(False)

        # ---------- TOP PERFORMERS ---------- #

        self.cursor.execute(
            """
            SELECT full_name, cgpa
            FROM students
            ORDER BY cgpa DESC
            LIMIT 3
            """
        )

        toppers = self.cursor.fetchall()

        self.topper_card = ctk.CTkFrame(
            self.analytics_frame,
            width=180,
            height=180,
            fg_color=soft_blue,
            corner_radius=12,
            border_width=1,
            border_color=line
        )

        self.topper_card.place(
            x=20,
            y=75
        )

        self.topper_card.pack_propagate(False)

        ctk.CTkLabel(
            self.analytics_frame,
            text="Top Performers",
            font=("Georgia", 20, "bold"),
            text_color=navy
        ).place(x=20, y=18)

        ctk.CTkLabel(
            self.analytics_frame,
            text="Highest CGPA across students",
            font=("Segoe UI", 12),
            text_color=muted
        ).place(x=20, y=45)

        for index, student in enumerate(toppers, start=1):

            row_y = 14 + ((index - 1) * 53)

            ctk.CTkLabel(
                self.topper_card,
                text=f"{index}. {student[0]}",
                font=("Segoe UI", 13, "bold"),
                text_color=navy,
                anchor="w",
                width=150
            ).place(x=14, y=row_y)

            ctk.CTkLabel(
                self.topper_card,
                text=f"CGPA {student[1]}",
                font=("Segoe UI", 13),
                text_color=slate,
                anchor="w",
                width=150
            ).place(x=28, y=row_y + 21)

        # ------------------------------------------------ #
        # LOGOUT BUTTON
        # ------------------------------------------------ #

        logout_button = ctk.CTkButton(
            shell,
            text="Logout",
            width=150,
            height=44,
            corner_radius=10,
            fg_color=soft_button,
            hover_color="#5F76A8",
            font=("Segoe UI", 15, "bold"),
            command=self.logout
        )

        logout_button.place(
            x=840,
            y=530
        )

    # ------------------------------------------------ #
    # EXPORT REPORT
    # ------------------------------------------------ #

    def export_report(self):

        try:

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"{self.full_name}_Report.pdf"
            )

            if not save_path:
                return

            # ------------------------------------------------ #
            # TEMP GRAPH FILE
            # ------------------------------------------------ #

            temp_graph = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            )

            graph_path = temp_graph.name

            temp_graph.close()

            # SAVE GRAPH TEMPORARILY

            self.fig.savefig(graph_path)

            # ------------------------------------------------ #
            # PDF
            # ------------------------------------------------ #

            doc = SimpleDocTemplate(save_path)

            styles = getSampleStyleSheet()

            elements = []

            # TITLE

            title = Paragraph(
                "VIREON Student Report",
                styles["Title"]
            )

            elements.append(title)

            elements.append(
                Spacer(1, 20)
            )

            # DETAILS

            details = f"""
            <b>Roll Number:</b> {self.roll_no}<br/>
            <b>Name:</b> {self.full_name}<br/>
            <b>Department:</b> {self.department}<br/>
            <b>Year:</b> {self.year}<br/>
            <b>CGPA:</b> {self.cgpa}<br/>
            <b>Attendance:</b> {self.attendance}%<br/>
            <b>Email:</b> {self.email}<br/>
            """

            paragraph = Paragraph(
                details,
                styles["BodyText"]
            )

            elements.append(paragraph)

            elements.append(
                Spacer(1, 25)
            )

            # GRAPH IMAGE

            graph = PDFImage(
                graph_path,
                width=400,
                height=250
            )

            elements.append(graph)

            elements.append(
                Spacer(1, 20)
            )

            # PERFORMANCE

            remarks = Paragraph(
                f"""
                <b>Performance Remark:</b>
                {self.performance}
                """,
                styles["BodyText"]
            )

            elements.append(remarks)

            # BUILD PDF

            doc.build(elements)

            # DELETE TEMP FILE

            os.remove(graph_path)

            messagebox.showinfo(
                "Success",
                "Report downloaded successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )

    # ------------------------------------------------ #
    # LOGOUT
    # ------------------------------------------------ #

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


# ------------------------------------------------ #
# RUN APP
# ------------------------------------------------ #

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")

    app.title("Vireon Student Dashboard")

    app.resizable(False, False)

    dashboard = StudentDashboard(
        app,
        25
    )

    dashboard.pack(
        fill="both",
        expand=True
    )

    app.mainloop()
