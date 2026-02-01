import sqlite3
from datetime import datetime

# Step 1: Connect to database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Step 2: Create categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        color TEXT
    )
''')

# Step 3: Create transactions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
''')

# Step 4: Insert sample categories
categories = [
    ('raw material', 'expense', '#FF6B6B'),
    ('extra cost', 'expense', '#FFD93D'),
    ('fruit', 'expense', '#6BCB77'),
    ('sales', 'income', '#4D96FF')
]

for name, cat_type, color in categories:
    try:
        cursor.execute('''
            INSERT INTO categories (name, type, color)
            VALUES (?, ?, ?)
        ''', (name, cat_type, color))
    except sqlite3.IntegrityError:
        # Category already exists, skip
        pass

# Step 5: Insert sample transactions
transactions = [
    (1, 500, '2025-10-09', 'none'),
    (2, 150, '2025-10-09', 'office supplies'),
    (3, 300, '2025-10-09', 'none'),
    (4, 1000, '2025-10-09', 'cash')
]

for cat_id, amount, date, desc in transactions:
    cursor.execute('''
        INSERT INTO transactions (category_id, amount, date, description)
        VALUES (?, ?, ?, ?)
    ''', (cat_id, amount, date, desc))

# Commit changes
conn.commit()

print("✅ Database created and populated!")

# Step 6: Read and display data
print("\n" + "="*60)
print("ALL TRANSACTIONS WITH CATEGORIES")
print("="*60)

cursor.execute('''
    SELECT 
        t.id,
        c.name as category,
        c.type,
        t.amount,
        t.date
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
''')

rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Category: {row[1]}, Type: {row[2]}, Amount: {row[3]}, Date: {row[4]}")

# Step 7: Calculate totals
print("\n" + "="*60)
print("FINANCIAL SUMMARY")
print("="*60)

cursor.execute('''
    SELECT SUM(t.amount)
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    WHERE c.type = 'income'
''')
total_income = cursor.fetchone()[0] or 0

cursor.execute('''
    SELECT SUM(t.amount)
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    WHERE c.type = 'expense'
''')
total_expenses = cursor.fetchone()[0] or 0

profit = total_income - total_expenses

print(f"Total Income:    ${total_income:,.2f}")
print(f"Total Expenses:  ${total_expenses:,.2f}")
print(f"Profit:          ${profit:,.2f}")

# Step 8: Close connection
conn.close()
print("\n✅ Database closed!")