import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import hashlib

from database.db_connection import get_connection
from utils.resource_path import resource_path


class FacultyPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            width=1200,
            height=700
        )

        # ---------------- BACKGROUND ---------------- #

        bg_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/images/vireon_facultyadmin.png")),
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

        self.faculty_id_entry = ctk.CTkEntry(
            self,
            placeholder_text="Faculty ID",
            **entry_style
        )

        self.faculty_id_entry.place(x=730, y=150)

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Faculty Name",
            **entry_style
        )

        self.name_entry.place(x=730, y=210)

        self.department_entry = ctk.CTkEntry(
            self,
            placeholder_text="Department",
            **entry_style
        )

        self.department_entry.place(x=730, y=270)

        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Email",
            **entry_style
        )

        self.email_entry.place(x=730, y=330)

        self.phone_entry = ctk.CTkEntry(
            self,
            placeholder_text="Phone Number",
            **entry_style
        )

        self.phone_entry.place(x=730, y=390)

        self.designation_entry = ctk.CTkEntry(
            self,
            placeholder_text="Designation",
            **entry_style
        )

        self.designation_entry.place(x=730, y=450)

        # ---------------- SEARCH ---------------- #

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search Faculty",
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

        search_button = ctk.CTkButton(
            self,
            text="Search",
            width=80,
            height=34,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 13),
            command=self.search_faculty
        )

        search_button.place(x=220, y=20)

        # ---------------- FILTER ---------------- #

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

        # ---------------- SORT ---------------- #

        sort_button = ctk.CTkButton(
            self,
            text="Sort A-Z",
            width=120,
            height=34,
            fg_color="#8792AE",
            hover_color="#7380A3",
            font=("Georgia", 13),
            command=self.sort_faculty
        )

        sort_button.place(x=450, y=20)

        # ---------------- BUTTONS ---------------- #

        update_button = ctk.CTkButton(
            self,
            text="Update",
            width=100,
            height=36,
            corner_radius=14,
            fg_color="#6F8CB8",
            hover_color="#5875A0",
            font=("Georgia", 14),
            command=self.update_faculty
        )

        update_button.place(x=730, y=560)

        add_button = ctk.CTkButton(
            self,
            text="Add Faculty",
            width=140,
            height=36,
            corner_radius=14,
            fg_color="#8792AE",
            hover_color="#7380A3",
            text_color="#FFFFFF",
            font=("Georgia", 14),
            command=self.add_faculty
        )

        add_button.place(x=840, y=560)

        delete_button = ctk.CTkButton(
            self,
            text="Delete",
            width=100,
            height=36,
            corner_radius=14,
            fg_color="#B86F7A",
            hover_color="#A05B67",
            font=("Georgia", 14),
            command=self.delete_faculty
        )

        delete_button.place(x=990, y=560)

        # ---------------- TABLE ---------------- #

        self.faculty_box = ctk.CTkTextbox(
            self,
            width=350,
            height=170,
            fg_color="#EDF4FC",
            text_color="#19325F",
            font=("Georgia", 11),
            corner_radius=10
        )

        self.faculty_box.place(x=120, y=490)

        self.load_faculty()

    # ---------------- DISPLAY ---------------- #

    def display_faculty(self, faculty):

        self.faculty_box.delete("1.0", "end")

        header = (
            f"{'ID':<10}"
            f"{'NAME':<18}"
            f"{'DEPT'}\n"
        )

        self.faculty_box.insert("end", header)

        self.faculty_box.insert(
            "end",
            "─" * 40 + "\n"
        )

        for member in faculty:

            row = (
                f"{member[0]:<10}"
                f"{member[1]:<18}"
                f"{member[2]}\n\n"
            )

            self.faculty_box.insert("end", row)

    # ---------------- LOAD ---------------- #

    def load_faculty(self):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                faculty_id,
                full_name,
                department
                FROM faculty
            """)

            faculty = cursor.fetchall()

            self.display_faculty(faculty)

        finally:

            cursor.close()

            connection.close()

    # ---------------- ADD FACULTY ---------------- #

    def add_faculty(self):

        faculty_id = self.faculty_id_entry.get()

        full_name = self.name_entry.get()

        department = self.department_entry.get()

        email = self.email_entry.get()

        phone = self.phone_entry.get()

        designation = self.designation_entry.get()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ---------- INSERT FACULTY ---------- #

            query = """
            INSERT INTO faculty
            (
            faculty_id,
            full_name,
            department,
            email,
            phone,
            designation
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
            """

            values = (
                faculty_id,
                full_name,
                department,
                email,
                phone,
                designation
            )

            cursor.execute(query, values)

            # ---------- AUTO PASSWORD ---------- #

            raw_password = (
                full_name.split()[0].lower()
                + "@"
                + faculty_id
            )

            hashed_password = hashlib.sha256(
                raw_password.encode()
            ).hexdigest()

            username = (
                full_name.split()[0].lower()
            )

            # ---------- INSERT USER ---------- #

            user_query = """
            INSERT INTO users
            (
            username,
            password_hash,
            role,
            linked_id
            )
            VALUES
            (%s, %s, %s, %s)
            """

            user_values = (
                username,
                hashed_password,
                "faculty",
                faculty_id
            )

            cursor.execute(
                user_query,
                user_values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                f"Faculty Added Successfully!\n\n"
                f"Username: {username}\n"
                f"Password: {raw_password}"
            )

            self.clear_entries()

            self.load_faculty()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()

    # ---------------- SEARCH ---------------- #

    def search_faculty(self):

        keyword = self.search_entry.get()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            query = """
            SELECT
            faculty_id,
            full_name,
            department
            FROM faculty
            WHERE full_name LIKE %s
            """

            cursor.execute(
                query,
                (f"%{keyword}%",)
            )

            faculty = cursor.fetchall()

            self.display_faculty(faculty)

        finally:

            cursor.close()

            connection.close()

    # ---------------- FILTER ---------------- #

    def filter_department(self, selected):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            if selected == "All":

                cursor.execute("""
                    SELECT
                    faculty_id,
                    full_name,
                    department
                    FROM faculty
                """)

            else:

                cursor.execute(
                    """
                    SELECT
                    faculty_id,
                    full_name,
                    department
                    FROM faculty
                    WHERE department=%s
                    """,
                    (selected,)
                )

            faculty = cursor.fetchall()

            self.display_faculty(faculty)

        finally:

            cursor.close()

            connection.close()

    # ---------------- SORT ---------------- #

    def sort_faculty(self):

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                faculty_id,
                full_name,
                department
                FROM faculty
                ORDER BY full_name ASC
            """)

            faculty = cursor.fetchall()

            self.display_faculty(faculty)

        finally:

            cursor.close()

            connection.close()

    # ---------------- UPDATE ---------------- #

    def update_faculty(self):

        faculty_id = self.faculty_id_entry.get()

        if faculty_id == "":

            messagebox.showwarning(
                "Warning",
                "Enter Faculty ID"
            )

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ---------- FETCH EXISTING DATA ---------- #

            cursor.execute(
                """
                SELECT
                full_name,
                department,
                email,
                phone,
                designation
                FROM faculty
                WHERE faculty_id=%s
                """,
                (faculty_id,)
            )

            existing = cursor.fetchone()

            if not existing:

                messagebox.showerror(
                    "Error",
                    "Faculty not found"
                )

                return

            # ---------- KEEP OLD VALUES ---------- #

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

            email = (
                self.email_entry.get()
                if self.email_entry.get() != ""
                else existing[2]
            )

            phone = (
                self.phone_entry.get()
                if self.phone_entry.get() != ""
                else existing[3]
            )

            designation = (
                self.designation_entry.get()
                if self.designation_entry.get() != ""
                else existing[4]
            )

            # ---------- UPDATE FACULTY ---------- #

            query = """
            UPDATE faculty
            SET
            full_name=%s,
            department=%s,
            email=%s,
            phone=%s,
            designation=%s
            WHERE faculty_id=%s
            """

            values = (
                full_name,
                department,
                email,
                phone,
                designation,
                faculty_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Faculty updated successfully!"
            )

            self.clear_entries()

            self.load_faculty()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                str(e)
            )

        finally:

            cursor.close()

            connection.close()
    # ---------------- DELETE ---------------- #

    def delete_faculty(self):

        faculty_id = self.faculty_id_entry.get()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM users
                WHERE linked_id=%s
                """,
                (faculty_id,)
            )

            cursor.execute(
                """
                DELETE FROM faculty
                WHERE faculty_id=%s
                """,
                (faculty_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                "Faculty deleted successfully!"
            )

            self.clear_entries()

            self.load_faculty()

        finally:

            cursor.close()

            connection.close()

    # ---------------- CLEAR ---------------- #

    def clear_entries(self):

        self.faculty_id_entry.delete(0, "end")

        self.name_entry.delete(0, "end")

        self.department_entry.delete(0, "end")

        self.email_entry.delete(0, "end")

        self.phone_entry.delete(0, "end")

        self.designation_entry.delete(0, "end")


# ---------------- RUN ---------------- #

if __name__ == "__main__":

    ctk.set_appearance_mode("light")

    app = ctk.CTk()

    app.geometry("1200x700+160+70")

    app.title("Vireon Faculty Management")

    app.resizable(False, False)

    page = FacultyPage(app)

    page.pack(fill="both", expand=True)

    app.mainloop()