import flet as ft
from src.Config import theme
from src.Components.cardResultado import CardResultado
from src.Components.cardFornecedor import CardFornecedor
from src.Components.notificacao import notificacao
from src.Components.headerApp import HeaderApp
import time
import threading

def ConsultaProdutosPage(page: ft.Page):
    print("🔵 Tela Consulta Produtos carregada")
    
    th = theme.current_theme

    page.bgcolor = th["BACKGROUNDSCREEN"]
    page.window_bgcolor = th["BACKGROUNDSCREEN"]
    
    fornecedores_data = [{"id": "1", "cnpj": "", "codigo_produto": "", "valor_produto": "", "processando": False}]
    resultados_data = []
    processamento_global = False

    def onThemeChange(novo_tema):
        nonlocal th
        th = theme.current_theme
        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]

        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]
        
        header_container.content = HeaderApp(
            page, 
            titulo_tela="Consultar Produtos", 
            on_theme_changed=onThemeChange, 
            mostrar_voltar=True,
            mostrar_logo=False,        
            mostrar_nome_empresa=False 
        )
        atualizar_paineis_tema()
        atualizar_painel_fornecedores()
        atualizar_resultados()
        
        page.update()

    header_container = ft.Container(
        content=HeaderApp(
            page, 
            titulo_tela="Consultar Produtos", 
            on_theme_changed=onThemeChange, 
            mostrar_voltar=True,
            mostrar_logo=False, 
            mostrar_nome_empresa=False
        )
    )

    def format_currency(valor):
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def simular_dados_fornecedor(cnpj):
        dados_mock = {
            "11.222.333/0001-81": {"razao": "Tech Solutions LTDA", "fantasia": "TechSol", "regime": "Simples Nacional"},
            "44.555.666/0001-82": {"razao": "Comercial ABC S/A", "fantasia": "ABC Corp", "regime": "Lucro Real"},
            "77.888.999/0001-83": {"razao": "Industria XYZ LTDA", "fantasia": "XYZ Ind", "regime": "Simples Nacional"},
            "12.345.678/0001-90": {"razao": "Distribuidora DEF ME", "fantasia": "DEF Dist", "regime": "Simples Nacional"}
        }
        
        return dados_mock.get(cnpj, {
            "razao": "Empresa Exemplo LTDA",
            "fantasia": "Exemplo Corp", 
            "regime": "Simples Nacional"
        })
    
    def calcular_impostos(fornecedor):
        time.sleep(1.5)
        
        try:
            valor = float(fornecedor["valor_produto"].replace(',', '.'))
        except:
            raise ValueError("Valor inválido")
            
        dados = simular_dados_fornecedor(fornecedor["cnpj"])
        
        is_simples = dados["regime"] == "Simples Nacional"
        aliquota_icms = 12 if is_simples else 18
        aliquota_pis = 0 if is_simples else 1.65
        aliquota_cofins = 0 if is_simples else 7.6
        adicional = 0 if is_simples else 3
        
        icms = (valor * aliquota_icms) / 100
        pis = (valor * aliquota_pis) / 100
        cofins = (valor * aliquota_cofins) / 100
        valor_adicional = (valor * adicional) / 100
        valor_total = valor + icms + pis + cofins + valor_adicional

        isento = fornecedor["codigo_produto"] in ["12345", "99999"]
        
        return {
            "id": fornecedor["id"],
            "cnpj": fornecedor["cnpj"],
            "razao": dados["razao"],
            "fantasia": dados["fantasia"],
            "regime": dados["regime"],
            "valor_produto": valor,
            "icms": 0 if isento else icms,
            "pis": 0 if isento else pis,
            "cofins": 0 if isento else cofins,
            "adicional": 0 if isento else valor_adicional,
            "valor_total": valor if isento else valor_total,
            "aliquota_icms": aliquota_icms,
            "aliquota_pis": aliquota_pis,
            "aliquota_cofins": aliquota_cofins,
            "isento": isento,
            "melhor_opcao": False
        }
    
    def atualizar_fornecedor(index, campo, valor):
        if index < len(fornecedores_data):
            fornecedores_data[index][campo] = valor
            page.update()
    
    def atualizar_paineis_tema():
        nonlocal painel_fornecedores, resultados_card, titulo_secao, botao_processar_todos
        
        th = theme.current_theme

        titulo_secao.content = ft.Column([
            ft.Text("Comparação de Fornecedores", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Analise impostos e encontre a melhor opção para sua compra", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8)
        
        botao_processar_todos.bgcolor = th.get("SUCCESS", "#10B981")
        
        painel_fornecedores.content = ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            height=700,
            content=ft.Column([
                ft.Row([
                    ft.Row([
                        ft.Icon(name="business", color=th["PRIMARY_COLOR"], size=24),
                        ft.Text("Cadastro de Fornecedores", size=20, weight="bold", color=th["TEXT"])
                    ], spacing=12),
                    ft.Container(
                        content=ft.Text(f"{len(fornecedores_data)}/4", color=th["TEXT_SECONDARY"], size=14),
                        bgcolor="transparent",
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border=ft.border.all(1, th["TEXT_SECONDARY"]),
                        border_radius=4
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Text("Adicione até 4 fornecedores para comparar impostos e valores", 
                    color=th["TEXT_SECONDARY"], size=14),
                
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Column([fornecedores_container], scroll=ft.ScrollMode.AUTO),
                    height=520, 
                ),
                ft.Container(
                    content=botao_processar_todos,
                    margin=ft.margin.only(top=16),
                    height=48
                )
            ], spacing=16)
        )
        
        resultados_card.content = ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            height=700,
            content=ft.Column([
                ft.Row([
                    ft.Icon(name="assessment", color=th.get("SUCCESS", "#10B981"), size=24),
                    ft.Text("Resultado da Análise", size=20, weight="bold", color=th["TEXT"]),
                    ft.Container(
                        content=ft.Text(f"{len(resultados_data)} resultado{'s' if len(resultados_data) != 1 else ''}", 
                                    color="white", size=12, weight="bold"),
                        bgcolor=th.get("SUCCESS", "#10B981"),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12,
                        visible=len(resultados_data) > 0
                    )
                ], spacing=12),
                
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Column([painel_resultados], scroll=ft.ScrollMode.AUTO),
                    height=620,
                )
            ], spacing=16)
        )

    def processar_fornecedor(fornecedor_id):
        fornecedor = next((f for f in fornecedores_data if f["id"] == fornecedor_id), None)
        if not fornecedor or not all([fornecedor["cnpj"], fornecedor["codigo_produto"], fornecedor["valor_produto"]]):
            notificacao(page, "Atenção", "Preencha todos os campos antes de processar!", "alerta")
            return
        
        if len(fornecedor["cnpj"].replace(".", "").replace("/", "").replace("-", "")) != 14:
            notificacao(page, "CNPJ Inválido", "O CNPJ deve ter 14 dígitos", "erro")
            return
        
        for f in fornecedores_data:
            if f["id"] == fornecedor_id:
                f["processando"] = True
                break
        atualizar_painel_fornecedores()
        
        def processar():
            try:
                resultado = calcular_impostos(fornecedor)
                
                nonlocal resultados_data
                resultados_data = [r for r in resultados_data if r["id"] != fornecedor_id]
                resultados_data.append(resultado)
                
                if len(resultados_data) > 1:
                    min_total = min(r["valor_total"] for r in resultados_data)
                    for r in resultados_data:
                        r["melhor_opcao"] = r["valor_total"] == min_total
                else:
                    resultados_data[0]["melhor_opcao"] = True
                
                notificacao(page, "Sucesso", f"Fornecedor #{fornecedor_id} processado com sucesso!", "sucesso")
                
                atualizar_paineis_tema()
                atualizar_resultados()
                
            except Exception as e:
                notificacao(page, "Erro", f"Erro ao processar fornecedor: {str(e)}", "erro")
                print(f"Erro ao processar fornecedor: {e}")
            finally:
                for f in fornecedores_data:
                    if f["id"] == fornecedor_id:
                        f["processando"] = False
                        break
                atualizar_painel_fornecedores()
        
        threading.Thread(target=processar).start()
    
    def remover_fornecedor(fornecedor_id):
        nonlocal fornecedores_data, resultados_data
        
        if fornecedor_id == "1":
            notificacao(page, "Ação Bloqueada", "O Fornecedor #1 não pode ser removido", "alerta")
            return
        
        if len(fornecedores_data) > 1:
            fornecedor_removido = next((f for f in fornecedores_data if f["id"] == fornecedor_id), None)
            fornecedores_data = [f for f in fornecedores_data if f["id"] != fornecedor_id]
            resultados_data = [r for r in resultados_data if r["id"] != fornecedor_id]
            
            if len(resultados_data) > 0:
                min_total = min(r["valor_total"] for r in resultados_data)
                for r in resultados_data:
                    r["melhor_opcao"] = r["valor_total"] == min_total
            
            atualizar_paineis_tema()
            atualizar_painel_fornecedores()
            atualizar_resultados()
            
            if fornecedor_removido:
                notificacao(page, "Fornecedor Removido", f"Fornecedor #{fornecedor_id} foi removido", "info")

    def contar_fornecedores_validos():
        return len([f for f in fornecedores_data if all([f["cnpj"], f["codigo_produto"], f["valor_produto"]])])
    
    def atualizar_resultados():
        th = theme.current_theme
        painel_resultados.controls.clear()
        
        if not resultados_data:
            painel_resultados.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(name="calculate", size=48, color=th["TEXT_SECONDARY"]),
                            bgcolor=th["CARD"],
                            width=96,
                            height=96,
                            border_radius=48,
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(bottom=16),
                            border=ft.border.all(1, th["TEXT_SECONDARY"])
                        ),
                        ft.Text("Aguardando Processamento", 
                            size=20, weight="bold", color=th["TEXT"], text_align="center"),
                        ft.Text("Processe pelo menos um fornecedor para ver os resultados da análise tributária", 
                            color=th["TEXT_SECONDARY"], text_align="center", size=14),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=64,
                    alignment=ft.alignment.center
                )
            )
        else:
            if len(resultados_data) > 1:
                economia_maxima = max(r["valor_total"] for r in resultados_data) - min(r["valor_total"] for r in resultados_data)
                success_color = th.get("SUCCESS", "#10B981")
                
                economia_card = ft.Container(
                    content=ft.Row([
                        ft.Icon("emoji_events", color=success_color, size=20),
                        ft.Text(f"Economia de até {format_currency(economia_maxima)}", 
                            color=success_color, weight="bold", size=16)
                    ], spacing=8),
                    bgcolor=f"{success_color}1A",
                    padding=16,
                    border_radius=8,
                    border=ft.border.all(1, f"{success_color}4D"), 
                    margin=ft.margin.only(bottom=16)
                )
                painel_resultados.controls.append(economia_card)
            
            for resultado in sorted(resultados_data, key=lambda x: x["valor_total"]):
                painel_resultados.controls.append(CardResultado(resultado))
        
        page.update()
    
    def adicionar_fornecedor(e):
        if len(fornecedores_data) < 4:
            novo_id = str(len(fornecedores_data) + 1)
            fornecedores_data.append({
                "id": novo_id,
                "cnpj": "",
                "codigo_produto": "",
                "valor_produto": "",
                "processando": False
            })
            atualizar_paineis_tema()
            atualizar_painel_fornecedores()
            notificacao(page, "Fornecedor Adicionado", f"Fornecedor #{novo_id} adicionado com sucesso!", "info")
    
    def processar_todos(e):
        nonlocal processamento_global
        
        fornecedores_validos = [
            f for f in fornecedores_data 
            if all([f["cnpj"], f["codigo_produto"], f["valor_produto"]])
        ]
        
        if not fornecedores_validos:
            notificacao(page, "Atenção", "Preencha pelo menos um fornecedor antes de processar!", "alerta")
            return
        
        processamento_global = True
        atualizar_botao_processar_todos()
        
        notificacao(page, "Processamento Iniciado", f"Processando {len(fornecedores_validos)} fornecedores...", "info")
        
        def processar_sequencial():
            try:
                for fornecedor in fornecedores_validos:
                    if not fornecedor["processando"]:
                        processar_fornecedor(fornecedor["id"])
                        time.sleep(0.5)
                
                while any(f["processando"] for f in fornecedores_data):
                    time.sleep(0.1)
                
                notificacao(page, "Concluído", "Todos os fornecedores foram processados!", "sucesso")
                
            finally:
                nonlocal processamento_global
                processamento_global = False
                atualizar_botao_processar_todos()
        
        threading.Thread(target=processar_sequencial).start()
    
    def atualizar_botao_processar_todos():
        th = theme.current_theme
        fornecedores_validos = contar_fornecedores_validos()
        
        botao_processar_todos.disabled = processamento_global or fornecedores_validos < 2
        botao_processar_todos.visible = fornecedores_validos > 1
        botao_processar_todos.bgcolor = th.get("SUCCESS", "#10B981")
        botao_processar_todos.content = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="white") if processamento_global else ft.Icon(name="calculate", size=16, color="white"),
            ft.Text(f"Processando..." if processamento_global else f"Processar Todos ({fornecedores_validos})", color="white")
        ], spacing=8)
        page.update()
    
    def atualizar_painel_fornecedores():
        th = theme.current_theme
        fornecedores_container.controls.clear()
        
        for i, fornecedor in enumerate(fornecedores_data):
            card = CardFornecedor(
                fornecedor=fornecedor,
                index=i,
                total=len(fornecedores_data),
                on_update=atualizar_fornecedor,
                on_processar=processar_fornecedor,
                on_remover=remover_fornecedor
            )
            fornecedores_container.controls.append(card)
        
        if len(fornecedores_data) < 4:
            botao_adicionar = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(name="add", size=16, color=th["TEXT_SECONDARY"]),
                    ft.Text(f"Adicionar Fornecedor ({len(fornecedores_data)}/4)", 
                        color=th["TEXT_SECONDARY"], weight="bold")
                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                on_click=adicionar_fornecedor,
                bgcolor="transparent",
                width=float("inf"),
                height=48,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, th["TEXT_SECONDARY"]),
                    shape=ft.RoundedRectangleBorder(radius=8),
                    overlay_color={ft.ControlState.HOVERED: th["CARD"]}
                )
            )
            fornecedores_container.controls.append(botao_adicionar)
        
        atualizar_botao_processar_todos()
        page.update()

    titulo_secao = ft.Container(
        content=ft.Column([
            ft.Text("Comparação de Fornecedores", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Analise impostos e encontre a melhor opção para sua compra", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8),
        margin=ft.margin.only(bottom=32)
    )

    fornecedores_container = ft.Column(spacing=24)
    
    botao_processar_todos = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name="calculate", size=16, color="white"),
            ft.Text("Processar Todos", color="white")
        ], spacing=8),
        on_click=processar_todos,
        bgcolor=th.get("SUCCESS", "#10B981"),
        disabled=True,
        visible=False,
        width=float("inf"),
        height=48,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            overlay_color={ft.ControlState.HOVERED: th.get("SUCCESS", "#10B981")}
        )
    )
    
    painel_fornecedores = ft.Card(
        elevation=8,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            height=700,
            content=ft.Column([
                ft.Row([
                    ft.Row([
                        ft.Icon(name="business", color=th["PRIMARY_COLOR"], size=24),
                        ft.Text("Cadastro de Fornecedores", size=20, weight="bold", color=th["TEXT"])
                    ], spacing=12),
                    ft.Container(
                        content=ft.Text(f"{len(fornecedores_data)}/4", color=th["TEXT_SECONDARY"], size=14),
                        bgcolor="transparent",
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border=ft.border.all(1, th["TEXT_SECONDARY"]),
                        border_radius=4
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Text("Adicione até 4 fornecedores para comparar impostos e valores", 
                    color=th["TEXT_SECONDARY"], size=14),
                
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Column([fornecedores_container], scroll=ft.ScrollMode.AUTO),
                    height=520,
                ),
                ft.Container(
                    content=botao_processar_todos,
                    margin=ft.margin.only(top=16),
                    height=48
                )
            ], spacing=16)
        )
    )
    
    painel_resultados = ft.Column(spacing=24)
    
    resultados_card = ft.Card(
        elevation=8,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            height=700,
            content=ft.Column([
                ft.Row([
                    ft.Icon(name="assessment", color=th.get("SUCCESS", "#10B981"), size=24),
                    ft.Text("Resultado da Análise", size=20, weight="bold", color=th["TEXT"]),
                    ft.Container(
                        content=ft.Text(f"{len(resultados_data)} resultado{'s' if len(resultados_data) != 1 else ''}", 
                                    color="white", size=12, weight="bold"),
                        bgcolor=th.get("SUCCESS", "#10B981"),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12,
                        visible=len(resultados_data) > 0
                    )
                ], spacing=12),
                
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Column([painel_resultados], scroll=ft.ScrollMode.AUTO),
                    height=620,
                )
            ], spacing=16)
        )
    )

    layout_principal = ft.Row([
        ft.Container(
            content=painel_fornecedores,
            expand=True,
            padding=ft.padding.only(right=16)
        ),
        ft.Container(
            content=resultados_card,
            expand=True,
            padding=ft.padding.only(left=16)
        )
    ], spacing=0)
    
    atualizar_painel_fornecedores()
    atualizar_resultados()
    
    return ft.View(
        route="/consulta_produtos",
        bgcolor=th["BACKGROUNDSCREEN"],
        controls=[
            ft.Column([
                header_container,
                ft.Container(
                    content=ft.Column([
                        titulo_secao,
                        layout_principal
                    ], spacing=0),
                    padding=24,
                    expand=True
                ),
            ])
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
    )