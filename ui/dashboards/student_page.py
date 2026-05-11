import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

from database.db_connection import get_connection


class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            width=1200,
            height=700
        )

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
            "font": ("Georgia", 12)
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

        # ---------------- SEARCH ENTRY ---------------- #

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search Student",
            width=160,
            height=34,
            corner_radius=8,
            fg_color="#EDF4FC",
            border_width=1,
            border_color="#C9D8F0",
            text_color="#19325F",
            font=("Georgia", 13)
        )

        self.search_entry.place(x=50, y=20)

        # ---------------- SEARCH BUTTON ---------------- #

        search_button = ctk.CTkButton(
            self,
            text="Search",
            width=80,
            height=34,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 13),
            command=self.search_student
        )

        search_button.place(x=220, y=20)

        # ---------------- FILTER DROPDOWN ---------------- #

        self.department_filter = ctk.CTkOptionMenu(
            self,
            values=[
                "All",
                "CSE",
                "ECE",
                "EEE",
                "IT",
                "MECH"
            ],
            width=120,
            height=34,
            fg_color="#8792AE",
            button_color="#7380A3",
            button_hover_color="#5F6D94",
            command=self.filter_department
        )

        self.department_filter.place(x=310, y=20)

        # ---------------- SORT BUTTON ---------------- #

        sort_button = ctk.CTkButton(
            self,
            text="Sort by CGPA",
            width=130,
            height=34,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 13),
            command=self.sort_students
        )

        sort_button.place(x=440, y=20)

        # ---------------- CRUD BUTTONS ---------------- #

        update_button = ctk.CTkButton(
            self,
            text="Update",
            width=100,
            height=36,
            corner_radius=14,
            fg_color="#6F8CB8",
            hover_color="#5875A0",
            font=("Georgia", 14),
            command=self.update_student
        )

        update_button.place(x=730, y=600)

        add_button = ctk.CTkButton(
            self,
            text="Add Student",
            width=140,
            height=36,
            corner_radius=14,
            fg_color="#8792AE",
            hover_color="#7380A3",
            text_color="#FFFFFF",
            font=("Georgia", 14),
            command=self.add_student
        )

        add_button.place(x=840, y=600)

        delete_button = ctk.CTkButton(
            self,
            text="Delete",
            width=100,
            height=36,
            corner_radius=14,
            fg_color="#B86F7A",
            hover_color="#A05B67",
            font=("Georgia", 14),
            command=self.delete_student
        )

        delete_button.place(x=990, y=600)

        # ---------------- STUDENT TABLE ---------------- #

        self.students_box = ctk.CTkTextbox(
            self,
            width=350,
            height=170,
            fg_color="#EDF4FC",
            text_color="#19325F",
            font=("Georgia", 11),
            corner_radius=10
        )

        self.students_box.place(x=120, y=490)

        self.load_students()

    # ---------------- DISPLAY TABLE ---------------- #

    def display_students(self, students):

        self.students_box.delete("1.0", "end")

        header = (
            f"{'ROLL':<10}"
            f"{'NAME':<18}"
            f"{'DEPT':<10}"
            f"{'CGPA'}\n"
        )

        self.students_box.insert("end", header)

        self.students_box.insert(
            "end",
            "─" * 50 + "\n"
        )

        for student in students:

            row = (
                f"{student[0]:<10}"
                f"{student[1]:<18}"
                f"{student[2]:<10}"
                f"{student[3]}\n\n"
            )

            self.students_box.insert("end", row)

    # ---------------- LOAD STUDENTS ---------------- #

    def load_students(self):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                roll_no,
                full_name,
                department,
                cgpa
                FROM students
            """)

            students = cursor.fetchall()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- SEARCH STUDENT ---------------- #

    def search_student(self):

        keyword = self.search_entry.get()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            SELECT
            roll_no,
            full_name,
            department,
            cgpa
            FROM students
            WHERE full_name LIKE %s
            """

            cursor.execute(
                query,
                (f"%{keyword}%",)
            )

            students = cursor.fetchall()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- FILTER DEPARTMENT ---------------- #

    def filter_department(self, selected):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            if selected == "All":

                query = """
                SELECT
                roll_no,
                full_name,
                department,
                cgpa
                FROM students
                """

                cursor.execute(query)

            else:

                query = """
                SELECT
                roll_no,
                full_name,
                department,
                cgpa
                FROM students
                WHERE department = %s
                """

                cursor.execute(
                    query,
                    (selected,)
                )

            students = cursor.fetchall()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Filter Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- SORT STUDENTS ---------------- #

    def sort_students(self):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            SELECT
            roll_no,
            full_name,
            department,
            cgpa
            FROM students
            ORDER BY cgpa DESC
            """

            cursor.execute(query)

            students = cursor.fetchall()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Sort Error",
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
            (
            roll_no,
            full_name,
            department,
            year,
            cgpa,
            attendance,
            email,
            phone
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
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

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            self.clear_entries()

            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- UPDATE STUDENT ---------------- #

    def update_student(self):

        roll_no = self.roll_entry.get()

        if roll_no == "":

            messagebox.showwarning(
                "Warning",
                "Enter Roll Number"
            )

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ---------- FETCH CURRENT DATA ---------- #

            cursor.execute(
                """
                SELECT
                full_name,
                department,
                year,
                cgpa,
                attendance,
                email,
                phone
                FROM students
                WHERE roll_no=%s
                """,
                (roll_no,)
            )

            existing = cursor.fetchone()

            if not existing:

                messagebox.showerror(
                    "Error",
                    "Student not found"
                )

                return

            # ---------- KEEP OLD VALUES IF EMPTY ---------- #

            full_name = (
                self.name_entry.get()
                if self.name_entry.get() != ""
                else existing[0]
            )

            department = (
                self.department_entry.get()
                if self.department_entry.get() != ""
                else existing[1]
            )

            year = (
                self.year_entry.get()
                if self.year_entry.get() != ""
                else existing[2]
            )

            cgpa = (
                self.cgpa_entry.get()
                if self.cgpa_entry.get() != ""
                else existing[3]
            )

            attendance = (
                self.attendance_entry.get()
                if self.attendance_entry.get() != ""
                else existing[4]
            )

            email = (
                self.email_entry.get()
                if self.email_entry.get() != ""
                else existing[5]
            )

            phone = (
                self.phone_entry.get()
                if self.phone_entry.get() != ""
                else existing[6]
            )

            # ---------- UPDATE QUERY ---------- #

            query = """
            UPDATE students
            SET
            full_name=%s,
            department=%s,
            year=%s,
            cgpa=%s,
            attendance=%s,
            email=%s,
            phone=%s
            WHERE roll_no=%s
            """

            values = (
                full_name,
                department,
                year,
                cgpa,
                attendance,
                email,
                phone,
                roll_no
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Student updated successfully!"
            )

            self.clear_entries()

            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- DELETE STUDENT ---------------- #

    def delete_student(self):

        roll_no = self.roll_entry.get()

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this student?"
        )

        if not confirm:

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            DELETE FROM students
            WHERE roll_no = %s
            """

            cursor.execute(
                query,
                (roll_no,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Student deleted successfully!"
            )

            self.clear_entries()

            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- CLEAR ENTRIES ---------------- #

    def clear_entries(self):

        self.roll_entry.delete(0, "end")

        self.name_entry.delete(0, "end")

        self.department_entry.delete(0, "end")

        self.year_entry.delete(0, "end")

        self.cgpa_entry.delete(0, "end")

        self.attendance_entry.delete(0, "end")

        self.email_entry.delete(0, "end")

        self.phone_entry.delete(0, "end")


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