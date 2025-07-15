import os
import flet as ft
from src.Config import theme
from src.Components.trocaTema import ThemeToggle

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
    usuario_id = getattr(page, "usuario_id", "0")
    is_admin = str(usuario_id) == "1"

    usuario = getattr(page, "usuario_logado", None)

    #print("DEBUG HeaderApp - usuario_id:", usuario_id, "is_admin:", is_admin)

    if not usuario:
        usuario = "usuário"
    
    th = theme.get_theme()

    def logout(e):
        page.go("/login")

    def voltar(e):
        page.go(rota_voltar)

    controles_esquerda = []
    
    if mostrar_logo:
        controles_esquerda.append(
            ft.Image(src=os.path.join("images", "icone.png"), width=40, height=40)
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
    
    if mostrar_usuario and is_admin:
        controles_direita.append(
            ft.IconButton(
                icon="SETTINGS",
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
            ft.Container(
                content=ft.Icon(name="exit_to_app", size=24, color=th["TEXT"]),
                on_click=logout,
                tooltip="Sair",
            )
        )

    conteudo_principal = [
        ft.Row(controles_esquerda, spacing=spacing_esquerda) if controles_esquerda else ft.Container(),
        ft.Row(controles_direita, spacing=spacing_direita) if controles_direita else ft.Container()
    ]

    container_header = ft.Container(
        content=ft.Row(
            conteudo_principal,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=padding_horizontal, vertical=padding_vertical),
        bgcolor=cor_fundo or th["CARD"],
        expand=expand,
        border_radius=ft.border_radius.all(8),
        height=altura_customizada,
        width=largura_maxima,
        margin=ft.margin.symmetric(horizontal=margin_horizontal) if margin_horizontal else None  # NOVO
    )

    if mostrar_divider:
        return ft.Column([
            container_header,
            ft.Divider(color=th["TEXT_SECONDARY"], opacity=0.3, height=1)
        ], spacing=0)
    
    return container_header

def HeaderSimples(page: ft.Page, titulo="", on_theme_changed=None):
    return HeaderApp(
        page=page,
        titulo_tela=titulo,
        on_theme_changed=on_theme_changed,
        mostrar_usuario=False,
        mostrar_theme_toggle=False,
        mostrar_logout=False
    )

def HeaderCompleto(page: ft.Page, titulo="", on_theme_changed=None, mostrar_voltar=True):
    return HeaderApp(
        page=page,
        titulo_tela=titulo,
        on_theme_changed=on_theme_changed,
        mostrar_voltar=mostrar_voltar,
        mostrar_divider=True
    )

def HeaderCustom(page: ft.Page, botoes_extras=None, **kwargs):
    return HeaderApp(
        page=page,
        botoes_customizados=botoes_extras or [],
        **kwargs
    )

def HeaderAlinhado(page: ft.Page, titulo="", on_theme_changed=None, **kwargs):
    return HeaderApp(
        page=page,
        titulo_tela=titulo,
        on_theme_changed=on_theme_changed,
        expand=False,
        largura_maxima=None,
        **kwargs
    )

