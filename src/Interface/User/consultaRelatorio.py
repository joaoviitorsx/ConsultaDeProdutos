import flet as ft
from datetime import datetime, timedelta
from src.Config import theme
from src.Components.headerApp import HeaderApp
from src.Components.notificacao import notificacao
import threading
import time

def ConsultaRelatorioPage(page: ft.Page):
    print("🟡 Tela Consulta Relatórios carregada")
    
    th = theme.current_theme
    page.bgcolor = th["BACKGROUNDSCREEN"]
    page.window_bgcolor = th["BACKGROUNDSCREEN"]
    
    # Estados da aplicação
    dados_relatorio = []
    carregando = False
    periodo_selecionado = {"mes": "", "ano": ""}

    def on_theme_change(novo_tema):
        nonlocal th
        th = theme.current_theme
        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]

        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]
        
        header_container.content = HeaderApp(
            page, 
            titulo_tela="Relatórios", 
            on_theme_changed=on_theme_change, 
            mostrar_voltar=True,
            mostrar_logo=False,        
            mostrar_nome_empresa=False 
        )
        
        atualizar_tema_componentes()
        page.update()

    def atualizar_tema_componentes():
        # Atualizar título
        titulo_secao.content = ft.Column([
            ft.Text("Histórico de Consultas", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Visualize e exporte relatórios das suas consultas tributárias", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8)
        
        # Atualizar card de filtros
        filtros_card.content.bgcolor = th["CARD"]
        combo_mes.bgcolor = th["BACKGROUNDSCREEN"]
        combo_mes.color = th["TEXT"]
        combo_mes.border_color = th["TEXT_SECONDARY"]
        combo_mes.focused_border_color = th["PRIMARY_COLOR"]
        
        combo_ano.bgcolor = th["BACKGROUNDSCREEN"]
        combo_ano.color = th["TEXT"]
        combo_ano.border_color = th["TEXT_SECONDARY"]
        combo_ano.focused_border_color = th["PRIMARY_COLOR"]
        
        botao_consultar.bgcolor = th["PRIMARY_COLOR"]
        botao_pdf.bgcolor = th.get("SUCCESS", "#10B981")
        
        resultados_card.content.bgcolor = th["CARD"]
        
        if dados_relatorio:
            atualizar_tabela()

    def format_currency(valor):
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def gerar_dados_mock(mes, ano):
        dados = []
        for i in range(15):
            data_base = datetime(int(ano), int(mes[:2]), 1)
            data_consulta = data_base + timedelta(days=i)
            
            fornecedores = [
                {"nome": "Tech Solutions LTDA", "cnpj": "11.222.333/0001-81"},
                {"nome": "Comercial ABC S/A", "cnpj": "44.555.666/0001-82"},
                {"nome": "Industria XYZ LTDA", "cnpj": "77.888.999/0001-83"},
                {"nome": "Distribuidora DEF ME", "cnpj": "12.345.678/0001-90"}
            ]
            
            fornecedor = fornecedores[i % len(fornecedores)]
            valor_base = 100 + (i * 50)
            aliquota = 12 if i % 2 == 0 else 18
            adicional = 0 if i % 2 == 0 else 3
            total_impostos = (valor_base * aliquota / 100) + (valor_base * adicional / 100)
            valor_final = valor_base + total_impostos
            
            dados.append({
                "data": data_consulta.strftime("%d/%m/%Y"),
                "fornecedor": fornecedor["nome"],
                "cnpj": fornecedor["cnpj"],
                "produto": f"Produto {chr(65 + (i % 10))}",
                "codigo": f"{12345 + i}",
                "valor_base": valor_base,
                "aliquota": f"{aliquota}%",
                "adicional": f"{adicional}%" if adicional > 0 else "Isento",
                "total_impostos": total_impostos,
                "valor_final": valor_final,
                "regime": "Simples Nacional" if i % 2 == 0 else "Lucro Real"
            })
        
        return dados

    def consultar_relatorio(e):
        if not combo_mes.value or not combo_ano.value:
            notificacao(page, "Atenção", "Selecione o mês e ano para consulta", "alerta")
            return
        
        nonlocal carregando, dados_relatorio, periodo_selecionado
        carregando = True
        periodo_selecionado = {"mes": combo_mes.value, "ano": combo_ano.value}
        
        # Atualizar interface
        botao_consultar.disabled = True
        botao_consultar.content = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="white"),
            ft.Text("Consultando...", color="white")
        ], spacing=8)
        
        atualizar_area_resultados(carregando=True)
        page.update()
        
        def processar_consulta():
            time.sleep(2)
            
            nonlocal dados_relatorio, carregando
            dados_relatorio = gerar_dados_mock(combo_mes.value, combo_ano.value)
            carregando = False
            
            botao_consultar.disabled = False
            botao_consultar.content = ft.Row([
                ft.Icon(name="search", size=16, color="white"),
                ft.Text("Consultar", color="white")
            ], spacing=8)
            
            atualizar_area_resultados()
            
            notificacao(page, "Sucesso", f"Encontrados {len(dados_relatorio)} registros", "sucesso")
            page.update()
        
        threading.Thread(target=processar_consulta).start()

    def gerar_pdf(e):
        if not dados_relatorio:
            notificacao(page, "Atenção", "Consulte os dados antes de gerar o PDF", "alerta")
            return
        
        botao_pdf.disabled = True
        botao_pdf.content = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="white"),
            ft.Text("Gerando...", color="white")
        ], spacing=8)
        page.update()
        
        def processar_pdf():
            time.sleep(3)
            
            botao_pdf.disabled = False
            botao_pdf.content = ft.Row([
                ft.Icon(name="picture_as_pdf", size=16, color="white"),
                ft.Text("Gerar PDF", color="white")
            ], spacing=8)
            
            notificacao(page, "PDF Gerado", "Relatório exportado com sucesso!", "sucesso")
            page.update()
        
        threading.Thread(target=processar_pdf).start()

    def atualizar_tabela():
        if not dados_relatorio:
            return
        
        colunas = [
            ft.DataColumn(ft.Text("Data", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Fornecedor", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("CNPJ", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Produto", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Código", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Valor Base", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Regime", color=th["TEXT"], weight="bold")),
            ft.DataColumn(ft.Text("Total", color=th["TEXT"], weight="bold"))
        ]
        
        linhas = []
        for item in dados_relatorio:
            cor_regime = th.get("SUCCESS", "#10B981") if "Simples" in item["regime"] else th.get("INFO", "#3B82F6")
            
            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["data"], color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["fornecedor"][:20] + "..." if len(item["fornecedor"]) > 20 else item["fornecedor"], 
                                          color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["cnpj"], color=th["TEXT"], size=12, font_family="monospace")),
                        ft.DataCell(ft.Text(item["produto"], color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["codigo"], color=th["TEXT"], size=12, font_family="monospace")),
                        ft.DataCell(ft.Text(format_currency(item["valor_base"]), color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(item["regime"], color="white", size=10, weight="bold"),
                            bgcolor=cor_regime,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12
                        )),
                        ft.DataCell(ft.Text(format_currency(item["valor_final"]), color=th["TEXT"], size=12, weight="bold"))
                    ]
                )
            )
        
        nova_tabela = ft.DataTable(
            columns=colunas,
            rows=linhas,
            heading_row_color=f"{th['PRIMARY_COLOR']}20",
            data_row_color={"": "transparent", ft.ControlState.HOVERED: f"{th['TEXT_SECONDARY']}10"},
            divider_thickness=1,
            data_row_min_height=50,
            data_row_max_height=50,
            column_spacing=20,
            border=ft.border.all(1, f"{th['TEXT_SECONDARY']}30"),
            border_radius=8
        )
        
        tabela_container.content = ft.Container(
            content=nova_tabela,
            padding=16,
            bgcolor=th["BACKGROUNDSCREEN"],
            border_radius=8
        )

    def atualizar_area_resultados(carregando=False):
        if carregando:
            resultados_card.content.content = ft.Container(
                content=ft.Column([
                    ft.ProgressRing(width=48, height=48, stroke_width=4, color=th["PRIMARY_COLOR"]),
                    ft.Text("Carregando dados...", size=16, color=th["TEXT"], text_align="center"),
                    ft.Text("Aguarde enquanto buscamos suas consultas", size=14, color=th["TEXT_SECONDARY"], text_align="center")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                padding=64,
                alignment=ft.alignment.center
            )
        elif not dados_relatorio:
            resultados_card.content.content = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(name="assessment", size=48, color=th["TEXT_SECONDARY"]),
                        bgcolor=th["BACKGROUNDSCREEN"],
                        width=96,
                        height=96,
                        border_radius=48,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=16),
                        border=ft.border.all(1, th["TEXT_SECONDARY"])
                    ),
                    ft.Text("Nenhum relatório encontrado", size=20, weight="bold", color=th["TEXT"], text_align="center"),
                    ft.Text("Selecione um período e clique em 'Consultar' para visualizar os dados", 
                            color=th["TEXT_SECONDARY"], text_align="center", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=64,
                alignment=ft.alignment.center
            )
        else:
            total_consultas = len(dados_relatorio)
            valor_total = sum(item["valor_final"] for item in dados_relatorio)
            total_impostos = sum(item["total_impostos"] for item in dados_relatorio)
            
            stats_row = ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(str(total_consultas), size=24, weight="bold", color=th["PRIMARY_COLOR"]),
                        ft.Text("Consultas", size=14, color=th["TEXT_SECONDARY"])
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor=f"{th['PRIMARY_COLOR']}10",
                    padding=16,
                    border_radius=8,
                    border=ft.border.all(1, f"{th['PRIMARY_COLOR']}30"),
                    expand=True
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(format_currency(valor_total), size=20, weight="bold", color=th.get("SUCCESS", "#10B981")),
                        ft.Text("Valor Total", size=14, color=th["TEXT_SECONDARY"])
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor=f"{th.get('SUCCESS', '#10B981')}10",
                    padding=16,
                    border_radius=8,
                    border=ft.border.all(1, f"{th.get('SUCCESS', '#10B981')}30"),
                    expand=True
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(format_currency(total_impostos), size=20, weight="bold", color=th.get("WARNING", "#F59E0B")),
                        ft.Text("Total Impostos", size=14, color=th["TEXT_SECONDARY"])
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor=f"{th.get('WARNING', '#F59E0B')}10",
                    padding=16,
                    border_radius=8,
                    border=ft.border.all(1, f"{th.get('WARNING', '#F59E0B')}30"),
                    expand=True
                )
            ], spacing=16)
            
            resultados_card.content.content = ft.Column([
                ft.Row([
                    ft.Icon(name="assessment", color=th.get("SUCCESS", "#10B981"), size=24),
                    ft.Text("Resultados da Consulta", size=20, weight="bold", color=th["TEXT"]),
                    ft.Container(
                        content=ft.Text(f"{periodo_selecionado['mes']} de {periodo_selecionado['ano']}", 
                                      color="white", size=12, weight="bold"),
                        bgcolor=th["PRIMARY_COLOR"],
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=12
                    )
                ], spacing=12),
                
                ft.Container(height=16),
                
                stats_row,
                
                ft.Container(height=16),
                
                ft.Container(
                    content=tabela_container,
                    height=400,
                    padding=0
                )
            ], spacing=16)
            
            atualizar_tabela()

    header_container = ft.Container(
        content=HeaderApp(
            page, 
            titulo_tela="Relatórios", 
            on_theme_changed=on_theme_change, 
            mostrar_voltar=True,
            mostrar_logo=False, 
            mostrar_nome_empresa=False
        )
    )

    titulo_secao = ft.Container(
        content=ft.Column([
            ft.Text("Histórico de Consultas", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Visualize e exporte relatórios das suas consultas tributárias", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8),
        margin=ft.margin.only(bottom=32)
    )

    data_atual = datetime.now()
    mes_atual = f"{data_atual.month:02d} - {['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][data_atual.month-1]}"
    
    anos = [str(data_atual.year - i) for i in range(2, -1, -1)]
    meses = [
        "01 - Janeiro", "02 - Fevereiro", "03 - Março", "04 - Abril", "05 - Maio", "06 - Junho",
        "07 - Julho", "08 - Agosto", "09 - Setembro", "10 - Outubro", "11 - Novembro", "12 - Dezembro"
    ]

    combo_mes = ft.Dropdown(
        label="Selecione o Mês",
        options=[ft.dropdown.Option(m) for m in meses],
        value=mes_atual,
        width=200,
        border_radius=8,
        bgcolor=th["BACKGROUNDSCREEN"],
        color=th["TEXT"],
        border_color=th["TEXT_SECONDARY"],
        focused_border_color=th["PRIMARY_COLOR"]
    )

    combo_ano = ft.Dropdown(
        label="Selecione o Ano",
        options=[ft.dropdown.Option(a) for a in anos],
        value=str(data_atual.year),
        width=150,
        border_radius=8,
        bgcolor=th["BACKGROUNDSCREEN"],
        color=th["TEXT"],
        border_color=th["TEXT_SECONDARY"],
        focused_border_color=th["PRIMARY_COLOR"]
    )

    botao_consultar = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name="search", size=16, color="white"),
            ft.Text("Consultar", color="white", weight="bold")
        ], spacing=8),
        on_click=consultar_relatorio,
        bgcolor=th["PRIMARY_COLOR"],
        height=56,
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        )
    )

    botao_pdf = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name="picture_as_pdf", size=16, color="white"),
            ft.Text("Gerar PDF", color="white", weight="bold")
        ], spacing=8),
        on_click=gerar_pdf,
        bgcolor=th.get("SUCCESS", "#10B981"),
        height=56,
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        )
    )

    filtros_card = ft.Card(
        elevation=4,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            content=ft.Column([
                ft.Row([
                    ft.Icon(name="filter_alt", color=th["PRIMARY_COLOR"], size=24),
                    ft.Text("Filtros de Consulta", size=18, weight="bold", color=th["TEXT"])
                ], spacing=12),
                
                ft.Container(height=16),
                
                ft.Row([
                    combo_mes,
                    combo_ano,
                    botao_consultar,
                    botao_pdf
                ], spacing=16, alignment=ft.MainAxisAlignment.START)
            ], spacing=8)
        )
    )

    tabela_container = ft.Container()

    resultados_card = ft.Card(
        elevation=4,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            height=600,
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(name="assessment", size=48, color=th["TEXT_SECONDARY"]),
                        bgcolor=th["BACKGROUNDSCREEN"],
                        width=96,
                        height=96,
                        border_radius=48,
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=16),
                        border=ft.border.all(1, th["TEXT_SECONDARY"])
                    ),
                    ft.Text("Pronto para consultar", size=20, weight="bold", color=th["TEXT"], text_align="center"),
                    ft.Text("Selecione um período e clique em 'Consultar' para visualizar os dados", 
                            color=th["TEXT_SECONDARY"], text_align="center", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=64,
                alignment=ft.alignment.center
            )
        )
    )

    return ft.View(
        route="/consulta_relatorio",
        bgcolor=th["BACKGROUNDSCREEN"],
        controls=[
            ft.Column([
                header_container,
                ft.Container(
                    content=ft.Column([
                        titulo_secao,
                        filtros_card,
                        resultados_card
                    ], spacing=24),
                    padding=24,
                    expand=True
                )
            ])
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )