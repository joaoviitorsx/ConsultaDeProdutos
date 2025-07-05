import flet as ft
from src.Config import theme


def CardResultado(resultado: dict) -> ft.Card:
    th = theme.current_theme
    
    # Função para formatar moeda
    def format_currency(valor):
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Função para calcular percentual sobre valor total
    def calcular_percentual(valor, total):
        if total == 0:
            return "0,0%"
        return f"{(valor/total)*100:.1f}%".replace('.', ',')
    
    # Paleta de cores que se adapta ao tema
    cores = {
        "melhor_opcao": th.get("SUCCESS", "#10B981"),  # Usar cor do tema
        "melhor_opcao_light": th.get("SUCCESS_LIGHT", "#34D399"),  # Variação mais clara
        "destaque": th.get("WARNING", "#F59E0B"),  # Amarelo/dourado do tema
        "sucesso": th.get("SUCCESS", "#10B981"),  # Verde do tema
        "alerta": th.get("ERROR", "#EF4444"),  # Vermelho do tema
        "neutro": th["TEXT_SECONDARY"],  # Cinza do tema
        "fundo_sutil": th["BACKGROUNDSCREEN"],  # Fundo do tema
        "borda_sutil": f"{th['TEXT_SECONDARY']}30",  # Borda sutil baseada no tema
        "azul_corporativo": th.get("INFO", "#3B82F6"),  # Azul do tema
        "cinza_escuro": th["TEXT"],  # Texto principal do tema
    }
    
    # Cores baseadas no estado que se adaptam ao tema
    cor_borda = cores["melhor_opcao"] if resultado["melhor_opcao"] else cores["borda_sutil"]
    cor_principal = cores["melhor_opcao"] if resultado["melhor_opcao"] else th["TEXT"]
    
    # Cálculos para insights
    total_impostos = resultado["icms"] + resultado["pis"] + resultado["cofins"] + resultado["adicional"]
    percentual_impostos_total = calcular_percentual(total_impostos, resultado["valor_total"])
    economia_vs_sem_isencao = 0
    
    # Se isento, calcular economia hipotética
    if resultado["isento"]:
        valor_base = resultado["valor_produto"]
        icms_simulado = (valor_base * resultado["aliquota_icms"]) / 100
        pis_simulado = (valor_base * resultado["aliquota_pis"]) / 100
        cofins_simulado = (valor_base * resultado["aliquota_cofins"]) / 100
        economia_vs_sem_isencao = icms_simulado + pis_simulado + cofins_simulado

    # Header mais profissional
    header_section = ft.Column(spacing=12)
    
    if resultado["melhor_opcao"]:
        badge_melhor = ft.Container(
            content=ft.Row([
                ft.Icon(name="verified", color="white", size=16),
                ft.Text("MELHOR OPÇÃO FINANCEIRA", color="white", size=12, weight="w700"),
            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=cores["melhor_opcao"],
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            border_radius=8,
            border=ft.border.all(1, cores["melhor_opcao_light"]),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=f"{cores['melhor_opcao']}40",
                offset=ft.Offset(0, 2)
            )
        )
        header_section.controls.append(
            ft.Container(
                content=badge_melhor,
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=12)
            )
        )

    # Informações da empresa - design adaptativo
    cor_regime = cores["sucesso"] if resultado["regime"] == "Simples Nacional" else cores["azul_corporativo"]
    
    empresa_header = ft.Container(
        content=ft.Column([
            # Linha superior com regime e ID
            ft.Row([
                ft.Container(
                    content=ft.Row([
                        ft.Icon("business", color="white", size=14),
                        ft.Text(resultado["regime"], color="white", size=11, weight="w600")
                    ], spacing=4),
                    bgcolor=cor_regime,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=4
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(f"Fornecedor #{resultado['id']}", 
                                   color=cores["neutro"], 
                                   size=10, 
                                   weight="w600"),
                    bgcolor=f"{cores['neutro']}15",
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=4,
                    border=ft.border.all(1, f"{cores['neutro']}30")
                )
            ]),
            
            ft.Container(height=12),
            
            # Informações da empresa
            ft.Column([
                ft.Text(resultado["razao"], 
                       size=15, 
                       weight="w700", 
                       color=cores["cinza_escuro"],
                       max_lines=2,
                       overflow=ft.TextOverflow.ELLIPSIS),
                ft.Text(resultado["fantasia"], 
                       size=12, 
                       color=cores["neutro"],
                       weight="w500"),
                ft.Container(height=6),
                ft.Row([
                    ft.Icon("numbers", color=cores["neutro"], size=12),
                    ft.Text(f"CNPJ: {resultado['cnpj']}", 
                           size=10, 
                           color=cores["neutro"],
                           weight="w500")
                ], spacing=4)
            ], spacing=3)
        ], spacing=0),
        padding=ft.padding.all(16),
        bgcolor=th["CARD"],  # Usar cor do card do tema
        border_radius=8,
        border=ft.border.all(1, cores["borda_sutil"]),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=2,
            color="#00000008" if th["CARD"] == "#FFFFFF" else "#FFFFFF05",  # Sombra adaptativa
            offset=ft.Offset(0, 1)
        )
    )

    # Seção de valores - layout adaptativo
    valores_principais = ft.Container(
        content=ft.Row([
            # Valor Base
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon("attach_money", color=cores["neutro"], size=14),
                            width=24,
                            height=24,
                            bgcolor=f"{cores['neutro']}15",
                            border_radius=12,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Valor Base", size=11, color=cores["neutro"], weight="w600")
                    ], spacing=6),
                    ft.Text(format_currency(resultado["valor_produto"]),
                           size=16,
                           weight="w700",
                           color=cores["cinza_escuro"])
                ], spacing=8),
                expand=True,
                padding=16,
                bgcolor=th["CARD"],  # Background adaptativo
                border_radius=6,
                border=ft.border.all(1, cores["borda_sutil"])
            ),
            
            ft.Container(width=12),
            
            # Valor Total
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon("account_balance_wallet", color="white", size=14),
                            width=24,
                            height=24,
                            bgcolor=cor_principal if resultado["melhor_opcao"] else cores["neutro"],
                            border_radius=12,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Valor Final", size=11, color=cores["neutro"], weight="w600")
                    ], spacing=6),
                    ft.Text(format_currency(resultado["valor_total"]),
                           size=18,
                           weight="w700",
                           color=cor_principal if resultado["melhor_opcao"] else cores["cinza_escuro"])
                ], spacing=8),
                expand=True,
                padding=16,
                bgcolor=f"{cor_principal}08" if resultado["melhor_opcao"] else th["CARD"],
                border_radius=6,
                border=ft.border.all(2, cor_principal) if resultado["melhor_opcao"] else ft.border.all(1, cores["borda_sutil"])
            )
        ]),
        margin=ft.margin.symmetric(vertical=12)
    )

    # Seção de impostos - design adaptativo ao tema
    impostos_section = ft.Container(
        content=ft.Column(spacing=16),
        padding=ft.padding.all(20),
        bgcolor=th["CARD"],  # Background adaptativo
        border_radius=8,
        border=ft.border.all(1, cores["borda_sutil"])
    )

    if resultado["isento"]:
        # Card de isenção adaptativo
        impostos_section.content.controls.extend([
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon("verified_user", color="white", size=20),
                        width=40,
                        height=40,
                        bgcolor=cores["sucesso"],
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text("PRODUTO COM ISENÇÃO FISCAL", 
                               color=cores["sucesso"], 
                               size=13, 
                               weight="w700"),
                        ft.Text("Não há incidência de impostos sobre este item",
                               color=cores["neutro"],
                               size=11,
                               weight="w500")
                    ], expand=True, spacing=3)
                ], spacing=16),
                bgcolor=f"{cores['sucesso']}10",
                padding=20,
                border_radius=8,
                border=ft.border.all(1, f"{cores['sucesso']}30")
            )
        ])
        
        if economia_vs_sem_isencao > 0:
            impostos_section.content.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("trending_up", color=cores["destaque"], size=16),
                        ft.Text(f"Economia estimada: {format_currency(economia_vs_sem_isencao)}",
                               color=cores["destaque"],
                               size=12,
                               weight="w600")
                    ], spacing=8),
                    margin=ft.margin.only(top=12),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    bgcolor=f"{cores['destaque']}10",
                    border_radius=6
                )
            )
    else:
        # Header da seção impostos
        impostos_section.content.controls.extend([
            ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Icon("receipt_long", color=cores["azul_corporativo"], size=16),
                        width=28,
                        height=28,
                        bgcolor=f"{cores['azul_corporativo']}15",
                        border_radius=14,
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Composição Tributária", 
                           size=14, 
                           weight="w700", 
                           color=cores["cinza_escuro"])
                ], spacing=8),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(f"{percentual_impostos_total} do valor total",
                                   color=cores["neutro"],
                                   size=10,
                                   weight="w600"),
                    bgcolor=f"{cores['neutro']}15",
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                    border_radius=4,
                    border=ft.border.all(1, f"{cores['neutro']}30")
                )
            ])
        ])

        # Grid de impostos adaptativo
        impostos_data = [
            ("ICMS", resultado["icms"], resultado["aliquota_icms"], cores["alerta"]),
            ("PIS", resultado["pis"], resultado["aliquota_pis"], cores["azul_corporativo"]),
            ("COFINS", resultado["cofins"], resultado["aliquota_cofins"], cores["destaque"]),
            ("Adicional", resultado["adicional"], 3, cores["neutro"])
        ]

        impostos_grid = ft.Column(spacing=12)
        
        for nome, valor, aliquota, cor in impostos_data:
            if valor > 0 or nome == "ICMS":
                percentual_do_total = calcular_percentual(valor, resultado["valor_total"])
                progresso_width = min((valor / resultado["valor_total"]) * 100, 100) if resultado["valor_total"] > 0 else 0
                
                imposto_card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(nome, color="white", size=9, weight="w700"),
                                bgcolor=cor,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=3
                            ),
                            ft.Container(expand=True),
                            ft.Text(f"Alíq: {aliquota}%", 
                                   color=cores["neutro"], 
                                   size=9,
                                   weight="w600")
                        ]),
                        
                        ft.Row([
                            ft.Text(format_currency(valor),
                                   color=cores["cinza_escuro"],
                                   size=13,
                                   weight="w700"),
                            ft.Container(expand=True),
                            ft.Text(f"({percentual_do_total})",
                                   color=cores["neutro"],
                                   size=10,
                                   weight="w500")
                        ]),
                        
                        # Barra de progresso adaptativa
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    width=f"{progresso_width}%",
                                    height=3,
                                    bgcolor=cor,
                                    border_radius=2
                                )
                            ]),
                            width=float("inf"),
                            height=3,
                            bgcolor=f"{cor}15",
                            border_radius=2
                        )
                    ], spacing=6),
                    padding=ft.padding.all(12),
                    bgcolor=th["CARD"],  # Background adaptativo
                    border_radius=6,
                    border=ft.border.all(1, f"{cor}20")
                )
                
                impostos_grid.controls.append(imposto_card)

        impostos_section.content.controls.append(impostos_grid)

        # Total de impostos - adaptativo ao tema
        impostos_section.content.controls.extend([
            ft.Container(height=8),
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon("calculate", color="white", size=14),
                            width=24,
                            height=24,
                            bgcolor=cores["cinza_escuro"],
                            border_radius=12,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Total Tributário:",
                               color=cores["cinza_escuro"],
                               size=13,
                               weight="w700")
                    ], spacing=8),
                    ft.Container(expand=True),
                    ft.Column([
                        ft.Text(format_currency(total_impostos),
                               color=cores["cinza_escuro"],
                               size=16,
                               weight="w700"),
                        ft.Text(f"({percentual_impostos_total})",
                               color=cores["neutro"],
                               size=10,
                               weight="w500")
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=2)
                ]),
                bgcolor=f"{cores['neutro']}08",
                padding=16,
                border_radius=6,
                border=ft.border.all(1, f"{cores['neutro']}20")
            )
        ])

    # Construir o card final
    card_content = [header_section, empresa_header, valores_principais, impostos_section]

    return ft.Card(
        elevation=8 if resultado["melhor_opcao"] else 4,
        shadow_color=f"{cor_principal}20" if resultado["melhor_opcao"] else (
            "#00000010" if th["CARD"] == "#FFFFFF" else "#FFFFFF05"  # Sombra adaptativa
        ),
        surface_tint_color=f"{cor_principal}05" if resultado["melhor_opcao"] else None,
        content=ft.Container(
            bgcolor=th["CARD"],  # Background adaptativo
            border=ft.border.all(2, cor_borda),
            padding=24,
            border_radius=12,
            content=ft.Column(card_content, spacing=20)
        )
    )