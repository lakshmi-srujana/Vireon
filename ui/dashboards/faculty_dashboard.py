import customtkinter as ctk
import mysql.connector

from PIL import Image
import csv
from ui.dashboards.student_pagefaculty import StudentsPage

from tkinter import filedialog
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils.resource_path import resource_path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage
)

from reportlab.lib.styles import getSampleStyleSheet

import tempfile
import os


class FacultyDashboard(ctk.CTkFrame):

    def __init__(self, parent, faculty_id):

        super().__init__(parent)

        self.faculty_id = faculty_id

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
        # FETCH FACULTY DATA
        # ------------------------------------------------ #

        query = """
        SELECT
        faculty_id,
        full_name,
        department,
        designation,
        email,
        phone
        FROM faculty
        WHERE faculty_id = %s
        """

        self.cursor.execute(
            query,
            (self.faculty_id,)
        )

        faculty = self.cursor.fetchone()

        self.faculty_id_value = faculty[0]
        self.full_name = faculty[1]
        self.department = faculty[2]
        self.designation = faculty[3]
        self.email = faculty[4]
        self.phone = faculty[5]

        # ------------------------------------------------ #
        # ANALYTICS
        # ------------------------------------------------ #

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE department = %s
            """,
            (self.department,)
        )

        self.total_students = self.cursor.fetchone()[0]

        self.cursor.execute(
            """
            SELECT AVG(cgpa)
            FROM students
            WHERE department = %s
            """,
            (self.department,)
        )

        avg = self.cursor.fetchone()[0]

        self.avg_cgpa = round(avg, 2)

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM students
            WHERE department = %s
            AND attendance < 75
            """,
            (self.department,)
        )

        self.low_attendance = self.cursor.fetchone()[0]


        # ------------------------------------------------ #
        # PERFORMANCE STATUS
        # ------------------------------------------------ #

        if self.avg_cgpa >= 9:

            self.performance = "Outstanding Department Performance"

        elif self.avg_cgpa >= 8:

            self.performance = "Very Good Department Performance"

        else:

            self.performance = "Department Needs Improvement"

        # ------------------------------------------------ #
        # BACKGROUND IMAGE
        # ------------------------------------------------ #

        self.bg_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/images/vireon_studentdash.png")),
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
        warning = "#D65F6B"
        soft_warning = "#FFF0F2"
        soft_button = "#6F86B8"

        # ------------------------------------------------ #
        # MAIN SURFACE
        # ------------------------------------------------ #

        shell = ctk.CTkFrame(
            self,
            width=1080,
            height=600,
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
            height=82,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        header.place(x=30, y=22)

        title = ctk.CTkLabel(
            header,
            text="Faculty Dashboard",
            font=("Georgia", 31, "bold"),
            text_color=navy
        )

        title.place(x=28, y=13)

        subtitle = ctk.CTkLabel(
            header,
            text=f"{self.full_name}  |  {self.department}  |  {self.designation}",
            font=("Segoe UI", 14),
            text_color=slate
        )

        subtitle.place(x=31, y=54)

        status_badge = ctk.CTkLabel(
            header,
            text=self.performance,
            width=310,
            height=34,
            fg_color=soft_blue,
            corner_radius=17,
            font=("Segoe UI", 13, "bold"),
            text_color=accent
        )

        status_badge.place(x=680, y=24)

        # ------------------------------------------------ #
        # QUICK STATS
        # ------------------------------------------------ #

        stat_data = [
            ("Students", self.total_students, "in department", accent),
            ("Average CGPA", self.avg_cgpa, "department score", mid_blue),
            ("Low Attendance", self.low_attendance, "need review", warning),
            ("Department", self.department, "assigned group", deep_blue)
        ]

        for index, (label, value, caption, color) in enumerate(stat_data):

            stat_card = ctk.CTkFrame(
                shell,
                width=235,
                height=82,
                fg_color=card,
                corner_radius=12,
                border_width=1,
                border_color="#E1E8F6"
            )

            stat_card.place(x=30 + (index * 260), y=120)

            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color=muted
            ).place(x=18, y=12)

            ctk.CTkLabel(
                stat_card,
                text=str(value),
                font=("Georgia", 24, "bold"),
                text_color=color
            ).place(x=18, y=34)

            ctk.CTkLabel(
                stat_card,
                text=caption,
                font=("Segoe UI", 11),
                text_color=muted
            ).place(x=122, y=46)

        # ------------------------------------------------ #
        # PROFILE CARD
        # ------------------------------------------------ #

        profile_card = ctk.CTkFrame(
            shell,
            width=320,
            height=250,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        profile_card.place(x=30, y=222)

        profile_title = ctk.CTkLabel(
            profile_card,
            text="Profile",
            font=("Georgia", 22, "bold"),
            text_color=navy
        )

        profile_title.place(x=22, y=16)

        details = [

            f"Faculty ID : {self.faculty_id_value}",
            f"Name : {self.full_name}",
            f"Department : {self.department}",
            f"Designation : {self.designation}",
            f"Students : {self.total_students}",
            f"Average CGPA : {self.avg_cgpa}",
            f"Email : {self.email}",
            f"Phone : {self.phone}"

        ]

        for index, detail in enumerate(details):

            label_name, label_value = detail.split(" : ", 1)

            label = ctk.CTkLabel(
                profile_card,
                text=label_name.upper(),
                font=("Segoe UI", 10, "bold"),
                text_color=muted,
                anchor="w"
            )

            label.place(
                x=22,
                y=54 + index * 24
            )

            value = ctk.CTkLabel(
                profile_card,
                text=label_value,
                font=("Segoe UI", 13),
                text_color=navy,
                anchor="w"
            )

            value.place(
                x=128,
                y=51 + index * 24
            )

        # ------------------------------------------------ #
        # GRAPH CARD
        # ------------------------------------------------ #

        graph_card = ctk.CTkFrame(
            shell,
            width=405,
            height=250,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        graph_card.place(x=370, y=222)

        graph_title = ctk.CTkLabel(
            graph_card,
            text="Department Analytics",
            font=("Georgia", 22, "bold"),
            text_color=navy
        )

        graph_title.place(x=22, y=16)

        graph_caption = ctk.CTkLabel(
            graph_card,
            text="CGPA and low-attendance counts are normalized for comparison.",
            font=("Segoe UI", 11),
            text_color=muted
        )

        graph_caption.place(x=24, y=47)

        # ------------------------------------------------ #
        # GRAPH
        # ------------------------------------------------ #

        labels = [
            "Students",
            "Avg CGPA",
            "Low Attendance"
        ]

        values = [
            self.total_students,
            self.avg_cgpa * 10,
            self.low_attendance * 10
        ]

        self.fig = plt.Figure(
            figsize=(3.6, 1.75),
            dpi=100
        )

        ax = self.fig.add_subplot(111)

        ax.bar(
            labels,
            values,
            color=[accent, mid_blue, warning],
            width=0.48,
            edgecolor="#FFFFFF",
            linewidth=1.4
        )

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
            labelsize=8
        )

        self.fig.patch.set_facecolor(card)

        ax.set_facecolor(card)

        self.fig.tight_layout(
            pad=1.1
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

        performance_label = ctk.CTkLabel(
            graph_card,
            text=self.performance,
            font=("Segoe UI", 13, "bold"),
            text_color=accent,
            fg_color=soft_blue,
            corner_radius=15,
            width=275,
            height=30
        )

        performance_label.place(
            x=65,
            y=210
        )

        # ------------------------------------------------ #
        # ALERTS CARD
        # ------------------------------------------------ #
        self.cursor.execute(
            """
            SELECT
            roll_no,
            full_name,
            attendance

            FROM attendance_alerts

            ORDER BY created_at DESC

            LIMIT 5
            """
        )

        alerts = self.cursor.fetchall()
        alert_text = ""

        for alert in alerts:

            alert_text += (
                f"{alert[1]} "
                f"(Roll: {alert[0]})\n"
                f"- Attendance: {alert[2]}%\n\n"
            )

        alert_frame = ctk.CTkFrame(
            shell,
            width=320,
            height=88,
            fg_color=soft_warning,
            corner_radius=12,
            border_width=1,
            border_color="#F2BDC5"
        )

        alert_frame.place(
            x=30,
            y=488
        )

        alert_title = ctk.CTkLabel(
            alert_frame,
            text="Attendance Alerts",
            font=("Georgia", 17, "bold"),
            text_color=warning
        )

        alert_title.place(
            x=18,
            y=8
        )

        alert_box = ctk.CTkTextbox(
            alert_frame,
            width=280,
            height=42,
            fg_color="#FFE3E7",
            text_color="#9F3441",
            font=("Segoe UI", 11),
            corner_radius=8
        )

        alert_box.place(
            x=18,
            y=38
        )

        alert_box.insert(
            "0.0",
            alert_text
        )
        # ------------------------------------------------ #
        # TOPPER CARD
        # ------------------------------------------------ #

        topper_frame = ctk.CTkFrame(
            shell,
            width=245,
            height=170,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        topper_frame.place(x=805, y=222)

        self.cursor.execute(
            """
            SELECT full_name, cgpa
            FROM students
            WHERE department = %s
            ORDER BY cgpa DESC
            LIMIT 3
            """,
            (self.department,)
        )

        toppers = self.cursor.fetchall()

        ctk.CTkLabel(
            topper_frame,
            text=f"Top {self.department} Students",
            font=("Georgia", 18, "bold"),
            text_color=navy
        ).place(
            x=18,
            y=15
        )

        for index, student in enumerate(toppers, start=1):

            row_y = 48 + ((index - 1) * 36)

            ctk.CTkLabel(
                topper_frame,
                text=f"{index}. {student[0]}",
                font=("Segoe UI", 13, "bold"),
                text_color=navy,
                anchor="w",
                width=190
            ).place(x=20, y=row_y)

            ctk.CTkLabel(
                topper_frame,
                text=f"CGPA {student[1]}",
                font=("Segoe UI", 12),
                text_color=slate,
                anchor="w",
                width=190
            ).place(x=35, y=row_y + 18)

        # ------------------------------------------------ #
        # BONUS FRAME
        # ------------------------------------------------ #

        bonus_frame = ctk.CTkFrame(
            shell,
            width=245,
            height=140,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        bonus_frame.place(x=805, y=408)

        self.roll_entry = ctk.CTkEntry(
            bonus_frame,
            width=205,
            placeholder_text="Roll No",
            font=("Segoe UI", 12),
            border_color=line,
        )

        self.roll_entry.place(
            x=20,
            y=14
        )

        self.bonus_entry = ctk.CTkEntry(
            bonus_frame,
            width=205,
            placeholder_text="Bonus CGPA",
            font=("Segoe UI", 12),
            border_color=line,
        )

        self.bonus_entry.place(
            x=20,
            y=46
        )

        bonus_button = ctk.CTkButton(
            bonus_frame,
            text="Add Bonus",
            width=205,
            height=26,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color=soft_button,
            hover_color="#5F76A8",
            command=self.add_bonus_marks
        )

        bonus_button.place(
            x=20,
            y=78
        )

        csv_button = ctk.CTkButton(
            bonus_frame,
            text="Export CSV",
            width=205,
            height=26,
            corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color=accent,
            hover_color="#226BC7",
            command=self.export_toppers_csv
        )

        csv_button.place(
            x=20,
            y=108
        )
        # ------------------------------------------------ #   
        # ADD/EDIT STUDENTS BUTTON     
        # ------------------------------------------------ #        

        addstudent_button = ctk.CTkButton(
            shell,
            text="Add/Edit Students",
            width=220,
            height=38,
            corner_radius=10,
            fg_color=soft_button,
            hover_color="#5F76A8",
            font=("Segoe UI", 14, "bold"),
            command=self.open_students
        )

        addstudent_button.place(
            x=370,
            y=550
        )

        # ------------------------------------------------ #
        # STUDENT TABLE
        # ------------------------------------------------ #

        student_frame = ctk.CTkFrame(
            shell,
            width=405,
            height=66,
            fg_color=card,
            corner_radius=12,
            border_width=1,
            border_color="#E1E8F6"
        )

        student_frame.place(
            x=370,
            y=476
        )

        student_title = ctk.CTkLabel(
            student_frame,
            text=f"{self.department} Students",
            font=("Georgia", 17, "bold"),
            text_color=navy
        )

        student_title.place(
            x=20,
            y=5
        )

        self.student_box = ctk.CTkTextbox(
            student_frame,
            width=365,
            height=30,
            font=("Consolas", 11),
            text_color=navy,
            fg_color=soft_blue,
            corner_radius=8
        )

        self.student_box.place(
            x=20,
            y=31
        )

        self.refresh_students()

        # ------------------------------------------------ #
        # BOTTOM BUTTONS
        # ------------------------------------------------ #

        export_button = ctk.CTkButton(
            shell,
            text="Download Report",
            width=220,
            height=38,
            corner_radius=10,
            fg_color=accent,
            hover_color="#226BC7",
            font=("Segoe UI", 14, "bold"),
            command=self.export_report
        )

        export_button.place(
            x=605,
            y=550
        )

        logout_button = ctk.CTkButton(
            shell,
            text="Logout",
            width=150,
            height=38,
            corner_radius=10,
            fg_color="#748ABE",
            hover_color="#6178AC",
            font=("Segoe UI", 14, "bold"),
            command=self.logout
        )

        logout_button.place(
            x=840,
            y=550
        )

    # ------------------------------------------------ #
    # REFRESH STUDENTS
    # ------------------------------------------------ #

    def refresh_students(self):

        self.student_box.delete(
            "0.0",
            "end"
        )

        self.cursor.execute(
            """
            SELECT
            roll_no,
            full_name,
            cgpa,
            attendance

            FROM students

            WHERE department = %s

            ORDER BY cgpa DESC
            """,
            (self.department,)
        )

        students = self.cursor.fetchall()

        student_text = ""

        for student in students:

            student_text += (
                f"{student[0]}   "
                f"{student[1]}   "
                f"CGPA:{student[2]}   "
                f"ATT:{student[3]}%\n"
            )

        self.student_box.insert(
            "0.0",
            student_text
        )

    # ------------------------------------------------ #
    # BONUS MARKS
    # ------------------------------------------------ #

    def add_bonus_marks(self):

        try:

            roll_no = self.roll_entry.get()

            bonus = float(
                self.bonus_entry.get()
            )

            self.cursor.execute(
                """
                SELECT cgpa
                FROM students
                WHERE roll_no = %s
                AND department = %s
                """,
                (
                    roll_no,
                    self.department
                )
            )

            result = self.cursor.fetchone()

            if not result:

                messagebox.showerror(
                    "Error",
                    "Student not found!"
                )

                return

            current_cgpa = float(result[0])

            updated_cgpa = current_cgpa + bonus

            if updated_cgpa > 10:
                updated_cgpa = 10

            self.cursor.execute(
                """
                UPDATE students
                SET cgpa = %s
                WHERE roll_no = %s
                AND department = %s
                """,
                (
                    updated_cgpa,
                    roll_no,
                    self.department
                )
            )

            self.connection.commit()

            self.refresh_students()

            messagebox.showinfo(
                "Success",
                f"Updated CGPA to {updated_cgpa}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ------------------------------------------------ #
    # EXPORT CSV
    # ------------------------------------------------ #

    def export_toppers_csv(self):

        try:

            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                initialfile=f"{self.department}_Toppers.csv"
            )

            if not save_path:
                return

            self.cursor.execute(
                """
                SELECT
                roll_no,
                full_name,
                cgpa,
                attendance

                FROM students

                WHERE department = %s

                ORDER BY cgpa DESC

                LIMIT 10
                """,
                (self.department,)
            )

            students = self.cursor.fetchall()

            with open(
                save_path,
                mode="w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Roll No",
                        "Name",
                        "CGPA",
                        "Attendance"
                    ]
                )

                writer.writerows(students)

            messagebox.showinfo(
                "Success",
                "CSV exported successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ------------------------------------------------ #
    # EXPORT REPORT
    # ------------------------------------------------ #

    def export_report(self):

        try:

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"{self.full_name}_Faculty_Report.pdf"
            )

            if not save_path:
                return

            temp_graph = tempfile.NamedTemporaryFile(
                suffix=".png",
                delete=False
            )

            graph_path = temp_graph.name

            temp_graph.close()

            self.fig.savefig(graph_path)

            doc = SimpleDocTemplate(save_path)

            styles = getSampleStyleSheet()

            elements = []

            title = Paragraph(
                "VIREON Faculty Report",
                styles["Title"]
            )

            elements.append(title)

            elements.append(
                Spacer(1, 20)
            )

            details = f"""
            <b>Faculty ID:</b> {self.faculty_id_value}<br/>
            <b>Name:</b> {self.full_name}<br/>
            <b>Department:</b> {self.department}<br/>
            <b>Designation:</b> {self.designation}<br/>
            <b>Total Students:</b> {self.total_students}<br/>
            <b>Average CGPA:</b> {self.avg_cgpa}<br/>
            """

            paragraph = Paragraph(
                details,
                styles["BodyText"]
            )

            elements.append(paragraph)

            elements.append(
                Spacer(1, 25)
            )

            graph = PDFImage(
                graph_path,
                width=350,
                height=220
            )

            elements.append(graph)

            doc.build(elements)

            os.remove(graph_path)

            messagebox.showinfo(
                "Success",
                "Faculty report downloaded successfully!"
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

    # ----------------------------------------------- #
    # ADD/EDIT STUDENTS
    # ----------------------------------------------- #

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


# ------------------------------------------------ #
# RUN APP
# ------------------------------------------------ #

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")

    app.title("Vireon Faculty Dashboard")

    app.resizable(False, False)

    dashboard = FacultyDashboard(
        app,
        "1001"
    )

    dashboard.pack(
        fill="both",
        expand=True
    )

    app.mainloop()
