import os
import json
import flet as ft
from src.Config import theme
from src.Components.headerApp import HeaderApp
from src.Components.cardSection import DashboardCards
from src.Components.section import welcomeSection, titleSection, footer

def DashboardPage(page: ft.Page, usuario_info=None):
    print("🟠 Tela Dashboard carregada")

    th = theme.apply_theme(page)

    if usuario_info:
        page.usuario_info = usuario_info
        if isinstance(usuario_info, dict) and usuario_info.get("empresa_id"):
            page.selected_empresa_id = usuario_info.get("empresa_id")

    header_container = ft.Container()
    main_content = ft.Column([], spacing=0, expand=True)

    def onThemeChange(novo_tema):
        theme.set_theme(novo_tema)
        th = theme.get_theme()

        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]

        header_container.content = HeaderApp(
            page,
            on_theme_changed=onThemeChange,
            mostrar_voltar=False,
            expand=False,
            mostrar_divider=False
        )

        updateDashboardContent()
        page.update()

    def updateDashboardContent():
        usuario = getattr(page, "usuario_info", {"nome": "usuário"})
        main_content.controls.clear()
        main_content.controls.extend([
            welcomeSection(usuario, page),
            ft.Container(height=40),
            titleSection("Módulos Disponíveis", "Acesse as funcionalidades do sistema"),
            DashboardCards(
                page,
                estilo="horizontal",
                animacao=True,
                spacing=24,
                run_spacing=24,
                padding_card=8,
                border_radius=16,
                altura_customizada=180
            ),
            ft.Container(height=40),
            footer()
        ])
        page.update()

    header_container.content = HeaderApp(
        page,
        on_theme_changed=onThemeChange,
        mostrar_voltar=False,
        expand=False,
        mostrar_divider=False
    )

    updateDashboardContent()

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Column([
                ft.Container(
                    content=header_container,
                    padding=ft.padding.symmetric(horizontal=24)
                ),
                ft.Container(
                    content=main_content,
                    padding=ft.padding.symmetric(horizontal=24, vertical=16),
                    expand=True
                )
            ])
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=theme.get_theme()["BACKGROUNDSCREEN"]
    )
