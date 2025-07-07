import flet as ft
from src.Config import theme
from src.Components.cardAction import ActionCard

def CardSection(
    page: ft.Page,
    cards_data=None,
    tipo_card="action",  # "action", "stats", "info", "custom"
    colunas_responsivas=None,  # {"sm": 12, "md": 6, "lg": 4}
    spacing=0,
    run_spacing=0,
    padding_card=8,
    elevacao=2,
    border_radius=12,
    mostrar_sombra=True,
    padding_interno=20,
    alignment=ft.MainAxisAlignment.START,
    cross_alignment=ft.CrossAxisAlignment.START,
    wrap=True,
    altura_customizada=None,
    largura_customizada=None,
    cor_fundo_customizada=None,
    border_customizado=None,
    animacao=False,
    on_hover=None,
    estilo_customizado=None
):

    th = theme.current_theme
    
    configs_padrao = {
        "action": {
            "colunas": {"sm": 12, "md": 6, "lg": 4},
            "elevacao": 2,
            "padding": 8
        },
        "stats": {
            "colunas": {"sm": 12, "md": 6, "lg": 3},
            "elevacao": 2,
            "padding": 8
        },
        "info": {
            "colunas": {"sm": 12, "md": 4, "lg": 3},
            "elevacao": 1,
            "padding": 4
        },
        "custom": {
            "colunas": {"sm": 12, "md": 6, "lg": 6},
            "elevacao": 2,
            "padding": 8
        }
    }
    
    config = configs_padrao.get(tipo_card, configs_padrao["custom"])
    if not colunas_responsivas:
        colunas_responsivas = config["colunas"]
    if elevacao is None:
        elevacao = config["elevacao"]
    if padding_card is None:
        padding_card = config["padding"]
    
    if not cards_data:
        return ft.Container()
    
    cards = []
    
    for card_data in cards_data:
        if tipo_card == "action":
            card = _create_action_card(page, card_data, th, padding_interno, border_radius, 
                                     altura_customizada, cor_fundo_customizada, 
                                     border_customizado, animacao)
        elif tipo_card == "stats":
            card = _create_stats_card(card_data, th, padding_interno, border_radius,
                                    altura_customizada, cor_fundo_customizada,
                                    border_customizado, animacao)
        elif tipo_card == "info":
            card = _create_info_card(card_data, th, padding_interno, border_radius,
                                   altura_customizada, cor_fundo_customizada,
                                   border_customizado, animacao)
        else:  # custom
            card = _create_custom_card(card_data, th, padding_interno, border_radius,
                                     altura_customizada, cor_fundo_customizada,
                                     border_customizado, animacao, estilo_customizado)
        
        if on_hover:
            card.on_hover = on_hover
        
        cards.append(card)
    
    if wrap:
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col=colunas_responsivas,
                    content=card,
                    padding=padding_card,
                    width=largura_customizada,
                    height=altura_customizada
                ) for card in cards
            ],
            spacing=spacing,
            run_spacing=run_spacing,
            alignment=alignment
        )
    else:
        return ft.Row(
            controls=cards,
            spacing=spacing,
            alignment=alignment,
            scroll=ft.ScrollMode.AUTO if len(cards) > 4 else None
        )

def _create_action_card(page, card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    # Card clicável
    def on_click(e):
        page.go(card_data.get("rota", "/"))
    
    # Layout horizontal com ícone à esquerda e conteúdo à direita
    container_content = ft.Row([
        # Ícone à esquerda
        ft.Container(
            content=ft.Icon(
                name=card_data.get("icone", "info"),
                color=card_data.get("cor", th["PRIMARY_COLOR"]),
                size=32
            ),
            width=50,
            alignment=ft.alignment.center_left
        ),
        # Conteúdo principal
        ft.Column([
            ft.Text(
                card_data.get("titulo", ""),
                color=th["TEXT"],
                size=16,
                weight="bold",
                text_align=ft.TextAlign.LEFT
            ),
            ft.Text(
                card_data.get("descricao", ""),
                color=th["TEXT_SECONDARY"],
                size=12,
                text_align=ft.TextAlign.LEFT
            ),
            # Features/recursos se existirem
            ft.Column([
                ft.Text(
                    f"• {feature}",
                    color=th["TEXT_SECONDARY"],
                    size=11,
                    text_align=ft.TextAlign.LEFT
                ) for feature in card_data.get("features", [])
            ], spacing=2) if card_data.get("features") else ft.Container()
        ], 
        spacing=4, 
        tight=True,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.START,
        expand=True
        )
    ], 
    spacing=12,
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.START
    )

    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=padding,
        border_radius=border_radius,
        height=altura or 120,  # Altura padrão ajustada
        border=border,
        content=container_content,
        on_click=on_click  # Evento de clique no Container
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        container.animate_opacity = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=2,
        content=container
    )

