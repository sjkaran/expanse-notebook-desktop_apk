import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# --- System Configuration ---
ctk.set_appearance_mode("Dark") # Force Dark mode for better contrast with the green theme
ctk.set_default_color_theme("green")

class BusinessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Visionary Business Tracker v2.0")
        self.geometry("1100x800")

        # --- Data Model ---
        self.expense_categories = ["Fruits", "Milk", "Grocery", "Ice-Cream", "Drink-Ware", "Employee Cost", "Equipment Cost", "Rent"]
        self.profit_categories = ["Online Payments", "Cash Payments", "Online Orders"]
        
        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="BIZ-TRACK", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_page1 = ctk.CTkButton(self.sidebar_frame, text="Daily Dashboard", height=40, font=("Helvetica", 14, "bold"), command=lambda: self.show_frame("page1"))
        self.btn_page1.grid(row=1, column=0, padx=20, pady=10)

        self.btn_page2 = ctk.CTkButton(self.sidebar_frame, text="Reports & Export", height=40, font=("Helvetica", 14, "bold"), command=lambda: self.show_frame("page2"))
        self.btn_page2.grid(row=2, column=0, padx=20, pady=10)

        # --- Main Container ---
        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
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
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # --- State Management ---
        # We store transactions as objects to allow deletion and recalculation
        self.transactions = [] 
        self.serial_counter = 0

        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Radhey Lassi And Juice", font=("Georgia", 36, "bold"), text_color="#2CC985")
        self.title_label.pack(side="left")

        # --- Dashboard / Summary Cards (Top Right) ---
        self.summary_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.summary_frame.pack(side="right")
        
        # Helper to make cards
        def create_card(parent, title, color):
            frame = ctk.CTkFrame(parent, border_width=2, border_color=color, fg_color="#2b2b2b")
            frame.pack(side="left", padx=10)
            lbl_title = ctk.CTkLabel(frame, text=title, font=("Helvetica", 14), text_color="gray")
            lbl_title.pack(padx=15, pady=(5,0))
            lbl_val = ctk.CTkLabel(frame, text="0.00", font=("Helvetica", 20, "bold"), text_color=color)
            lbl_val.pack(padx=15, pady=(0,5))
            return lbl_val

        self.lbl_total_income = create_card(self.summary_frame, "Total Income", "#2ecc71")
        self.lbl_total_expense = create_card(self.summary_frame, "Total Expense", "#e74c3c")
        self.lbl_net_balance = create_card(self.summary_frame, "Net Balance", "#3498db")

        # --- Input Section ---
        self.input_card = ctk.CTkFrame(self, border_width=1, border_color="#444")
        self.input_card.pack(padx=30, pady=20, fill="x")
        self.input_card.grid_columnconfigure((0, 1, 2), weight=1)

        # -- ROW 1 --
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="Amount", font=("Helvetica", 24, "bold"), height=50, border_color="#146721")
        self.amount_entry.grid(row=0, column=0, padx=15, pady=20, sticky="ew")

        self.type_dropdown = ctk.CTkOptionMenu(
            self.input_card, values=["Expense", "Profit"], command=self.update_categories,
            font=("Helvetica", 16, "bold"), height=50, fg_color="#444", button_color="#555"
        )
        self.type_dropdown.grid(row=0, column=1, padx=15, pady=20, sticky="ew")

        self.category_dropdown = ctk.CTkComboBox(
            self.input_card, values=self.controller.expense_categories,
            font=("Helvetica", 16), height=50, dropdown_font=("Helvetica", 14)
        )
        self.category_dropdown.grid(row=0, column=2, padx=15, pady=20, sticky="ew")
        
        self.update_categories("Expense") # Init

        # -- ROW 2 --
        self.date_dropdown = ctk.CTkOptionMenu(
            self.input_card, values=["Today", "Select Date..."], command=self.handle_date_selection,
            font=("Helvetica", 14), height=40, fg_color="#333"
        )
        self.date_dropdown.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 20), sticky="ew")

        self.add_btn = ctk.CTkButton(
            self.input_card, text="ADD TRANSACTION +", font=("Helvetica", 16, "bold"),
            height=45, fg_color="#159b10", hover_color="#107a0c",
            command=self.add_transaction
        )
        self.add_btn.grid(row=1, column=2, padx=15, pady=(0, 20), sticky="ew")

        # --- Transactions Table ---
        # Header Row
        self.table_header_frame = ctk.CTkFrame(self, height=40, corner_radius=5, fg_color="#333")
        self.table_header_frame.pack(padx=30, pady=(10,0), fill="x")
        
        headers = [("ID", 50), ("Date", 120), ("Time", 80), ("Type", 100), ("Category", 200), ("Amount", 150), ("Action", 80)]
        for col_name, width in headers:
            lbl = ctk.CTkLabel(self.table_header_frame, text=col_name, width=width, font=("Helvetica", 14, "bold"), anchor="w")
            lbl.pack(side="left", padx=5)

        # Scrollable Area
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(padx=30, pady=(5, 30), fill="both", expand=True)

    def update_categories(self, choice):
        if choice == "Profit":
            self.category_dropdown.configure(values=self.controller.profit_categories)
        else:
            self.category_dropdown.configure(values=self.controller.expense_categories)
        self.category_dropdown.set("Select Category")

    def handle_date_selection(self, choice):
        if choice == "Select Date...":
            custom_date = ctk.CTkInputDialog(text="YYYY-MM-DD:", title="Date").get_input()
            if custom_date:
                self.date_dropdown.set(custom_date)
            else:
                self.date_dropdown.set("Today")

    def update_dashboard_totals(self):
        """Recalculates total income, expense and balance from scratch."""
        total_income = 0.0
        total_expense = 0.0
        
        for txn in self.transactions:
            if txn['type'] == "Profit":
                total_income += txn['amount']
            else:
                total_expense += txn['amount']
        
        balance = total_income - total_expense
        
        self.lbl_total_income.configure(text=f"₹{total_income:,.2f}")
        self.lbl_total_expense.configure(text=f"₹{total_expense:,.2f}")
        self.lbl_net_balance.configure(text=f"₹{balance:,.2f}")

    def delete_transaction(self, txn_id, widget_ref):
        """Removes a transaction from logic and UI."""
        # 1. Remove from Data List
        self.transactions = [t for t in self.transactions if t['id'] != txn_id]
        
        # 2. Remove from UI
        widget_ref.destroy()
        
        # 3. Recalculate Totals
        self.update_dashboard_totals()

    def add_transaction(self):
        amount_str = self.amount_entry.get()
        t_type = self.type_dropdown.get()
        category = self.category_dropdown.get()
        date_val = self.date_dropdown.get()

        # --- Validation ---
        if category == "Select Category":
            messagebox.showwarning("Validation", "Please select a valid Category.")
            return
        if not amount_str or not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Invalid Amount.")
            return
        amount_float = float(amount_str)
        if amount_float <= 0:
            messagebox.showerror("Error", "Amount must be positive.")
            return

        # --- Data Prep ---
        self.serial_counter += 1
        
        # Handle Date Logic
        final_date = datetime.now().strftime("%Y-%m-%d") if date_val == "Today" else date_val
        current_time = datetime.now().strftime('%H:%M')
        
        # Store Data
        txn_data = {
            "id": self.serial_counter,
            "date": final_date,
            "type": t_type,
            "amount": amount_float
        }
        self.transactions.append(txn_data)

        # --- UI Rendering (Row Creation) ---
        row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2b2b2b", corner_radius=6)
        row_frame.pack(fill="x", pady=2)
        
        # Visual Config
        color = "#2ecc71" if t_type == "Profit" else "#e74c3c"
        
        # Columns (Must match header widths roughly)
        ctk.CTkLabel(row_frame, text=f"#{self.serial_counter:03}", width=50, anchor="w", font=("Consolas", 14)).pack(side="left", padx=5)
        ctk.CTkLabel(row_frame, text=final_date, width=120, anchor="w", font=("Arial", 14)).pack(side="left", padx=5)
        ctk.CTkLabel(row_frame, text=current_time, width=80, anchor="w", font=("Arial", 14)).pack(side="left", padx=5)
        ctk.CTkLabel(row_frame, text=t_type, width=100, anchor="w", text_color=color, font=("Arial", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(row_frame, text=category, width=200, anchor="w", font=("Arial", 14)).pack(side="left", padx=5)
        ctk.CTkLabel(row_frame, text=f"₹{amount_float:,.2f}", width=150, anchor="w", text_color=color, font=("Arial", 14, "bold")).pack(side="left", padx=5)
        
        # Delete Button
        del_btn = ctk.CTkButton(
            row_frame, text="X", width=40, height=30, fg_color="#c0392b", hover_color="#e74c3c",
            command=lambda: self.delete_transaction(txn_data['id'], row_frame)
        )
        del_btn.pack(side="left", padx=15)

        # --- Finalize ---
        self.amount_entry.delete(0, 'end')
        self.update_dashboard_totals()
        
        # Update Categories Logic
        target_list = self.controller.profit_categories if t_type == "Profit" else self.controller.expense_categories
        if category not in target_list:
            target_list.append(category)
            self.category_dropdown.configure(values=target_list)

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.label = ctk.CTkLabel(self, text="Financial Reports", font=("Georgia", 24, "bold"))
        self.label.pack(pady=20)
        self.info = ctk.CTkLabel(self, text="Excel Export functionality will be implemented here.", font=("Arial", 16))
        self.info.pack(pady=10)

if __name__ == "__main__":
    app = BusinessTrackerApp()
    app.mainloop()