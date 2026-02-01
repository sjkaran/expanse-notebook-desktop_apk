import flet as ft
import datetime

def main(page: ft.Page):
    # --- 1. SETUP & THEME ---
    page.title = "Finance Tracker"
    page.padding = 20
    page.bgcolor = ft.Colors.GREY_50
    page.scroll = ft.ScrollMode.HIDDEN # We handle scrolling inside the list
    
    # Define our "Pro" Color Palette
    COLOR_INCOME = ft.Colors.GREEN_600
    COLOR_EXPENSE = ft.Colors.RED_500
    COLOR_BALANCE = ft.Colors.BLUE_700
    COLOR_TEXT_MAIN = ft.Colors.BLUE_GREY_900

    # --- 2. DATA (State) ---
    transactions = [
        {"id": 1, "category": "Salary", "amount": 5000.00, "date": "Jan 20", "icon": ft.Icons.WORK, "type": "income"},
        {"id": 2, "category": "Groceries", "amount": 150.00, "date": "Jan 19", "icon": ft.Icons.LOCAL_GROCERY_STORE, "type": "expense"},
        {"id": 3, "category": "Transport", "amount": 30.00, "date": "Jan 19", "icon": ft.Icons.DIRECTIONS_BUS, "type": "expense"},
        {"id": 4, "category": "Freelance", "amount": 500.00, "date": "Jan 18", "icon": ft.Icons.LAPTOP, "type": "income"},
        {"id": 5, "category": "Restaurant", "amount": 85.00, "date": "Jan 17", "icon": ft.Icons.RESTAURANT, "type": "expense"},
    ]

    # --- 3. UI CONTROLS (Placeholder Variables) ---
    # We define these outside so we can update them in functions
    text_income = ft.Text("$0", size=18, weight="bold", color=COLOR_INCOME)
    text_expense = ft.Text("$0", size=18, weight="bold", color=COLOR_EXPENSE)
    text_balance = ft.Text("$0", size=26, weight="bold", color=ft.Colors.WHITE)
    
    transaction_list_col = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    # --- 4. LOGIC FUNCTIONS ---
    
    def delete_transaction(e, item_id):
        # Filter out the item with this ID
        # (We use [:] to modify the list in place so global reference keeps working)
        item_to_remove = next((x for x in transactions if x["id"] == item_id), None)
        if item_to_remove:
            transactions.remove(item_to_remove)
            update_dashboard()
            page.show_dialog(ft.SnackBar(ft.Text("Transaction deleted"), bgcolor=ft.Colors.GREY_800))

    def update_dashboard():
        # A. Calculate Totals
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        balance = total_income - total_expense

        # B. Update Text
        text_income.value = f"${total_income:,.0f}"
        text_expense.value = f"${total_expense:,.0f}"
        text_balance.value = f"${balance:,.2f}"

        # C. Render Transactions List
        transaction_list_col.controls.clear()
        
        for t in transactions:
            is_income = t["type"] == "income"
            amount_color = COLOR_INCOME if is_income else COLOR_EXPENSE
            amount_prefix = "+" if is_income else "-"
            
            # Create the card
            item_card = ft.Container(
                content=ft.Row([
                    # Icon Box
                    ft.Container(
                        content=ft.Icon(t["icon"], color=ft.Colors.WHITE, size=20),
                        width=45, height=45,
                        border_radius=12,
                        bgcolor=COLOR_INCOME if is_income else COLOR_EXPENSE,
                        alignment=ft.Alignment.CENTER
                    ),
                    # Text Info
                    ft.Column([
                        ft.Text(t["category"], weight="bold", size=15, color=COLOR_TEXT_MAIN),
                        ft.Text(t["date"], size=12, color=ft.Colors.GREY_500),
                    ], spacing=2, expand=True),
                    # Amount & Delete
                    ft.Column([
                        ft.Text(f"{amount_prefix}${t['amount']}", weight="bold", size=15, color=amount_color),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.IconButton(
                        ft.Icons.DELETE_OUTLINE, 
                        icon_color=ft.Colors.GREY_400,
                        icon_size=20,
                        on_click=lambda e, x=t["id"]: delete_transaction(e, x)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=12,
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.5,ft.Colors.BLACK_12))
            )
            transaction_list_col.controls.append(item_card)
        
        page.update()

    def show_quick_actions(e):
        # Create a BottomSheet for "Add Income/Expense"
        bs = ft.BottomSheet(
            ft.Container(
                ft.Column([
                    ft.Text("Quick Actions", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
                    ft.Divider(),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ARROW_UPWARD, color=COLOR_INCOME), title=ft.Text("Add Income"), on_click=lambda e: setattr(bs, 'open', False) or page.update()),
                    ft.ListTile(leading=ft.Icon(ft.Icons.ARROW_DOWNWARD, color=COLOR_EXPENSE), title=ft.Text("Add Expense"), on_click=lambda e: setattr(bs, 'open', False) or page.update()),
                ], tight=True),
                padding=20,
            )
        )
        page.show_dialog(bs)

    # --- 5. BUILD UI COMPONENTS ---

    # Helper to make the top Summary Cards
    def make_summary_card(title, value_control, icon, color, bg_color=ft.Colors.WHITE, is_main=False):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color if not is_main else ft.Colors.WHITE, size=16),
                    ft.Text(title, size=12, color=ft.Colors.GREY_500 if not is_main else ft.Colors.WHITE_70)
                ], spacing=5),
                value_control,
            ], spacing=5),
            padding=15,
            bgcolor=bg_color,
            border_radius=15,
            expand=1,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLUE_GREY_100)
        )

    # AppBar Custom Row
    header = ft.Row([
        ft.Column([
            ft.Text("Welcome Back,", size=12, color=ft.Colors.GREY_500),
            ft.Text("Zero1 Finance", size=22, weight="bold", color=COLOR_TEXT_MAIN)
        ], spacing=2),
        ft.Container(
            content=ft.Row([
                ft.Text("Jan 2025", size=13, weight="bold"),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, size=18)
            ]),
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=20,
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Summary Section
    summary_row = ft.Row([
        # Income Card
        make_summary_card("Income", text_income, ft.Icons.ARROW_UPWARD, COLOR_INCOME),
        # Expense Card
        make_summary_card("Expense", text_expense, ft.Icons.ARROW_DOWNWARD, COLOR_EXPENSE),
    ])
    
    # Main Balance Card (Full Width)
    balance_card = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text("Total Balance", color=ft.Colors.WHITE_70),
                text_balance
            ]),
            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color=ft.Colors.WHITE, size=40, opacity=0.8)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=25,
        border_radius=20,
        gradient=ft.LinearGradient(colors=[ft.Colors.BLUE_700, ft.Colors.BLUE_500]),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLUE_200, offset=ft.Offset(0, 5))
    )

    # --- 6. FINAL PAGE ASSEMBLY ---
    
    page.add(
        ft.Column([
            # Top Section
            ft.Container(header, padding=ft.Padding.only(bottom=15)),
            
            balance_card,
            ft.Container(height=10),
            summary_row,
            
            ft.Container(height=15),
            
            # Transactions Title
            ft.Row([
                ft.Text("Recent Transactions", size=18, weight="bold", color=COLOR_TEXT_MAIN),
                ft.Text("View All", size=13, color=ft.Colors.BLUE_600, weight="bold"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(height=5),
            
            # The List
            ft.Container(
                content=transaction_list_col,
                expand=True # Lets the list take remaining space
            )
        ], expand=True)
    )

    # Floating Action Button
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.BLACK,
        on_click=show_quick_actions
    )
    # Centered in the dock
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    # Bottom Navigation
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.PIE_CHART, label="Stats"),
            # Placeholder for the middle FAB gap
            ft.NavigationBarDestination(icon=ft.Icons.WALLET, label="Wallet"), 
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Settings"),
        ],
        border=ft.Border(top=ft.BorderSide(1, ft.Colors.GREY_200)),
        height=65,
        elevation=0,
        bgcolor=ft.Colors.WHITE
    )

    # Init
    update_dashboard()

if __name__ == "__main__":
    ft.run(main)