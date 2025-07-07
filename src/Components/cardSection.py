import flet as ft
from src.Config import theme

def CardSection(
    page: ft.Page,
    cards_data=None,
    tipo_card="action",  
    colunas_responsivas=None,
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
        "action_vertical": {
            "colunas": {"sm": 12, "md": 6, "lg": 4},
            "elevacao": 15,
            "padding": 12
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
            card = createActionCard(page, card_data, th, padding_interno, border_radius, altura_customizada, cor_fundo_customizada, border_customizado, animacao)
                                     
                                     
        elif tipo_card == "stats":
            card = createStatsCard(card_data, th, padding_interno, border_radius,altura_customizada, cor_fundo_customizada,border_customizado, animacao)
                                    
                                    
        elif tipo_card == "info":
            card = createInfoCard(card_data, th, padding_interno, border_radius,altura_customizada, cor_fundo_customizada,border_customizado, animacao)
                                   
        else:
            card = createCustomCard(card_data, th, padding_interno, border_radius,altura_customizada, cor_fundo_customizada,border_customizado, animacao, estilo_customizado)
                                     
        if on_hover:
            card.on_hover = on_hover
        
        cards.append(card)
    
    if wrap:
        return ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col=colunas_responsivas,
                    content=card,
                    padding=padding_card
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

def createActionCard(page, card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    hover_scale = ft.Scale(1)
    
    def on_hover(e):
        if animacao:
            hover_scale.scale = 1.03 if e.data == "true" else 1
            page.update()
    
    def on_click(e):
        page.go(card_data.get("rota", "/"))
    
    icon_container = ft.Container(
        content=ft.Icon(
            name=card_data.get("icone", "info"),
            color="white",
            size=32
        ),
        bgcolor=card_data.get("cor", th["PRIMARY_COLOR"]),
        border_radius=12,
        padding=14,
        alignment=ft.alignment.center,
        width=60,
        height=60
    )
    
    content_column = ft.Column([
        ft.Text(
            card_data.get("titulo", ""),
            color=th["TEXT"],
            size=17,
            weight="bold",
            text_align=ft.TextAlign.LEFT,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS
        ),
        ft.Container(height=4),
        ft.Text(
            card_data.get("descricao", ""),
            color=th["TEXT_SECONDARY"],
            size=13,
            text_align=ft.TextAlign.LEFT,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS
        ),
        ft.Container(height=10),
        ft.Column([
            ft.Text(
                f"• {feature}",
                color=th["TEXT_SECONDARY"],
                size=12,
                text_align=ft.TextAlign.LEFT,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS
            ) for feature in card_data.get("features", [])[:3]
        ], spacing=3) if card_data.get("features") else ft.Container(),
        ft.Container(height=10),
    ],
    spacing=0,
    tight=True,
    horizontal_alignment=ft.CrossAxisAlignment.START,
    alignment=ft.MainAxisAlignment.START,
    expand=True
    )
    
    container_content = ft.Row([
        icon_container,
        content_column
    ],
    spacing=20,
    alignment=ft.MainAxisAlignment.START,
    vertical_alignment=ft.CrossAxisAlignment.START
    )
    
    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=ft.padding.all(24),
        border_radius=border_radius or 16,
        height=altura or 320,
        border=border,
        content=container_content,
        on_click=on_click,
        scale=hover_scale,
        animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT) if animacao else None,
        on_hover=on_hover if animacao else None,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#19000000",
            offset=ft.Offset(0, 8),
            spread_radius=0
        ) if animacao else None
    )
    
    return ft.Card(
        elevation=3 if not animacao else 0,
        content=container,
        surface_tint_color=th["CARD"]
    )

