"""
SOLUTION: Finance Tracker Mini Dashboard
Study this ONLY after you try yourself!
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Finance Tracker"
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_100
    
    # Sample data
    total_income = 5500
    total_expense = 3200
    balance = total_income - total_expense
    
    recent_transactions = [
        {"category": "Salary", "amount": 5000, "date": "Jan 20, 10:00 AM", "type": "income", "icon": ft.Icons.WORK},
        {"category": "Groceries", "amount": -150, "date": "Jan 19, 3:30 PM", "type": "expense", "icon": ft.Icons.SHOPPING_CART},
        {"category": "Transport", "amount": -30, "date": "Jan 19, 9:15 AM", "type": "expense", "icon": ft.Icons.DIRECTIONS_BUS},
        {"category": "Freelance", "amount": 500, "date": "Jan 18, 6:00 PM", "type": "income", "icon": ft.Icons.COMPUTER},
        {"category": "Restaurant", "amount": -85, "date": "Jan 17, 7:45 PM", "type": "expense", "icon": ft.Icons.RESTAURANT},
    ]
    
    # AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("Finance Tracker"),
        center_title=False,
        bgcolor=ft.Colors.BLUE,
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="January 2025"),
                    ft.PopupMenuItem(text="December 2024"),
                    ft.PopupMenuItem(text="November 2024"),
                ]
            ),
            ft.IconButton(ft.Icons.SETTINGS),
        ]
    )
    
    # Function to create summary card
    def create_summary_card(title, amount, icon, color, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color, size=30),
                    ft.Column([
                        ft.Text(title, size=12, color=ft.Colors.GREY_700),
                        ft.Text(f"${abs(amount):,.2f}", size=22, weight="bold", color=color),
                    ], spacing=0, expand=True),
                ], spacing=10),
                ft.Text("+12.5% from last month", size=10, color=ft.Colors.GREY_600),
            ], spacing=8),
            bgcolor=bg_color,
            border_radius=15,
            padding=15,
            expand=1,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 2),
            )
        )
    
    # Function to create transaction item
    def create_transaction_item(transaction):
        is_income = transaction["type"] == "income"
        amount_color = ft.Colors.GREEN_700 if is_income else ft.Colors.RED_700
        amount_sign = "+" if is_income else ""
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(transaction["icon"], size=20, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BLUE_400 if is_income else ft.Colors.ORANGE_400,
                    border_radius=10,
                    padding=10,
                ),
                ft.Column([
                    ft.Text(transaction["category"], size=15, weight="bold"),
                    ft.Text(transaction["date"], size=11, color=ft.Colors.GREY_600),
                ], spacing=2, expand=True),
                ft.Text(
                    f"{amount_sign}${abs(transaction['amount']):,.2f}",
                    size=16,
                    weight="bold",
                    color=amount_color
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.GREY_400,
                    icon_size=20,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=12,
            margin=8,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.GREY_200,
                offset=ft.Offset(0, 1),
            )
        )
    
    # Main content
    content = ft.Column([
        # Summary Cards
        ft.Container(
            content=ft.Row([
                create_summary_card("Income", total_income, ft.Icons.TRENDING_UP, ft.Colors.GREEN_700, ft.Colors.GREEN_50),
                create_summary_card("Expenses", total_expense, ft.Icons.TRENDING_DOWN, ft.Colors.RED_700, ft.Colors.RED_50),
                create_summary_card("Balance", balance, ft.Icons.ACCOUNT_BALANCE_WALLET, ft.Colors.BLUE_700, ft.Colors.BLUE_50),
            ], spacing=10),
            padding=20,
        ),
        
        # Recent Transactions
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Recent Transactions", size=20, weight="bold"),
                    ft.TextButton("View All →"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=5),
                
                # Transaction list
                ft.Column([
                    create_transaction_item(t) for t in recent_transactions
                ]),
            ]),
            padding=20,
        ),
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Floating Action Button
    fab = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda e: print("Add transaction"),
    )
    
    # Bottom Navigation
    def nav_change(e):
        print(f"Selected: {e.control.selected_index}")
    
    bottom_nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST, label="Transactions"),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Stats"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Settings"),
        ],
        on_change=nav_change,
    )
    
    page.add(content)
    page.floating_action_button = fab
    page.navigation_bar = bottom_nav

if __name__ == "__main__":
    ft.app(main)