import asyncio
import flet as ft
import aiohttp
from src.Config import theme
from src.Components.notificacao import notificacao
from src.Components.headerApp import HeaderApp

def ConsultaFornecedorPage(page: ft.Page):
    print("🟣 Tela Consulta Fornecedor carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    th = theme.current_theme
    fornecedor_data = {}
    
    API_BASE_URL = "http://localhost:8000/api"

    def onThemeChange(novo_tema):
        nonlocal th
        th = theme.current_theme
        page.bgcolor = th["BACKGROUNDSCREEN"]
        page.window_bgcolor = th["BACKGROUNDSCREEN"]
        if hasattr(page, 'views') and page.views:
            page.views[-1].bgcolor = th["BACKGROUNDSCREEN"]
        
        header_container.content = HeaderApp(
            page, 
            titulo_tela="Consultar Fornecedor", 
            on_theme_changed=onThemeChange, 
            mostrar_voltar=True,
            mostrar_logo=False,        
            mostrar_nome_empresa=False,
            mostrar_usuario=True
        )
        
        cnpj_field.bgcolor = th["CARD"]
        cnpj_field.color = th["TEXT"]
        cnpj_field.border_color = th["TEXT_SECONDARY"]
        cnpj_field.hint_style = ft.TextStyle(color=th["TEXT_SECONDARY"])
        
        status_text.color = th["ERROR"]
        loader.color = th["PRIMARY_COLOR"]
        
        search_card.content.bgcolor = th["CARD"]
        
        page.update()

    header_container = ft.Container(
        content=HeaderApp(
            page, 
            titulo_tela="Consultar Fornecedor", 
            on_theme_changed=onThemeChange, 
            mostrar_voltar=True,
            mostrar_logo=False,           
            mostrar_nome_empresa=False,  
            mostrar_usuario=True         
        )
    )

    def formatarCnpj(value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) <= 2:
            return digits
        elif len(digits) <= 5:
            return f"{digits[:2]}.{digits[2:]}"
        elif len(digits) <= 8:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:]}"
        elif len(digits) <= 12:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:]}"
        else:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"

    def validateCnpj(cnpj):
        digits = ''.join(filter(str.isdigit, cnpj))
        return len(digits) == 14

    def onCnpjChange(e):
        formatted = formatarCnpj(e.control.value)
        cnpj_field.value = formatted
        page.update()

    def onEnterPressed(e):
        buscarFornecedor(e)

    def buscarFornecedor(e):
        cnpj = cnpj_field.value.strip()
        
        if not validateCnpj(cnpj):
            notificacao(
                page,
                titulo="CNPJ inválido",
                mensagem="Por favor, digite um CNPJ com 14 dígitos numéricos.",
                tipo="erro"
            )
            resultado_container.visible = False
            page.update()
            return

        status_text.visible = False
        loader.visible = True
        resultado_container.visible = False
        page.update()

        page.run_task(buscarFornecedorApi, cnpj)

    cnpj_field = ft.TextField(
        label="CNPJ",
        hint_text="00.000.000/0000-00",
        width=400,
        border_radius=8,
        filled=True,
        bgcolor=th["CARD"],
        color=th["TEXT"],
        border_color=th["TEXT_SECONDARY"],
        hint_style=ft.TextStyle(color=th["TEXT_SECONDARY"]),
        max_length=18,
        on_change=onCnpjChange,
        on_submit=onEnterPressed, 
        autofocus=True 
    )

    status_text = ft.Text(value="", color=th["ERROR"], visible=False, size=12)
    loader = ft.ProgressRing(width=20, height=20, visible=False, color=th["PRIMARY_COLOR"])
    resultado_container = ft.Container(
        visible=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(name="info", size=64, color=th["TEXT_SECONDARY"]),
                    margin=ft.margin.only(bottom=16)
                ),
                ft.Text(
                    "Nenhum fornecedor buscado ainda",
                    size=18,
                    weight="bold",
                    color=th["TEXT"],
                    text_align="center"
                ),
                ft.Text(
                    "Digite um CNPJ válido acima e pressione Enter ou clique em buscar.",
                    size=14,
                    color=th["TEXT_SECONDARY"],
                    text_align="center"
                )
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=80,
            border_radius=12
        )
    )

    async def buscarFornecedorApi(cnpj):
        try:
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            url = f"{API_BASE_URL}/consulta-fornecedor/{cnpj_limpo}"
            
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        data = response_data.get("data", {})
                        
                        fornecedor_data.update({
                            "cnpj": formatarCnpj(data.get("cnpj", cnpj_limpo)),
                            "razao": data.get("razao_social", "Não informado"),
                            "uf": data.get("uf", "N/A"),
                            "regime": data.get("regime_tributario", "Não informado"),
                            "cnae": data.get("cnae", "N/A"),
                            "simples": data.get("simples", False),
                            "isento": data.get("isento", False),
                        })
                        
                        preencherResultado()
                        loader.visible = False
                        resultado_container.visible = True
                        
                        notificacao(
                            page,
                            titulo="Fornecedor encontrado",
                            mensagem="Dados carregados com sucesso!",
                            tipo="sucesso"
                        )
                        
                        if fornecedor_data["regime"] != "Simples Nacional":
                            notificacao(
                                page,
                                titulo="Atenção ao regime tributário",
                                mensagem=f"Fornecedor no regime {fornecedor_data['regime']}. Verifique as alíquotas.",
                                tipo="alerta"
                            )
                        
                        if fornecedor_data["isento"]:
                            notificacao(
                                page,
                                titulo="Fornecedor isento",
                                mensagem="Este fornecedor é isento de ICMS conforme Decreto 29.560/08.",
                                tipo="info"
                            )
                            
                    elif response.status == 404:
                        mostrarErro("Fornecedor não encontrado", "CNPJ não localizado na base de dados.")
                    elif response.status == 400:
                        mostrarErro("CNPJ inválido", "Formato de CNPJ inválido.")
                    else:
                        error_detail = await response.text()
                        mostrarErro("Erro no servidor", f"Erro {response.status}. Tente novamente.")
                        
        except aiohttp.ClientError as e:
            mostrarErro("Erro de conexão", "Não foi possível conectar ao servidor. Verifique se a API está rodando.")
            print(f"[ERRO] Conexão: {e}")
        except asyncio.TimeoutError:
            mostrarErro("Timeout", "A consulta demorou muito para responder. Tente novamente.")
        except Exception as e:
            mostrarErro("Erro inesperado", f"Erro: {str(e)}")
            print(f"[ERRO] Inesperado: {e}")
        
        page.update()

    def mostrarErro(titulo, mensagem):
        loader.visible = False
        resultado_container.visible = True
        resultado_container.content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(name="error", size=64, color=th["ERROR"]),
                    margin=ft.margin.only(bottom=16)
                ),
                ft.Text(
                    titulo,
                    size=18,
                    weight="bold",
                    color=th["ERROR"],
                    text_align="center"
                ),
                ft.Text(
                    mensagem,
                    size=14,
                    color=th["TEXT_SECONDARY"],
                    text_align="center"
                )
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=80,
            border_radius=12,
            alignment=ft.alignment.center
        )
        
        notificacao(page, titulo, mensagem, tipo="erro")

    def preencherResultado():
        cor_regime = "#22c55e" if fornecedor_data["simples"] else "#3b82f6"
        texto_regime = fornecedor_data["regime"]

        resultado_container.content = ft.Card(
            elevation=4,
            content=ft.Container(
                bgcolor=th["CARD"],
                padding=24,
                border_radius=12,
                content=ft.Column([
                    ft.Row([
                        ft.Row([
                            ft.Icon(name="business", color=th["TEXT"], size=20),
                            ft.Text("Dados do Fornecedor", size=18, weight="bold", color=th["TEXT"])
                        ], spacing=8),
                        ft.Container(
                            content=ft.Text(texto_regime, color="white", size=12, weight="bold"),
                            bgcolor=cor_regime,
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=16
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    ft.Divider(color=th["TEXT_SECONDARY"], opacity=0.3),

                    ft.ResponsiveRow([
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=ft.Column([
                                ft.Text("CNPJ", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Text(fornecedor_data["cnpj"], color=th["TEXT"], size=14, font_family="monospace")
                            ], spacing=4)
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=ft.Column([
                                ft.Text("UF", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Row([
                                    ft.Icon(name="location_on", color=th["TEXT_SECONDARY"], size=16),
                                    ft.Text(fornecedor_data["uf"], color=th["TEXT"], size=14)
                                ], spacing=4)
                            ], spacing=4)
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 12},  # ALTERADO: Ocupa toda a largura
                            content=ft.Column([
                                ft.Text("Razão Social", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Text(fornecedor_data["razao"], color=th["TEXT"], size=14)
                            ], spacing=4)
                        ),
                        # REMOVIDO: Nome Fantasia
                        ft.Container(
                            col={"sm": 12},
                            content=ft.Column([
                                ft.Text("CNAE Principal", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Row([
                                    ft.Icon(name="description", color=th["TEXT_SECONDARY"], size=16),
                                    ft.Text(fornecedor_data["cnae"], color=th["TEXT"], size=14)  # REMOVIDO: descrição
                                ], spacing=4)
                            ], spacing=4)
                        )
                    ], spacing=16),

                    ft.Divider(color=th["TEXT_SECONDARY"], opacity=0.3),

                    ft.Row([
                        ft.Row([
                            ft.Icon(
                                name="check_circle" if fornecedor_data["simples"] else "cancel",
                                color="#22c55e" if fornecedor_data["simples"] else "#ef4444",
                                size=20
                            ),
                            ft.Text("Simples Nacional", color=th["TEXT"], size=14)
                        ], spacing=8),

                        ft.Row([
                            ft.Icon(
                                name="check_circle" if fornecedor_data["isento"] else "cancel",
                                color="#22c55e" if fornecedor_data["isento"] else "#ef4444",
                                size=20
                            ),
                            ft.Text("Decreto 29.560/08", color=th["TEXT"], size=14)
                        ], spacing=8)
                    ], spacing=32)
                ], spacing=20)
            )
        )

    search_card = ft.Card(
        elevation=4,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            content=ft.Column([
                ft.Row([
                    ft.Text("Consultar Fornecedor", size=18, weight="bold", color=th["TEXT"])
                ], spacing=8),
                
                ft.Container(height=16),
                
                ft.Row([
                    cnpj_field,
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(name="search", size=28, color="white"),
                        ], spacing=4),
                        on_click=buscarFornecedor,
                        bgcolor=th["PRIMARY_COLOR"],
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.all(16)
                        ),
                        disabled=False
                    ),
                    loader
                ], spacing=12, alignment=ft.MainAxisAlignment.START),
                status_text
            ], spacing=8)
        )
    )

    return ft.View(
        route="/consulta_fornecedor",
        bgcolor=th["BACKGROUNDSCREEN"],
        controls=[
            ft.Container(
                padding=24,
                content=ft.Column([
                    header_container, 
                    search_card,
                    resultado_container
                ], spacing=24),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )