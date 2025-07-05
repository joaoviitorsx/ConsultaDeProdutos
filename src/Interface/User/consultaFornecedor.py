import flet as ft
from src.Config import theme
from src.Components.notificacao import notificacao

import asyncio

def ConsultaFornecedorPage(page: ft.Page):
    print("🟣 Tela Consulta Fornecedor carregada")

    page.bgcolor = theme.current_theme["BACKGROUNDSCREEN"]
    page.window_bgcolor = theme.current_theme["BACKGROUNDSCREEN"]

    th = theme.current_theme
    fornecedor_data = {}

    def voltar_dashboard(e):
        page.go("/dashboard")

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
        max_length=18
    )

    status_text = ft.Text(value="", color=th["ERROR"], visible=False, size=12)
    loader = ft.ProgressRing(width=20, height=20, visible=False, color=th["PRIMARY_COLOR"])
    resultado_container = ft.Container(visible=False)

    def format_cnpj(value):
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

    def validate_cnpj(cnpj):
        digits = ''.join(filter(str.isdigit, cnpj))
        return len(digits) == 14

    def on_cnpj_change(e):
        formatted = format_cnpj(e.control.value)
        cnpj_field.value = formatted
        page.update()

    cnpj_field.on_change = on_cnpj_change

    def buscar_fornecedor(e):
        cnpj = cnpj_field.value.strip()
        
        if not validate_cnpj(cnpj):
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

        page.run_task(simular_busca, cnpj)

    async def simular_busca(cnpj):
        await asyncio.sleep(2)

        if cnpj == "12.345.678/0000-09":
            fornecedor_data.update({
                "cnpj": "54.616.173/0001-68",
                "razao": "EMPRESA EXEMPLO LTDA",
                "fantasia": "Exemplo Corp",
                "uf": "SP",
                "regime": "Simples Nacional",
                "cnae": "4712-1/00",
                "desc": "Comércio varejista de mercadorias em geral",
                "simples": True,
                "isento": False,
            })
        else:
            import random
            regime = "Simples Nacional" if random.random() > 0.5 else "Lucro Real"

            fornecedor_data.update({
                "cnpj": cnpj,
                "razao": "EMPRESA EXEMPLO LTDA",
                "fantasia": "Exemplo Corp",
                "uf": "SP",
                "regime": regime,
                "cnae": "4712-1/00",
                "desc": "Comércio varejista de mercadorias em geral",
                "simples": regime == "Simples Nacional",
                "isento": random.random() > 0.8,
            })

        preencher_resultado()
        loader.visible = False
        resultado_container.visible = True

        notificacao(
            page,
            titulo="Fornecedor encontrado",
            mensagem="Dados carregados com sucesso!",
            tipo="sucesso"
        )

        if fornecedor_data["regime"] == "Lucro Real":
            notificacao(
                page,
                titulo="Atenção ao regime tributário",
                mensagem="Fornecedor no regime Lucro Real. Verifique as alíquotas com cuidado.",
                tipo="alerta"
            )

        if fornecedor_data["isento"]:
            notificacao(
                page,
                titulo="Fornecedor isento",
                mensagem="Este fornecedor é isento de ICMS conforme Decreto 29.560/08.",
                tipo="info"
            )

        page.update()

    def preencher_resultado():
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
                            col={"sm": 12, "md": 6},
                            content=ft.Column([
                                ft.Text("Razão Social", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Text(fornecedor_data["razao"], color=th["TEXT"], size=14)
                            ], spacing=4)
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            content=ft.Column([
                                ft.Text("Nome Fantasia", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Text(fornecedor_data["fantasia"], color=th["TEXT"], size=14)
                            ], spacing=4)
                        ),
                        ft.Container(
                            col={"sm": 12},
                            content=ft.Column([
                                ft.Text("CNAE Principal", color=th["TEXT_SECONDARY"], size=12, weight="bold"),
                                ft.Row([
                                    ft.Icon(name="description", color=th["TEXT_SECONDARY"], size=16),
                                    ft.Text(f'{fornecedor_data["cnae"]} - {fornecedor_data["desc"]}', 
                                           color=th["TEXT"], size=14)
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

    header = ft.Container(
        content=ft.Row([
            ft.IconButton(
                icon="arrow_back",
                icon_color=th["TEXT"],
                tooltip="Voltar ao Dashboard",
                on_click=voltar_dashboard
            ),
            ft.Text("Consultar Fornecedor", size=20, weight="bold", color=th["TEXT"])
        ], spacing=8),
        padding=ft.padding.symmetric(horizontal=8, vertical=16)
    )

    search_card = ft.Card(
        elevation=4,
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=12,
            content=ft.Column([
                ft.Row([
                    ft.Icon(name="search", color=th["TEXT"], size=20),
                    ft.Text("Consultar Fornecedor", size=18, weight="bold", color=th["TEXT"])
                ], spacing=8),
                
                ft.Container(height=16),
                
                ft.Row([
                    cnpj_field,
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(name="search", size=16, color="white"),
                        ], spacing=4),
                        on_click=buscar_fornecedor,
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
                    header,
                    search_card,
                    resultado_container
                ], spacing=24),
                expand=True
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )