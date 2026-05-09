import customtkinter as ctk
from PIL import Image


class SplashScreen(ctk.CTkFrame):

    def __init__(self, parent, callback):
        super().__init__(parent)

        self.callback = callback

        # ---------------- IMAGE ---------------- #

        splash_image = ctk.CTkImage(
            light_image=Image.open("assets/images/vireon_splashscreen.png"),
            size=(1200, 700)
        )

        splash_label = ctk.CTkLabel(
            self,
            image=splash_image,
            text=""
        )

        splash_label.place(x=0, y=0)

        # Keep image alive
        self.image = splash_image

        # ---------------- LOADING ---------------- #

        self.loading = ctk.CTkProgressBar(
            self,
            width=300,
            height=8,
            corner_radius=10,
            progress_color="#8792AE",
            fg_color="#DCE6F7"
        )

        self.loading.place(relx=0.5, rely=0.67, anchor="center")

        self.progress = 0

        self.animate()

    # ---------------- ANIMATION ---------------- #

    def animate(self):

        self.progress += 0.01
        self.loading.set(self.progress)

        if self.progress < 1:
            self.after(20, self.animate)

        else:
            self.after(300, self.callback)