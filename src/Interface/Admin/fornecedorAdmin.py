import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao
from src.Components.cadastroDialog import CadastroDialog
from src.Controllers.fornecedorController import FornecedorController

def FornecedorAdminContent(page: ft.Page):
    th = theme.get_theme()
    controller = FornecedorController()
    page.prod_search = getattr(page, "prod_search", "")
    tabela_container = ft.Container(expand=True)

    def _on_search_change(e):
        page.prod_search = e.control.value
        atualizarTabela()

    def buscar_fornecedores():
        termo = page.prod_search.lower()
        fornecedores = controller.listar()
        return [
            {
                "id": f["id"],
                "empresa_id": f["empresa_id"],
                "CNPJ": f["cnpj"],
                "Razão Social": f["razaoSocial"],
                "CNAE": f["cnae"] or "",
                "UF": f["uf"] or "",
                "Simples": "Sim" if f["simples"] else "Não",
                "Decreto": "Sim" if f["decreto"] else "Não"
            }
            for f in fornecedores
            if termo in f["cnpj"].lower() or termo in (f["razaoSocial"] or "").lower()
        ]

    def action_buttons(fornecedor):
        return ft.Row([
            ft.IconButton(
                icon="edit",
                tooltip="Editar",
                icon_color=th["PRIMARY_COLOR"],
                on_click=lambda e: dialogo(fornecedor)
            ),
            ft.IconButton(
                icon="delete",
                tooltip="Excluir",
                icon_color=th["ERROR"],
                on_click=lambda e: excluir_fornecedor(fornecedor["id"])
            ),
        ], spacing=4)

    def excluir_fornecedor(id: int):
        controller.excluir(id)
        notificacao(page, "Excluído", "Fornecedor excluído com sucesso!", "info")
        atualizarTabela()
        page.update()

    def atualizarTabela():
        tabela_container.content = build_table()
        page.update()

    def build_table():
        min_spacing = 40
        max_spacing = 95
        if hasattr(page, "width") and page.width:
            spacing = int(min_spacing + (max_spacing - min_spacing) * min(page.width, 1600) / 1600)
        else:
            spacing = min_spacing

        fornecedores = buscar_fornecedores()
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
                            ft.DataCell(ft.Text(f["CNPJ"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(f["Razão Social"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(f["CNAE"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(f["UF"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(f["Simples"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(f["Decreto"], color=th["TEXT"])),
                            ft.DataCell(action_buttons(f)),
                        ])
                        for f in fornecedores
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

    def on_novo_fornecedor_click(e):
        dialogo()

    def dialogo(fornecedor: dict = None):
        valores = fornecedor or {}
        CadastroDialog(
            page,
            titulo="Editar Fornecedor" if fornecedor else "Novo Fornecedor",
            valores_iniciais=valores,
            campos=[
                {"name": "cnpj", "label": "CNPJ", "hint": "Digite o CNPJ", "required": True},
                {"name": "razaoSocial", "label": "Razão Social", "hint": "Digite a razão social", "required": True},
                {"name": "cnae", "label": "CNAE", "hint": "Digite o código CNAE"},
                {"name": "uf", "label": "UF", "type": "dropdown", "options": [
                    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT",
                    "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO",
                    "RR", "SC", "SP", "SE", "TO"
                ]},
                {"name": "simples", "label": "Optante do Simples?", "type": "dropdown", "options": ["Sim", "Não"]},
                {"name": "decreto", "label": "Possui Decreto?", "type": "dropdown", "options": ["Sim", "Não"]},
            ],
            on_confirmar=lambda dados: salvarFornecedor(dados, id=fornecedor["id"] if fornecedor else None)
        )

    def salvarFornecedor(dados: dict, id: int = None):
        dados["empresa_id"] = 1
        dados["simples"] = 1 if dados.get("simples") == "Sim" else 0
        dados["decreto"] = 1 if dados.get("decreto") == "Sim" else 0
        try:
            if id:
                controller.editar(id, dados)
                notificacao(page, "Atualizado", "Fornecedor atualizado com sucesso!", "sucesso")
            else:
                controller.adicionar(dados)
                notificacao(page, "Adicionado", "Fornecedor cadastrado com sucesso!", "sucesso")
        except ValueError as err:
            notificacao(page, str(err), "error")

        atualizarTabela()
        page.update()

    atualizarTabela()

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
                    on_click=on_novo_fornecedor_click
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
                            f"Lista de Fornecedores ({len(buscar_fornecedores())})",
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
                                controls=[tabela_container]
                            )
                        )
                    ], expand=True)
                )
            )
        )
    ], spacing=12, expand=True)