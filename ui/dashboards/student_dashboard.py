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
            text="Analytics Dashboard",
            font=("Georgia", 34, "bold"),
            text_color="#5B6FB8",
            fg_color="#EEF3FF",
            corner_radius=10,
            width=450,
            height=60
        )

        title.place(x=375, y=35)

        # ------------------------------------------------ #
        # PROFILE CARD
        # ------------------------------------------------ #

        profile_card = ctk.CTkFrame(
            self,
            width=300,
            height=400,
            fg_color="#EEF3FF",
            corner_radius=25,
            border_width=3,
            border_color="#B8C4E8"
        )

        profile_card.place(x=70, y=170)

        profile_title = ctk.CTkLabel(
            profile_card,
            text="Student Profile",
            font=("Georgia", 24, "bold"),
            text_color="#5B6FB8"
        )

        profile_title.pack(pady=(20, 20))

        details = [
            f"Roll Number : {self.roll_no}",
            f"Name : {self.full_name}",
            f"Department : {self.department}",
            f"Year : {self.year}",
            f"CGPA : {self.cgpa}",
            f"Attendance : {self.attendance}%",
            f"Email : {self.email}"
        ]

        for detail in details:

            label = ctk.CTkLabel(
                profile_card,
                text=detail,
                font=("Georgia", 16),
                text_color="#394B8A",
                anchor="w"
            )

            label.pack(
                pady=10,
                padx=25,
                anchor="w"
            )

        # ------------------------------------------------ #
        # GRAPH CARD
        # ------------------------------------------------ #

        graph_card = ctk.CTkFrame(
            self,
            width=750,
            height=400,
            fg_color="#EEF3FF",
            corner_radius=25,
            border_width=3,
            border_color="#B8C4E8"
        )

        graph_card.place(x=420, y=170)

        graph_title = ctk.CTkLabel(
            graph_card,
            text="Performance Analytics",
            font=("Georgia", 26, "bold"),
            text_color="#5B6FB8"
        )

        graph_title.pack(pady=(20, 10))

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
            figsize=(4.8, 2.8),
            dpi=100
        )

        ax = self.fig.add_subplot(111)

        ax.bar(
            subjects,
            values
        )

        ax.set_title(
            "Student Performance"
        )

        ax.set_ylim(0, 100)

        self.fig.patch.set_facecolor("#DCE6FF")

        ax.set_facecolor("#EEF3FF")

        canvas = FigureCanvasTkAgg(
            self.fig,
            master=graph_card
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            pady=10
        )

        # ------------------------------------------------ #
        # PERFORMANCE LABEL
        # ------------------------------------------------ #

        performance_label = ctk.CTkLabel(
            graph_card,
            text=self.performance,
            font=("Georgia", 20, "bold"),
            text_color="#5B6FB8"
        )

        performance_label.pack(
            pady=(5, 10)
        )

        # ------------------------------------------------ #
        # DOWNLOAD BUTTON
        # ------------------------------------------------ #

        export_button = ctk.CTkButton(
            self,
            text="Download Report",
            width=220,
            height=50,
            corner_radius=18,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 18),
            command=self.export_report
        )

        export_button.place(
            x=630,
            y=600
        )

        # ---------- ANALYTICS FRAME ---------- #

        self.analytics_frame = ctk.CTkFrame(
            self,
            width=310,
            height=200,
            fg_color="#E8EEFF",
            corner_radius=10,
            border_width=2,
            border_color="#B8C4E8"
        )

        self.analytics_frame.place(
            x=980,
            y=310,
            anchor="n"
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

        topper_text = "Top Performers\n\n"

        for student in toppers:

            topper_text += (
                f"{student[0]}  -  CGPA {student[1]}\n"
            )

        self.topper_card = ctk.CTkFrame(
            self.analytics_frame,
            width=240,
            height=150,
            fg_color="#DCE6FF",
            corner_radius=20,
            border_width=2,
            border_color="#A8B8E8"
        )

        self.topper_card.place(
            x=40,
            y=30
        )

        self.topper_card.pack_propagate(False)

        topper_label = ctk.CTkLabel(
            self.topper_card,
            text=topper_text,
            font=("Georgia", 16),
            text_color="#394B8A",
            justify="left"
        )

        topper_label.pack(
            pady=15,
            padx=10
        )

        # ------------------------------------------------ #
        # LOGOUT BUTTON
        # ------------------------------------------------ #

        logout_button = ctk.CTkButton(
            self,
            text="Logout",
            width=150,
            height=50,
            corner_radius=18,
            fg_color="#C27A86",
            hover_color="#AA6570",
            font=("Georgia", 18),
            command=self.logout
        )

        logout_button.place(
            x=900,
            y=600
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

        self.master.destroy()


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