import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# --- System Configuration ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BusinessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Visionary Business Tracker v1.1")
        self.geometry("900x650") # Slightly adjusted default size

        # --- Data Model ---
        self.categories = ["Sales", "Rent", "Utilities", "Inventory", "Marketing"]
        
        # --- Layout Grid Configuration ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Navigation (Left Panel) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="BIZ-TRACK", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_page1 = ctk.CTkButton(self.sidebar_frame, text="Daily Transactions", command=lambda: self.show_frame("page1"))
        self.btn_page1.grid(row=1, column=0, padx=20, pady=10)

        self.btn_page2 = ctk.CTkButton(self.sidebar_frame, text="Reports & Export", command=lambda: self.show_frame("page2"))
        self.btn_page2.grid(row=2, column=0, padx=20, pady=10)

        # --- Main Content Area (Right Panel) ---
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.setup_frames()
        self.show_frame("page1")

    def setup_frames(self):
        for PageClass in (TransactionPage, ReportsPage):
            page_name = "page1" if PageClass == TransactionPage else "page2"
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class TransactionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.serial_counter = 0  # Initialize transaction counter
        
        # --- Header ---
        self.label = ctk.CTkLabel(self, text="Daily Business Ledger", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(15, 20))

        # --- Input Section (Refactored for Responsiveness) ---
        self.input_card = ctk.CTkFrame(self)
        self.input_card.pack(padx=20, pady=10, fill="x")
        
        # Configure Grid: 3 columns, equal weight
        self.input_card.grid_columnconfigure((0, 1, 2), weight=1)

        # -- ROW 1: Core Data --
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="Amount (e.g. 500)")
        self.amount_entry.grid(row=0, column=0, padx=10, pady=(15, 5), sticky="ew")

        self.type_dropdown = ctk.CTkOptionMenu(self.input_card, values=["Profit", "Expense"])
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=(15, 5), sticky="ew")

        self.category_dropdown = ctk.CTkComboBox(self.input_card, values=self.controller.categories)
        self.category_dropdown.grid(row=0, column=2, padx=10, pady=(15, 5), sticky="ew")
        self.category_dropdown.set("Select Category")

        # -- ROW 2: Metadata & Action --
        self.date_dropdown = ctk.CTkOptionMenu(self.input_card, values=["Today", "Select Date..."], command=self.handle_date_selection)
        self.date_dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="ew")

        self.add_btn = ctk.CTkButton(
            self.input_card, 
            text="Add Transaction", 
            fg_color="#2ecc71", 
            hover_color="#27ae60", 
            command=self.add_transaction
        )
        self.add_btn.grid(row=1, column=2, padx=10, pady=(5, 15), sticky="ew")

        # --- Display Section ---
        header_text = f"{'Sr.':<4} | {'Time':<6} | {'Type':<8} | {'Category':<15} | {'Amount'}"
        self.table_label = ctk.CTkLabel(self, text="Today's Transactions", font=ctk.CTkFont(size=16, weight="bold"))
        self.table_label.pack(pady=(20, 5), anchor="w", padx=30)
        
        # Headers for the scrollable list
        self.headers = ctk.CTkLabel(self, text=header_text, font=("Consolas", 12, "bold"), anchor="w")
        self.headers.pack(fill="x", padx=35)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def handle_date_selection(self, choice):
        if choice == "Select Date...":
            custom_date = ctk.CTkInputDialog(text="Enter date (YYYY-MM-DD):", title="Date Selector").get_input()
            if custom_date:
                self.date_dropdown.set(custom_date)
            else:
                self.date_dropdown.set("Today")

    def add_transaction(self):
        amount_str = self.amount_entry.get()
        t_type = self.type_dropdown.get()
        category = self.category_dropdown.get()
        date = self.date_dropdown.get()

        # --- Engineering Validation Block ---
        # 1. Check for empty
        if not amount_str:
            messagebox.showwarning("Input Error", "Please enter an amount.")
            return

        # 2. Check for numeric validity
        if not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Type Error", "Amount must be a number.")
            return
            
        # 3. Check for Zero value
        amount_float = float(amount_str)
        if amount_float <= 0:
            messagebox.showerror("Value Error", "Transaction amount must be greater than 0.")
            return

        # --- Success Logic ---
        self.serial_counter += 1
        current_time = datetime.now().strftime('%H:%M')
        
        # Formatting for Monospace Font (alignment)
        # Structure: Sr. | Time | Type | Category | Amount
        display_text = f"#{self.serial_counter:03}  | {current_time}  | {t_type:<8} | {category:<15} | ${amount_float:,.2f}"
        
        color = "#2ecc71" if t_type == "Profit" else "#e74c3c"
        
        entry_row = ctk.CTkLabel(
            self.scrollable_frame, 
            text=display_text, 
            text_color=color, 
            anchor="w", 
            font=("Consolas", 13)
        )
        entry_row.pack(fill="x", padx=10, pady=2)

        # Reset & Update Memory
        self.amount_entry.delete(0, 'end')
        
        if category not in self.controller.categories:
            self.controller.categories.append(category)
            self.category_dropdown.configure(values=self.controller.categories)

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.label = ctk.CTkLabel(self, text="Financial Reports (Excel)", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)
        self.info_label = ctk.CTkLabel(self, text="Export history and monthly summaries below.")
        self.info_label.pack(pady=10)

if __name__ == "__main__":
    app = BusinessTrackerApp()
    app.mainloop()