import flet as ft
from src.Config import theme
from src.Components.adminLayout import AdminLayout

def ProdutosAdminContent(page):
    th = theme.current_theme
    return ft.Column([
        ft.Text("Gestão de Produtos", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Gerencie, edite e consulte produtos cadastrados. PRIQTO", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você adiciona tabela de produtos, filtros, etc.
    ], spacing=8, expand=True)


def ProdutosPage(page: ft.Page):
    print("🛠️ Tela Produtos carregada")
    th = theme.current_theme
    main_content = ProdutosPage(page)
    return ft.View(
        route="/admin/produtos",
        controls=[
            AdminLayout(page, main_content, selected_route="/admin/produtos")
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )