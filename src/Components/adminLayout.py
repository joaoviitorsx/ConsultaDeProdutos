import flet as ft
from src.Config import theme
from src.Components.trocaTema import ThemeToggle

def DashboardContent(page):
    from src.Interface.Admin.dashboardAdmin import AdminDashboardContent
    return AdminDashboardContent(page)

def ProdutosContent(page):
    from src.Interface.Admin.produtosAdmin import ProdutosAdminContent
    return ProdutosAdminContent(page)

def UsuariosContent(page):
    from src.Interface.Admin.usuariosAdmin import UsuariosAdminContent
    return UsuariosAdminContent(page)

def FornecedorContent(page):
    from src.Interface.Admin.fornecedorAdmin import FornecedorAdminContent
    return FornecedorAdminContent(page)

def RelatoriosContent(page):
    from src.Interface.Admin.relatoriosAdmin import RelatoriosAdminContent
    return RelatoriosAdminContent(page)

def cardContent(content):
    th = theme.current_theme
    return ft.Container(
        content=ft.Column(
            controls=[content],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=16,
        bgcolor=th["CARD"],
        border_radius=8,
        expand=True,
        alignment=ft.alignment.top_left,
        shadow=ft.BoxShadow(
            blur_radius=16,
            color=th["BORDER"] + "33",
            offset=ft.Offset(0, 4)
        )
    )

def AdminLayout(page: ft.Page, main_content=None, selected_route=None):
    content_map = {
        "/admin_dashboard": DashboardContent,
        "/admin/produtos": ProdutosContent,
        "/admin/usuarios": UsuariosContent,
        "/admin/fornecedores": FornecedorContent,
        "/admin/relatorios": RelatoriosContent,
    }

    if selected_route is not None:
        page.admin_selected_route = selected_route
    elif not hasattr(page, "admin_selected_route"):
        page.admin_selected_route = "/admin_dashboard"

    main_content_container = ft.Container(
        expand=True,
        content=cardContent(main_content if main_content else content_map[page.admin_selected_route](page))
    )

    def on_tab_selected(tab_route):
        page.admin_selected_route = tab_route
        main_content_container.content = cardContent(content_map[tab_route](page))
        sidebar_container.content = AdminSidebar(tab_route, on_tab_selected)
        page.update()

    sidebar_container = ft.Container(
        content=AdminSidebar(page.admin_selected_route, on_tab_selected)
    )

    def on_theme_change(_):
        page.clean()
        page.add(AdminLayout(page))

    header = AdminHeader(page, on_theme_change)

    return ft.Column([
        header,
        ft.Row([
            sidebar_container,
            main_content_container
        ], expand=True)
    ], expand=True)

def AdminHeader(page: ft.Page, on_theme_change):
    th = theme.current_theme

    def logout(_):
        page.go("/login")

    def voltar(_):
        page.go("/dashboard")

    return ft.Container(
        bgcolor=th["CARD"],
        height=80,
        padding=ft.padding.symmetric(horizontal=24),
        border_radius=ft.border_radius.only(
            top_left=8,
            top_right=8,
            bottom_right=8,
            bottom_left=8
        ),
        content=ft.Row([
            ft.Row([
                ft.IconButton(
                    icon="arrow_back",
                    icon_color=th["TEXT"],
                    tooltip="Voltar",
                    on_click=voltar
                ),
                ft.Text(
                    "Painel do Administrador",
                    size=20,
                    weight="bold",
                    color=th["TEXT"]
                )
            ], spacing=12),
            ft.Row([
                ThemeToggle(page, on_theme_changed=on_theme_change),
                ft.IconButton(
                    icon="exit_to_app",
                    icon_color=th["TEXT"],
                    tooltip="Sair",
                    on_click=logout
                )
            ], spacing=8)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

def AdminSidebar(selected_route, on_tab_selected):
    th = theme.current_theme
    menu_items = [
        {"label": "Dashboard", "icon": "dashboard", "route": "/admin_dashboard"},
        {"label": "Produtos", "icon": "shopping_cart", "route": "/admin/produtos"},
        {"label": "Usuários", "icon": "people", "route": "/admin/usuarios"},
        {"label": "Fornecedor", "icon": "business", "route": "/admin/fornecedores"},
        {"label": "Relatórios", "icon": "bar_chart", "route": "/admin/relatorios"},
    ]

    def handle_click(route):
        def handler(e):
            on_tab_selected(route)
        return handler

    menu_controls = []
    for item in menu_items:
        is_selected = item["route"] == selected_route
        menu_controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        name=item["icon"],
                        size=20,
                        color=th["PRIMARY_COLOR"] if is_selected else th["TEXT_SECONDARY"]
                    ),
                    ft.Text(
                        item["label"],
                        size=14,
                        weight="bold" if is_selected else "normal",
                        color=th["TEXT"] if is_selected else th["TEXT_SECONDARY"]
                    )
                ],
                spacing=12),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor=th["PRIMARY_COLOR"] + "22" if is_selected else None,
                border_radius=8,
                on_click=handle_click(item["route"]),
                ink=True
            )
        )

    return ft.Container(
        width=170,
        bgcolor=th["CARD"],
        border_radius=ft.border_radius.only(
            top_left=8,
            top_right=8,
            bottom_left=8,
            bottom_right=8
        ),
        content=ft.Column(
            controls=[
                ft.Column(menu_controls, spacing=4),
                ft.Container(expand=True)
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )
    )