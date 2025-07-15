import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao

PRODUCTS = [
    {"id": 1, "Usuario": "João", "Empresa": "JV LTDA", "ID Empresa": 1, "Ultimo Login": "4 Dias"},
    {"id": 2, "Usuario": "Bernardo", "Empresa": "JV LTDA", "ID Empresa": 2, "Ultimo Login": "1 Dias"},
    {"id": 3, "Usuario": "Anderson", "Empresa": "JV LTDA", "ID Empresa": 3, "Ultimo Login": "2 Dias"},

]

def UsuariosAdminContent(page: ft.Page):
    th = theme.get_theme()
    page.prod_search = getattr(page, "prod_search", "")

    def _on_search_change(e):
        page.prod_search = e.control.value
        page.update()

    def usuarioFilter():
        term = page.prod_search.lower()
        return [p for p in PRODUCTS if term in p["Usuario"].lower() or term in p["ID Empresa"].lower() or term in p["Ultimo Login"].lower()]

    def action_buttons(prod):
        return ft.Row([
            ft.IconButton(icon="edit", tooltip="Editar", icon_color=th["PRIMARY_COLOR"]),
            ft.IconButton(icon="delete", tooltip="Excluir", icon_color=th["ERROR"]),
        ], spacing=4)

    def build_table():
        min_spacing = 40
        max_spacing = 95
        if hasattr(page, "width") and page.width:
            spacing = int(min_spacing + (max_spacing - min_spacing) * min(page.width, 1600) / 1600)
        else:
            spacing = min_spacing

        return ft.ResponsiveRow([
            ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Usuario")),
                        ft.DataColumn(ft.Text("Empresa")),
                        ft.DataColumn(ft.Text("ID Empresa")),
                        ft.DataColumn(ft.Text("Ultimo Login")),
                        ft.DataColumn(ft.Text("Ações")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(p["Usuario"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["Empresa"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["ID Empresa"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["Ultimo Login"], color=th["TEXT"])),
                            ft.DataCell(action_buttons(p)),
                        ])
                        for p in usuarioFilter()
                    ],
                    heading_row_color=th["CARD"],
                    data_row_color={"even": th.get("INPUT_BG", "#F5F5F5"), "odd": th["CARD"]},
                    border=ft.border.all(1, th["BORDER"]),
                    column_spacing=spacing
                ),
                col={"xs": 12, "sm": 12, "md": 12, "lg": 12},
                expand=True
            )
        ])

    search = ft.TextField(
        hint_text="Buscar Usuarios..",
        prefix_icon="search",
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        border_radius=8,
        border_color=th["BORDER"],
        color=th["TEXT"],
        expand=True,
        on_change=_on_search_change,
    )

    def onNovoUsuario(e):
        notificacao(page, "Novo Usuario", "Funcionalidade ainda em desenvolvimento.", tipo="info")

    return ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Text("Gerenciar Usuarios", size=22, weight="bold", color=th["TEXT"]),
                    ft.Text("Adicione, edite e gerencie usuarios do sistema", size=14, color=th["TEXT_SECONDARY"]),
                ]),
                col={"xs": 12, "sm": 8, "md": 9, "lg": 10}
            ),
            ft.Container(
                content=ft.FilledButton(
                    "Novo Usuario",
                    icon="add",
                    bgcolor=th["PRIMARY_COLOR"],
                    color=th["ON_PRIMARY"],
                    on_click=onNovoUsuario
                ),
                alignment=ft.alignment.center_right,
                col={"xs": 12, "sm": 4, "md": 3, "lg": 2}
            )
        ]),

        ft.Container(height=16),

        ft.ResponsiveRow([
            ft.Container(search, col={"xs": 12, "sm": 12, "md": 8, "lg": 6})
        ]),

        ft.Container(height=16),

        ft.Container(
            expand=True,
            content=ft.Card(
                content=ft.Container(
                    bgcolor=th["CARD"],
                    border_radius=8,
                    padding=16,
                    border=ft.border.all(1, th["BORDER"]),
                    expand=True,
                    content=ft.Column([
                        ft.Text(
                            f"Lista de Usuarios ({len(usuarioFilter())})",
                            size=16,
                            weight="bold",
                            color=th["TEXT"]
                        ),
                        ft.Container(height=8),
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[build_table()]
                            )
                        )
                    ], expand=True)
                )
            )
        )
    ], spacing=12, expand=True)