def createStatsCard(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    container_content = ft.Column([
        ft.Row([
            ft.Icon(
                name=card_data.get("icone", "info"),
                color=card_data.get("cor", th["PRIMARY_COLOR"]),
                size=24
            ),
            ft.Text(
                card_data.get("titulo", ""),
                color=th["TEXT_SECONDARY"],
                size=14,
                weight="w500",
                text_align=ft.TextAlign.LEFT
            )
        ], alignment=ft.MainAxisAlignment.START, spacing=12),
        
        ft.Container(height=8),
        
        ft.Text(
            card_data.get("valor", "0"),
            color=th["TEXT"],
            size=32,
            weight="bold",
            text_align=ft.TextAlign.LEFT
        ),
        
        ft.Container(height=8),
        
        ft.Row([
            ft.Icon(
                name="trending_up" if card_data.get("tendencia", "up") == "up" else "trending_down",
                color="#22c55e" if card_data.get("tendencia", "up") == "up" else "#ef4444",
                size=18
            ),
            ft.Text(
                card_data.get("variacao", ""),
                color="#22c55e" if card_data.get("tendencia", "up") == "up" else "#ef4444",
                size=13,
                weight="w600",
                text_align=ft.TextAlign.LEFT
            )
        ], spacing=6, alignment=ft.MainAxisAlignment.START) if card_data.get("variacao") else ft.Container()
        
    ], 
    spacing=0, 
    tight=True,
    horizontal_alignment=ft.CrossAxisAlignment.START,
    alignment=ft.MainAxisAlignment.START
    )

    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=ft.padding.all(24),
        border_radius=border_radius or 16,
        height=altura or 140,
        border=border,
        content=container_content
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        container.animate_opacity = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=2,
        content=container,
        surface_tint_color=th["CARD"]
    )

def createInfoCard(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao):
    container_content = ft.Row([
        ft.Container(
            content=ft.Icon(
                name=card_data.get("icone", "info"),
                color=card_data.get("cor", th["PRIMARY_COLOR"]),
                size=28
            ),
            width=50,
            alignment=ft.alignment.center_left
        ),
        ft.Column([
            ft.Text(
                card_data.get("titulo", ""),
                color=th["TEXT"],
                size=15,
                weight="bold",
                text_align=ft.TextAlign.LEFT
            ),
            ft.Container(height=4),
            ft.Text(
                card_data.get("descricao", ""),
                color=th["TEXT_SECONDARY"],
                size=12,
                text_align=ft.TextAlign.LEFT,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS
            ) if card_data.get("descricao") else ft.Container()
        ], 
        spacing=0,
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
        padding=ft.padding.all(20),
        border_radius=border_radius or 12,
        height=altura or 100,
        border=border,
        content=container_content
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=1,
        content=container,
        surface_tint_color=th["CARD"]
    )

def createCustomCard(card_data, th, padding, border_radius, altura, cor_fundo, border, animacao, estilo):
    if estilo and callable(estilo):
        return estilo(card_data, th)
    
    container = ft.Container(
        bgcolor=cor_fundo or th["CARD"],
        padding=ft.padding.all(padding or 20),
        border_radius=border_radius or 16,
        height=altura,
        border=border,
        content=card_data.get("conteudo", ft.Text("Card customizado", text_align=ft.TextAlign.LEFT))
    )
    
    if animacao:
        container.animate_scale = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
    
    return ft.Card(
        elevation=2,
        content=container,
        surface_tint_color=th["CARD"]
    )

def DashboardCards(page: ft.Page, estilo="horizontal", **kwargs):
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
    
    tipo = "action" if estilo == "horizontal" else "action_vertical"
    return CardSection(page, cards_data, tipo_card=tipo, **kwargs)

def StatsCards(page: ft.Page, stats_data, **kwargs):
    return CardSection(page, stats_data, tipo_card="stats", **kwargs)

def InfoCards(page: ft.Page, info_data, **kwargs):
    return CardSection(page, info_data, tipo_card="info", **kwargs)

def CustomCards(page: ft.Page, cards_data, estilo_customizado=None, **kwargs):
    return CardSection(page, cards_data, tipo_card="custom", estilo_customizado=estilo_customizado, **kwargs)
                      
def create_dashboard_cards(page: ft.Page):
    return DashboardCards(page)

def create_stats_section(page: ft.Page, stats_data):
    return StatsCards(page, stats_data)