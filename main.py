import customtkinter as ctk

from ui.splash_screen import SplashScreen
from ui.login_page import LoginPage

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.geometry("1200x700+160+70")
app.title("Vireon")
app.resizable(False, False)

# ---------------- SHOW LOGIN ---------------- #

def show_login():

    splash.pack_forget()

    login = LoginPage(app)
    login.pack(fill="both", expand=True)

# ---------------- SPLASH SCREEN ---------------- #

splash = SplashScreen(app, show_login)
splash.pack(fill="both", expand=True)

app.mainloop()