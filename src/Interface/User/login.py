import flet as ft
import os
from src.Config import theme
from src.Components.trocaTema import ThemeToggle
from src.Components.notificacao import notificacao

def LoginPage(page: ft.Page):
    print("🟢 Tela Login carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    def entrar(e=None):
        usuario = input_usuario.value.strip()
        senha = input_senha.value.strip()

        botao_entrar.disabled = True
        botao_entrar.text = "Acessando..."
        botao_entrar.bgcolor = theme.current_theme["TEXT_SECONDARY"]
        page.update()

        if usuario == "" and senha == "":
            notificacao(
                page,
                titulo="Login realizado",
                mensagem="Você entrou no sistema com sucesso!",
                tipo="sucesso"
            )

            page.client_storage.set("usuario_logado", usuario)
            
            def navegar_apos_delay():
                page.go("/dashboard")
            
            import threading
            timer = threading.Timer(2.5, navegar_apos_delay)
            timer.start()
            
        else:
            botao_entrar.disabled = False
            botao_entrar.text = "Entrar"
            botao_entrar.bgcolor = theme.current_theme["PRIMARY_COLOR"]
            texto_erro.visible = True
            input_usuario.focus()
            page.update()

    def on_enter_pressed(e):
        entrar()

    def on_usuario_change(e):
        if texto_erro.visible:
            texto_erro.visible = False
            page.update()

    def on_senha_change(e):
        if texto_erro.visible:
            texto_erro.visible = False
            page.update()

    def on_theme_change(novo_tema):
        page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        card_container.bgcolor = theme.current_theme["CARD"]
        titulo_texto.color = theme.current_theme["TEXT"]
        botao_entrar.bgcolor = theme.current_theme["PRIMARY_COLOR"]
        texto_erro.color = theme.current_theme["ERROR"]
        
        input_usuario.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        input_usuario.color = theme.current_theme["TEXT"]
        input_usuario.border_color = theme.current_theme["TEXT_SECONDARY"]
        input_usuario.focused_border_color = theme.current_theme["PRIMARY_COLOR"]
        
        input_senha.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        input_senha.color = theme.current_theme["TEXT"]
        input_senha.border_color = theme.current_theme["TEXT_SECONDARY"]
        input_senha.focused_border_color = theme.current_theme["PRIMARY_COLOR"]
        
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
        
        page.update()

    input_usuario = ft.TextField(
        label="Usuário",
        hint_text="Digite seu usuário",
        width=320,
        border_radius=theme.CARD_RADIUS,
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        color=theme.current_theme["TEXT"],
        border_color=theme.current_theme["TEXT_SECONDARY"],
        focused_border_color=theme.current_theme["PRIMARY_COLOR"],
        prefix_icon="person",
        on_submit=on_enter_pressed, 
        on_change=on_usuario_change,
        autofocus=True,
        text_size=14,
        label_style=ft.TextStyle(color=theme.current_theme["TEXT_SECONDARY"]),
        cursor_color=theme.current_theme["PRIMARY_COLOR"]
    )

    input_senha = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        password=True,
        can_reveal_password=True,
        width=320,
        border_radius=theme.CARD_RADIUS,
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        color=theme.current_theme["TEXT"],
        border_color=theme.current_theme["TEXT_SECONDARY"],
        focused_border_color=theme.current_theme["PRIMARY_COLOR"],
        prefix_icon="lock",
        on_submit=on_enter_pressed,
        on_change=on_senha_change,
        text_size=14,
        label_style=ft.TextStyle(color=theme.current_theme["TEXT_SECONDARY"]),
        cursor_color=theme.current_theme["PRIMARY_COLOR"]
    )

    texto_erro = ft.Text(
        "Usuário ou senha inválidos.",
        color=theme.current_theme["ERROR"],
        visible=False,
        size=12,
        weight="w500"
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
            blur_radius=32, 
            spread_radius=5, 
            color="#00000015", 
            offset=ft.Offset(0, 8)
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
                texto_erro,
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

    toggle_container = ft.Container(
        content=ThemeToggle(page, on_theme_changed=on_theme_change),
        top=20,
        right=20,
        width=55,
        height=35
    )

    layout = ft.Stack(
        controls=[
            main_area,
            #toggle_container
        ],
        expand=True
    )

    return ft.View(
        route="/login",
        controls=[layout],
        bgcolor=theme.current_theme["BACKGROUNDSCREEN"],
        padding=0,
        spacing=0
    )