import flet as ft
from src.Config import theme

def ActionCard(page: ft.Page, title, description, icon_path, button_color, rota, features):
    hover_scale = ft.Scale(1)

    def on_hover(e):
        hover_scale.scale = 1.04 if e.data == "true" else 1
        page.update()

    def ir_para():
        page.go(rota)

    return ft.Container(
        width=350,
        height=350,
        margin=ft.margin.only(bottom=20),
        content=ft.Card(
            elevation=15,
            content=ft.Container(
                padding=32,
                bgcolor=theme.current_theme["CARD"],
                border_radius=16,
                scale=hover_scale,
                animate_scale=ft.Animation(300, curve="easeInOut"),
                on_hover=on_hover,
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(name=icon_path, size=48, color=button_color),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=12)
                    ),
                    ft.Text(title, size=18, weight="bold", color=theme.current_theme["TEXT"], text_align=ft.TextAlign.CENTER),
                    ft.Text(description, size=13, color=theme.current_theme["TEXT_SECONDARY"], text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(name="check_circle", size=16, color="#22c55e"),
                                ft.Text(f, size=12, color=theme.current_theme["TEXT_SECONDARY"])
                            ]) for f in features
                        ], spacing=6),
                        padding=ft.padding.symmetric(vertical=12)
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Acessar",
                            on_click=lambda _: ir_para(),
                            bgcolor=button_color,
                            color="white",
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=24, vertical=12),
                                shape=ft.RoundedRectangleBorder(radius=10),
                                text_style=ft.TextStyle(weight="bold", size=14)
                            ),
                            width=200
                        ),
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8)
            )
        )
    )