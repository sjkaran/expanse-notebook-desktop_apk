import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("500x400"),
root.title("ctk check")
lbl = ctk.CTkLabel(
    root,
    text="CTK is running Bitch",
    font=("Georgia",50)
)
lbl.pack(pady=50)

root.mainloop()