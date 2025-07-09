import flet as ft
from src.Components.adminLayout import AdminLayout
from src.Config import theme

def ProdutosAdminPage(page: ft.Page):
    th = theme.current_theme

    content = ft.Column([
        ft.Text("Gestão de Produtos", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Gerencie, edite e consulte produtos cadastrados.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você adiciona tabela de produtos, filtros, etc.
    ], spacing=8, expand=True)

    return ft.View(
        route="/admin/produtos",
        controls=[AdminLayout(page, content, selected_route="/admin/produtos")],
        bgcolor=th["BACKGROUNDSCREEN"]
    )
