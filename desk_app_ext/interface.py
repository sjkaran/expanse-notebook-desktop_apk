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
        self.title("Visionary Business Tracker v1.2")
        self.geometry("900x650")

        # --- Data Model (Segregated Logic) ---
        # We separate categories to keep the UI context-aware
        self.expense_categories = ["Fruits","Milk", "Grocery","Ice-Cream","Drink-Ware","Employe Cost","Extra cost","Equipment Cost","Rent"]
        self.profit_categories = ["Online Payments", "Cash Payments","Online Orders"] # Starts with only three, as requested.

        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="BIZ-TRACK", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_page1 = ctk.CTkButton(self.sidebar_frame, text="Daily Transactions", command=lambda: self.show_frame("page1"))
        self.btn_page1.grid(row=1, column=0, padx=20, pady=10)

        self.btn_page2 = ctk.CTkButton(self.sidebar_frame, text="Reports & Export", command=lambda: self.show_frame("page2"))
        self.btn_page2.grid(row=2, column=0, padx=20, pady=10)

        # --- Main Container ---
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
        self.serial_counter = 0
        
        # --- Header ---
        self.label = ctk.CTkLabel(self, text="Radhey Lassi And Juice", font=ctk.CTkFont("Georgia",size=34))
        self.label.pack(pady=(15, 20))

        # --- Input Section ---
        self.input_card = ctk.CTkFrame(self)
        self.input_card.pack(padx=20, pady=10, fill="x")
        self.input_card.grid_columnconfigure((0, 1, 2), weight=1)

        # -- ROW 1 --
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="Amount (e.g. 500)",border_color="#146721",font=("Helvetica",23,"bold"),height=40)
        self.amount_entry.grid(row=0, column=0, padx=10, pady=(15, 5), sticky="ew")

        # Logic Upgrade: Added command=self.update_categories
        self.type_dropdown = ctk.CTkOptionMenu(
            self.input_card, 
            values=["Expense", "Profit"], # Default first value
            command=self.update_categories 
        )
        self.type_dropdown.grid(row=0, column=1, padx=10, pady=(15, 5), sticky="ew")

        # Category Box (Starts empty/default)
        self.category_dropdown = ctk.CTkComboBox(self.input_card, values=self.controller.expense_categories)
        self.category_dropdown.grid(row=0, column=2, padx=10, pady=(15, 5), sticky="ew")
        
        # Initialize the categories based on the default Type ("Expense")
        self.update_categories("Expense")

        # -- ROW 2 --
        self.date_dropdown = ctk.CTkOptionMenu(self.input_card, values=["Today", "Select Date..."], command=self.handle_date_selection)
        self.date_dropdown.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="ew")

        self.add_btn = ctk.CTkButton(
            self.input_card, 
            text="Add Transaction", 
            text_color="#efefef",
            fg_color="#159b10", 
            hover_color="#154a2b", 
            font=("Helvetica",15,"bold"),
            command=self.add_transaction
        )
        self.add_btn.grid(row=1, column=2, padx=10, pady=(5, 15), sticky="ew")

        # --- Display Section ---
        header_text = f"{'Sr.':<4} | {'Time':<6} | {'Type':<8} | {'Category':<15} | {'Amount'}"
        self.table_label = ctk.CTkLabel(self, text="Today's Transactions", font=ctk.CTkFont(size=16, weight="bold"))
        self.table_label.pack(pady=(20, 5), anchor="w", padx=30)
        
        self.headers = ctk.CTkLabel(self, text=header_text, font=("Consolas", 12, "bold"), anchor="w")
        self.headers.pack(fill="x", padx=35)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def update_categories(self, choice):
        """
        Event Handler: Triggered immediately when user changes 'Profit'/'Expense'.
        Swaps the list inside the Category Dropdown.
        """
        if choice == "Profit":
            self.category_dropdown.configure(values=self.controller.profit_categories)
            self.category_dropdown.set("Select Category")
        else:
            self.category_dropdown.configure(values=self.controller.expense_categories)
            self.category_dropdown.set("Select Category")

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

        # --- Validation ---
        if not amount_str:
            messagebox.showwarning("Input Error", "Please enter an amount.")
            return
        if not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Type Error", "Amount must be a number.")
            return
        amount_float = float(amount_str)
        if amount_float <= 0:
            messagebox.showerror("Value Error", "Transaction amount must be greater than 0.")
            return

        # --- Success Logic ---
        self.serial_counter += 1
        current_time = datetime.now().strftime('%H:%M')
        
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

        # Reset Entry
        self.amount_entry.delete(0, 'end')

        # --- Context-Aware Memory Update ---
        # If the user typed a NEW category, we must save it to the CORRECT list.
        if t_type == "Profit":
            if category not in self.controller.profit_categories:
                self.controller.profit_categories.append(category)
                # If we are still on "Profit" mode, update the dropdown immediately
                self.category_dropdown.configure(values=self.controller.profit_categories)
        else:
            if category not in self.controller.expense_categories:
                self.controller.expense_categories.append(category)
                # If we are still on "Expense" mode, update the dropdown immediately
                self.category_dropdown.configure(values=self.controller.expense_categories)

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_report_df = None # Store data here for saving later
        self.selected_year_month = None

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=20)
        
        self.label = ctk.CTkLabel(self.header_frame, text="Monthly Reports & Analytics", font=("Georgia", 28, "bold"))
        self.label.pack(side="left")

        # --- Control Bar ---
        self.control_frame = ctk.CTkFrame(self, fg_color="#333", height=60)
        self.control_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(self.control_frame, text="Select Month:", font=("Arial", 14)).pack(side="left", padx=20, pady=10)
        
        self.month_dropdown = ctk.CTkOptionMenu(
            self.control_frame, values=["No Data"], width=180,
            font=("Arial", 14), command=self.on_month_select
        )
        self.month_dropdown.pack(side="left", padx=10, pady=10)

        self.preview_btn = ctk.CTkButton(
            self.control_frame, text="Load Preview", 
            font=("Helvetica", 14, "bold"), fg_color="#3498db", hover_color="#2980b9",
            command=self.load_preview
        )
        self.preview_btn.pack(side="left", padx=20, pady=10)

        self.download_btn = ctk.CTkButton(
            self.control_frame, text="Download Excel", 
            font=("Helvetica", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71",
            state="disabled", command=self.download_excel
        )
        self.download_btn.pack(side="right", padx=20, pady=10)

        # --- Preview Table Area ---
        self.preview_label = ctk.CTkLabel(self, text="Report Preview (First 50 rows)", font=("Arial", 14, "italic"), text_color="gray")
        self.preview_label.pack(padx=30, anchor="w")

        # Container for the grid
        self.table_container = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.table_container.pack(padx=30, pady=10, fill="both", expand=True)

    def refresh_status(self):
        """Called when switching to this tab. Updates month list."""
        months = self.controller.backend.get_available_months()
        if months:
            self.month_dropdown.configure(values=months)
            self.month_dropdown.set(months[0])
            self.selected_year_month = months[0]
        else:
            self.month_dropdown.configure(values=["No Data"])
            self.month_dropdown.set("No Data")
            self.selected_year_month = None

    def on_month_select(self, choice):
        self.selected_year_month = choice
        # Reset buttons when selection changes
        self.download_btn.configure(state="disabled")
        # Clear previous table
        for widget in self.table_container.winfo_children():
            widget.destroy()

    def load_preview(self):
        if not self.selected_year_month or self.selected_year_month == "No Data":
            messagebox.showwarning("Warning", "No data available to load.")
            return

        # Parse "YYYY-MM"
        year, month = map(int, self.selected_year_month.split('-'))
        
        # Fetch DataFrame from Backend
        df = self.controller.backend.get_monthly_pivot_data(year, month)
        
        if df is None:
            messagebox.showinfo("Info", "No transactions found for this month.")
            return

        self.current_report_df = df
        self.render_preview_table(df)
        
        # Enable Download
        self.download_btn.configure(state="normal")

    def render_preview_table(self, df):
        # Clear old widgets
        for widget in self.table_container.winfo_children():
            widget.destroy()

        # Reset Grid
        df_reset = df.reset_index() # Make Date a normal column
        columns = list(df_reset.columns)
        
        # 1. Render Headers
        for col_idx, col_name in enumerate(columns):
            ctk.CTkLabel(
                self.table_container, text=str(col_name), 
                font=("Arial", 12, "bold"), fg_color="#444", corner_radius=4, width=100
            ).grid(row=0, column=col_idx, padx=2, pady=5, sticky="ew")

        # 2. Render Data Rows
        # Limit to 50 rows for performance in preview
        for row_idx, row in enumerate(df_reset.head(50).itertuples(index=False), start=1):
            for col_idx, value in enumerate(row):
                # Formatting: If float, show currency
                display_text = f"{value}"
                if isinstance(value, (int, float)) and col_idx > 0: # Skip date column for currency
                    display_text = f"{value:,.0f}" if value == 0 else f"{value:,.2f}"
                
                # Highlight "Total" or "Margin" columns
                bg_color = "transparent"
                text_color = "white"
                
                if "Total Income" in columns[col_idx]: text_color = "#2ecc71"
                elif "Total Expense" in columns[col_idx]: text_color = "#e74c3c"
                elif "Net Margin" in columns[col_idx]: text_color = "#3498db"

                ctk.CTkLabel(
                    self.table_container, text=display_text, 
                    font=("Consolas", 12), text_color=text_color
                ).grid(row=row_idx, column=col_idx, padx=5, pady=2)

    def download_excel(self):
        if self.current_report_df is None:
            return
            
        year, month = map(int, self.selected_year_month.split('-'))
        try:
            filename = self.controller.backend.save_report_to_excel(self.current_report_df, year, month)
            messagebox.showinfo("Success", f"File Downloaded Successfully:\n\n{filename}\n\nCheck your app folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    app = BusinessTrackerApp()
    app.mainloop()






"""
* must show the total profit, expenses and income int the top of the transactions table. rather than the format of transactions.
* must store the date of the transactions in the table with the serial number.
* must have an option to delete or remove a transaction.
* must not store a transaction with the category of "select category".

* styling: making texts larger.
* styling: making the colors more high contrasts.
"""