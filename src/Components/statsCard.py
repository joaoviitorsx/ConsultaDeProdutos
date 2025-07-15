import flet as ft
from src.Config import theme

def StatsCard(title, value, icon_name, trend=None, trend_up=True):
    th = theme.get_theme()

    trend_color = th["PRIMARY_COLOR"] if trend_up else th["ERROR"]
    trend_icon = ft.Icon(name="trending_up" if trend_up else "trending_down", size=16, color=trend_color)

    return ft.Container(
        bgcolor=th["CARD"],  # Usa a cor correta do card do theme
        border=ft.border.all(1, th["BORDER"]),
        border_radius=theme.STYLE["CARD_RADIUS"],
        padding=20,
        width=220,
        content=ft.Column([
            ft.Row([
                ft.Text(title, size=14, color=th["TEXT_SECONDARY"], weight="bold"),
                ft.Container(
                    ft.Icon(name=icon_name, color=th["PRIMARY_COLOR"], size=24),
                    padding=ft.padding.only(left=8)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),

            ft.Text(value, size=28, weight="bold", color=th["TEXT"]),

            ft.Row([
                ft.Text(trend or "", size=12, color=trend_color, weight="bold"),
                trend_icon,
                ft.Text(" desde o mês passado", size=12, color=th["TEXT_SECONDARY"])
            ], spacing=4) if trend else ft.Container()
        ], spacing=10)
    )