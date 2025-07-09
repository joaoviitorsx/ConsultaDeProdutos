import flet as ft
from src.Config import theme
from src.Components.trocaTema import ThemeToggle

def AdminLayout(page: ft.Page):
    content_map = {
        "/admin_dashboard": dashboard_content,
        "/admin/produtos": produtos_content,
        "/admin/usuarios": usuarios_content,
        "/admin/fornecedores": fornecedor_content,
        "/admin/relatorios": relatorios_content,
    }
    
    if not hasattr(page, "admin_selected_route"):
        page.admin_selected_route = page.route if page.route in content_map else "/admin_dashboard"

    main_content_container = ft.Container(
        expand=True,
        content=content_map[page.admin_selected_route]()
    )

    def on_tab_selected(tab_route):
        page.admin_selected_route = tab_route
        main_content_container.content = content_map[tab_route]()
        page.update()

    def on_theme_change(_):
        page.clean()
        page.add(AdminDashboardPage(page))

    header = AdminHeader(page, on_theme_change)
    sidebar = AdminSidebar(page.admin_selected_route, on_tab_selected)

    return ft.Column([
        header,
        ft.Row([
            sidebar,
            ft.Container(width=1, bgcolor=theme.current_theme["BORDER"], opacity=0.1),
            main_content_container
        ], expand=True)
    ], expand=True)

def get_main_content(tab):
    t = theme.current_theme
    titles = {
        "dashboard": "Dashboard do admin",
        "produtos": "Gestão de Produtos",
        "usuarios": "Gestão de Usuários",
        "fornecedor": "Gestão de Fornecedores",
        "relatorios": "Relatórios Administrativos"
    }
    return ft.Container(
        expand=True,
        padding=ft.padding.all(24),
        content=ft.Text(
            titles.get(tab, "Selecione uma aba..."),
            size=22,
            color=t["TEXT"]
        )
    )

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
            bottom_right=0,
            bottom_left=0
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
            top_left=0,
            top_right=0,
            bottom_left=8,
            bottom_right=0
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

def AdminDashboardPage(page: ft.Page):
    return ft.View(
        route="/admin_dashboard",
        controls=[AdminLayout(page)],
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        scroll=ft.ScrollMode.HIDDEN
    )

def dashboard_content():
    th = theme.current_theme
    return ft.Text("Dashboard do admin", size=22, color=th["TEXT"])

def produtos_content():
    th = theme.current_theme
    return ft.Text("Gestão de Produtos", size=22, color=th["TEXT"])

def usuarios_content():
    th = theme.current_theme
    return ft.Text("Gestão de Usuários", size=22, color=th["TEXT"])

def fornecedor_content():
    th = theme.current_theme
    return ft.Text("Gestão de Fornecedores", size=22, color=th["TEXT"])

def relatorios_content():
    th = theme.current_theme
    return ft.Text("Relatórios Administrativos", size=22, color=th["TEXT"])