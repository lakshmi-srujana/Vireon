import customtkinter as ctk
import mysql.connector
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

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
            border_color="#B8C4E8"
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

    # ---------- CLEAN WINDOW CLOSE ---------- #

    def close_window(self):

        plt.close(self.fig)

        self.master.destroy()

    # ---------- MAIN ---------- #

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            width=1200,
            height=700
        )

        # ---------- DATABASE CONNECTION ---------- #

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vireon"
        )

        self.cursor = self.connection.cursor()

        # ---------- FETCH ANALYTICS ---------- #

        self.cursor.execute("SELECT COUNT(*) FROM students")
        total_students = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT ROUND(AVG(cgpa), 2) FROM students"
        )

        avg_cgpa = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT MAX(cgpa) FROM students"
        )

        highest_cgpa = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) FROM students WHERE attendance < 75"
        )

        low_attendance = self.cursor.fetchone()[0]

        # ---------- GRAPH DATA ---------- #

        self.cursor.execute(
            "SELECT full_name, cgpa FROM students"
        )

        graph_data = self.cursor.fetchall()

        student_names = []
        cgpa_values = []

        for row in graph_data:

            student_names.append(row[0])

            cgpa_values.append(float(row[1]))

        # ---------- BACKGROUND IMAGE ---------- #

        self.bg_image = ctk.CTkImage(
            light_image=Image.open(
                "assets/images/vireon_analytics.png"
            ),
            size=(1200, 700)
        )

        bg_label = ctk.CTkLabel(
            self,
            image=self.bg_image,
            text=""
        )

        bg_label.place(
            x=0,
            y=0
        )

        # ---------- TITLE ---------- #

        title = ctk.CTkLabel(
            self,
            text="Analytics Dashboard",
            font=("Georgia", 34, "bold"),
            text_color="#5B6FB8"
        )

        title.place(
            relx=0.5,
            y=40,
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
            y=140,
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
            "Average CGPA",
            avg_cgpa
        )

        self.create_card(
            kpi_frame,
            "Highest CGPA",
            highest_cgpa
        )

        self.create_card(
            kpi_frame,
            "Low Attendance",
            low_attendance
        )

        # ---------- ANALYTICS FRAME ---------- #

        analytics_frame = ctk.CTkFrame(
            self,
            width=950,
            height=320,
            fg_color="#E8EEFF",
            corner_radius=30,
            border_width=2,
            border_color="#B8C4E8"
        )

        analytics_frame.place(
            relx=0.5,
            y=300,
            anchor="n"
        )

        analytics_frame.pack_propagate(False)

        # ---------- GRAPH ---------- #

        self.fig, ax = plt.subplots(
            figsize=(8, 4),
            dpi=100
        )

        self.fig.patch.set_facecolor("#DCE6FF")

        ax.set_facecolor("#DCE6FF")

        ax.bar(
            student_names,
            cgpa_values
        )

        ax.set_title(
            "CGPA Distribution",
            fontsize=18,
            color="#394B8A"
        )

        ax.set_xlabel(
            "Students",
            color="#394B8A"
        )

        ax.set_ylabel(
            "CGPA",
            color="#394B8A"
        )

        ax.tick_params(colors="#394B8A")

        for spine in ax.spines.values():
            spine.set_color("#B8C4E8")

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=analytics_frame
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

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