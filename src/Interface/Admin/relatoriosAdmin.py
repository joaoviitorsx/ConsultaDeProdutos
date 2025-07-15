import flet as ft
from src.Config import theme
from src.Components.adminLayout import AdminLayout

def RelatoriosAdminContent(page):
    th = theme.get_theme()
    return ft.Column([
        ft.Text("Relatórios Administrativos", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Visualize e gere relatórios administrativos do sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você pode inserir filtros e lista de relatórios.
    ], spacing=8, expand=True)


def RelatorioPage(page: ft.Page):
    print("🛠️ Tela Relatorios carregada")
    th = theme.get_theme()
    main_content = RelatorioPage(page)
    return ft.View(
        route="/admin/relatorios",
        controls=[
            AdminLayout(page, main_content, selected_route="/admin/relatorios")
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )