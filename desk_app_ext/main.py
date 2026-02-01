import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from backend import BackendManager  # Importing our engineering brain

# --- System Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class BusinessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Engineering: Initialize Backend ---
        self.backend = BackendManager()

        # --- Window Configuration ---
        self.title("Visionary Business Tracker v3.0 (Production)")
        self.geometry("1100x800")
        
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
        # Auto-refresh data when switching to reports
        if page_name == "page2":
            self.frames[page_name].refresh_status()

    def on_closing(self):
        self.backend.close()
        self.destroy()

class TransactionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # State: Currently selected date (defaults to today)
        self.current_view_date = datetime.now().strftime("%Y-%m-%d")

        # --- Header Section ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Radhey Lassi And Juice", font=("Georgia", 36, "bold"), text_color="#2CC985")
        self.title_label.pack(side="left")

        # --- Dashboard Cards ---
        self.summary_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.summary_frame.pack(side="right")
        
        self.lbl_total_income = self.create_card(self.summary_frame, "Income", "#2ecc71")
        self.lbl_total_expense = self.create_card(self.summary_frame, "Expense", "#e74c3c")
        self.lbl_net_balance = self.create_card(self.summary_frame, "Net Balance", "#3498db")

        # --- Input Section ---
        self.input_card = ctk.CTkFrame(self, border_width=1, border_color="#444")
        self.input_card.pack(padx=30, pady=20, fill="x")
        self.input_card.grid_columnconfigure((0, 1, 2), weight=1)

        # Row 1
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="Amount", font=("Helvetica", 24, "bold"), height=50, border_color="#146721")
        self.amount_entry.grid(row=0, column=0, padx=15, pady=20, sticky="ew")

        self.type_dropdown = ctk.CTkOptionMenu(
            self.input_card, values=["Expense", "Profit"], command=self.update_categories,
            font=("Helvetica", 16, "bold"), height=50, fg_color="#444", button_color="#555"
        )
        self.type_dropdown.grid(row=0, column=1, padx=15, pady=20, sticky="ew")

        self.category_dropdown = ctk.CTkComboBox(
            self.input_card, values=[], # Loaded dynamically
            font=("Helvetica", 16), height=50, dropdown_font=("Helvetica", 14)
        )
        self.category_dropdown.grid(row=0, column=2, padx=15, pady=20, sticky="ew")

        # Row 2
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

        # --- Table Headers ---
        self.table_header_frame = ctk.CTkFrame(self, height=40, corner_radius=5, fg_color="#333")
        self.table_header_frame.pack(padx=30, pady=(10,0), fill="x")
        
        headers = [("ID", 50), ("Time", 80), ("Type", 100), ("Category", 200), ("Amount", 150), ("Action", 80)]
        for col_name, width in headers:
            lbl = ctk.CTkLabel(self.table_header_frame, text=col_name, width=width, font=("Helvetica", 14, "bold"), anchor="w")
            lbl.pack(side="left", padx=5)

        # --- Scrollable List ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(padx=30, pady=(5, 30), fill="both", expand=True)

        # --- Initial Data Load ---
        self.update_categories("Expense")
        self.load_daily_data()

    def create_card(self, parent, title, color):
        frame = ctk.CTkFrame(parent, border_width=2, border_color=color, fg_color="#2b2b2b")
        frame.pack(side="left", padx=10)
        lbl_title = ctk.CTkLabel(frame, text=title, font=("Helvetica", 14), text_color="gray")
        lbl_title.pack(padx=15, pady=(5,0))
        lbl_val = ctk.CTkLabel(frame, text="0.00", font=("Helvetica", 20, "bold"), text_color=color)
        lbl_val.pack(padx=15, pady=(0,5))
        return lbl_val

    def update_categories(self, choice):
        # Fetch from DB based on selection
        cats = self.controller.backend.get_categories(choice)
        self.category_dropdown.configure(values=cats)
        if cats:
            self.category_dropdown.set(cats[0])
        else:
            self.category_dropdown.set("")

    def handle_date_selection(self, choice):
        if choice == "Select Date...":
            custom_date = ctk.CTkInputDialog(text="YYYY-MM-DD:", title="Date").get_input()
            if custom_date:
                self.current_view_date = custom_date
                self.date_dropdown.set(custom_date)
            else:
                self.date_dropdown.set("Today")
        else:
            self.current_view_date = datetime.now().strftime("%Y-%m-%d")
        
        # REFRESH UI FOR NEW DATE
        self.load_daily_data()

    def load_daily_data(self):
        """The Core Refresh Engine: Clears UI and rebuilds from DB."""
        # 1. Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 2. Fetch from Backend
        transactions = self.controller.backend.fetch_today_transactions(self.current_view_date)
        
        # 3. Calculate Totals
        total_inc = 0.0
        total_exp = 0.0

        # 4. Render Rows
        # Row format from DB: (id, date, time, type, category, amount)
        for idx, txn in enumerate(transactions, start=1):
            db_id, date, time, t_type, category, amount = txn
            
            if t_type == "Profit":
                total_inc += amount
            else:
                total_exp += amount

            # Create Row
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2b2b2b", corner_radius=6)
            row_frame.pack(fill="x", pady=2)
            
            color = "#2ecc71" if t_type == "Profit" else "#e74c3c"
            
            # Visual Columns
            ctk.CTkLabel(row_frame, text=f"#{idx:02}", width=50, anchor="w", font=("Consolas", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=time, width=80, anchor="w", font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=t_type, width=100, anchor="w", text_color=color, font=("Arial", 14, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=category, width=200, anchor="w", font=("Arial", 14)).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=f"${amount:,.2f}", width=150, anchor="w", text_color=color, font=("Arial", 14, "bold")).pack(side="left", padx=5)
            
            # Delete Button (Passes DB ID, not Visual ID)
            del_btn = ctk.CTkButton(
                row_frame, text="X", width=40, height=30, fg_color="#c0392b", hover_color="#e74c3c",
                command=lambda tid=db_id: self.delete_transaction(tid)
            )
            del_btn.pack(side="left", padx=15)

        # 5. Update Dashboard
        self.lbl_total_income.configure(text=f"${total_inc:,.2f}")
        self.lbl_total_expense.configure(text=f"${total_exp:,.2f}")
        self.lbl_net_balance.configure(text=f"${total_inc - total_exp:,.2f}")

    def add_transaction(self):
        amount_str = self.amount_entry.get()
        t_type = self.type_dropdown.get()
        category = self.category_dropdown.get()
        
        # Validation
        if not category:
            messagebox.showwarning("Validation", "Category cannot be empty.")
            return
        if not amount_str or not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Invalid Amount.")
            return
        amount_float = float(amount_str)
        if amount_float <= 0:
            messagebox.showerror("Error", "Amount must be positive.")
            return

        # Time Logic
        current_time = datetime.now().strftime('%H:%M')

        # Send to Backend
        self.controller.backend.add_transaction(
            self.current_view_date, current_time, t_type, category, amount_float
        )

        # Clear Input & Refresh UI
        self.amount_entry.delete(0, 'end')
        
        # If user added a new category, update the dropdown list
        self.update_categories(t_type)
        self.category_dropdown.set(category) # Keep the one they just typed
        
        self.load_daily_data()

    def delete_transaction(self, db_id):
        if messagebox.askyesno("Confirm", "Delete this transaction?"):
            self.controller.backend.delete_transaction(db_id)
            self.load_daily_data()

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_report_df = None 
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
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(padx=30, fill="x")
        self.preview_label = ctk.CTkLabel(self.info_frame, text="Preview (Click any amount to edit/delete)", font=("Arial", 14, "italic"), text_color="gray")
        self.preview_label.pack(side="left")

        self.table_container = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.table_container.pack(padx=30, pady=10, fill="both", expand=True)

    def refresh_status(self):
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
        self.download_btn.configure(state="disabled")
        # Clear table immediately on selection change
        for widget in self.table_container.winfo_children():
            widget.destroy()

    def load_preview(self):
        # 1. Clear previous table (Fix for the lingering data bug)
        for widget in self.table_container.winfo_children():
            widget.destroy()

        if not self.selected_year_month or self.selected_year_month == "No Data":
            messagebox.showwarning("Warning", "No data available.")
            return

        year, month = map(int, self.selected_year_month.split('-'))
        df = self.controller.backend.get_monthly_pivot_data(year, month)
        
        # 2. Handle Empty Data Correctly
        if df is None or df.empty:
            ctk.CTkLabel(self.table_container, text="No transactions found for this month.", font=("Arial", 16)).pack(pady=20)
            self.download_btn.configure(state="disabled")
            return

        self.current_report_df = df
        self.render_preview_table(df)
        self.download_btn.configure(state="normal")

    def render_preview_table(self, df):
        df_reset = df.reset_index()
        columns = list(df_reset.columns)
        
        # Headers
        for col_idx, col_name in enumerate(columns):
            ctk.CTkLabel(
                self.table_container, text=str(col_name), 
                font=("Arial", 12, "bold"), fg_color="#444", corner_radius=4, width=100
            ).grid(row=0, column=col_idx, padx=2, pady=5, sticky="ew")

        # Data Rows
        for row_idx, row in enumerate(df_reset.itertuples(index=False), start=1):
            row_date = row[0] 

            for col_idx, value in enumerate(row):
                # Formatting
                display_text = f"{value}"
                is_amount = False
                if isinstance(value, (int, float)) and col_idx > 0:
                    display_text = f"{value:,.0f}" if value == 0 else f"{value:,.2f}"
                    is_amount = True
                
                # Colors
                text_color = "white"
                col_name = columns[col_idx]
                if "Total Income" in col_name: text_color = "#2ecc71"
                elif "Total Expense" in col_name: text_color = "#e74c3c"
                elif "Net Margin" in col_name: text_color = "#3498db"

                label = ctk.CTkLabel(
                    self.table_container, text=display_text, 
                    font=("Consolas", 12), text_color=text_color
                )
                label.grid(row=row_idx, column=col_idx, padx=5, pady=2)

                # Clickable Logic
                if is_amount and value != 0 and "Total" not in col_name and "Margin" not in col_name:
                    label.bind("<Enter>", lambda e, l=label: l.configure(text_color="#f1c40f", font=("Consolas", 12, "underline")))
                    label.bind("<Leave>", lambda e, l=label, c=text_color: l.configure(text_color=c, font=("Consolas", 12)))
                    label.bind("<Button-1>", lambda event, d=row_date, c=col_name: self.open_drill_down(d, c))

    def open_drill_down(self, date_str, category):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title(f"Edit: {category}")
        toplevel.geometry("500x400")
        toplevel.transient(self) 
        toplevel.grab_set()

        ctk.CTkLabel(toplevel, text=f"{category} ({date_str})", font=("Georgia", 20, "bold")).pack(pady=15)
        
        scroll = ctk.CTkScrollableFrame(toplevel)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        txns = self.controller.backend.fetch_transactions_for_cell(date_str, category)
        
        if not txns:
            ctk.CTkLabel(scroll, text="No records found.").pack(pady=20)
            return

        for txn in txns:
            tid, time, amount, t_type = txn
            row = ctk.CTkFrame(scroll, fg_color="#333")
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row, text=f"{time}", width=60).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"₹{amount:,.2f}", width=100, font=("Arial", 14, "bold")).pack(side="left", padx=5)
            
            ctk.CTkButton(
                row, text="Delete", width=60, fg_color="#c0392b", hover_color="#e74c3c",
                command=lambda i=tid, w=toplevel: self.delete_and_refresh(i, w)
            ).pack(side="right", padx=10, pady=5)

    def delete_and_refresh(self, txn_id, window):
        if messagebox.askyesno("Confirm", "Delete this transaction?"):
            self.controller.backend.delete_transaction(txn_id)
            window.destroy()
            # Force UI update so the "deleted" entry vanishes instantly
            self.load_preview() 
            messagebox.showinfo("Success", "Transaction deleted.")

    def download_excel(self):
        if self.current_report_df is None: return
        year, month = map(int, self.selected_year_month.split('-'))
        try:
            filename = self.controller.backend.save_report_to_excel(self.current_report_df, year, month)
            messagebox.showinfo("Success", f"File Downloaded Successfully:\n\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

            
if __name__ == "__main__":
    app = BusinessTrackerApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.on_closing()