import customtkinter as ctk

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main Window
app = ctk.CTk()
app.geometry("1400x800")
app.title("Student Intelligence System")

# Sidebar
sidebar = ctk.CTkFrame(app, width=250, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="🎓 SIS",
    font=("Poppins", 28, "bold")
)
logo.pack(pady=40)

buttons = ["Dashboard", "Students", "Analytics", "Reports", "Settings"]

for btn in buttons:
    b = ctk.CTkButton(
        sidebar,
        text=btn,
        height=45,
        corner_radius=12
    )
    b.pack(pady=10, padx=20, fill="x")

# Main Area
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", expand=True, fill="both")

title = ctk.CTkLabel(
    main_frame,
    text="Dashboard",
    font=("Poppins", 35, "bold")
)
title.pack(pady=30)

# Stat Cards
card_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
card_frame.pack(pady=20)

stats = [
    ("Total Students", "520"),
    ("Average GPA", "8.7"),
    ("Top Performer", "Aarav"),
    ("Alerts", "12")
]

for text, value in stats:
    card = ctk.CTkFrame(
        card_frame,
        width=220,
        height=140,
        corner_radius=20
    )
    card.pack(side="left", padx=20)

    label = ctk.CTkLabel(
        card,
        text=text,
        font=("Poppins", 18)
    )
    label.pack(pady=(25,10))

    number = ctk.CTkLabel(
        card,
        text=value,
        font=("Poppins", 32, "bold")
    )
    number.pack()

app.mainloop()