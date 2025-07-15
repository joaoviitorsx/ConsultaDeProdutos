import flet as ft
from src.Config import theme

def MonthlyCard():
    th = theme.get_theme()

    # Dados simulados
    data = [
        {"month": "Jan", "consultas": 1200, "produtos": 80},
        {"month": "Fev", "consultas": 1350, "produtos": 90},
        {"month": "Mar", "consultas": 1100, "produtos": 100},
        {"month": "Abr", "consultas": 1600, "produtos": 120},
        {"month": "Mai", "consultas": 1700, "produtos": 130},
        {"month": "Jun", "consultas": 1800, "produtos": 140},
        {"month": "Jul", "consultas": 2000, "produtos": 160},
    ]

    # Grupos de barras (um par de barras por mês)
    bar_groups = []
    for i, d in enumerate(data):
        bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        to_y=d["consultas"],
                        color=th["PRIMARY_COLOR"],
                        width=10,
                    ),
                    ft.BarChartRod(
                        to_y=d["produtos"] * 10,  # escala só para visualização
                        color=th["PRIMARY_HOVER"],
                        width=10,
                    ),
                ],
                bars_space=4
            )
        )

    chart = ft.BarChart(
        bar_groups=bar_groups,
        max_y=2200,
        border=ft.border.all(1, th["BORDER"]),
        left_axis=ft.ChartAxis(
            title=ft.Text("Consultas", size=12, color=th["TEXT_SECONDARY"]),
            labels=[
                ft.Text(str(y), size=10, color=th["TEXT_SECONDARY"])
                for y in range(0, 2500, 500)
            ],
            labels_size=32
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.Text(d["month"], size=10, color=th["TEXT_SECONDARY"]) for d in data
            ],
            labels_size=28
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color=th["TEXT_SECONDARY"] + "33"
        ),
        vertical_grid_lines=ft.ChartGridLines(
            color="transparent"
        ),
        tooltip_bgcolor=th["CARD"],
        height=300,
        width=550
    )

    legenda = ft.Row([
        ft.Row([
            ft.Container(width=10, height=10, bgcolor=th["PRIMARY_COLOR"], border_radius=5),
            ft.Text("Consultas", size=12, color=th["TEXT"])
        ], spacing=6),
        ft.Row([
            ft.Container(width=10, height=10, bgcolor=th["PRIMARY_HOVER"], border_radius=5),
            ft.Text("Produtos", size=12, color=th["TEXT"])
        ], spacing=6),
    ], spacing=20)

    return ft.Container(
        bgcolor=th["CARD"],
        border=ft.border.all(1, th["BORDER"]),
        border_radius=theme.STYLE["CARD_RADIUS"],
        padding=20,
        content=ft.Column([
            ft.Text("Consultas Mensais", size=18, weight="bold", color=th["TEXT"]),
            chart,
            legenda
        ], spacing=16)
    )
