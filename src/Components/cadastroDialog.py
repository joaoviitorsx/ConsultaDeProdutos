import re
import flet as ft
from src.Config import theme

def CadastroDialog(
    page: ft.Page,
    titulo: str,
    campos: list[dict],
    on_confirmar,
    valores_iniciais: dict = None
):
    th = theme.get_theme()
    valores_iniciais = valores_iniciais or {}

    inputs = {}

    def _validate(e: ft.ControlEvent):
        for campo in campos:
            nome = campo["name"]
            if campo.get("required") and not inputs[nome].value.strip():
                save_button.disabled = True
                page.update()
                return
        save_button.disabled = False
        page.update()

    layout_campos = []

    for campo in campos:
        tipo = campo.get("type", "text")
        nome = campo["name"]
        label = campo["label"]
        hint = campo.get("hint", "")
        required = campo.get("required", False)
        value = valores_iniciais.get(nome, "")
        expand = campo.get("expand", True)

        if tipo == "dropdown":
            input_field = ft.Dropdown(
                label=label,
                hint_text=hint,
                value=value,
                options=[ft.dropdown.Option(o) for o in campo.get("options", [])],
                border_color=th["BORDER"],
                border_radius=8,
                filled=True,
                expand=expand,
                on_change=_validate if required else None
            )
        elif tipo == "password":
            input_field = ft.TextField(
                label=label,
                hint_text=hint,
                password=True,
                can_reveal_password=True,
                border_color=th["BORDER"],
                bgcolor=th.get("INPUT_BG", th["CARD"]),
                color=th["TEXT"],
                border_radius=8,
                dense=True,
                expand=expand,
                on_change=_validate if required else None
            )
        else:
            input_field = ft.TextField(
                label=label,
                hint_text=hint,
                value=value,
                border_color=th["BORDER"],
                bgcolor=th.get("INPUT_BG", th["CARD"]),
                color=th["TEXT"],
                border_radius=8,
                dense=True,
                expand=expand,
                on_change=_validate if required else None
            )
            
        inputs[nome] = input_field
        layout_campos.append(input_field)

    def confirmar(e: ft.ControlEvent):
        dados = {k: v.value.strip() for k, v in inputs.items()}
        on_confirmar(dados)
        page.close(dlg)

    def cancelar(e: ft.ControlEvent):
        page.close(dlg)

    save_button = ft.FilledButton(
        text="Salvar",
        on_click=confirmar,
        bgcolor=th["PRIMARY_COLOR"],
        color=th["ON_PRIMARY"],
        disabled=True
    )

    cancel_button = ft.TextButton(
        text="Cancelar",
        on_click=cancelar
    )

    _validate(None)

    header = ft.Row([
        ft.Icon(name="inventory_2", size=24, color=th["PRIMARY_COLOR"]),
        ft.Text(titulo, size=20, weight="bold", color=th["TEXT"])
    ], spacing=8, alignment=ft.MainAxisAlignment.START)

    dlg = ft.AlertDialog(
        modal=True,
        title=header,
        content=ft.Container(
            width=480,
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            content=ft.Column(
                layout_campos + [ft.Divider(height=1, thickness=1, color=th["BORDER"])],
                spacing=16,
                scroll=ft.ScrollMode.AUTO
            )
        ),
        actions=[save_button, cancel_button],
        actions_alignment="end",
        shape=ft.RoundedRectangleBorder(radius=12),
        content_padding=0
    )

    page.open(dlg)

