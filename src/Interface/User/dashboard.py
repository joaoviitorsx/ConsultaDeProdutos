import os
import flet as ft
from src.Config import theme
from src.Components.headerApp import HeaderApp
from src.Components.cardSection import DashboardCards, StatsCards
from src.Components.section import welcomeSection, titleSection, footer 

def DashboardPage(page: ft.Page):
    print("🟠 tela Dashboard carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    th = theme.current_theme

    def on_theme_change(novo_tema):
        nonlocal th
        th = theme.current_theme
        
        header_container.content = HeaderApp(
            page, 
            on_theme_changed=on_theme_change,
            mostrar_voltar=False,
            expand=False,
            mostrar_divider=True
        )
        
        update_dashboard_content()
        
        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]
        
        page.update()

    def update_dashboard_content():
        usuario_logado = page.client_storage.get("usuario_logado")
        if not usuario_logado:
            usuario_logado = "usuário"
        
        main_content.controls = [
            welcomeSection(usuario_logado, page),
        
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
        ]
        page.update()

    header_container = ft.Container(
        content=HeaderApp(
            page, 
            on_theme_changed=on_theme_change,
            mostrar_voltar=False,
            expand=False,
            mostrar_divider=True
        )
    )

    main_content = ft.Column([], spacing=0, expand=True)
    
    update_dashboard_content()

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Column([
                ft.Container(
                    content=header_container,
                    padding=ft.padding.symmetric(horizontal=24), 
                    width=None 
                ),
                ft.Container(
                    content=main_content, 
                    padding=ft.padding.symmetric(horizontal=24, vertical=16),
                    expand=True
                )
            ])
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )