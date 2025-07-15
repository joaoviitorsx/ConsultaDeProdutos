import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao

PRODUCTS = [
    {"CNPJ": "12.345.678/00001-09", "Razão Social": "RealizeSoftware", "CNAE": "12345", "UF": "CE", "Simples": "Sim", "Decreto": "Não"},
    {"CNPJ": "12.345.678/00001-09", "Razão Social": "Assertivus Contabil", "CNAE": "12345", "UF": "SP", "Simples": "Sim", "Decreto": "Não"},
    {"CNPJ": "12.345.678/00001-09", "Razão Social": "Up Value", "CNAE": "12345", "UF": "MG", "Simples": "Sim", "Decreto": "Não"},
]

def FornecedorAdminContent(page: ft.Page):
    th = theme.get_theme()
    page.prod_search = getattr(page, "prod_search", "")

    def _on_search_change(e):
        page.prod_search = e.control.value
        page.update()
    
    def filter_products():
        term = page.prod_search.lower()
        return [p for p in PRODUCTS if term in p["CNPJ"].lower() or term in p["Razão Social"].lower()]

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
                        ft.DataColumn(ft.Text("CNPJ")),
                        ft.DataColumn(ft.Text("Razão Social")),
                        ft.DataColumn(ft.Text("CNAE")),
                        ft.DataColumn(ft.Text("UF")),
                        ft.DataColumn(ft.Text("Simples")),
                        ft.DataColumn(ft.Text("Decreto")),
                        ft.DataColumn(ft.Text("Ações")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(p["CNPJ"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["Razão Social"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["CNAE"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["UF"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["Simples"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["Decreto"], color=th["TEXT"])),
                            ft.DataCell(action_buttons(p)),
                        ])
                        for p in filter_products()
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
        hint_text="Buscar Fornecedores...",
        prefix_icon="search",
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        border_radius=8,
        border_color=th["BORDER"],
        color=th["TEXT"],
        expand=True,
        on_change=_on_search_change,
    )

    def on_novo_produto_click(e):
        notificacao(page, "Novo Produto", "Funcionalidade ainda em desenvolvimento.", tipo="info")

    return ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Text("Gerenciar Fornecedores", size=22, weight="bold", color=th["TEXT"]),
                    ft.Text("Adicione, edite e gerencie Fornecedores do sistema", size=14, color=th["TEXT_SECONDARY"]),
                ]),
                col={"xs": 12, "sm": 8, "md": 9, "lg": 10}
            ),
            ft.Container(
                content=ft.FilledButton(
                    "Novo Fornecedor",
                    icon="add",
                    bgcolor=th["PRIMARY_COLOR"],
                    color=th["ON_PRIMARY"],
                    on_click=on_novo_produto_click
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
                            f"Lista de Fornecedores ({len(filter_products())})",
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

