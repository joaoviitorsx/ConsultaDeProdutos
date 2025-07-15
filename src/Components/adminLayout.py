import flet as ft
from src.Config import theme
from src.Components.headerApp import HeaderApp

ROUTE_CONTENT_MAP = {
    "/admin_dashboard": lambda page: __import__("src.Interface.Admin.dashboardAdmin").Interface.Admin.dashboardAdmin.AdminDashboardContent(page),
    "/admin/produtos": lambda page: __import__("src.Interface.Admin.produtosAdmin").Interface.Admin.produtosAdmin.ProdutosAdminContent(page),
    "/admin/usuarios": lambda page: __import__("src.Interface.Admin.usuariosAdmin").Interface.Admin.usuariosAdmin.UsuariosAdminContent(page),
    "/admin/fornecedores": lambda page: __import__("src.Interface.Admin.fornecedorAdmin").Interface.Admin.fornecedorAdmin.FornecedorAdminContent(page),
    "/admin/relatorios": lambda page: __import__("src.Interface.Admin.relatoriosAdmin").Interface.Admin.relatoriosAdmin.RelatoriosAdminContent(page),
}

def build_card(content):
    th = theme.get_theme()
    return ft.Container(
        bgcolor=th["CARD"],
        padding=24,
        border_radius=theme.STYLE["CARD_RADIUS"],
        expand=True,
        content=content
    )

def AdminSidebar(selected_route, on_tab_selected):
    th = theme.get_theme()

    menu_items = [
        {"label": "Produtos", "icon": "shopping_cart", "route": "/admin/produtos"},
        {"label": "Usuários", "icon": "people", "route": "/admin/usuarios"},
        {"label": "Fornecedor", "icon": "business", "route": "/admin/fornecedores"},
        {"label": "Relatórios", "icon": "bar_chart", "route": "/admin/relatorios"},
    ]

    def build_item(item):
        selected = item["route"] == selected_route
        return ft.Container(
            bgcolor=th["PRIMARY_COLOR"] + "22" if selected else "transparent",
            border_radius=theme.STYLE["CARD_RADIUS"],
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            on_click=lambda _: on_tab_selected(item["route"]),
            ink=True,
            content=ft.Row([
                ft.Icon(name=item["icon"], size=20,
                        color=th["PRIMARY_COLOR"] if selected else th["TEXT_SECONDARY"]),
                ft.Text(
                    item["label"],
                    size=14,
                    weight="bold" if selected else "normal",
                    color=th["TEXT"] if selected else th["TEXT_SECONDARY"]
                )
            ], spacing=12)
        )

    return ft.Container(
        bgcolor=th["CARD"],
        width=180,
        padding=ft.padding.symmetric(horizontal=12, vertical=16),
        border_radius=theme.STYLE["CARD_RADIUS"],
        expand=True,
        content=ft.ResponsiveRow(
            controls=[build_item(i) for i in menu_items],
            spacing=8,
            expand=True,
            height=930
        )
    )

def AdminLayout(page: ft.Page, main_content=None, selected_route=None):
    theme.apply_theme(page)

    if selected_route:
        page.admin_selected_route = selected_route
    elif not hasattr(page, "admin_selected_route"):
        page.admin_selected_route = "/admin/produtos"

    sidebar_container = ft.Container()
    main_content_container = ft.Container(expand=True)

    def on_tab_selected(tab_route):
        page.admin_selected_route = tab_route
        main_content_container.content = build_card(ROUTE_CONTENT_MAP[tab_route](page))
        sidebar_container.content = AdminSidebar(tab_route, on_tab_selected)
        page.update()

    header = HeaderApp(
        page,
        titulo_tela="Painel do Administrador",
        mostrar_voltar=True,
        mostrar_theme_toggle=False,
        mostrar_logout=True,
        mostrar_nome_empresa=False,
        mostrar_divider=False,
        mostrar_logo=False,  
        on_theme_changed=lambda _: theme.apply_theme(page)
    )

    sidebar_container.content = AdminSidebar(page.admin_selected_route, on_tab_selected)
    main_content_container.content = build_card(
        main_content or ROUTE_CONTENT_MAP[page.admin_selected_route](page)
    )

    layout = ft.Container(
        expand=True,
        content=ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                sidebar_container,
                main_content_container
            ]
        )
    )

    return ft.View(
        route="/admin",
        bgcolor=theme.get_theme()["BACKGROUNDSCREEN"],
        controls=[
            ft.Column([
                ft.Container(content=header, padding=ft.padding.symmetric(horizontal=16)),
                ft.Container(content=layout, expand=True, padding=ft.padding.symmetric(horizontal=16)),
            ], expand=True)
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )
