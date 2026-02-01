import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend import BackendManager
import os
import ctypes


# --- System Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class BusinessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.backend = BackendManager()
        
        # --- Load Global Settings ---
        self.currency_symbol = self.backend.get_setting("currency") or "₹"
        # New: Load Business Name (Default to "My Business Dashboard" if not set)
        self.business_name = self.backend.get_setting("business_name") or "Daily Business Ledger"

        self.title("Visionary Business Suite v4.2")
        self.geometry("1280x850")

        icon_path = os.path.join(os.path.dirname(__file__),"icon.ico")

        #setting window icon
        try: 
            self.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"Warning: Could not load icon. {e}")
        
        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # App Logo (Static)
        self.logo = ctk.CTkLabel(self.sidebar, text="BIZ-TRACK", font=("Georgia", 26, "bold"), text_color="#2CC985")
        self.logo.grid(row=0, column=0, padx=20, pady=(40, 30))

        # Navigation Buttons
        self.nav_btns = {}
        nav_items = [
            ("Dashboard", "page1"),
            ("Analytics & Trends", "page_visuals"), 
            ("Reports & Export", "page2"),
            ("System Settings", "page_settings")
        ]
        
        for idx, (text, page) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar, 
                text=text, 
                height=50, 
                font=("Helvetica", 15, "bold"), 
                fg_color="transparent", 
                text_color=("gray90"),
                hover_color="#333",
                anchor="w",
                command=lambda p=page: self.show_frame(p)
            )
            btn.grid(row=idx+1, column=0, padx=20, pady=5, sticky="ew")
            self.nav_btns[page] = btn

        # --- Main Content Area ---
        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color="#222")
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.setup_frames()
        self.show_frame("page1")

    def setup_frames(self):
        for PageClass, name in [
            (TransactionPage, "page1"),
            (ReportsPage, "page2"),
            (VisualsPage, "page_visuals"),
            (SettingsPage, "page_settings")
        ]:
            frame = PageClass(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        for name, btn in self.nav_btns.items():
            if name == page_name:
                btn.configure(fg_color="#107a0c", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="gray90")
        
        if hasattr(frame, "refresh"):
            frame.refresh()

    def update_currency(self, new_symbol):
        self.currency_symbol = new_symbol
        self.backend.set_setting("currency", new_symbol)
        for f in self.frames.values():
            if hasattr(f, "refresh"): f.refresh()

    def update_business_name(self, new_name):
        self.business_name = new_name
        self.backend.set_setting("business_name", new_name)
        # Force refresh mainly on the Dashboard to show new name
        if "page1" in self.frames:
            self.frames["page1"].refresh()

    def on_closing(self):
        self.backend.close()  # 1. Save and close the database safely
        self.quit()           # 2. Stop the background scaling timers
        self.destroy()        # 3. Now actually destroy the window

# --- PAGE 1: TRANSACTION DASHBOARD ---
class TransactionPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_view_date = datetime.now().strftime("%Y-%m-%d")
        
        # --- Header Section ---
        self.head = ctk.CTkFrame(self, fg_color="transparent")
        self.head.pack(fill="x", padx=40, pady=(30, 20))
        
        # Title Left (Now Dynamic)
        self.title_label = ctk.CTkLabel(self.head, text=self.controller.business_name, font=("Georgia", 36, "bold"), text_color="#eee")
        self.title_label.pack(side="left")

        # Cards Right
        self.card_frame = ctk.CTkFrame(self.head, fg_color="transparent")
        self.card_frame.pack(side="right")
        self.lbl_inc = self.create_card("Total Income", "#2ecc71")
        self.lbl_exp = self.create_card("Total Expense", "#e74c3c")
        self.lbl_bal = self.create_card("Net Balance", "#3498db")

        # --- Input Section ---
        self.input_card = ctk.CTkFrame(self, fg_color="#2b2b2b", border_width=1, border_color="#444")
        self.input_card.pack(padx=40, pady=10, fill="x")
        self.input_card.grid_columnconfigure((0,1,2), weight=1)
        
        # Row 1 Inputs
        self.amount_entry = ctk.CTkEntry(self.input_card, placeholder_text="Amount", height=50, font=("Arial", 20, "bold"), border_color="#107a0c")
        self.amount_entry.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        
        self.type_menu = ctk.CTkOptionMenu(self.input_card, values=["Expense", "Profit"], command=self.update_cats, height=50, font=("Arial", 16, "bold"), fg_color="#444")
        self.type_menu.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
        
        self.cat_menu = ctk.CTkComboBox(self.input_card, values=[], height=50, font=("Arial", 16), dropdown_font=("Arial", 14))
        self.cat_menu.grid(row=0, column=2, padx=15, pady=20, sticky="ew")

        # Row 2 Inputs
        self.date_menu = ctk.CTkOptionMenu(self.input_card, values=["Today", "Select Date..."], command=self.handle_date, height=40, fg_color="#333")
        self.date_menu.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 20), sticky="ew")
        
        ctk.CTkButton(self.input_card, text="ADD ENTRY +", fg_color="#107a0c", hover_color="#0d630a", height=45, font=("Arial", 16, "bold"), command=self.add_txn).grid(row=1, column=2, padx=15, pady=(0, 20), sticky="ew")

        # --- Table Header ---
        self.table_head = ctk.CTkFrame(self, height=40, fg_color="#333", corner_radius=5)
        self.table_head.pack(padx=40, pady=(20, 0), fill="x")
        headers = [("Time", 100), ("Type", 120), ("Category", 250), ("Amount", 150), ("Action", 80)]
        for name, w in headers:
            ctk.CTkLabel(self.table_head, text=name, width=w, font=("Arial", 14, "bold"), anchor="w", text_color="#ccc").pack(side="left", padx=10)

        # --- Scrollable Table ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(padx=40, pady=(5, 30), fill="both", expand=True)

    def create_card(self, title, color):
        f = ctk.CTkFrame(self.card_frame, border_width=2, border_color=color, fg_color="#1a1a1a")
        f.pack(side="left", padx=10)
        ctk.CTkLabel(f, text=title, text_color="gray", font=("Arial", 13)).pack(padx=20, pady=(10,2))
        l = ctk.CTkLabel(f, text="0.00", text_color=color, font=("Arial", 22, "bold"))
        l.pack(padx=20, pady=(0,10))
        return l

    def refresh(self):
        # Update the Title to match the Settings
        self.title_label.configure(text=self.controller.business_name)
        self.update_cats(self.type_menu.get())
        self.load_data()

    def update_cats(self, choice):
        cats = self.controller.backend.get_categories(choice)
        self.cat_menu.configure(values=cats)
        if cats: self.cat_menu.set(cats[0])
        else: self.cat_menu.set("")

    def handle_date(self, val):
        if val == "Select Date...":
            d = ctk.CTkInputDialog(title="Date Selector", text="Enter Date (YYYY-MM-DD):").get_input()
            if d: 
                self.current_view_date = d
                self.date_menu.set(d)
            else:
                self.date_menu.set("Today")
        else:
            self.current_view_date = datetime.now().strftime("%Y-%m-%d")
        self.load_data()

    def load_data(self):
        for w in self.scroll.winfo_children(): w.destroy()
        txns = self.controller.backend.fetch_today_transactions(self.current_view_date)
        inc, exp = 0, 0
        sym = self.controller.currency_symbol

        for t in txns:
            tid, date, time, typ, cat, amt = t
            if typ == "Profit": inc += amt
            else: exp += amt
            
            row = ctk.CTkFrame(self.scroll, fg_color="#2b2b2b", corner_radius=6)
            row.pack(fill="x", pady=3)
            
            color = "#2ecc71" if typ == "Profit" else "#e74c3c"
            
            ctk.CTkLabel(row, text=time, width=100, font=("Consolas", 14), anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=typ, width=120, text_color=color, font=("Arial", 14, "bold"), anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=cat, width=250, font=("Arial", 14), anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{sym}{amt:,.2f}", width=150, text_color=color, font=("Arial", 14, "bold"), anchor="w").pack(side="left", padx=10)
            
            ctk.CTkButton(row, text="Delete", width=60, fg_color="#922b21", hover_color="#c0392b", height=30, 
                          command=lambda i=tid: self.del_txn(i)).pack(side="right", padx=15, pady=5)

        self.lbl_inc.configure(text=f"{sym}{inc:,.2f}")
        self.lbl_exp.configure(text=f"{sym}{exp:,.2f}")
        self.lbl_bal.configure(text=f"{sym}{inc-exp:,.2f}")

    def add_txn(self):
        try:
            amt_str = self.amount_entry.get()
            if not amt_str: return
            amt = float(amt_str)
            if amt <= 0: raise ValueError
            
            cat = self.cat_menu.get()
            if not cat: 
                messagebox.showerror("Error", "Category required")
                return

            self.controller.backend.add_transaction(
                self.current_view_date, datetime.now().strftime('%H:%M'),
                self.type_menu.get(), cat, amt
            )
            self.amount_entry.delete(0, 'end')
            self.refresh()
        except: messagebox.showerror("Error", "Invalid Amount")

    def del_txn(self, tid):
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?"):
            self.controller.backend.delete_transaction(tid)
            self.refresh()

# --- PAGE 2: REPORTS ---
class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_df = None
        self.cur_ym = None
        
        ctk.CTkLabel(self, text="Monthly Reports & Analytics", font=("Georgia", 32, "bold")).pack(pady=(30, 20))
        
        self.ctrl = ctk.CTkFrame(self, fg_color="#333", height=60)
        self.ctrl.pack(fill="x", padx=40, pady=(0, 20))
        
        ctk.CTkLabel(self.ctrl, text="Select Month:", font=("Arial", 14)).pack(side="left", padx=20)
        self.menu = ctk.CTkOptionMenu(self.ctrl, values=["No Data"], command=self.on_sel, width=180)
        self.menu.pack(side="left", padx=10, pady=15)
        
        ctk.CTkButton(self.ctrl, text="Load Preview", font=("Arial", 14, "bold"), fg_color="#3498db", width=150, command=self.load).pack(side="left", padx=20)
        self.dl_btn = ctk.CTkButton(self.ctrl, text="Download Excel", font=("Arial", 14, "bold"), fg_color="#27ae60", state="disabled", width=150, command=self.dl)
        self.dl_btn.pack(side="right", padx=20)
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.scroll.pack(fill="both", expand=True, padx=40, pady=10)

    def refresh(self):
        ms = self.controller.backend.get_available_months()
        if ms: 
            self.menu.configure(values=ms)
            self.menu.set(ms[0])
            self.cur_ym = ms[0]
        else: 
            self.menu.configure(values=["No Data"])
            self.menu.set("No Data")

    def on_sel(self, c): 
        self.cur_ym = c
        for w in self.scroll.winfo_children(): w.destroy()
        self.dl_btn.configure(state="disabled")
    
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        if not self.cur_ym or self.cur_ym == "No Data": return
        y, m = map(int, self.cur_ym.split('-'))
        df = self.controller.backend.get_monthly_pivot_data(y, m)
        if df is None or df.empty: 
            ctk.CTkLabel(self.scroll, text="No Data Available", font=("Arial", 16)).pack(pady=20)
            return
        
        self.current_df = df
        self.dl_btn.configure(state="normal")
        
        cols = list(df.reset_index().columns)
        for i, c in enumerate(cols):
            ctk.CTkLabel(self.scroll, text=str(c), font=("Arial",12,"bold"), fg_color="#444", width=100, corner_radius=4).grid(row=0, column=i, padx=2, pady=5, sticky="ew")
        
        for r_idx, row in enumerate(df.reset_index().itertuples(index=False), 1):
            date_val = row[0]
            for c_idx, val in enumerate(row):
                if isinstance(val, (int, float)) and c_idx > 0:
                    txt = f"{val:,.0f}" if val == 0 else f"{val:,.2f}"
                else:
                    txt = str(val)
                
                fg = "white"
                col_name = cols[c_idx]
                if "Total Income" in col_name: fg = "#2ecc71"
                elif "Total Expense" in col_name: fg = "#e74c3c"
                elif "Margin" in col_name: fg = "#3498db"

                lbl = ctk.CTkLabel(self.scroll, text=txt, font=("Consolas",12), text_color=fg)
                lbl.grid(row=r_idx, column=c_idx, padx=5, pady=2)
                
                if isinstance(val, (int,float)) and val!=0 and c_idx>0:
                    if "Total" not in col_name and "Margin" not in col_name:
                        lbl.bind("<Enter>", lambda e, l=lbl: l.configure(text_color="#f1c40f", font=("Consolas", 12, "underline")))
                        lbl.bind("<Leave>", lambda e, l=lbl, c=fg: l.configure(text_color=c, font=("Consolas", 12)))
                        lbl.bind("<Button-1>", lambda e, d=date_val, c=col_name: self.popup(d,c))

    def popup(self, d, c):
        top = ctk.CTkToplevel(self)
        top.title(f"Details: {c}")
        top.geometry("400x350")
        top.transient(self)
        top.grab_set()
        
        ctk.CTkLabel(top, text=f"{c} on {d}", font=("Georgia", 18, "bold")).pack(pady=10)
        sc = ctk.CTkScrollableFrame(top)
        sc.pack(fill="both", expand=True, padx=10, pady=10)
        
        txns = self.controller.backend.fetch_transactions_for_cell(d, c)
        for t in txns:
            tid, tim, amt, _ = t
            r = ctk.CTkFrame(sc, fg_color="#333")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=tim, width=60).pack(side="left", padx=5)
            ctk.CTkLabel(r, text=f"{amt:,.2f}", font=("Arial",14,"bold")).pack(side="left", padx=5)
            ctk.CTkButton(r, text="Delete", fg_color="#c0392b", width=60, command=lambda i=tid, w=top: self.del_refresh(i,w)).pack(side="right", padx=5, pady=5)

    def del_refresh(self, tid, w):
        self.controller.backend.delete_transaction(tid)
        w.destroy()
        self.load()
        messagebox.showinfo("Deleted", "Transaction removed from report.")

    def dl(self):
        if self.current_df is not None:
            # 1. Suggest a filename based on the selected month
            suggested_name = f"Monthly_Report_{self.cur_ym}.xlsx"
            
            # 2. Open the "Save As" Dialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=suggested_name,
                title="Save Report As"
            )
            
            # 3. If user clicked "Cancel", stop
            if not file_path:
                return

            # 4. Save to the chosen path
            try:
                fn = self.controller.backend.save_report_to_excel(self.current_df, file_path)
                messagebox.showinfo("Success", f"Report saved successfully at:\n{fn}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

# --- PAGE 3: VISUALS ---
class VisualsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        ctk.CTkLabel(self, text="Visual Analytics", font=("Georgia", 32, "bold")).pack(pady=(30, 20))
        
        self.ctrl = ctk.CTkFrame(self, fg_color="transparent")
        self.ctrl.pack(fill="x", padx=40)
        ctk.CTkLabel(self.ctrl, text="Select Month for Analysis:", font=("Arial", 14)).pack(side="left")
        self.menu = ctk.CTkOptionMenu(self.ctrl, values=["No Data"], command=self.load_charts, width=200)
        self.menu.pack(side="left", padx=20)
        
        self.chart_area = ctk.CTkScrollableFrame(self, fg_color="#2b2b2b")
        self.chart_area.pack(fill="both", expand=True, padx=40, pady=20)

    def refresh(self):
        ms = self.controller.backend.get_available_months()
        if ms:
            self.menu.configure(values=ms)
            self.menu.set(ms[0])
            self.load_charts(ms[0])
        else:
            self.menu.configure(values=["No Data"])
            self.menu.set("No Data")

    def load_charts(self, val):
        for w in self.chart_area.winfo_children(): w.destroy()
        if val == "No Data" or not val: return
        
        y, m = map(int, val.split('-'))
        
        # Pie Chart
        exp_data = self.controller.backend.fetch_category_breakdown(y, m, "Expense")
        if exp_data:
            fig, ax = plt.subplots(figsize=(7, 5), facecolor='#2b2b2b')
            wedges, texts, autotexts = ax.pie(exp_data.values(), labels=exp_data.keys(), autopct='%1.1f%%', startangle=90, textprops={'color':"white"})
            for t in texts: t.set_color("white")
            for t in autotexts: t.set_color("black")
            ax.set_title("Expense Breakdown", color="white", fontsize=14, pad=20)
            self.embed_chart(fig)

        # Bar Chart
        trend_df = self.controller.backend.fetch_daily_trends(y, m)
        if trend_df is not None:
            fig2, ax2 = plt.subplots(figsize=(9, 5), facecolor='#2b2b2b')
            ax2.set_facecolor('#2b2b2b')
            
            dates = [d[-2:] for d in trend_df.index] 
            ax2.bar(dates, trend_df['Profit'], color='#2ecc71', alpha=0.7, label='Income')
            ax2.bar(dates, -trend_df['Expense'], color='#e74c3c', alpha=0.7, label='Expense')
            
            ax2.axhline(0, color='white', linewidth=0.8)
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
            for spine in ax2.spines.values(): spine.set_color('#555')
            ax2.legend(facecolor='#333', labelcolor='white')
            ax2.set_title("Daily Cash Flow", color="white", fontsize=14, pad=20)
            self.embed_chart(fig2)

    def embed_chart(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=30)

# --- PAGE 4: SETTINGS (Updated with Business Name) ---
class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        ctk.CTkLabel(self, text="System Configuration", font=("Georgia", 32, "bold")).pack(pady=(30, 30))
        
        # Container
        self.main_box = ctk.CTkFrame(self, fg_color="transparent")
        self.main_box.pack(fill="both", expand=True, padx=100)

        # 1. Business Name Settings (New)
        biz_box = ctk.CTkFrame(self.main_box, fg_color="#2b2b2b", border_width=1, border_color="#444")
        biz_box.pack(fill="x", pady=10)
        ctk.CTkLabel(biz_box, text="Business Name", font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=20)
        self.biz_entry = ctk.CTkEntry(biz_box, width=250, font=("Arial", 16))
        self.biz_entry.insert(0, self.controller.business_name)
        self.biz_entry.pack(side="left", padx=10)
        ctk.CTkButton(biz_box, text="Save Name", command=self.save_name, fg_color="#3498db").pack(side="left", padx=20)

        # 2. Currency Settings
        curr_box = ctk.CTkFrame(self.main_box, fg_color="#2b2b2b", border_width=1, border_color="#444")
        curr_box.pack(fill="x", pady=10)
        ctk.CTkLabel(curr_box, text="Currency Symbol", font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=20)
        self.curr_entry = ctk.CTkEntry(curr_box, width=60, font=("Arial", 16))
        self.curr_entry.insert(0, self.controller.currency_symbol)
        self.curr_entry.pack(side="left", padx=10)
        ctk.CTkButton(curr_box, text="Save Symbol", command=self.save_curr, fg_color="#107a0c").pack(side="left", padx=20)

        # 3. Backup Settings
        bkp_box = ctk.CTkFrame(self.main_box, fg_color="#2b2b2b", border_width=1, border_color="#444")
        bkp_box.pack(fill="x", pady=10)
        ctk.CTkLabel(bkp_box, text="Data Protection", font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(bkp_box, text="Backup Database Now", command=self.backup, fg_color="#e67e22").pack(side="left", padx=10)

        # 4. Category Manager
        ctk.CTkLabel(self.main_box, text="Category Manager (Rename / Delete)", font=("Arial", 18, "bold"), anchor="w").pack(fill="x", pady=(30, 10))
        self.cat_scroll = ctk.CTkScrollableFrame(self.main_box, height=350, fg_color="#2b2b2b")
        self.cat_scroll.pack(fill="x")
        
    def refresh(self):
        # Refresh inputs in case they were changed externally
        self.biz_entry.delete(0, 'end')
        self.biz_entry.insert(0, self.controller.business_name)

        # Refresh Categories
        for w in self.cat_scroll.winfo_children(): w.destroy()
        
        exps = self.controller.backend.get_categories("Expense")
        profs = self.controller.backend.get_categories("Profit")
        
        for cat, typ in [(c, "Expense") for c in exps] + [(c, "Profit") for c in profs]:
            row = ctk.CTkFrame(self.cat_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            col = "#e74c3c" if typ == "Expense" else "#2ecc71"
            ctk.CTkLabel(row, text=f"[{typ}]", text_color=col, width=80, anchor="w", font=("Consolas", 12)).pack(side="left")
            
            ent = ctk.CTkEntry(row)
            ent.insert(0, cat)
            ent.pack(side="left", padx=10, fill="x", expand=True)
            
            ctk.CTkButton(row, text="Rename", width=70, fg_color="#3498db", 
                          command=lambda o=cat, n=ent, t=typ: self.rename(o, n.get(), t)).pack(side="left", padx=5)
            ctk.CTkButton(row, text="Remove", width=70, fg_color="#c0392b", 
                          command=lambda c=cat, t=typ: self.delete(c,t)).pack(side="right", padx=5)

    def save_name(self):
        new_name = self.biz_entry.get()
        if new_name:
            self.controller.update_business_name(new_name)
            messagebox.showinfo("Success", "Business name updated on Dashboard!")

    def save_curr(self):
        new_sym = self.curr_entry.get()
        self.controller.update_currency(new_sym)
        messagebox.showinfo("Success", "Currency symbol updated.")

    def backup(self):
        folder = filedialog.askdirectory()
        if folder:
            path = self.controller.backend.create_backup(folder)
            messagebox.showinfo("Backup Successful", f"Database saved to:\n{path}")

    def rename(self, old, new, typ):
        if old == new or not new: return
        self.controller.backend.rename_category(old, new, typ)
        self.refresh()
        messagebox.showinfo("Success", f"Renamed '{old}' to '{new}'")

    def delete(self, cat, typ):
        if messagebox.askyesno("Confirm Removal", f"Remove '{cat}' from future options?"):
            self.controller.backend.delete_category_from_list(cat, typ)
            self.refresh()

if __name__ == "__main__":
    app = BusinessTrackerApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.on_closing()