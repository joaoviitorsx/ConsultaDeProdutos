import re
import flet as ft
from src.Config import theme

def CadastroDialog(
    page: ft.Page,
    titulo: str,
    on_confirmar,
    valores_iniciais: dict = None
):
    th = theme.get_theme()
    valores_iniciais = valores_iniciais or {}

    def _validate(e: ft.ControlEvent):
        save_button.disabled = not bool(nome.value.strip())
        page.update()

    nome = ft.TextField(
        label="Nome",
        hint_text="Digite o nome do produto",
        value=valores_iniciais.get("produto", ""),
        border_color=th["BORDER"],
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        color=th["TEXT"],
        border_radius=8,
        dense=True,
        expand=True,
        on_change=_validate
    )

    codigo = ft.TextField(
        label="Código",
        hint_text="Ex: PROD-001",
        value=valores_iniciais.get("codigo", ""),
        border_color=th["BORDER"],
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        color=th["TEXT"],
        border_radius=8,
        dense=True,
        expand=True,
        on_change=_validate
    )

    ncm = ft.TextField(
        label="NCM",
        hint_text="Ex: 1234.56.78",
        value=valores_iniciais.get("ncm", ""),
        border_color=th["BORDER"],
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        color=th["TEXT"],
        border_radius=8,
        dense=True,
        expand=True
    )

    aliquota = ft.TextField(
        label="Alíquota (%)",
        hint_text="Digite a alíquota",
        value=valores_iniciais.get("aliquota", ""),
        border_color=th["BORDER"],
        bgcolor=th.get("INPUT_BG", th["CARD"]),
        color=th["TEXT"],
        border_radius=8,
        dense=True,
        expand=True
    )

    categoriaFiscal = ft.Dropdown(
        label="Categoria Fiscal",
        hint_text="Selecione uma categoria",
        value=valores_iniciais.get("categoriaFiscal", ""),
        border_color=th["BORDER"],
        border_radius=8,
        filled=True,
        options=[
            ft.dropdown.Option("28% Bebida Alcoólica"),
            ft.dropdown.Option("20% Regra Geral"),
            ft.dropdown.Option("12% Cesta Básica"),
            ft.dropdown.Option("7% Cesta Básica"),
        ],
        expand=True
    )

    def confirmar(e: ft.ControlEvent):
        def tratarCategoria(valor):
            if not valor:
                return ""
            valor = valor.replace("%", "")
            valor = re.sub(r"[áàãâä]", "a", valor, flags=re.IGNORECASE)
            valor = re.sub(r"[éèêë]", "e", valor, flags=re.IGNORECASE)
            valor = re.sub(r"[íìîï]", "i", valor, flags=re.IGNORECASE)
            valor = re.sub(r"[óòõôö]", "o", valor, flags=re.IGNORECASE)
            valor = re.sub(r"[úùûü]", "u", valor, flags=re.IGNORECASE)
            valor = re.sub(r"[^a-zA-Z0-9]", "", valor)
            return valor

        categoria_tratada = tratarCategoria(categoriaFiscal.value)
        print("Categoria fiscal selecionada:", categoriaFiscal.value)
        print("Categoria fiscal tratada:", categoria_tratada)

        dados = {
            "produto": nome.value.strip(),
            "codigo": codigo.value.strip(),
            "ncm": ncm.value.strip(),
            "aliquota": aliquota.value.strip(),
            "categoriaFiscal": categoria_tratada
        }
        print("Dados enviados:", dados)
        on_confirmar(dados)
        page.close(dlg)

    def cancelar(e: ft.ControlEvent):
        page.close(dlg)

    save_button = ft.FilledButton(
        text="Salvar",
        on_click=confirmar,
        bgcolor=th["PRIMARY_COLOR"],
        color=th["ON_PRIMARY"],
        disabled=not bool(valores_iniciais.get("produto", ""))
    )

    cancel_button = ft.TextButton(
        text="Cancelar",
        on_click=cancelar
    )

    import_button = ft.FilledButton(
        text="Importar",
        on_click=confirmar,
        bgcolor=th["PRIMARY_COLOR"],
        color=th["ON_PRIMARY"],
        disabled=not bool(valores_iniciais.get("produto", ""))
    )

    header = ft.Row([
        ft.Icon(name="inventory_2", size=24, color=th["PRIMARY_COLOR"]),
        ft.Text(titulo, size=20, weight="bold", color=th["TEXT"])
    ], spacing=8, alignment=ft.MainAxisAlignment.START)

    fields_grid = ft.Row([
        ft.Column([nome, ncm], spacing=12, expand=True),
        ft.Column([codigo, aliquota], spacing=12, expand=True)
    ], spacing=16)

    dlg = ft.AlertDialog(
        modal=True,
        title=header,
        content=ft.Container(
            width=480,
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            content=ft.Column([
                fields_grid,
                categoriaFiscal,
                import_button,
                ft.Divider(height=1, thickness=1, color=th["BORDER"])
            ], spacing=16, scroll=ft.ScrollMode.AUTO)
        ),
        actions=[save_button, cancel_button],
        actions_alignment="end",
        shape=ft.RoundedRectangleBorder(radius=12),
        content_padding=0
    )

    page.open(dlg)
