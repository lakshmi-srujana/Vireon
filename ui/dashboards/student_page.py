import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from database.db_connection import get_connection


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(width=1200, height=700)

        # ---------------- BACKGROUND IMAGE ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open(
                "assets/images/vireon_studentadmin.png"
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

        # ---------------- ENTRY STYLE ---------------- #

        entry_style = {
            "width": 320,
            "height": 34,
            "corner_radius": 8,
            "fg_color": "#A3BEDD",
            "border_width": 1,
            "border_color": "#C9D8F0",
            "text_color": "#19325F",
            "font": ("Georgia", 14)
        }

        # ---------------- ENTRIES ---------------- #

        self.roll_entry = ctk.CTkEntry(
            self,
            placeholder_text="Roll Number",
            **entry_style
        )
        self.roll_entry.place(x=730, y=135)

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Full Name",
            **entry_style
        )
        self.name_entry.place(x=730, y=190)

        self.department_entry = ctk.CTkEntry(
            self,
            placeholder_text="Department",
            **entry_style
        )
        self.department_entry.place(x=730, y=245)

        self.year_entry = ctk.CTkEntry(
            self,
            placeholder_text="Year",
            **entry_style
        )
        self.year_entry.place(x=730, y=300)

        self.cgpa_entry = ctk.CTkEntry(
            self,
            placeholder_text="CGPA",
            **entry_style
        )
        self.cgpa_entry.place(x=730, y=355)

        self.attendance_entry = ctk.CTkEntry(
            self,
            placeholder_text="Attendance",
            **entry_style
        )
        self.attendance_entry.place(x=730, y=410)

        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Email",
            **entry_style
        )
        self.email_entry.place(x=730, y=465)

        self.phone_entry = ctk.CTkEntry(
            self,
            placeholder_text="Phone Number",
            **entry_style
        )
        self.phone_entry.place(x=730, y=520)

        # ---------------- BUTTON ---------------- #

        add_button = ctk.CTkButton(
            self,
            text="Add Student",
            width=180,
            height=42,
            corner_radius=18,
            fg_color="#8792AE",
            hover_color="#7380A3",
            text_color="#FFFFFF",
            font=("Georgia", 18),
            command=self.add_student
        )

        add_button.place(x=820, y=595)

    # ---------------- STUDENT TABLE ---------------- #

        self.students_box = ctk.CTkTextbox(
            self,
            width=400,
            height=150,
            fg_color="#EDF4FC",
            text_color="#19325F",
            font=("Georgia", 13),
            corner_radius=8
        )

        self.students_box.place(x=100, y=500)

        self.load_students()

    def load_students(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT roll_no, full_name, department, cgpa
                FROM students
            """)

            students = cursor.fetchall()

            self.students_box.delete("1.0", "end")

            # ---------------- HEADERS ---------------- #

            header = (
                f"{'ROLL':<8}"
                f"{'NAME':<15}"
                f"{'DEPT':<10}"
                f"{'CGPA'}\n"
            )

            self.students_box.insert("end", header)
            self.students_box.insert(
                "end",
                "─" * 32 + "\n"
            )

            # ---------------- ROWS ---------------- #

            for student in students:

                row = (
                    f"{student[0]:<8}"
                    f"{student[1]:<15}"
                    f"{student[2]:<10}"
                    f"{student[3]}\n\n"
                )

                self.students_box.insert("end", row)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()
    # ---------------- ADD STUDENT ---------------- #

    def add_student(self):

        roll_no = self.roll_entry.get()
        full_name = self.name_entry.get()
        department = self.department_entry.get()
        year = self.year_entry.get()
        cgpa = self.cgpa_entry.get()
        attendance = self.attendance_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        try:

            connection = get_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO students
            (roll_no, full_name, department, year,
             cgpa, attendance, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                roll_no,
                full_name,
                department,
                year,
                cgpa,
                attendance,
                email,
                phone
            )

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            # ---------------- CLEAR ENTRIES ---------------- #

            self.roll_entry.delete(0, "end")
            self.name_entry.delete(0, "end")
            self.department_entry.delete(0, "end")
            self.year_entry.delete(0, "end")
            self.cgpa_entry.delete(0, "end")
            self.attendance_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.phone_entry.delete(0, "end")
            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()


# ---------------- RUN ---------------- #

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")
    app.title("Vireon")
    app.resizable(False, False)

    page = StudentsPage(app)
    page.pack(fill="both", expand=True)

    app.mainloop()