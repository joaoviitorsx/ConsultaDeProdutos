import flet as ft
from src.Components.adminLayout import AdminLayout
from src.Config import theme

def FornecedorAdminPage(page: ft.Page):
    th = theme.current_theme

    content = ft.Column([
        ft.Text("Gestão de Fornecedores", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Gerencie, edite e consulte fornecedores cadastrados no sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você adiciona tabela, filtros, etc.
    ], spacing=8, expand=True)

    return ft.View(
        route="/admin/fornecedores",
        controls=[AdminLayout(page, content, selected_route="/admin/fornecedores")],
        bgcolor=th["BACKGROUNDSCREEN"]
    )
