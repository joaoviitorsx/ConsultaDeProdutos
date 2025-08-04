import os
import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao
from src.Controllers.loginController import realizarLogin
from src.Utils.path import resourcePath

def LoginPage(page: ft.Page):
    print("🟢 Tela Login carregada")

    th = theme.apply_theme(page)

    def entrar(e=None):
        usuario = input_usuario.value.strip()
        senha = input_senha.value.strip()

        if not usuario or not senha:
            notificacao(page, "Campos obrigatórios", "Preencha todos os campos.", "erro")
            return

        botao_entrar.disabled = True
        botao_entrar.text = "Acessando..."
        botao_entrar.bgcolor = th["TEXT_SECONDARY"]
        page.update()

        async def login_task():
            try:
                data = await realizarLogin(page, usuario, senha)
                if data and "data" in data and "id" in data["data"]:
                    page.usuario_id = str(data["data"]["id"])
                    page.usuario_logado = data["data"]["usuario"]
                    page.razao_social = data["data"].get("nome")
                    page.selected_empresa_id = data["data"]["empresa_id"]
                    page.usuario_info = {
                        "nome": data["data"].get("nome"),
                        "usuario": data["data"]["usuario"],
                        "empresa_id": data["data"]["empresa_id"]
                    }
                    page.go("/dashboard")
                else:
                    return
            except Exception as ex:
                notificacao(page, "Erro inesperado", str(ex), "erro")
            finally:
                resetar_botao()

        page.run_task(login_task)

    def resetar_botao():
        botao_entrar.disabled = False
        botao_entrar.text = "Entrar"
        botao_entrar.bgcolor = theme.get_theme()["PRIMARY_COLOR"]
        page.update()

    def togglePasswordVisibility(e):
        input_senha.password = not input_senha.password
        atualizar_theme_fields()

    def atualizar_theme_fields():
        th = theme.get_theme()

        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]

        card_container.bgcolor = th["CARD"]
        titulo_texto.color = th["TEXT"]
        botao_entrar.bgcolor = th["PRIMARY_COLOR"]

        input_usuario.bgcolor = th["BACKGROUNDSCREEN"]
        input_usuario.color = th["TEXT"]
        input_usuario.border_color = th["TEXT_SECONDARY"]
        input_usuario.focused_border_color = th["PRIMARY_COLOR"]
        input_usuario.prefix_icon = ft.Icon(name="person", color=th["TEXT"])
        input_usuario.label_style = ft.TextStyle(color=th["TEXT_SECONDARY"])
        input_usuario.cursor_color = th["PRIMARY_COLOR"]

        input_senha.bgcolor = th["BACKGROUNDSCREEN"]
        input_senha.color = th["TEXT"]
        input_senha.border_color = th["TEXT_SECONDARY"]
        input_senha.focused_border_color = th["PRIMARY_COLOR"]
        input_senha.prefix_icon = ft.Icon(name="lock", color=th["TEXT"])
        input_senha.suffix_icon = ft.IconButton(
            icon="visibility_off" if input_senha.password else "visibility",
            icon_color="black",
            on_click=togglePasswordVisibility,
            tooltip="Mostrar/Ocultar senha"
        )
        input_senha.label_style = ft.TextStyle(color=th["TEXT_SECONDARY"])
        input_senha.cursor_color = th["PRIMARY_COLOR"]

        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]

        page.update()

    input_usuario = ft.TextField(
        label="Usuário",
        hint_text="Digite seu usuário",
        width=320,
        border_radius=theme.STYLE["CARD_RADIUS"],
        on_submit=entrar,
        on_change=lambda e: page.update(),
        autofocus=True,
    )

    input_senha = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        password=True,
        width=320,
        border_radius=theme.STYLE["CARD_RADIUS"],
        on_submit=entrar,
        on_change=lambda e: page.update()
    )

    titulo_texto = ft.Text(
        "Acessar Sistema",
        size=24,
        weight="bold",
        text_align="center",
        style=ft.TextStyle(font_family="Roboto", letter_spacing=0.5, height=1.2)
    )

    botao_entrar = ft.ElevatedButton(
        "Entrar",
        on_click=entrar,
        width=180,
        height=48,
        bgcolor=th["PRIMARY_COLOR"],
        color=th["ON_PRIMARY"], 
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=theme.STYLE["CARD_RADIUS"]),
            text_style=ft.TextStyle(weight="bold", size=16),
            elevation=3,
            animation_duration=200
        )
    )

    logo = resourcePath("src/Assets/images/logo.png")

    card_container = ft.Container(
        width=420,
        height=580,
        padding=30,
        border_radius=theme.STYLE["CARD_RADIUS"],
        shadow=ft.BoxShadow(blur_radius=40, spread_radius=8, color="#00000030", offset=ft.Offset(0, 12)),
        content=ft.Column(
            controls=[
                ft.Image(src=logo, width=380, height=140),
                ft.Container(height=8), titulo_texto,
                ft.Container(height=8), input_usuario,
                ft.Container(height=4), input_senha,
                ft.Container(height=8), botao_entrar,
                ft.Container(height=4),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )
    )

    main_area = ft.Container(content=card_container, alignment=ft.alignment.center, expand=True)
    layout = ft.Stack(controls=[main_area], expand=True)

    atualizar_theme_fields()

    return ft.View(
        route="/login",
        controls=[layout],
        bgcolor=theme.get_theme()["BACKGROUNDSCREEN"],
        padding=0,
        spacing=0
    )
