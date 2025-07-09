import flet as ft
from src.Components.adminLayout import AdminLayout
from src.Config import theme

def RelatoriosAdminPage(page: ft.Page):
    th = theme.current_theme

    content = ft.Column([
        ft.Text("Relatórios Administrativos", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Visualize e gere relatórios administrativos do sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você pode inserir filtros e lista de relatórios.
    ], spacing=8, expand=True)

    return ft.View(
        route="/admin/relatorios",
        controls=[AdminLayout(page, content, selected_route="/admin/relatorios")],
        bgcolor=th["BACKGROUNDSCREEN"]
    )
