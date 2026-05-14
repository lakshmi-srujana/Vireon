import customtkinter as ctk
import mysql.connector

from PIL import Image
import csv

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
            light_image=Image.open(
                "assets/images/vireon_common.png"
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
        # TITLE
        # ------------------------------------------------ #

        title = ctk.CTkLabel(
            self,
            text="Faculty Dashboard",
            font=("Georgia", 34, "bold"),
            text_color="#5B6FB8",
            fg_color="#EEF3FF",
            corner_radius=10,
            width=450,
            height=60
        )

        title.place(x=375, y=25)

        # ------------------------------------------------ #
        # PROFILE CARD
        # ------------------------------------------------ #

        profile_card = ctk.CTkFrame(
            self,
            width=280,
            height=430,
            fg_color="#EEF3FF",
            corner_radius=25,
            border_width=3,
            border_color="#B8C4E8"
        )

        profile_card.place(x=80, y=170)

        profile_title = ctk.CTkLabel(
            profile_card,
            text="Faculty Profile",
            font=("Georgia", 20, "bold"),
            text_color="#5B6FB8"
        )

        profile_title.pack(pady=(20, 20))

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

        for detail in details:

            label = ctk.CTkLabel(
                profile_card,
                text=detail,
                font=("Georgia", 15),
                text_color="#394B8A",
                anchor="w"
            )

            label.pack(
                pady=8,
                padx=20,
                anchor="w"
            )

        # ------------------------------------------------ #
        # GRAPH CARD
        # ------------------------------------------------ #

        graph_card = ctk.CTkFrame(
            self,
            width=490,
            height=430,
            fg_color="#EEF3FF",
            corner_radius=25,
            border_width=3,
            border_color="#B8C4E8"
        )

        graph_card.place(x=400, y=120)

        graph_title = ctk.CTkLabel(
            graph_card,
            text="Department Analytics",
            font=("Georgia", 26, "bold"),
            text_color="#5B6FB8"
        )

        graph_title.pack(pady=(20, 10))

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
            figsize=(3, 2.4),
            dpi=100
        )

        ax = self.fig.add_subplot(111)

        ax.bar(
            labels,
            values
        )

        ax.set_title(
            f"{self.department} Analytics"
        )

        self.fig.patch.set_facecolor("#DCE6FF")

        ax.set_facecolor("#EEF3FF")

        canvas = FigureCanvasTkAgg(
            self.fig,
            master=graph_card
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            pady=5
        )

        performance_label = ctk.CTkLabel(
            graph_card,
            text=self.performance,
            font=("Georgia",14, "bold"),
            text_color="#5B6FB8"
        )

        performance_label.pack(
            pady=(5, 10)
        )

        # ------------------------------------------------ #
        # TOPPER CARD
        # ------------------------------------------------ #

        topper_frame = ctk.CTkFrame(
            self,
            width=240,
            height=230,
            fg_color="#EEF3FF",
            corner_radius=20,
            border_width=2,
            border_color="#B8C4E8"
        )

        topper_frame.place(x=850, y=120)

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

        topper_text = (
            f"Top {self.department} Students\n\n"
        )

        for student in toppers:

            topper_text += (
                f"{student[0]}\nCGPA : {student[1]}\n\n"
            )

        topper_label = ctk.CTkLabel(
            topper_frame,
            text=topper_text,
            justify="left",
            font=("Georgia", 15),
            text_color="#394B8A"
        )

        topper_label.place(
            x=20,
            y=20
        )

        # ------------------------------------------------ #
        # BONUS FRAME
        # ------------------------------------------------ #

        bonus_frame = ctk.CTkFrame(
            self,
            width=240,
            height=170,
            fg_color="#EEF3FF",
            corner_radius=20,
            border_width=2,
            border_color="#B8C4E8"
        )

        bonus_frame.place(x=850, y=370)

        self.roll_entry = ctk.CTkEntry(
            bonus_frame,
            width=180,
            placeholder_text="Roll No",
            font=("Georgia", 12),
        )

        self.roll_entry.place(
            x=30,
            y=20
        )

        self.bonus_entry = ctk.CTkEntry(
            bonus_frame,
            width=180,
            placeholder_text="Bonus CGPA",
            font=("Georgia", 12),
        )

        self.bonus_entry.place(
            x=30,
            y=60
        )

        bonus_button = ctk.CTkButton(
            bonus_frame,
            text="Add Bonus",
            width=180,
            font=("Georgia", 12),
            fg_color="#8792AE",
            command=self.add_bonus_marks
        )

        bonus_button.place(
            x=30,
            y=100
        )

        csv_button = ctk.CTkButton(
            bonus_frame,
            text="Export CSV",
            width=180,
            font=("Georgia", 12),
            fg_color="#5B6FB8",
            command=self.export_toppers_csv
        )

        csv_button.place(
            x=30,
            y=135
        )

        # ------------------------------------------------ #
        # STUDENT TABLE
        # ------------------------------------------------ #

        student_frame = ctk.CTkFrame(
            self,
            width=400,
            height=120,
            fg_color="#EEF3FF",
            corner_radius=20,
            border_width=2,
            border_color="#B8C4E8"
        )

        student_frame.place(
            x=365,
            y=460
        )

        student_title = ctk.CTkLabel(
            student_frame,
            text=f"{self.department} Students",
            font=("Georgia", 18, "bold"),
            text_color="#5B6FB8"
        )

        student_title.place(
            x=20,
            y=5
        )

        self.student_box = ctk.CTkTextbox(
            student_frame,
            width=350,
            height=70,
            font=("Consolas", 11),
            text_color="#394B8A",
            fg_color="#DCE6FF"
        )

        self.student_box.place(
            x=20,
            y=40
        )

        self.refresh_students()

        # ------------------------------------------------ #
        # BOTTOM BUTTONS
        # ------------------------------------------------ #

        export_button = ctk.CTkButton(
            self,
            text="Download Report",
            width=220,
            height=40,
            corner_radius=18,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 16),
            command=self.export_report
        )

        export_button.place(
            x=670,
            y=600
        )

        logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=150,
            height=40,
            corner_radius=18,
            fg_color="#C27A86",
            hover_color="#AA6570",
            font=("Georgia", 16),
            command=self.logout
        )

        logout_button.place(
            x=900,
            y=600
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

        self.master.destroy()


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