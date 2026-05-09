import customtkinter as ctk
from PIL import Image

# ---------------- APP ---------------- #

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("1200x700+160+70")
app.title("Vireon")
app.resizable(False, False)

# ---------------- BACKGROUND IMAGE ---------------- #

bg_image = ctk.CTkImage(
    light_image=Image.open("assets/images/vireon.png"),
    size=(1200, 700)
)

bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(x=0, y=0)

# ---------------- ROLE MENU ---------------- #

role_menu = ctk.CTkOptionMenu(
    app,
    values=["Admin", "Faculty", "Student"],
    width=300,
    height=22,
    fg_color="#A3BEDD",
    button_color="#A3BEDD",
    button_hover_color="#A3BEDD",
    dropdown_fg_color="#EDF3FF",
    dropdown_hover_color="#D1DDF8",
    dropdown_text_color="#19325F",
    text_color="#19325F",
    font=("Georgia", 13),
    corner_radius=15,
    anchor="w"
)

role_menu.place(x=680, y=310)

# ---------------- USERNAME ENTRY ---------------- #

username_entry = ctk.CTkEntry(
    app,
    width=300,
    height=22,
    corner_radius=25,
    fg_color="#A3BEDD",
    border_width=0,
    text_color="#19325F",
    font=("Georgia", 13)
)

username_entry.place(x=680, y=390)

# ---------------- PASSWORD ENTRY ---------------- #

password_entry = ctk.CTkEntry(
    app,
    width=300,
    height=22,
    corner_radius=25,
    fg_color="#A3BEDD",
    border_width=0,
    text_color="#19325F",
    show="•",
    font=("Georgia", 13)
)

password_entry.place(x=680, y=470)

# ---------------- LOGIN BUTTON ---------------- #

login_button = ctk.CTkButton(
    app,
    text="Login",
    width=220,
    height=48,
    corner_radius=30,
    fg_color="#8792AE",
    text_color="#F5F8F9",
    border_width=0,
    font=("Georgia", 30)
)

login_button.place(x=760, y=530)

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.mainloop()