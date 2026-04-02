import sqlite3
import shutil
from datetime import datetime
import os

class BackendManager:
    def __init__(self, db_name="business_data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        # 1. Transactions Ledger
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        # 2. Categories
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT,
                type TEXT,
                PRIMARY KEY (name, type)
            )
        """)
        # 3. Settings (New for v4.0)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        # Seed Defaults
        self.cursor.execute("SELECT count(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            defaults = [
                ("Fruits", "Expense"), ("Milk", "Expense"), ("Grocery", "Expense"),
                ("Online Payments", "Profit"), ("Cash Payments", "Profit")
            ]
            self.cursor.executemany("INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)", defaults)
        
        # Seed Currency
        self.cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('currency', '₹')")
        self.conn.commit()

    # --- Core Transactions ---
    def add_transaction(self, date, time, t_type, category, amount):
        try:
            self.cursor.execute("""
                INSERT INTO transactions (date, time, type, category, amount)
                VALUES (?, ?, ?, ?, ?)
            """, (date, time, t_type, category, amount))
            self.cursor.execute("INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)", (category, t_type))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return None

    def delete_transaction(self, txn_id):
        self.cursor.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        self.conn.commit()

    def update_transaction_amount(self, txn_id, new_amount):
        """Updates the amount of an existing transaction."""
        self.cursor.execute("UPDATE transactions SET amount = ? WHERE id = ?", (new_amount, txn_id))
        self.conn.commit()

    def fetch_today_transactions(self, date_str):
        import pandas as pd
        self.cursor.execute("SELECT * FROM transactions WHERE date = ?", (date_str,))
        return self.cursor.fetchall()

    def get_categories(self, t_type):
        self.cursor.execute("SELECT name FROM categories WHERE type = ?", (t_type,))
        return [row[0] for row in self.cursor.fetchall()]

    # --- Analytics Engine (Track A) ---
    def fetch_category_breakdown(self, year, month, t_type):
        """Returns {'Category': Amount} for Pie Charts."""
        date_pattern = f"{year}-{month:02d}%"
        self.cursor.execute("""
            SELECT category, SUM(amount) FROM transactions 
            WHERE date LIKE ? AND type = ? 
            GROUP BY category
        """, (date_pattern, t_type))
        return dict(self.cursor.fetchall())

    def fetch_daily_trends(self, year, month):
        import pandas as pd
        """Returns DataFrame of Daily Income vs Expense for Bar Charts."""
        date_pattern = f"{year}-{month:02d}%"
        query = f"SELECT date, type, amount FROM transactions WHERE date LIKE '{date_pattern}'"
        df = pd.read_sql_query(query, self.conn)
        
        if df.empty: return None

        # Pivot to get Date | Expense | Profit
        pivot = df.pivot_table(index='date', columns='type', values='amount', aggfunc='sum', fill_value=0)
        
        # Ensure both columns exist even if one is missing data
        if 'Expense' not in pivot.columns: pivot['Expense'] = 0
        if 'Profit' not in pivot.columns: pivot['Profit'] = 0
        
        return pivot

    # --- Settings & Maintenance (Track B) ---
    def get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        res = self.cursor.fetchone()
        return res[0] if res else None

    def set_setting(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def rename_category(self, old_name, new_name, t_type):
        # 1. Update the Category List
        self.cursor.execute("UPDATE categories SET name = ? WHERE name = ? AND type = ?", (new_name, old_name, t_type))
        # 2. Update Historical Transactions (So reports don't break)
        self.cursor.execute("UPDATE transactions SET category = ? WHERE category = ? AND type = ?", (new_name, old_name, t_type))
        self.conn.commit()

    def delete_category_from_list(self, name, t_type):
        # Only removes from the dropdown options, NOT historical data
        self.cursor.execute("DELETE FROM categories WHERE name = ? AND type = ?", (name, t_type))
        self.conn.commit()

    def create_backup(self, dest_folder):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Backup_BusinessData_{timestamp}.db"
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy2(self.db_name, dest_path)
        return dest_path

    # --- Excel Export (Preserved) ---
    def get_available_months(self):
        self.cursor.execute("SELECT DISTINCT strftime('%Y-%m', date) FROM transactions ORDER BY date DESC")
        return [row[0] for row in self.cursor.fetchall() if row[0]]

    def get_monthly_pivot_data(self, year, month):
        import pandas as pd
        # (Same logic as before - abbreviated for brevity, but needed)
        date_pattern = f"{year}-{month:02d}%"
        query = f"SELECT date, type, category, amount FROM transactions WHERE date LIKE '{date_pattern}'"
        df = pd.read_sql_query(query, self.conn)
        if df.empty: return None
        
        exp = df[df['type'] == 'Expense']
        inc = df[df['type'] == 'Profit']

        p_exp = exp.pivot_table(index='date', columns='category', values='amount', aggfunc='sum', fill_value=0) if not exp.empty else pd.DataFrame(columns=['Total Expense'])
        if not exp.empty: p_exp['Total Expense'] = p_exp.sum(axis=1)

        p_inc = inc.pivot_table(index='date', columns='category', values='amount', aggfunc='sum', fill_value=0) if not inc.empty else pd.DataFrame(columns=['Total Income'])
        if not inc.empty: p_inc['Total Income'] = p_inc.sum(axis=1)

        final = pd.concat([p_exp, p_inc], axis=1).fillna(0)
        final['Net Margin'] = (final['Total Income'] if 'Total Income' in final else 0) - (final['Total Expense'] if 'Total Expense' in final else 0)
        return final

    def save_report_to_excel(self, df, file_path):
        import pandas as pd
        """
        Saves the dataframe to the specific path chosen by the user.
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Summary')
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Summary']
                for column_cells in worksheet.columns:
                    length = max(len(str(cell.value)) for cell in column_cells)
                    worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2
            return file_path
        except Exception as e:
            raise e

    def fetch_transactions_for_cell(self, date, cat):
        self.cursor.execute("SELECT id, time, amount, type FROM transactions WHERE date = ? AND category = ?", (date, cat))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()