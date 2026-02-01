import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name ='finance.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connected(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.db_name}")

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE NOT NULL,
                            type TEXT NOT NULL,
                            color TEXT
                            )
                            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                descriprion TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id))
            ''')
        self.conn.commit()
        print("table created / varified")

        