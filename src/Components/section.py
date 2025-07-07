import flet as ft
from src.Config import theme
import datetime

def welcomeSection(usuario_logado, page=None):
    th = theme.current_theme
    
    # Obter saudação baseada no horário
    def get_greeting():
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            return "Bom dia"
        elif 12 <= hora < 18:
            return "Boa tarde"
        else:
            return "Boa noite"
    
    # Obter data formatada
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
    
    # Função para ações rápidas
    def ir_para_consulta(e):
        if page:
            page.go("/consulta_fornecedor")
    
    def ir_para_produtos(e):
        if page:
            page.go("/consulta_produtos")
    
    def ir_para_relatorios(e):
        if page:
            page.go("/relatorios")
    
    # Criar ações rápidas
    acoes_rapidas = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Icon("search", color=th["PRIMARY_COLOR"], size=24),
                ft.Text("Nova Consulta", size=12, color=th["TEXT"], weight="w500")
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=12,
            bgcolor=th["CARD"],
            border=ft.border.all(1, th["PRIMARY_COLOR"]),
            on_click=ir_para_consulta,
            tooltip="Consultar novo fornecedor",
            ink=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon("inventory", color="#F03E3E", size=24),
                ft.Text("Produtos", size=12, color=th["TEXT"], weight="w500")
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=12,
            bgcolor=th["CARD"],
            border=ft.border.all(1, "#F03E3E"),
            on_click=ir_para_produtos,
            tooltip="Comparar produtos",
            ink=True
        ),
        ft.Container(
            content=ft.Column([
                ft.Icon("assessment", color="#00C897", size=24),
                ft.Text("Relatórios", size=12, color=th["TEXT"], weight="w500")
            ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=12,
            bgcolor=th["CARD"],
            border=ft.border.all(1, "#00C897"),
            on_click=ir_para_relatorios,
            tooltip="Ver relatórios",
            ink=True
        ),
    ], spacing=16, alignment=ft.MainAxisAlignment.CENTER)
    
    return ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                f"{get_greeting()}, {usuario_logado.capitalize()}!", 
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
                border=ft.border.all(1, th["TEXT_SECONDARY"] + "20"),
            ),
            
            ft.Container(height=24),
        ], spacing=0),
        margin=ft.margin.only(bottom=32)
    )

def welcomeSectionSimple(usuario_logado):
    th = theme.current_theme
    
    return ft.Container(
        content=ft.Column([
            ft.Text(
                f"Bem-vindo, {usuario_logado.capitalize()}", 
                size=32, 
                weight="bold", 
                color=th["TEXT"]
            ),
            ft.Text(
                "O que você deseja fazer hoje?", 
                size=18, 
                color=th["TEXT_SECONDARY"]
            ),
        ], spacing=8),
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