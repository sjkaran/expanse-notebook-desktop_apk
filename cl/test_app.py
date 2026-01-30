from cl.database_manager import DatabaseManager

# Initialize database
db = DatabaseManager('finance.db')

# Add some categories
print("\n" + "="*60)
print("ADDING CATEGORIES")
print("="*60)
db.add_category('raw material', 'expense', '#FF6B6B')
db.add_category('extra cost', 'expense', '#FFD93D')
db.add_category('fruit', 'expense', '#6BCB77')
db.add_category('sales', 'income', '#4D96FF')

# Add transactions
print("\n" + "="*60)
print("ADDING TRANSACTIONS")
print("="*60)
db.add_transaction(1, 500, '2025-10-09', 'none')
db.add_transaction(2, 150, '2025-10-09', 'office supplies')
db.add_transaction(3, 300, '2025-10-09', 'none')
db.add_transaction(4, 1000, '2025-10-09', 'cash')

# Display all transactions
print("\n" + "="*60)
print("ALL TRANSACTIONS")
print("="*60)
transactions = db.get_all_transactions()
for t in transactions:
    print(f"ID: {t[0]}, {t[1]} ({t[2]}): ${t[3]} - {t[4]} - {t[5]}")

# Display financial summary
print("\n" + "="*60)
print("FINANCIAL SUMMARY")
print("="*60)
print(f"Total Income:    ${db.get_total_income():,.2f}")
print(f"Total Expenses:  ${db.get_total_expenses():,.2f}")
print(f"Profit:          ${db.get_profit():,.2f}")

# Expenses by category
print("\n" + "="*60)
print("EXPENSES BY CATEGORY")
print("="*60)
for expense in db.get_expense_by_category():
    print(f"{expense[0]}: ${expense[1]} ({expense[2]} transactions)")

# Income by category
print("\n" + "="*60)
print("INCOME BY CATEGORY")
print("="*60)
for income in db.get_income_by_category():
    print(f"{income[0]}: ${income[1]} ({income[2]} transactions)")

# Test update
print("\n" + "="*60)
print("UPDATING TRANSACTION")
print("="*60)
db.update_transaction(1, amount=550)  # Update first transaction amount

# Verify update
print("\n" + "="*60)
print("ALL TRANSACTIONS AFTER UPDATE")
print("="*60)
transactions = db.get_all_transactions()
for t in transactions:
    print(f"ID: {t[0]}, {t[1]} ({t[2]}): ${t[3]} - {t[4]} - {t[5]}")

# Test delete
print("\n" + "="*60)
print("DELETING TRANSACTION")
print("="*60)
db.delete_transaction(3)  # Delete fruit transaction

# Final count
print("\n" + "="*60)
print("FINAL FINANCIAL SUMMARY")
print("="*60)
print(f"Total Income:    ${db.get_total_income():,.2f}")
print(f"Total Expenses:  ${db.get_total_expenses():,.2f}")
print(f"Profit:          ${db.get_profit():,.2f}")

# Close database
db.close()