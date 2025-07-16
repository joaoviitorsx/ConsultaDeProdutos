import flet as ft
from src.Config import theme
from src.Utils.senha import hashSenha
from src.Components.notificacao import notificacao
from src.Components.cadastroDialog import CadastroDialog
from src.Controllers.usuarioController import UsuarioController  

def UsuariosAdminContent(page: ft.Page):
    th = theme.get_theme()
    controller = UsuarioController()
    page.prod_search = getattr(page, "prod_search", "")
    tabela_container = ft.Container(expand=True)

    def _on_search_change(e):
        page.prod_search = e.control.value
        atualizarTabela()

    def atualizarTabela():
        tabela_container.content = build_table()
        page.update()

    def buscar_usuarios():
        termo = page.prod_search.lower()
        return [
            {
                "id": u["id"],
                "usuario": u["usuario"],
                "empresa": u.get("razaoSocial", ""),
                "empresa_id": str(u.get("empresa_id", "")),
                "ativo": "Sim" if u.get("ativo", True) else "Não",
                "ultimo_login": u.get("ultimo_login", "-")
            }
            for u in controller.listar()
            if termo in u["usuario"].lower() or termo in str(u.get("empresa_id", "")).lower() or termo in u.get("razaoSocial", "").lower()
        ]

    def action_buttons(user):
        return ft.Row([
            ft.IconButton(
                icon="edit",
                tooltip="Editar",
                icon_color=th["PRIMARY_COLOR"],
                on_click=lambda e: dialogo(user)
            ),
            ft.IconButton(
                icon="delete",
                tooltip="Excluir",
                icon_color=th["ERROR"],
                on_click=lambda e: excluirUsuario(user["id"])
            ),
        ], spacing=4)

    def dialogo(user: dict = None):
        CadastroDialog(
            page,
            titulo="Editar Usuário" if user else "Novo Usuário",
            valores_iniciais=user or {},
            campos=[
                {"name": "usuario", "label": "Usuário", "hint": "Digite o nome de usuário", "required": True},
                {"name": "senha", "label": "Senha", "hint": "Digite a senha", "required": not user, "type": "password"},
                {"name": "razaoSocial", "label": "Razão Social", "hint": "Nome da empresa"}
            ],
            on_confirmar=lambda dados: salvarUsuario(dados, id=user["id"] if user else None)
        )

    def excluirUsuario(id: int):
        controller.excluir(id)
        notificacao(page, "Excluído", "Usuário excluído com sucesso!", "info")
        atualizarTabela()
        page.update()

    def salvarUsuario(dados: dict, id: int = None):
        dados["empresa_id"] = 1

        if id:
            if not dados.get("senha"):
                dados.pop("senha", None)
            else:
                dados["senha"] = hashSenha(dados["senha"])
        else:
            if "senha" in dados and dados["senha"]:
                dados["senha"] = hashSenha(dados["senha"])
        try:
            if id:
                controller.editar(id, dados)
                notificacao(page, "Atualizado", "Usuário atualizado com sucesso!", "sucesso")
            else:
                controller.adicionar(dados)
                notificacao(page, "Adicionado", "Usuário adicionado com sucesso!", "sucesso")
        except ValueError as err:
            notificacao(page, str(err), "error")

        atualizarTabela()
        page.update()

    def build_table():
        usuarios = buscar_usuarios()
        min_spacing = 40
        max_spacing = 95
        spacing = int(
            min_spacing +
            (max_spacing - min_spacing) *
            min(page.width or 800, 1600) / 1600
        )

        return ft.ResponsiveRow([
            ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Usuário")),
                        ft.DataColumn(ft.Text("Empresa")),
                        ft.DataColumn(ft.Text("ID Empresa")),
                        ft.DataColumn(ft.Text("Ativo")),
                        ft.DataColumn(ft.Text("Ações")),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(u["usuario"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(u["empresa"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(u["empresa_id"], color=th["TEXT"])),
                            ft.DataCell(ft.Text(u["ativo"], color=th["TEXT"])),
                            ft.DataCell(action_buttons(u)),
                        ])
                        for u in usuarios
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
        hint_text="Buscar Usuários...",
        prefix_icon="search",
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        border_radius=8,
        border_color=th["BORDER"],
        color=th["TEXT"],
        expand=True,
        on_change=_on_search_change,
    )

    def onNovoUsuario(e):
        dialogo(None)

    atualizarTabela()

    return ft.Column([
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Text("Gerenciar Usuários", size=22, weight="bold", color=th["TEXT"]),
                    ft.Text("Adicione, edite e gerencie usuários do sistema", size=14, color=th["TEXT_SECONDARY"]),
                ]),
                col={"xs": 12, "sm": 8, "md": 9, "lg": 10}
            ),
            ft.Container(
                content=ft.FilledButton(
                    "Novo Usuário",
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
                            f"Lista de Usuários ({len(buscar_usuarios())})",
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