import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao
from src.Components.cadastroDialog import CadastroDialog
from src.Controllers.produtosController import ProdutoController
from src.Controllers.usuarioController import UsuarioController

def ProdutosAdminContent(page: ft.Page):
    th = theme.get_theme()
    controller = ProdutoController()
    page.prod_search = getattr(page, "prod_search", "")
    tabela_container = ft.Container(expand=True)
    page.selected_empresa_id = getattr(page, "selected_empresa_id", None)
    usuarios_controller = UsuarioController()
    empresas = [{"empresa_id": None, "razaoSocial": "Todas"}] + [
        {**emp, "empresa_id": emp.get("empresa_id", emp.get("id"))} for emp in usuarios_controller.listar()
    ]

    def _on_empresa_change(e: ft.ControlEvent):
        page.selected_empresa_id = e.control.value if e.control.value != "None" else None
        atualizarTabela()

    def _on_search_change(e: ft.ControlEvent):
        page.prod_search = e.control.value
        atualizarTabela()

    def atualizarTabela():
        tabela_container.content = buildTable()
        page.update()

    def buscar_produtos():
        termo = page.prod_search.lower()
        empresa_id = page.selected_empresa_id
        produtos = controller.listar(empresa_id) 
        return [
            {
                "empresa_id": p["empresa_id"],
                "id": p["id"],
                "produto": p["produto"],
                "codigo": p["codigo"],
                "ncm": p["ncm"],
                "aliquota": f"{p['aliquota']:.2f}%" if isinstance(p["aliquota"], float) else str(p["aliquota"]),
                "categoriaFiscal": p.get("categoriaFiscal", "") or ""
            }
            for p in produtos
            if termo in p["produto"].lower() or termo in p["codigo"].lower() or termo in p["ncm"].lower()
        ]

    def action_buttons(prod: dict):
        return ft.Row([
            ft.IconButton(
                icon="edit",
                tooltip="Editar",
                icon_color=th["PRIMARY_COLOR"],
                on_click=lambda e: dialog(prod)
            ),
            ft.IconButton(
                icon="delete",
                tooltip="Excluir",
                icon_color=th["ERROR"],
                on_click=lambda e: excluirProduto(prod["id"])
            ),
        ], spacing=4)

    def dialog(prod: dict):
        CadastroDialog(
            page,
            titulo="Novo Produto",
            campos=[
                {
                    "name": "empresa_id",
                    "label": "Empresa",
                    "type": "dropdown",
                    "options": [emp["razaoSocial"] for emp in empresas if emp["empresa_id"] is not None],
                    "hint": "Selecione a empresa",
                    "required": True
                },
                {"name": "codigo", "label": "Código", "hint": "Ex: 01"},
                {"name": "ncm", "label": "NCM", "hint": "Ex: 1234.56.78"},
                {"name": "aliquota", "label": "Alíquota (%)", "hint": "Digite a alíquota"},
                {
                    "name": "categoriaFiscal",
                    "label": "Categoria Fiscal",
                    "type": "dropdown",
                    "options": [
                        "28% Bebida Alcoólica", "20% Regra Geral", "12% Cesta Básica", "7% Cesta Básica"
                    ]
                }
            ],
            valores_iniciais=prod,
            on_confirmar=lambda dados: salvarProduto(dados, prod["id"])
        )

    def excluirProduto(id: int):
        controller.excluir(id)
        notificacao(page, "Excluido", "Produto excluído com sucesso!", "info")
        atualizarTabela()
        page.update()

    def salvarProduto(dados: dict, id: int = None):
        empresa_nome = dados.get("empresa_id")
        empresa = next((emp for emp in empresas if emp["razaoSocial"] == empresa_nome), None)
        if empresa:
            dados["empresa_id"] = empresa["empresa_id"]
        else:
            notificacao(page, "Erro ao converter empresa_id", "Empresa inválida selecionada", "error")
            return

        categorias = {
            "28% Bebida Alcoólica": "28BebidaAlcoolica",
            "20% Regra Geral": "20RegraGeral",
            "12% Cesta Básica": "12CestaBasica",
            "7% Cesta Básica": "7CestaBasica"
        }
        if "categoriaFiscal" in dados:
            dados["categoriaFiscal"] = categorias.get(dados["categoriaFiscal"], dados["categoriaFiscal"])

        try:
            if id:
                controller.editar(id, dados)
                notificacao(page, "Atualizado", "Produto atualizado com sucesso!", "sucesso")
            else:
                controller.adicionar(dados)
                notificacao(page, "Adicionado", "Produto adicionado com sucesso!", "sucesso")
        except ValueError as err:
            notificacao(page, str(err), "error")

        atualizarTabela()
        page.update()

    def buildTable():
        produtos = buscar_produtos()
        min_spacing = 40
        max_spacing = 75
        spacing = int(
            min_spacing +
            (max_spacing - min_spacing) *
            min(page.width or 800, 1600) / 1600
        )

        return ft.ResponsiveRow([
            ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Empresa ID")),
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Código")),
                        ft.DataColumn(ft.Text("NCM")),
                        ft.DataColumn(ft.Text("Alíquota")),
                        ft.DataColumn(ft.Text("Categoria Fiscal")),
                        ft.DataColumn(ft.Text("Ações")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(p["empresa_id"], color=th["TEXT"])),   
                            ft.DataCell(ft.Text(p["produto"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["codigo"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["ncm"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["aliquota"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(p["categoriaFiscal"], color=th["TEXT"])),
                            ft.DataCell(action_buttons(p)),
                        ])
                        for p in produtos
                    ],
                    heading_row_color=th["CARD"],
                    data_row_color={"even": th.get("INPUT_BG", "#F5F5F5"), "odd": th["CARD"]},
                    border=ft.border.all(1, th["BORDER"]),
                    column_spacing=spacing
                ),
                col={"xs": 12}, expand=True
            )
        ])

    def onNovoProduto(e: ft.ControlEvent):
        CadastroDialog(
            page,
            titulo="Novo Produto",
            campos=[
                {
                    "name": "empresa_id",
                    "label": "Empresa",
                    "type": "dropdown",
                    "options": [emp["razaoSocial"] for emp in empresas if emp["empresa_id"] is not None],
                    "hint": "Selecione a empresa",
                    "required": True
                },
                {"name": "produto", "label": "Nome", "hint": "Digite o nome do produto", "required": True},
                {"name": "codigo", "label": "Código", "hint": "Ex: PROD-001"},
                {"name": "ncm", "label": "NCM", "hint": "Ex: 1234.56.78"},
                {"name": "aliquota", "label": "Alíquota (%)", "hint": "Digite a alíquota"},
                {
                    "name": "categoriaFiscal",
                    "label": "Categoria Fiscal",
                    "type": "dropdown",
                    "options": [
                        "28% Bebida Alcoólica", "20% Regra Geral", "12% Cesta Básica", "7% Cesta Básica"
                    ]
                }
            ],
            on_confirmar=lambda dados: salvarProduto(dados),
        )

    empresa_dropdown = ft.Dropdown(
        label="Empresa",
        value=page.selected_empresa_id,
        options=[
            ft.dropdown.Option(str(emp["empresa_id"]), emp["razaoSocial"])
            for emp in empresas
        ],
        on_change=_on_empresa_change,
        width=220,
        dense=True,
        border_color=th["BORDER"],
        border_radius=8,
        filled=True,
    )

    search = ft.TextField(
        hint_text="Buscar produtos...",
        prefix_icon="search",
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        border_radius=8,
        border_color=th["BORDER"],
        color=th["TEXT"],
        expand=True,
        on_change=_on_search_change,
    )

    atualizarTabela()

    return ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Text("Gerenciar Produtos", size=22, weight="bold", color=th["TEXT"]),
                    ft.Text("Adicione, edite e gerencie produtos do sistema", size=14, color=th["TEXT_SECONDARY"]),
                ]),
                col={"xs": 12, "sm": 8, "md": 9, "lg": 10}
            ),
            ft.Container(
                content=ft.FilledButton(
                    "Novo Produto",
                    icon="add",
                    bgcolor=th["PRIMARY_COLOR"],
                    color=th["ON_PRIMARY"],
                    on_click=onNovoProduto
                ),
                alignment=ft.alignment.center_right,
                col={"xs": 12, "sm": 4, "md": 3, "lg": 2}
            )
        ]),

        ft.Container(height=16),

        ft.ResponsiveRow([
            ft.Container(empresa_dropdown, col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
            ft.Container(search, col={"xs": 12, "sm": 6, "md": 8, "lg": 6})
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
                            f"Lista de Produtos ({len(buscar_produtos())})",
                            size=16,
                            weight="bold",
                            color=th["TEXT"]
                        ),
                        ft.Container(height=8),
                        tabela_container
                    ], expand=True)
                )
            )
        )
    ], spacing=12, expand=True)