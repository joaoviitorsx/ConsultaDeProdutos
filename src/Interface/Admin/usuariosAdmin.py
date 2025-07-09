import flet as ft
from src.Components.adminLayout import AdminLayout
from src.Config import theme

def UsuariosAdminPage(page: ft.Page):
    th = theme.current_theme

    content = ft.Column([
        ft.Text("Gestão de Usuários", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Administre usuários, permissões e acessos do sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Aqui você adiciona lista de usuários, ações, etc.
    ], spacing=8, expand=True)

    return ft.View(
        route="/admin/usuarios",
        controls=[AdminLayout(page, content, selected_route="/admin/usuarios")],
        bgcolor=th["BACKGROUNDSCREEN"]
    )
