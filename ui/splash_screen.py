import customtkinter as ctk
from PIL import Image
import subprocess
import sys

# ---------------- APP ---------------- #

ctk.set_appearance_mode("light")

splash = ctk.CTk()
splash.geometry("1200x700+160+70")
splash.title("Vireon")
splash.resizable(False, False)

# ---------------- SPLASH IMAGE ---------------- #

splash_image = ctk.CTkImage(
    light_image=Image.open("assets/images/vireon_splashscreen.png"),
    size=(1200, 700)
)

splash_label = ctk.CTkLabel(
    splash,
    image=splash_image,
    text=""
)

splash_label.place(x=0, y=0)

loading = ctk.CTkProgressBar(
    splash,
    width=300,
    height=8,
    corner_radius=10,
    progress_color="#8792AE",
    fg_color="#DCE6F7"
)

loading.place(relx=0.5, rely=0.67, anchor="center")
loading.set(0)

# ---------------- OPEN LOGIN ---------------- #


progress_value = 0

def animate_loading():
    global progress_value

    progress_value += 0.01
    loading.set(progress_value)

    if progress_value < 1:
        splash.after(20, animate_loading)
    else:
        open_login()

def open_login():
    splash.destroy()
    subprocess.Popen([sys.executable, "ui/login_page.py"])

animate_loading()


# ---------------- RUN ---------------- #

splash.mainloop()