def _create_stats_card(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    container_content = ft.Column([
        ft.Row([
            ft.Icon(
                name=card_data.get("icone", "info"),
                color=card_data.get("cor", th["PRIMARY_COLOR"]),
                size=20
            ),
            ft.Text(
                card_data.get("titulo", ""),
                color=th["TEXT_SECONDARY"],
                size=14,
                weight="w500",
                text_align=ft.TextAlign.LEFT
            )
        ], alignment=ft.MainAxisAlignment.START, spacing=8),
        
        ft.Text(
            card_data.get("valor", "0"),
            color=th["TEXT"],
            size=28,
            weight="bold",
            text_align=ft.TextAlign.LEFT
        ),
        
        ft.Row([
            ft.Icon(
                name="trending_up" if card_data.get("tendencia", "up") == "up" else "trending_down",
                color="#22c55e" if card_data.get("tendencia", "up") == "up" else "#ef4444",
                size=16
            ),
            ft.Text(
                card_data.get("variacao", ""),
                color="#22c55e" if card_data.get("tendencia", "up") == "up" else "#ef4444",
                size=12,
                weight="w500",
                text_align=ft.TextAlign.LEFT
            )
        ], spacing=4, alignment=ft.MainAxisAlignment.START) if card_data.get("variacao") else ft.Container()
        
    ], 
    spacing=8, 
    tight=True,
    horizontal_alignment=ft.CrossAxisAlignment.START,
    alignment=ft.MainAxisAlignment.START
    )

    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=padding,
        border_radius=border_radius,
        height=altura,
        border=border,
        content=container_content
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        container.animate_opacity = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=2,
        content=container
    )

def _create_info_card(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    container_content = ft.Row([
        # Ícone à esquerda
        ft.Container(
            content=ft.Icon(
                name=card_data.get("icone", "info"),
                color=card_data.get("cor", th["PRIMARY_COLOR"]),
                size=24
            ),
            width=40,
            alignment=ft.alignment.center_left
        ),
        # Conteúdo à direita
        ft.Column([
            ft.Text(
                card_data.get("titulo", ""),
                color=th["TEXT"],
                size=14,
                weight="bold",
                text_align=ft.TextAlign.LEFT
            ),
            ft.Text(
                card_data.get("descricao", ""),
                color=th["TEXT_SECONDARY"],
                size=12,
                text_align=ft.TextAlign.LEFT
            ) if card_data.get("descricao") else ft.Container()
        ], 
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.START,
        expand=True
        )
    ], 
    spacing=8,
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.START
    )

    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=padding,
        border_radius=border_radius,
        height=altura,
        border=border,
        content=container_content
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=1,
        content=container
    )

def _create_custom_card(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao, estilo):
    if estilo and callable(estilo):
        return estilo(card_data, th)
    
    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=padding,
        border_radius=border_radius,
        height=altura,
        border=border,
        content=card_data.get("conteudo", ft.Text("Card customizado", text_align=ft.TextAlign.LEFT))
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=2,
        content=container
    )

def DashboardCards(page: ft.Page, **kwargs):
    cards_data = [
        {
            "titulo": "Consultar Fornecedor",
            "descricao": "Dados cadastrais, situação fiscal e isenções",
            "icone": "business_center",
            "cor": theme.current_theme["PRIMARY_COLOR"],
            "rota": "/consulta_fornecedor",
            "features": ["Dados cadastrais", "Situação fiscal", "Status de isenção"]
        },
        {
            "titulo": "Relatórios Mensais",
            "descricao": "Exportação de dados e filtros por período",
            "icone": "assessment",
            "cor": "#00C897",
            "rota": "/relatorios",
            "features": ["Histórico de consultas", "Exportação em PDF", "Filtros por período"]
        },
        {
            "titulo": "Consultar Produtos",
            "descricao": "Cálculo de impostos e comparação",
            "icone": "inventory",
            "cor": "#F03E3E",
            "rota": "/consulta_produtos",
            "features": ["Cálculo de impostos", "Preços finais", "Comparação entre fornecedores"]
        }
    ]
    
    return CardSection(page, cards_data, tipo_card="action", **kwargs)

def StatsCards(page: ft.Page, stats_data, **kwargs):
    return CardSection(page, stats_data, tipo_card="stats", **kwargs)

def InfoCards(page: ft.Page, info_data, **kwargs):
    return CardSection(page, info_data, tipo_card="info", **kwargs)

def CustomCards(page: ft.Page, cards_data, estilo_customizado=None, **kwargs):
    return CardSection(page, cards_data, tipo_card="custom", 
                      estilo_customizado=estilo_customizado, **kwargs)

def create_dashboard_cards(page: ft.Page):
    return DashboardCards(page)

def create_stats_section(page: ft.Page, stats_data):
    return StatsCards(page, stats_data)