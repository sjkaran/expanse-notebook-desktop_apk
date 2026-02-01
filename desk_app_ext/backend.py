import sqlite3
import pandas as pd
from datetime import datetime
import os

class BackendManager:
    def __init__(self, db_name="business_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                name TEXT,
                type TEXT,
                PRIMARY KEY (name, type)
            )
        """)
        # Seed default categories if empty
        self.cursor.execute("SELECT count(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            defaults = [
                ("Fruits", "Expense"), ("Milk", "Expense"), ("Grocery", "Expense"),
                ("Ice-Cream", "Expense"), ("Rent", "Expense"), ("Employee Cost", "Expense"),
                ("Online Payments", "Profit"), ("Cash Payments", "Profit")
            ]
            self.cursor.executemany("INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)", defaults)
        self.conn.commit()

    # --- Core Transaction Methods ---
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
            print(f"Error adding transaction: {e}")
            return None

    def delete_transaction(self, txn_id):
        self.cursor.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        self.conn.commit()

    def fetch_today_transactions(self, date_str):
        self.cursor.execute("SELECT * FROM transactions WHERE date = ?", (date_str,))
        return self.cursor.fetchall()

    def get_categories(self, t_type):
        self.cursor.execute("SELECT name FROM categories WHERE type = ?", (t_type,))
        return [row[0] for row in self.cursor.fetchall()]

    # --- NEW: Historical Data Methods ---
    def get_available_months(self):
        """Returns a list of 'YYYY-MM' strings for months that have data."""
        self.cursor.execute("SELECT DISTINCT strftime('%Y-%m', date) FROM transactions ORDER BY date DESC")
        results = [row[0] for row in self.cursor.fetchall() if row[0] is not None]
        return results

    def get_monthly_pivot_data(self, year, month):
        """
        Generates the pivot table DataFrame but DOES NOT save it. 
        Returns the DataFrame for the UI to preview.
        """
        date_pattern = f"{year}-{month:02d}%"
        query = f"SELECT date, type, category, amount FROM transactions WHERE date LIKE '{date_pattern}'"
        df = pd.read_sql_query(query, self.conn)
        
        if df.empty:
            return None

        # Pivot Logic
        expense_df = df[df['type'] == 'Expense']
        income_df = df[df['type'] == 'Profit']

        if not expense_df.empty:
            pivot_expense = expense_df.pivot_table(index='date', columns='category', values='amount', aggfunc='sum', fill_value=0)
            pivot_expense['Total Expense'] = pivot_expense.sum(axis=1)
        else:
            pivot_expense = pd.DataFrame(columns=['Total Expense'])

        if not income_df.empty:
            pivot_income = income_df.pivot_table(index='date', columns='category', values='amount', aggfunc='sum', fill_value=0)
            pivot_income['Total Income'] = pivot_income.sum(axis=1)
        else:
            pivot_income = pd.DataFrame(columns=['Total Income'])

        # Merge
        final_df = pd.concat([pivot_expense, pivot_income], axis=1).fillna(0)
        
        # Calculate Margin
        total_inc = final_df['Total Income'] if 'Total Income' in final_df else 0
        total_exp = final_df['Total Expense'] if 'Total Expense' in final_df else 0
        final_df['Net Margin'] = total_inc - total_exp
        
        return final_df

    def save_report_to_excel(self, df, year, month):
        """Saves a given DataFrame to Excel."""
        filename = f"Monthly_Report_{year}_{month:02d}.xlsx"
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Daily Summary')
            worksheet = writer.sheets['Daily Summary']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2
        return filename

    def close(self):
        self.conn.close()