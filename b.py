import flet as ft

def main(page: ft.Page):
    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 10),
                    ft.LineChartDataPoint(1, 20),
                    ft.LineChartDataPoint(2, 15),
                ],
                color="blue",
                stroke_width=2,
                curved=True
            )
        ],
        left_axis=ft.ChartAxis(labels=[ft.Text(str(y)) for y in range(0, 25, 5)], labels_size=32),
        bottom_axis=ft.ChartAxis(labels=[ft.Text(m) for m in ["Jan", "Fev", "Mar"]], labels_size=24),
        height=300,
        expand=True
    )
    page.add(chart)

ft.app(target=main)