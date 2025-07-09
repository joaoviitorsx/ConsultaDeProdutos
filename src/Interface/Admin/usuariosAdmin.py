import flet as ft
from src.Config import theme
from src.Components.adminLayout import AdminLayout

def UsuariosAdminContent(page):
    th = theme.current_theme
    return ft.Column([
        ft.Text("Gestão de Usuários", size=22, weight="bold", color=th["TEXT"]),
        ft.Text("Administre usuários, permissões e acessos do sistema.", size=14, color=th["TEXT_SECONDARY"]),
        ft.Container(height=24),
        # Adicione aqui a lista de usuários, etc.
    ], spacing=8, expand=True)


def UsuarioPage(page: ft.Page):
    print("🛠️ Tela Usuarios carregada")
    th = theme.current_theme
    main_content = UsuarioPage(page)
    return ft.View(
        route="/admin/usuarios",
        controls=[
            AdminLayout(page, main_content, selected_route="/admin/usuarios")
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor=th["BACKGROUNDSCREEN"]
    )