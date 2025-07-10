import flet as ft
from src.Config import theme
import datetime

def welcomeSection(usuario_logado, page=None):
    th = theme.current_theme
    print("DEBUG chamada welcomeSection:", usuario_logado)

    if isinstance(usuario_logado, dict):
        print("Bem-vindo(a) de volta, usuário logado:", usuario_logado)
        nome = usuario_logado.get("razaoSocial", "usuário")
    else:
        nome = usuario_logado or "usuário"

    def get_greeting():
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            return "Bom dia"
        elif 12 <= hora < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
    
    def get_formatted_date():
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
    
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                f"{get_greeting()}, {nome.capitalize()}!",
                                size=36, 
                                weight="bold", 
                                color=th["TEXT"]
                            ),
                        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        
                        ft.Text(
                            get_formatted_date(),
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
                    ], spacing=4, expand=True),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(32),
                border_radius=20,
                bgcolor=th["CARD"],
            ),
            
            ft.Container(height=24),
        ], spacing=0),
        margin=ft.margin.only(bottom=32)
    )

def titleSection(titulo, subtitulo=None):
    th = theme.current_theme
    
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
    th = theme.current_theme
    
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
                ft.Text("Versão 1.0.0", size=10, color=th["TEXT_SECONDARY"]),
                ft.Text("•", size=10, color=th["TEXT_SECONDARY"]),
                ft.Text("Suporte: suporte@realize.com.br", size=10, color=th["TEXT_SECONDARY"]),
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER)
        ]),
        margin=ft.margin.only(top=48)
    )