import os
import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao
from src.Controllers.loginController import realizarLogin

def LoginPage(page: ft.Page):
    print("🟢 Tela Login carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    def entrar(e=None):
        usuario = input_usuario.value.strip()
        senha = input_senha.value.strip()

        if not usuario or not senha:
            notificacao(page, "Campos obrigatórios", "Preencha todos os campos.", "erro")
            return

        botao_entrar.disabled = True
        botao_entrar.text = "Acessando.."
        botao_entrar.bgcolor = theme.current_theme["TEXT_SECONDARY"]
        page.update()

        async def login_task():
            try:
                data = await realizarLogin(page, usuario, senha)
                if data and "data" in data and "id" in data["data"]:
                    usuario_id = str(data["data"]["id"])
                    usuario_nome = data["data"]["usuario"]
                    page.usuario_id = usuario_id
                    page.usuario_logado = usuario_nome
                    print("DEBUG Login - usuario_id salvo:", usuario_id)
                    page.go("/dashboard")
                else:
                    notificacao(page, "Erro de login", "Usuário ou senha inválidos.", "erro")
                    print("DEBUG Login - resposta inválida:", data)
            except Exception as ex:
                notificacao(page, "Erro inesperado", str(ex), "erro")
                print("DEBUG Login - exceção:", ex)
            finally:
                resetarBotao()

        page.run_task(login_task)
        
    def resetarBotao():
        botao_entrar.disabled = False
        botao_entrar.text = "Entrar"
        botao_entrar.bgcolor = theme.current_theme["PRIMARY_COLOR"]
        page.update()

    def onEnterPressed(e):
        entrar(e)

    def onUsuarioChange(e):
        page.update()

    def onSenhaChange(e):
        page.update()
    
    def togglePasswordVisibility(e):
        input_senha.password = not input_senha.password
        input_senha.suffix_icon = ft.IconButton(
            icon="visibility_off" if input_senha.password else "visibility",
            icon_color="black",
            on_click=togglePasswordVisibility,
            tooltip="Mostrar/Ocultar senha"
        )
        page.update()

    def on_theme_change(novo_tema):
        page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        card_container.bgcolor = theme.current_theme["CARD"]
        titulo_texto.color = theme.current_theme["TEXT"]
        botao_entrar.bgcolor = theme.current_theme["PRIMARY_COLOR"]
        
        input_usuario.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        input_usuario.color = theme.current_theme["TEXT"]
        input_usuario.border_color = theme.current_theme["TEXT_SECONDARY"]
        input_usuario.focused_border_color = theme.current_theme["PRIMARY_COLOR"]
        input_usuario.prefix_icon = ft.Icon(name="person", color=theme.current_theme["TEXT"])
        
        input_senha.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        input_senha.color = theme.current_theme["TEXT"]
        input_senha.border_color = theme.current_theme["TEXT_SECONDARY"]
        input_senha.focused_border_color = theme.current_theme["PRIMARY_COLOR"]
        input_senha.prefix_icon = ft.Icon(name="lock", color=theme.current_theme["TEXT"])
        
        input_senha.suffix_icon = ft.IconButton(
            icon="visibility_off" if input_senha.password else "visibility",
            icon_color="black", 
            on_click=togglePasswordVisibility,
            tooltip="Mostrar/Ocultar senha"
        )
        
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        
        page.update()

    icone_usuario = ft.Icon(name="person", color=theme.current_theme["TEXT"])
    icone_senha = ft.Icon(name="lock", color=theme.current_theme["TEXT"])

    input_usuario = ft.TextField(
        label="Usuário",
        hint_text="Digite seu usuário",
        width=320,
        border_radius=theme.CARD_RADIUS,
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        color=theme.current_theme["TEXT"],
        border_color=theme.current_theme["TEXT_SECONDARY"],
        focused_border_color=theme.current_theme["PRIMARY_COLOR"],
        prefix_icon=icone_usuario,
        on_submit=onEnterPressed, 
        on_change=onUsuarioChange,
        autofocus=True,
        text_size=14,
        label_style=ft.TextStyle(color=theme.current_theme["TEXT_SECONDARY"]),
        cursor_color=theme.current_theme["PRIMARY_COLOR"]
    )

    input_senha = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        password=True,
        width=320,
        border_radius=theme.CARD_RADIUS,
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        color=theme.current_theme["TEXT"],
        border_color=theme.current_theme["TEXT_SECONDARY"],
        focused_border_color=theme.current_theme["PRIMARY_COLOR"],
        prefix_icon=icone_senha,
        suffix_icon=ft.IconButton(
            icon="visibility_off",
            icon_color="black",
            on_click=togglePasswordVisibility,
            tooltip="Mostrar/Ocultar senha"
        ),
        on_submit=onEnterPressed,
        on_change=onSenhaChange,
        text_size=14,
        label_style=ft.TextStyle(color=theme.current_theme["TEXT_SECONDARY"]),
        cursor_color=theme.current_theme["PRIMARY_COLOR"]
    )

    titulo_texto = ft.Text(
        "Acessar Sistema",
        size=24,
        weight="bold",
        text_align="center",
        color=theme.current_theme["TEXT"],
        style=ft.TextStyle(
            font_family="Roboto",
            letter_spacing=0.5,
            height=1.2
        )
    )

    botao_entrar = ft.ElevatedButton(
        "Entrar",
        on_click=entrar,
        bgcolor=theme.current_theme["PRIMARY_COLOR"],
        color="white",
        width=180,
        height=48,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=theme.CARD_RADIUS),
            text_style=ft.TextStyle(weight="bold", size=16),
            elevation=3,
            animation_duration=200
        )
    )

    logo = os.path.join("images", "logo.png")

    card_container = ft.Container(
        width=420,
        height=580,
        padding=30,
        bgcolor=theme.current_theme["CARD"],
        border_radius=theme.CARD_RADIUS,
        shadow=ft.BoxShadow(
            blur_radius=40,         
            spread_radius=8,         
            color="#00000030",       
            offset=ft.Offset(0, 12)  
        ),
        content=ft.Column(
            controls=[
                ft.Image(src=logo, width=380, height=140),
                ft.Container(height=8),  
                titulo_texto,
                ft.Container(height=8),  
                input_usuario,
                ft.Container(height=4),  
                input_senha,
                ft.Container(height=8),  
                botao_entrar,
                ft.Container(height=4),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12, 
        )
    )

    main_area = ft.Container(
        content=card_container,
        alignment=ft.alignment.center,
        expand=True
    )

    layout = ft.Stack(
        controls=[main_area],
        expand=True
    )

    def inicializar_pagina():
        page.update()
    
    import threading
    threading.Timer(0.1, inicializar_pagina).start()

    return ft.View(
        route="/login",
        controls=[layout],
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        padding=0,
        spacing=0
    )

