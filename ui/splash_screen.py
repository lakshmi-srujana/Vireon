import customtkinter as ctk


class SplashScreen(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window Setup
        self.geometry("900x500")
        self.title("Vireon")
        self.resizable(False, False)

        # Dark futuristic theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Background
        self.configure(fg_color="#0B0F1A")

        # Main Frame
        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        frame.pack(expand=True)

        # Logo / Title
        title = ctk.CTkLabel(
            frame,
            text="VIREON",
            font=("Poppins", 48, "bold"),
            text_color="#4CC9F0"
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            frame,
            text="Where Academic Data Becomes Intelligence",
            font=("Poppins", 18),
            text_color="#A0A0A0"
        )
        subtitle.pack(pady=(0, 40))

        # Progress Bar
        self.progress = ctk.CTkProgressBar(
            frame,
            width=400,
            progress_color="#4CC9F0"
        )
        self.progress.pack(pady=20)

        self.progress.set(0)

        # Loading Text
        self.loading = ctk.CTkLabel(
            frame,
            text="Initializing Academic Intelligence Engine...",
            font=("Poppins", 14),
            text_color="#808080"
        )
        self.loading.pack()

        # Animate Loading
        self.animate()

    def animate(self):

        current = self.progress.get()

        if current < 1:
            self.progress.set(current + 0.01)
            self.after(30, self.animate)

        else:
            self.loading.configure(
                text="System Ready"
            )


if __name__ == "__main__":
    app = SplashScreen()
    app.mainloop()