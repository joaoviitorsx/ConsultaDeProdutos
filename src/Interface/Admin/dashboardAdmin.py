import flet as ft
from src.Config import theme
from src.Components.section import footer
from src.Components.statsCard import StatsCard
from src.Components.adminLayout import AdminLayout
from src.Components.monthlyCard import MonthlyCard
from src.Components.activityCard import ActivityCard

def AdminDashboardContent(page):
    th = theme.current_theme

    stats_cards = [
        StatsCard(
            "Total Fornecedores", "1.284",
            ft.Icon(name="business", color="#E53935", size=24),
            trend="+12%", trend_up=True
        ),
        StatsCard(
            "Produtos Cadastrados", "8.459",
            ft.Icon(name="inventory_2", color="#E53935", size=24),
            trend="+8%", trend_up=True
        ),
        StatsCard(
            "Usuários Ativos", "23",
            ft.Icon(name="group", color="#E53935", size=24),
            trend="+2", trend_up=True
        ),
        StatsCard(
            "Consultas Hoje", "156",
            ft.Icon(name="trending_up", color="#E53935", size=24),
            trend="-3%", trend_up=False
        ),
    ]

    return ft.Column(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(card, col={"sm": 12, "md": 6, "lg": 3}, padding=8)
                    for card in stats_cards
                ],
                run_spacing=8,
                spacing=8
            ),
            ft.Container(height=32),
            ft.ResponsiveRow(
                controls=[
                    ft.Container(MonthlyCard(), col={"sm": 12, "md": 6}, padding=8),
                    ft.Container(ActivityCard(), col={"sm": 12, "md": 6}, padding=8),
                ],
                run_spacing=8,
                spacing=8
            ),
        ],
        expand=True,
        spacing=16
    )

def DashboardPage(page: ft.Page):
    print("🛠️ Tela Admin Dashboard carregada")
    th = theme.current_theme
    main_content = AdminDashboardContent(page)
    return ft.View(
        route="/admin_dashboard",
        controls=[
            AdminLayout(page, main_content, selected_route="/admin_dashboard")
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )