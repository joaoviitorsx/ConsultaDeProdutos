import asyncio
import flet as ft
from src.Config import theme
from src.Utils.validadores import formatador
from src.Components.headerApp import HeaderApp
from src.Config.database.db import sqlalchemy_url
from src.Components.notificacao import notificacao
from src.Components.cardFornecedor import CardFornecedor
from src.Components.cardResultado import CardResultado, melhorOpcao
from src.Services.consultaProdutosService import buscarFornecedorApi, buscarProdutoApi, ConsultaProdutosService  

def ConsultaProdutosPage(page: ft.Page):
    print("🔵 Tela Consulta Produtos carregada")

    if not hasattr(page, "selected_empresa_id") or page.selected_empresa_id is None:
        notificacao(page, "Erro", "Empresa não identificada. Faça login novamente.", "erro")
        return
    
    theme.apply_theme(page)
    th = theme.get_theme()

    page.bgcolor = th["BACKGROUNDSCREEN"]
    page.window_bgcolor = th["BACKGROUNDSCREEN"]

    fornecedores_data = [{"id": "1", "cnpj": "", "codigo_produto": "", "valor_produto": "", "processando": False}]
    resultados_data = []
    processamento_global = False

    def atualizar():
        atualizarPaineisTema()
        atualizarPainelFornecedor()
        atualizarResultados()


    def onThemeChange(novo_tema):
        nonlocal th
        theme.set_theme(novo_tema)
        th = theme.get_theme()

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
        atualizar()
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
    
    def atualizarFornecedor(index, campo, valor):
        if index < len(fornecedores_data):
            fornecedores_data[index][campo] = valor
            page.update()
    
    def atualizarPaineisTema():
        nonlocal painel_fornecedores, resultados_card, titulo_secao

        th = theme.get_theme()

        titulo_secao.content = ft.Column([
            ft.Text("Comparação de Fornecedores", 
                size=32, weight="bold", color=th["TEXT"]),
            ft.Text("Analise impostos e encontre a melhor opção para sua compra", 
                size=18, color=th["TEXT_SECONDARY"]),
        ], spacing=8)
        
        painel_fornecedores.content = ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
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
                    content=ft.Column([fornecedores_container], scroll=ft.ScrollMode.AUTO, expand=True),
                    expand=True
                ),
            ], spacing=16, expand=True)
        )

        resultados_card.content = ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
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
                    content=ft.Column([painel_resultados], scroll=ft.ScrollMode.AUTO, expand=True),
                    expand=True
                )
            ], spacing=16, expand=True)
        )

    async def processarFornecedor(fornecedor_id):
        fornecedor = next((f for f in fornecedores_data if f["id"] == fornecedor_id), None)
        if not fornecedor or not all([fornecedor["cnpj"], fornecedor["codigo_produto"], fornecedor["valor_produto"]]):
            return

        if len(fornecedor["cnpj"].replace(".", "").replace("/", "").replace("-", "")) != 14:
            notificacao(page, "CNPJ Inválido", "O CNPJ informado está incompleto ou inválido.", "alerta")
            return

        fornecedor["processando"] = True
        atualizarPainelFornecedor()

        try:
            fornecedor_api = await buscarFornecedorApi(fornecedor["cnpj"])
            produto_api = await buscarProdutoApi(fornecedor["codigo_produto"], page.selected_empresa_id)
            if not produto_api:
                notificacao(page, "Erro", "Produto não encontrado para esta empresa.", "erro")
                fornecedor["processando"] = False
                atualizarPainelFornecedor()
                return

            regime = fornecedor_api.get("regime_tributario", "Lucro Real")
            decreto = fornecedor_api.get("isento", False)
            valor_produto = float(fornecedor["valor_produto"].replace(',', '.'))
            categoria_fiscal = produto_api.get("categoriaFiscal", "")
            uf = fornecedor_api.get("uf", "")

            service = ConsultaProdutosService(sqlalchemy_url())

            resultado_api = service.calcularImposto(
                valor_produto=valor_produto,
                aliquota=produto_api.get("aliquota", ""),
                regime=regime,
                decreto=decreto,
                uf=uf,
                categoriaFiscal=categoria_fiscal
            )

            try:
                usuario_id = page.session.get("usuario_id")
                if not usuario_id:
                    usuario_id = 0
                
                dados_consulta = {
                    "usuario_id": usuario_id,
                    "empresa_id": page.selected_empresa_id,
                    "cnpjFornecedor": fornecedor["cnpj"],
                    "nomeFornecedor": fornecedor_api.get("razao_social", ""),
                    "codigoProduto": fornecedor["codigo_produto"],
                    "produto": produto_api.get("produto", ""),
                    "valorBase": valor_produto,
                    "uf": uf,
                    "regime": regime,
                    "aliquotaAplicada": str(resultado_api.get("aliquota_utilizada", "")),
                    "adicionalSimples": resultado_api.get("adicional_simples", 0),
                    "valorFinal": resultado_api.get("valor_final", valor_produto),
                }

                service.salvarConsultaUsuario(dados_consulta)

            except Exception as e:
                print(f"❌ Erro ao salvar consulta: {e}")

            resultado = {
                "id": fornecedor["id"],
                "cnpj": fornecedor["cnpj"],
                "razao": fornecedor_api.get("razao_social"),
                "fantasia": fornecedor_api.get("nome_fantasia"),
                "cnae": fornecedor_api.get("cnae", ""),
                "regime": regime,
                "valor_produto": valor_produto,
                "valor_final": resultado_api.get("valor_final", valor_produto),
                "aliquota_aplicada": resultado_api.get("aliquota_aplicada", False),
                "adicional_aplicado": resultado_api.get("adicional_simples", 0) > 0,
                "uf": fornecedor_api.get("uf", ""),
                "decreto": decreto,
                "melhor_opcao": False,
                # Dados do produto:
                "nome_produto": produto_api.get("produto", ""),
                "ncm": produto_api.get("ncm", ""),
                "aliquota_banco": produto_api.get("aliquota", ""),
                # Detalhes dos impostos:
                "percentual_aliquota": str(produto_api.get("aliquota", "")),
                "valor_aliquota": resultado_api.get("icms", 0),
                "percentual_aliquota": f"{resultado_api.get('aliquota_utilizada', '')}%",
                "valor_adicional_simples": resultado_api.get("adicional_simples", 0),
                "percentual_adicional": "3%" if "simples" in regime.lower() and resultado_api.get("adicional_simples", 0) > 0 else "0",
                "valor_adicional_simples": resultado_api.get("adicional_simples", 0),
            }

            nonlocal resultados_data
            resultados_data = [r for r in resultados_data if r["id"] != fornecedor_id]
            resultados_data.append(resultado)

            if len(resultados_data) > 1:
                min_total = min(r.get("valor_final", 0) for r in resultados_data)
                for r in resultados_data:
                    r["melhor_opcao"] = r.get("valor_final", 0) == min_total
            else:
                resultados_data[0]["melhor_opcao"] = True

            atualizarPaineisTema()
            atualizarResultados()

        except ValueError as ve:
            notificacao(page, "Erro", str(ve), "erro")
        except Exception as e:
            notificacao(page, "Erro", f"Erro ao processar fornecedor: {str(e)}", "erro")
        finally:
            fornecedor["processando"] = False
            atualizarPainelFornecedor()
    
    def removerFornecedor(fornecedor_id):
        nonlocal fornecedores_data, resultados_data
        
        if fornecedor_id == "1":
            notificacao(page, "Ação Bloqueada", "O Fornecedor #1 não pode ser removido", "alerta")
            return
        
        if len(fornecedores_data) > 1:
            fornecedor_removido = next((f for f in fornecedores_data if f["id"] == fornecedor_id), None)
            fornecedores_data = [f for f in fornecedores_data if f["id"] != fornecedor_id]
            resultados_data = [r for r in resultados_data if r["id"] != fornecedor_id]
            
            if len(resultados_data) > 0:
                min_total = min(r["valor_final"] for r in resultados_data)
                for r in resultados_data:
                    r["melhor_opcao"] = r["valor_final"] == min_total
            
            atualizar()
            
            if fornecedor_removido:
                notificacao(page, "Fornecedor Removido", f"Fornecedor #{fornecedor_id} foi removido", "info")

    def contarFornecedorValidos():
        return len([f for f in fornecedores_data if all([f["cnpj"], f["codigo_produto"], f["valor_produto"]])])
    
    def atualizarResultados():
        th = theme.get_theme()
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
            melhorOpcao(resultados_data)

            if len(resultados_data) > 1:
                economia_maxima = max(r["valor_final"] for r in resultados_data) - min(r["valor_final"] for r in resultados_data)
                success_color = th.get("SUCCESS", "#10B981")
                
                economia_card = ft.Container(
                    content=ft.Row([
                        ft.Icon("emoji_events", color=success_color, size=20),
                        ft.Text(f"Economia de até {formatador(economia_maxima)}", 
                            color=success_color, weight="bold", size=16)
                    ], spacing=8),
                    bgcolor=f"{success_color}1A",
                    padding=16,
                    border_radius=8,
                    border=ft.border.all(1, f"{success_color}4D"), 
                    margin=ft.margin.only(bottom=16)
                )
                painel_resultados.controls.append(economia_card)
            
            for resultado in sorted(resultados_data, key=lambda x: x["valor_final"]):
                painel_resultados.controls.append(CardResultado(resultado))
        
        page.update()
    
    def adicionarFornecedor(e):
        if len(fornecedores_data) < 4:
            novo_id = str(len(fornecedores_data) + 1)
            fornecedores_data.append({
                "id": novo_id,
                "cnpj": "",
                "codigo_produto": "",
                "valor_produto": "",
                "processando": False
            })
            atualizarPaineisTema()
            atualizarPainelFornecedor()
            notificacao(page, "Fornecedor Adicionado", f"Fornecedor #{novo_id} adicionado com sucesso!", "info")
   
    def atualizarPainelFornecedor():
        th = theme.get_theme()
        fornecedores_container.controls.clear()
        validos = contarFornecedorValidos()
        
        for i, fornecedor in enumerate(fornecedores_data):
            fornecedor_valido = all([fornecedor["cnpj"], fornecedor["codigo_produto"], fornecedor["valor_produto"]])
            card = CardFornecedor(
                fornecedor=fornecedor,
                index=i,
                total=len(fornecedores_data),
                on_update=atualizarFornecedor,
                on_processar=lambda fornecedor_id: asyncio.run(processarFornecedor(fornecedor_id)),
                on_remover=removerFornecedor,
                valido=fornecedor_valido
            )
            fornecedores_container.controls.append(card)
        
        if len(fornecedores_data) < 4:
            botao_adicionar = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(name="add", size=16, color=th["TEXT_SECONDARY"]),
                    ft.Text(f"Adicionar Fornecedor ({len(fornecedores_data)}/4)", 
                        color=th["TEXT_SECONDARY"], weight="bold")
                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                on_click=adicionarFornecedor,
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
                ),
            ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO,)
        ),
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
                        content=ft.Text(f"{len(resultados_data)} resultado{'s' if len(resultados_data) != 1 else ''}",color="white", size=12, weight="bold"), 
                        bgcolor=th.get("SUCCESS", "#10B981"),
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12,
                        visible=len(resultados_data) > 0
                    )
                ], spacing=12),
                
                ft.Container(height=16),
                
                ft.Container(
                    content=ft.Column([painel_resultados], scroll=ft.ScrollMode.AUTO, expand=True),
                    expand=True
                )
            ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO,)
        ),
    )

    layout_principal = ft.Row(
        controls=[
            ft.Container(
                content=painel_fornecedores,  
                expand=True,
                padding=ft.padding.only(right=8)
            ),
            ft.Container(
                content=resultados_card,  
                expand=True,
                padding=ft.padding.only(left=8)
            ),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    atualizarPainelFornecedor()
    atualizarResultados()
    
    return ft.View(
        route="/consulta_produtos",
        bgcolor=th.get("BACKGROUNDSCREEN", "#FFFFFF"),
        controls=[
            ft.Column([
                header_container,
                ft.Container(
                    content=ft.Column([
                        titulo_secao,
                        layout_principal
                    ], spacing=0, expand=True),
                    padding=24,
                    expand=True
                ),
            ], expand=True)
        ],
        scroll=ft.ScrollMode.AUTO,
    )
