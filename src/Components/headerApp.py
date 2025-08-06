import os
import flet as ft
from src.Config import theme
from src.Components.trocaTema import ThemeToggle
from src.Utils.path import resourcePath

def HeaderApp(
    page: ft.Page, 
    titulo_tela="", 
    on_theme_changed=None, 
    mostrar_voltar=False, 
    rota_voltar="/dashboard",
    mostrar_logo=True,
    mostrar_nome_empresa=True,
    mostrar_usuario=True,
    mostrar_theme_toggle=True,
    mostrar_logout=True,
    botoes_customizados=None,
    spacing_esquerda=12,
    spacing_direita=16,
    padding_horizontal=24,
    padding_vertical=16,
    mostrar_divider=False,
    cor_fundo=None,
    altura_customizada=None,
    expand=False,                    
    largura_maxima=None,            
    margin_horizontal=None          
):
    # Garantia de conversão segura para string
    usuario_id = str(getattr(page, "usuario_id", "0"))
    is_admin = usuario_id == "1"

    usuario = getattr(page, "usuario_logado", None)
    if not usuario:
        usuario = "usuário"

    # Debug opcional
    # print(f"🛠️ HeaderApp - usuario_id: {usuario_id} | is_admin: {is_admin}")

    th = theme.get_theme()

    def logout(e):
        page.go("/login")

    def voltar(e):
        page.go(rota_voltar)

    controles_esquerda = []
    
    logo = resourcePath("src/Assets/images/icone.png")

    if mostrar_logo:
        controles_esquerda.append(
            ft.Image(src=logo, width=40, height=40)
        )
    
    if mostrar_nome_empresa:
        controles_esquerda.append(
            ft.Text("Assertivus Contábil", size=16, weight="bold", color=th["TEXT"])
        )

    if mostrar_voltar:
        if controles_esquerda: 
            controles_esquerda.append(ft.Container(width=16))
        
        controles_esquerda.extend([
            ft.IconButton(
                icon="arrow_back",
                icon_color=th["TEXT"],
                tooltip="Voltar",
                on_click=voltar
            ),
            ft.Text(titulo_tela, size=20, weight="bold", color=th["TEXT"])
        ])

    controles_direita = []

    # Engrenagem de admin (usuário com ID = 1)
    if mostrar_usuario and is_admin:
        controles_direita.append(
            ft.IconButton(
                icon="SETTINGS_ROUNDED",
                icon_color=th["TEXT_SECONDARY"],
                tooltip="Acessar painel de administração",
                on_click=lambda e: page.go("/admin_dashboard")
            )
        )

    if botoes_customizados:
        controles_direita.extend(botoes_customizados)
    
    if mostrar_theme_toggle:
        controles_direita.append(
            ThemeToggle(page, on_theme_changed=on_theme_changed)
        )
    
    if mostrar_logout:
        controles_direita.append(
            ft.IconButton(
                content=ft.Icon(name="LOGOUT_OUTLINED", size=24, color=th["TEXT"]),
                on_click=logout,
                tooltip="Sair",
            )
        )

    container_header = ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Row(controles_esquerda, spacing=spacing_esquerda),
                    col={"sm": 12, "md": 6}
                ),
                ft.Container(
                    content=ft.Row(controles_direita, spacing=spacing_direita, alignment=ft.MainAxisAlignment.END),
                    col={"sm": 12, "md": 6}
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.symmetric(horizontal=padding_horizontal, vertical=padding_vertical),
        bgcolor=cor_fundo or th["CARD"],
        expand=expand,
        border_radius=ft.border_radius.all(8),
        height=altura_customizada,
        width=largura_maxima,
        margin=ft.margin.symmetric(horizontal=margin_horizontal) if margin_horizontal else None
    )

    if mostrar_divider:
        return ft.Column([container_header, ft.Divider(color=th["TEXT_SECONDARY"], opacity=0.3, height=1)], spacing=0)
    
    return container_header
