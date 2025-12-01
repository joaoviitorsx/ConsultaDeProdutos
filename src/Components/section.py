import flet as ft
from src.Config import theme
import datetime
from src.Utils.path import resourcePath

def welcomeSection(usuario_logado, page=None):
    th = theme.get_theme()

    if isinstance(usuario_logado, dict):
        nome = usuario_logado.get("nome") or usuario_logado.get("razaoSocial") or "usuário"
    else:
        nome = usuario_logado or "usuário"

    def getBoas():
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            return "Bom dia"
        elif 12 <= hora < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
    
    def getData():
        hoje = datetime.datetime.now()
        dias_semana = [
            "Segunda-feira", "Terça-feira", "Quarta-feira", 
            "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
        ]
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        dia_semana = dias_semana[hoje.weekday()]
        dia = hoje.day
        mes = meses[hoje.month - 1]
        ano = hoje.year
        
        return f"{dia_semana}, {dia} de {mes} de {ano}"
    
    def getAvatar():
        empresa_id = None
        if hasattr(page, 'selected_empresa_id') and page.selected_empresa_id:
            empresa_id = page.selected_empresa_id
        elif isinstance(usuario_logado, dict) and usuario_logado.get("empresa_id"):
            empresa_id = usuario_logado.get("empresa_id")
        elif isinstance(usuario_logado, dict) and usuario_logado.get("id"):
            empresa_id = usuario_logado.get("id")
        
        logoJM = resourcePath("src/Assets/images/jm.png")
        logoAT = resourcePath("src/Assets/images/atacado.png")
        
        if empresa_id == 3:
            return ft.Container(
                width=128,
                height=128,
                border_radius=64,
                content=ft.Image(src=logoJM, fit=ft.ImageFit.COVER),
                bgcolor=th["ON_PRIMARY"],
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        elif empresa_id == 2:
            return ft.Container(
                width=128,
                height=128,
                border_radius=64,
                content=ft.Image(src=logoAT, fit=ft.ImageFit.SCALE_DOWN),
                bgcolor=th["ON_PRIMARY"],
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            )
        else:
            if isinstance(usuario_logado, dict):
                razao_social = usuario_logado.get("razaoSocial", "")
                nome_usuario = usuario_logado.get("nome", "")
                iniciais = getIniciais(razao_social or nome_usuario)
            else:
                iniciais = getIniciais(nome)
            return ft.CircleAvatar(
                content=ft.Text(iniciais, size=20, weight="bold", color="white"),
                bgcolor=th["PRIMARY_COLOR"],
                radius=64,
            )

    def getIniciais(nome_completo):
        if not nome_completo:
            return "US"
        palavras = nome_completo.strip().split()
        if len(palavras) >= 2:
            return f"{palavras[0][0]}{palavras[1][0]}".upper()
        elif len(palavras) == 1:
            return palavras[0][:2].upper()
        else:
            return "US"

    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    f"{getBoas()}, {nome.capitalize()}!",
                                    size=36,
                                    weight="bold",
                                    color=th["TEXT"]
                                ),
                                ft.Text(
                                    getData(),
                                    size=16,
                                    color=th["TEXT_SECONDARY"],
                                    weight="w500"
                                ),
                                ft.Container(height=8),
                                ft.Text(
                                    "O que você gostaria de fazer hoje?",
                                    size=18,
                                    color=th["TEXT_SECONDARY"]
                                ),
                            ], spacing=4),
                            col={"sm": 12, "md": 9}
                        ),
                        ft.Container(
                            content=getAvatar(),
                            alignment=ft.alignment.center_right,
                            col={"sm": 12, "md": 3},
                            margin=ft.margin.only(top=16)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(32),
                border_radius=20,
                bgcolor=th["CARD"],
            ),
            ft.Container(height=24),
        ], spacing=0),
        margin=ft.margin.only(bottom=32)
    )

def titleSection(titulo, subtitulo=None):
    th = theme.get_theme()
    
    controls = [
        ft.Text(
            titulo, 
            size=24, 
            weight="bold", 
            color=th["TEXT"]
        )
    ]
    
    if subtitulo:
        controls.append(
            ft.Text(
                subtitulo, 
                size=16, 
                color=th["TEXT_SECONDARY"]
            )
        )
    
    return ft.Container(
        content=ft.Column(controls, spacing=4),
        margin=ft.margin.only(bottom=24)
    )

def footer():
    th = theme.get_theme()
    
    return ft.Container(
        content=ft.Column([
            ft.Divider(color=th["TEXT_SECONDARY"], opacity=0.3),
            ft.Container(height=16),
            ft.Row([
                ft.Text(
                    "© 2025 Assertivus Contábil. Todos os direitos reservados.",
                    size=12, 
                    color=th["TEXT_SECONDARY"]
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=8),
            ft.Row([
                ft.Text("Versão 1.0.5", size=10, color=th["TEXT_SECONDARY"]),
                ft.Text("•", size=10, color=th["TEXT_SECONDARY"]),
                ft.Text("Suporte: suporte@realize.com.br", size=10, color=th["TEXT_SECONDARY"]),
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        ]),
        margin=ft.margin.only(top=48)
    )
