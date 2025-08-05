import time
import httpx
import threading
import flet as ft
from datetime import datetime
from datetime import datetime, timedelta
from src.Config import theme
from src.Components.headerApp import HeaderApp
from src.Components.notificacao import notificacao
from src.Utils.validadores import formatador
from src.Utils.pdf import gerarPdfRelatorio

def ConsultaRelatorioPage(page: ft.Page):
    print("🟡 Tela Consulta Relatórios carregada")
    
    th = theme.get_theme()
    page.bgcolor = th["BACKGROUNDSCREEN"]
    page.window_bgcolor = th["BACKGROUNDSCREEN"]
    
    dados_relatorio = []
    carregando = False
    periodo_selecionado = {"mes": "", "ano": ""}

    def on_theme_change(novo_tema):
        nonlocal th
        th = theme.get_theme()
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
        titulo_secao.content = ft.Column([
            ft.Text("Histórico de Consultas", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Visualize e exporte relatórios das suas consultas tributárias", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8)
        
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

    def consultar_relatorio(e):
        if not combo_mes.value or not combo_ano.value:
            notificacao(page, "Atenção", "Selecione o mês e ano para consulta", "alerta")
            return

        nonlocal carregando, dados_relatorio, periodo_selecionado
        carregando = True
        periodo_selecionado = {"mes": combo_mes.value, "ano": combo_ano.value}

        botao_consultar.disabled = True
        botao_consultar.content = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="white"),
            ft.Text("Consultando...", color="white")
        ], spacing=8)

        atualizar_area_resultados(carregando=True)
        page.update()

        async def processar_consulta():
            try:
                empresa_id = getattr(page, "selected_empresa_id", 1)
                mes_num = int(combo_mes.value[:2])
                ano_num = int(combo_ano.value)
                url = "http://localhost:8000/api/consultas-relatorio"
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url, params={
                        "empresa_id": empresa_id,
                        "mes": mes_num,
                        "ano": ano_num
                    })
                    resp.raise_for_status()
                    dados = resp.json()
                nonlocal dados_relatorio, carregando
                dados_relatorio = [
                    {
                        "data": datetime.strptime(c["dataConsulta"], "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y") if c.get("dataConsulta") else "",
                        "fornecedor": c.get("nomeFornecedor", ""),
                        "cnpj": c.get("cnpjFornecedor", ""),
                        "produto": c.get("produto", ""),
                        "codigo": c.get("codigoProduto", ""),
                        "valor_base": c.get("valorBase", 0.0),
                        "aliquota": c.get("aliquotaAplicada", ""),
                        "adicional": f"{c.get('adicionalSimples', 0)}%" if c.get("adicionalSimples") else "Isento",
                        "total_impostos": (c.get("valorFinal", 0.0) - c.get("valorBase", 0.0)),
                        "valor_final": c.get("valorFinal", 0.0),
                        "regime": c.get("regime") or "Não informado"
                    }
                    for c in dados
                ]
                carregando = False
                notificacao(page, "Sucesso", f"Encontrados {len(dados_relatorio)} registros", "sucesso")
            except Exception as ex:
                notificacao(page, "Erro", f"Erro ao buscar dados: {ex}", "erro")
                dados_relatorio = []
            finally:
                botao_consultar.disabled = False
                botao_consultar.content = ft.Row([
                    ft.Icon(name="search", size=16, color="white"),
                    ft.Text("Consultar", color="white")
                ], spacing=8)
                atualizar_area_resultados()
                page.update()

        page.run_task(processar_consulta)

    def gerar_pdf(e):
        if not dados_relatorio:
            notificacao(page, "Atenção", "Consulte os dados antes de gerar o PDF", "alerta")
            return

        gerarPdfRelatorio(page, dados_relatorio, botao_pdf, notificacao)

    def atualizar_tabela():
        if not dados_relatorio:
            return

        colunas = [
            ft.DataColumn(ft.Text("Data", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Fornecedor", color="white", weight="bold")),
            ft.DataColumn(ft.Text("CNPJ", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Produto", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Código", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Valor Base", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Regime", color="white", weight="bold")),
            ft.DataColumn(ft.Text("Total", color="white", weight="bold"))
        ]

        linhas = []
        for idx, item in enumerate(dados_relatorio):
            cor_regime = th.get("SUCCESS", "#10B981") if "Simples" in item["regime"] else th.get("INFO", "#3B82F6")
            cor_linha = f"{th['CARD']}E" if idx % 2 == 0 else f"{th['BACKGROUNDSCREEN']}"

            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["data"], color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["fornecedor"][:20] + "..." if len(item["fornecedor"]) > 20 else item["fornecedor"], color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["cnpj"], color=th["TEXT"], size=12, font_family="monospace")),
                        ft.DataCell(ft.Text(item["produto"], color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Text(item["codigo"], color=th["TEXT"], size=12, font_family="monospace")),
                        ft.DataCell(ft.Text(formatador(item["valor_base"]), color=th["TEXT"], size=12)),
                        ft.DataCell(ft.Container(
                            content=ft.Text(item["regime"], color="white", size=10, weight="bold"),
                            bgcolor=cor_regime,
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=12
                        )),
                        ft.DataCell(ft.Text(formatador(item["valor_final"]), color=th["TEXT"], size=12, weight="bold"))
                    ],
                    color=cor_linha
                )
            )

        nova_tabela = ft.DataTable(
            columns=colunas,
            rows=linhas,
            heading_row_color=th["PRIMARY_COLOR"],
            heading_row_height=64,
            data_row_color={"even": f"{th['CARD']}E", "odd": th["BACKGROUNDSCREEN"]},
            divider_thickness=1,
            data_row_min_height=50,
            data_row_max_height=50,
            column_spacing=16,
            border=ft.border.all(1, th["PRIMARY_COLOR"]),
            border_radius=12,
            horizontal_margin=32,
        )

        tabela_container.content = ft.Container(
            expand=True,
            padding=0,
            bgcolor="transparent",
            content=ft.Container(
                padding=0,
                bgcolor=th["CARD"],
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=16, color="#00000022", offset=ft.Offset(0, 4)),
                expand=True,
                content=ft.ResponsiveRow([
                    ft.Container(
                        content=nova_tabela,
                        col={"sm": 12, "md": 12, "lg": 12},
                        expand=True
                    )
                ], spacing=0, run_spacing=0, expand=True)
            )
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
                    ft.Text("Selecione um período e clique em 'Consultar' para visualizar os dados", color=th["TEXT_SECONDARY"], text_align="center", size=14)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=64,
                alignment=ft.alignment.center
            )
        else:
            atualizar_tabela()
            resultados_card.content.content = ft.Column([
                ft.Row([
                    ft.Icon(name="assessment", color=th.get("SUCCESS", "#10B981"), size=24),
                    ft.Text("Resultados da Consulta", size=20, weight="bold", color=th["TEXT"]),
                    ft.Container(
                        content=ft.Text(f"{periodo_selecionado['mes']} de {periodo_selecionado['ano']}", color="white", size=12, weight="bold"),     
                        bgcolor=th["PRIMARY_COLOR"],
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=12
                    )
                ], spacing=12),
                ft.Container(height=24),
                tabela_container
            ], spacing=16, expand=True)

            atualizar_tabela()

    header_container = ft.Container(
        content=HeaderApp(
            page, 
            titulo_tela="Relatórios", 
            on_theme_changed=on_theme_change, 
            mostrar_voltar=True,
            mostrar_logo=False, 
            mostrar_nome_empresa=False,
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

    tabela_container = ft.Container(expand=True)

    resultados_card = ft.Card(
        elevation=8,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            expand=True,
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
                alignment=ft.alignment.center,
                expand=True
            )
        )
    )

    return ft.View(
        route="/consulta_relatorio",
        bgcolor=th["BACKGROUNDSCREEN"],
        controls=[
            ft.Container(
                content=ft.Column([
                    header_container,
                    titulo_secao,
                    filtros_card,
                    resultados_card
                ], spacing=24, expand=True),
                padding=24,
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )