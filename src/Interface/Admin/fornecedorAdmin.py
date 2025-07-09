import flet as ft
from src.Config import theme
from src.Components.adminLayout import AdminLayout

def FornecedorAdminContent(page):
    th = theme.current_theme
    return ft.Column([
        ft.Text("Gestão de Fornecedores", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Gerencie, edite e consulte fornecedores cadastrados no sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
    ], spacing=8, expand=True)


def FornecedorPage(page: ft.Page):
    print("🛠️ Tela Fornecedor carregada")
    th = theme.current_theme
    main_content = FornecedorAdminContent(page)
    return ft.View(
        route="/admin/fornecedores",
        controls=[
            AdminLayout(page, main_content, selected_route="/admin/fornecedores")
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )