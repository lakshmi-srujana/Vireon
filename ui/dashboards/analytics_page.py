import customtkinter as ctk
import mysql.connector
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from utils.resource_path import resource_path

ctk.set_appearance_mode("light")


class AnalyticsPage(ctk.CTkFrame):

    # ---------- KPI CARD ---------- #

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=220,
            height=120,
            fg_color="#DCE6FF",
            corner_radius=20,
            border_width=2,
            border_color="#A8B8E8"
        )

        card.pack(side="left", padx=18)

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Georgia", 18),
            text_color="#5B6FB8"
        )

        title_label.pack(pady=(22, 8))

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Georgia", 34, "bold"),
            text_color="#394B8A"
        )

        value_label.pack()

    # ---------- CLOSE WINDOW ---------- #

    def close_window(self):

        plt.close('all')

        self.master.destroy()

    # ---------- CLEAR GRAPH ---------- #

    def clear_graph(self):

        for widget in self.analytics_frame.winfo_children():

            if widget not in [
                self.topper_card,
                self.export_button
            ]:
                widget.destroy()

    # ---------- GRAPH STYLE ---------- #

    def style_graph(self, fig, ax):

        fig.patch.set_facecolor("#DCE6FF")

        ax.set_facecolor("#DCE6FF")

        ax.tick_params(colors="#394B8A")

        for spine in ax.spines.values():
            spine.set_color("#A8B8E8")

    # ---------- DISPLAY GRAPH ---------- #

    def display_graph(self, fig):

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.analytics_frame
        )

        canvas.draw()

        canvas.get_tk_widget().place(
            relx=0.60,
            rely=0.55,
            anchor="center"
        )

    # ---------- EXPORT ANALYTICS ---------- #

    def export_analytics(self):

        self.cursor.execute(
            f"""
            SELECT {', '.join(self.export_columns)}
            FROM students
            """
        )

        data = self.cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=self.export_headers
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Analytics Report"
        )

        if file_path:

            df.to_csv(
                file_path,
                index=False
            )

            messagebox.showinfo(
                "Export Successful",
                "Analytics exported successfully!"
            )

    # ---------- STUDENT TABLE COLUMNS ---------- #

    def configure_student_columns(self):

        self.cursor.execute(
            "SHOW COLUMNS FROM students"
        )

        columns = {
            column[0]
            for column in self.cursor.fetchall()
        }

        self.name_column = "full_name" if "full_name" in columns else "name"
        self.score_expression = "marks" if "marks" in columns else "(cgpa * 10)"

        if "roll_no" in columns:

            self.export_columns = [
                "roll_no",
                self.name_column,
                "department",
                f"{self.score_expression} AS marks"
            ]

            self.export_headers = [
                "Roll Number",
                "Full Name",
                "Department",
                "Marks"
            ]

        else:

            self.export_columns = [
                self.name_column,
                "department",
                f"{self.score_expression} AS marks"
            ]

            self.export_headers = [
                "Full Name",
                "Department",
                "Marks"
            ]

    # ---------- MARKS GRAPH ---------- #

    def show_marks_graph(self):

        self.clear_graph()

        self.cursor.execute(
            f"""
            SELECT {self.name_column}, {self.score_expression} AS marks
            FROM students
            """
        )

        data = self.cursor.fetchall()

        names = []
        values = []

        for row in data:

            names.append(row[0])

            values.append(float(row[1]))

        fig, ax = plt.subplots(
            figsize=(10, 3.5),
            dpi=100
        )

        self.style_graph(fig, ax)

        ax.bar(names, values)

        ax.set_title(
            "Marks Distribution",
            fontsize=16,
            color="#394B8A"
        )

        ax.set_xlabel(
            "Students",
            fontsize=10,
            color="#394B8A"
        )

        ax.set_ylabel(
            "Marks",
            fontsize=10,
            color="#394B8A"
        )

        ax.set_ylim(0, 100)

        plt.tight_layout()

        self.display_graph(fig)

    # ---------- GRADE DISTRIBUTION ---------- #

    def show_grade_distribution(self):

        self.clear_graph()

        self.cursor.execute(
            f"""
            SELECT
            SUM(CASE WHEN {self.score_expression} >= 90 THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN {self.score_expression} BETWEEN 75 AND 89 THEN 1 ELSE 0 END) AS B,
            SUM(CASE WHEN {self.score_expression} BETWEEN 60 AND 74 THEN 1 ELSE 0 END) AS C,
            SUM(CASE WHEN {self.score_expression} BETWEEN 40 AND 59 THEN 1 ELSE 0 END) AS D,
            SUM(CASE WHEN {self.score_expression} < 40 THEN 1 ELSE 0 END) AS F
            FROM students
            """
        )

        values = self.cursor.fetchone()
        grades = ["A", "B", "C", "D", "F"]
        counts = [
            value or 0
            for value in values
        ]

        fig, ax = plt.subplots(
            figsize=(10, 3.5),
            dpi=100
        )

        self.style_graph(fig, ax)

        ax.barh(
            grades,
            counts,
            color="#3B73D9"
        )

        ax.set_title(
            "Grade Distribution",
            fontsize=16,
            color="#394B8A"
        )

        ax.set_xlabel(
            "Students",
            fontsize=10,
            color="#394B8A"
        )

        ax.set_ylabel(
            "Grade Bands",
            fontsize=10,
            color="#394B8A"
        )

        plt.tight_layout()

        self.display_graph(fig)

    # ---------- DEPARTMENT SUMMARY ---------- #

    def show_department_summary(self):

        self.clear_graph()

        self.cursor.execute(
            f"""
            SELECT
            department,
            ROUND(AVG({self.score_expression}), 2) AS average_marks,
            MAX({self.score_expression}) AS highest_marks,
            MIN({self.score_expression}) AS lowest_marks
            FROM students
            GROUP BY department
            ORDER BY department
            """
        )

        department_data = self.cursor.fetchall()

        self.cursor.execute(
            """
            SELECT department, COUNT(*)
            FROM students
            GROUP BY department
            ORDER BY department
            """
        )

        pie_data = self.cursor.fetchall()

        departments = []
        counts = []

        for row in pie_data:

            departments.append(row[0])

            counts.append(row[1])

        fig, ax = plt.subplots(
            figsize=(5.2, 3.2),
            dpi=100
        )

        fig.patch.set_facecolor("#E8EEFF")

        ax.pie(
            counts,
            labels=departments,
            autopct="%1.1f%%",
            startangle=90,
            colors=[
                "#2559B8",
                "#3B73D9",
                "#5B8FE8",
                "#86ABF0",
                "#B4C8F6"
            ],
            textprops={
                "color": "#394B8A",
                "fontsize": 9
            }
        )

        ax.set_title(
            "Department Distribution",
            fontsize=14,
            color="#394B8A"
        )

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.analytics_frame
        )

        canvas.draw()

        canvas.get_tk_widget().place(
            x=295,
            y=28
        )

        summary = ctk.CTkTextbox(
            self.analytics_frame,
            width=310,
            height=240,
            fg_color="#DCE6FF",
            text_color="#394B8A",
            font=("Consolas", 12),
            corner_radius=12,
            border_width=2,
            border_color="#A8B8E8"
        )

        summary.place(
            x=765,
            y=40
        )

        header = (
            f"{'Dept':<10}"
            f"{'Avg':>8}"
            f"{'High':>8}"
            f"{'Low':>8}\n"
        )

        summary.insert("end", header)
        summary.insert("end", "-" * 34 + "\n")

        for row in department_data:

            summary.insert(
                "end",
                f"{row[0]:<10}"
                f"{float(row[1]):>8.2f}"
                f"{float(row[2]):>8.2f}"
                f"{float(row[3]):>8.2f}\n"
            )

        summary.configure(state="disabled")

    # ---------- MAIN ---------- #

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            width=1200,
            height=700
        )

        # ---------- DATABASE ---------- #

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        self.cursor = self.connection.cursor()

        self.configure_student_columns()

        # ---------- KPI DATA ---------- #

        self.cursor.execute(
            f"""
            SELECT
            COUNT(*),
            ROUND(AVG({self.score_expression}), 2),
            MAX({self.score_expression}),
            MIN({self.score_expression})
            FROM students
            """
        )

        kpi_data = self.cursor.fetchone()

        total_students = kpi_data[0]
        avg_marks = kpi_data[1]
        highest_marks = kpi_data[2]
        lowest_marks = kpi_data[3]

        self.cursor.execute(
            f"""
            SELECT
            SUM(CASE WHEN {self.score_expression} >= 90 THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN {self.score_expression} BETWEEN 75 AND 89 THEN 1 ELSE 0 END) AS B,
            SUM(CASE WHEN {self.score_expression} BETWEEN 60 AND 74 THEN 1 ELSE 0 END) AS C,
            SUM(CASE WHEN {self.score_expression} BETWEEN 40 AND 59 THEN 1 ELSE 0 END) AS D,
            SUM(CASE WHEN {self.score_expression} < 40 THEN 1 ELSE 0 END) AS F
            FROM students
            """
        )

        self.grade_distribution = self.cursor.fetchone()

        # ---------- BACKGROUND ---------- #

        self.bg_image = ctk.CTkImage(
            light_image=Image.open(resource_path(
                "assets/images/vireon_analytics.png"
            )),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(
            self,
            image=self.bg_image,
            text=""
        )

        bg_label.place(x=0, y=0)

        # ---------- TITLE ---------- #

        title = ctk.CTkLabel(
            self,
            text="Analytics Dashboard",
            font=("Georgia", 36, "bold"),
            text_color="#5B6FB8",
            fg_color="#DCE6FF",
            corner_radius=12,
            padx=18,
            pady=6
        )

        title.place(
            relx=0.55,
            y=50,
            anchor="center"
        )

        # ---------- KPI FRAME ---------- #

        kpi_frame = ctk.CTkFrame(
            self,
            fg_color="#EDF3FF",
            corner_radius=15
        )

        kpi_frame.place(
            relx=0.5,
            y=130,
            anchor="n"
        )

        # ---------- KPI CARDS ---------- #

        self.create_card(
            kpi_frame,
            "Total Students",
            total_students
        )

        self.create_card(
            kpi_frame,
            "Average Marks",
            avg_marks
        )

        self.create_card(
            kpi_frame,
            "Highest Marks",
            highest_marks
        )

        self.create_card(
            kpi_frame,
            "Lowest Marks",
            lowest_marks
        )

        # ---------- BUTTON FRAME ---------- #

        button_frame = ctk.CTkFrame(
            self,
            fg_color="#EDF3FF"
        )

        button_frame.place(
            relx=0.5,
            y=290,
            anchor="center"
        )

        # ---------- BUTTONS ---------- #

        marks_button = ctk.CTkButton(
            button_frame,
            text="Marks",
            font=("Georgia", 14),
            width=160,
            height=36,
            corner_radius=12,
            fg_color="#5B6FB8",
            hover_color="#394B8A",
            command=self.show_marks_graph
        )

        marks_button.pack(
            side="left",
            padx=12
        )

        grades_button = ctk.CTkButton(
            button_frame,
            text="Grades",
            font=("Georgia", 14),
            width=160,
            height=36,
            corner_radius=12,
            fg_color="#5B6FB8",
            hover_color="#394B8A",
            command=self.show_grade_distribution
        )

        grades_button.pack(
            side="left",
            padx=12
        )

        department_button = ctk.CTkButton(
            button_frame,
            text="Departments",
            font=("Georgia", 14),
            width=160,
            height=36,
            corner_radius=12,
            fg_color="#5B6FB8",
            hover_color="#394B8A",
            command=self.show_department_summary
        )

        department_button.pack(
            side="left",
            padx=12
        )

        # ---------- ANALYTICS FRAME ---------- #

        self.analytics_frame = ctk.CTkFrame(
            self,
            width=1100,
            height=320,
            fg_color="#E8EEFF",
            corner_radius=10,
            border_width=2,
            border_color="#B8C4E8"
        )

        self.analytics_frame.place(
            relx=0.503,
            y=325,
            anchor="n"
        )

        self.analytics_frame.pack_propagate(False)

        # ---------- TOP PERFORMERS ---------- #

        self.cursor.execute(
            f"""
            SELECT {self.name_column}, {self.score_expression} AS marks
            FROM students
            ORDER BY marks DESC
            LIMIT 3
            """
        )

        toppers = self.cursor.fetchall()

        topper_text = "Top Performers\n\n"

        for student in toppers:

            topper_text += (
                f"{student[0]}  -  Marks {student[1]}\n"
            )

        self.topper_card = ctk.CTkFrame(
            self.analytics_frame,
            width=230,
            height=150,
            fg_color="#DCE6FF",
            corner_radius=20,
            border_width=2,
            border_color="#A8B8E8"
        )

        self.topper_card.place(
            x=25,
            y=75
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

        # ---------- EXPORT BUTTON ---------- #

        self.export_button = ctk.CTkButton(
            self.analytics_frame,
            text="Export",
            text_color="#FFFFFF",
            width=120,
            height=40,
            corner_radius=8,
            font=("Georgia", 15),
            fg_color="#5B6FB8",
            hover_color="#394B8A",
            command=self.export_analytics
        )

        self.export_button.place(
            x=68,
            y=250
        )

        # ---------- DEFAULT GRAPH ---------- #

        self.show_grade_distribution()

        # ---------- CLEAN CLOSE ---------- #

        parent.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )


# ---------- RUN APP ---------- #

if __name__ == "__main__":

    app = ctk.CTk()

    app.geometry("1200x700+160+70")

    app.title("Vireon Analytics")

    app.resizable(False, False)

    page = AnalyticsPage(app)

    page.pack(fill="both", expand=True)

    app.mainloop()
