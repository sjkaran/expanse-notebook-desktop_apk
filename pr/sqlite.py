import sqlite3 as sql

conn = sql.connect("finance.db")
cursor = conn.cursor()
print("connected successfuly")

def clear_all_data():
    cursor.execute('''DELETE FORM transactions''')
    conn.commit()

def clear_all_categories():
    cursor.execute('''DELETE FROME categories''')
    conn.commit()

