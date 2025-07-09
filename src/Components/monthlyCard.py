import flet as ft
from src.Config import theme

def MonthlyCard():
    th = theme.current_theme

    data = [
        {"month": "Jan", "consultas": 1250, "produtos": 89},
        {"month": "Fev", "consultas": 1180, "produtos": 94},
        {"month": "Mar", "consultas": 1420, "produtos": 102},
        {"month": "Abr", "consultas": 1680, "produtos": 118},
        {"month": "Mai", "consultas": 1590, "produtos": 125},
        {"month": "Jun", "consultas": 1820, "produtos": 142},
        {"month": "Jul", "consultas": 1950, "produtos": 156},
    ]

    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i, d["consultas"]) for i, d in enumerate(data)],
                color=th["PRIMARY_COLOR"],
                stroke_width=2,
                curved=True
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i, d["produtos"]) for i, d in enumerate(data)],
                color=th["TEXT_SECONDARY"],  # Use uma cor do tema para a segunda linha
                stroke_width=2,
                curved=True
            ),
        ],
        left_axis=ft.ChartAxis(labels_size=32),
        bottom_axis=ft.ChartAxis(
            labels=[ft.Text(d["month"], color=th["TEXT_SECONDARY"]) for d in data],
            labels_size=24
        ),
        height=300,
        expand=True
    )

    return ft.Container(
        bgcolor=th["CARD_DARK"],
        border=ft.border.all(1, th["BORDER"]),
        border_radius=12,
        padding=20,
        content=ft.Column([
            ft.Text("Consultas Mensais", size=18, weight="bold", color=th["TEXT"]),
            chart
        ], spacing=16)
    )