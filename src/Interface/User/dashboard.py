import os
import flet as ft
from src.Config import theme
from src.Components.trocaTema import ThemeToggle
from src.Components.cardAction import ActionCard

def DashboardPage(page: ft.Page):
    print("🟠 tela Dashboard carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    usuario = page.client_storage.get("usuario_logado") or "usuário"
    th = theme.current_theme

    def ir_para(route):
        page.go(route)

    def logout(e):
        page.go("/login")

    header_container = ft.Container()
    bodyColumn = ft.Column()

    def buildCards():
        th = theme.current_theme
        return ft.Row(
            controls=[
                ActionCard(
                    page,
                    "Consultar Fornecedor",
                    "Dados cadastrais, situação fiscal e isenções",
                    "business_center",
                    th["PRIMARY_COLOR"],
                    "/consulta_fornecedor",
                    ["Dados cadastrais", "Situação fiscal", "Status de isenção"]
                ),
                ActionCard(
                    page,
                    "Relatórios Mensais",
                    "Exportação de dados e filtros por período",
                    "assessment",
                    "#00C897",
                    "/relatorios",
                    ["Histórico de consultas", "Exportação em PDF", "Filtros por período"]
                ),
                ActionCard(
                    page,
                    "Consultar Produtos",
                    "Cálculo de impostos e comparação",
                    "inventory",
                    "#F03E3E",
                    "/consulta_produtos",
                    ["Cálculo de impostos", "Preços finais", "Comparação entre fornecedores"]
                ),
            ],
            spacing=16,
            run_spacing=16,
            alignment=ft.MainAxisAlignment.CENTER
        )

    def on_theme_change(novo_tema):
        th = theme.current_theme

        header_container.bgcolor = th["CARD"]

        for control in header_container.content.controls:
            if isinstance(control, ft.Row):
                for item in control.controls:
                    if isinstance(item, ft.Text):
                        item.color = th["TEXT"]
                    elif isinstance(item, ft.Container) and hasattr(item.content, 'color'):
                        item.content.color = th["TEXT"]

        for control in bodyColumn.controls:
            if isinstance(control, ft.Text):
                if "Bem-vindo" in control.value:
                    control.color = th["TEXT"]
                elif "O que você deseja" in control.value:
                    control.color = th["TEXT_SECONDARY"]
                elif "Ações Disponíveis" in control.value:
                    control.color = th["TEXT"]
                elif "©" in control.value:
                    control.color = th["TEXT_SECONDARY"]

        bodyColumn.controls[4] = buildCards()

        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]

        page.update()

    header_container = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Image(src=os.path.join("images", "icone.png"), width=40, height=40),
                ft.Text("Assertivus Contábil", size=16, weight="bold", color=th["TEXT"])
            ], spacing=12),
            ft.Row([
                ft.Text(f"Olá, {usuario.capitalize()}", size=14, color=th["TEXT"], weight="bold"),
                ThemeToggle(page, on_theme_changed=on_theme_change),
                ft.Container(
                    content=ft.Icon(name="exit_to_app", size=24, color=th["TEXT"]),
                    on_click=logout,
                    tooltip="Sair",
                )
            ], spacing=16)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=24, vertical=16),
        bgcolor=th["CARD"],
        border_radius=ft.border_radius.all(8),
    )

    bodyColumn = ft.Column([
        ft.Text(f"Bem-vindo, {usuario.capitalize()}", size=24, weight="bold", color=th["TEXT"]),
        ft.Text("O que você deseja fazer hoje?", size=16, color=th["TEXT_SECONDARY"]),
        ft.Container(height=20),
        ft.Text("Ações Disponíveis", size=18, weight="bold", color=th["TEXT"]),
        buildCards(),
        ft.Container(height=20),
        ft.Row(
            [ft.Text("© 2025 Assertivus Contábil. Todos os direitos reservados.",size=12, color=th["TEXT_SECONDARY"])],alignment=ft.MainAxisAlignment.CENTER)
    ], spacing=20, expand=True)

    return ft.View(
        route="/dashboard",
        controls=[
            ft.Column([
                header_container,
                ft.Container(content=bodyColumn, padding=24, expand=True)
            ])
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )
