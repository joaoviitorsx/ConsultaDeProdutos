import flet as ft
from src.Config import theme
from src.Utils.validadores import formatarCnpj, formatarValorInput

def CardFornecedor(fornecedor: dict, index: int, total: int, on_update, on_processar, on_remover, valido=True) -> ft.Card:
    th = theme.get_theme()

    cnpj_field = None
    codigo_field = None
    valor_field = None
    botao_processar = None
    status_container = None
    validation_messages = {"cnpj": "", "codigo": "", "valor": ""}

    def onCnpjChange(e):
        formatado = formatarCnpj(e.control.value)
        e.control.value = formatado
        fornecedor["cnpj"] = formatado
        on_update(index, "cnpj", formatado)
        validarCampos()
    
    def onCodigoChange(e):
        codigo_limpo = ''.join(filter(str.isdigit, e.control.value))
        fornecedor["codigo_produto"] = codigo_limpo
        e.control.value = codigo_limpo
        on_update(index, "codigo_produto", codigo_limpo)
        validarCampos()
        e.page.update()
    
    def onValorChange(e):
        valor_formatado = formatarValorInput(e.control.value)
        fornecedor["valor_produto"] = valor_formatado
        e.control.value = valor_formatado
        on_update(index, "valor_produto", valor_formatado)
        validarCampos()
        e.page.update()
    
    def validarCampos():
        cnpj_digits = fornecedor["cnpj"].replace(".", "").replace("/", "").replace("-", "")
        cnpj_valido = len(cnpj_digits) == 14

        codigo_valido = len(fornecedor["codigo_produto"]) > 0
        valor_valido = len(fornecedor["valor_produto"]) > 0
        
        if fornecedor["cnpj"] and not cnpj_valido:
            validation_messages["cnpj"] = "CNPJ deve ter 14 dígitos"
        else:
            validation_messages["cnpj"] = ""
            
        if fornecedor["codigo_produto"] and not codigo_valido:
            validation_messages["codigo"] = "Código é obrigatório"
        else:
            validation_messages["codigo"] = ""
            
        if fornecedor["valor_produto"] and not valor_valido:
            validation_messages["valor"] = "Valor é obrigatório"
        else:
            validation_messages["valor"] = ""

        if botao_processar:
            todos_validos = cnpj_valido and codigo_valido and valor_valido
            botao_processar.disabled = fornecedor["processando"] or not todos_validos
            
            if fornecedor["processando"]:
                botao_processar.bgcolor = th.get("WARNING", "#F59E0B")
            elif todos_validos:
                botao_processar.bgcolor = th.get("SUCCESS", "#10B981")
            else:
                botao_processar.bgcolor = th["TEXT_SECONDARY"]
        
        if cnpj_field:
            if fornecedor["cnpj"]:
                cnpj_field.border_color = th.get("SUCCESS", "#10B981") if cnpj_valido else th.get("ERROR", "#EF4444")
                cnpj_field.error_text = validation_messages["cnpj"]
            else:
                cnpj_field.border_color = th["TEXT_SECONDARY"]
                cnpj_field.error_text = None
                
        if codigo_field:
            if fornecedor["codigo_produto"]:
                codigo_field.border_color = th.get("SUCCESS", "#10B981") if codigo_valido else th.get("ERROR", "#EF4444")
                codigo_field.error_text = validation_messages["codigo"]
            else:
                codigo_field.border_color = th["TEXT_SECONDARY"]
                codigo_field.error_text = None
                
        if valor_field:
            if fornecedor["valor_produto"]:
                valor_field.border_color = th.get("SUCCESS", "#10B981") if valor_valido else th.get("ERROR", "#EF4444")
                valor_field.error_text = validation_messages["valor"]
            else:
                valor_field.border_color = th["TEXT_SECONDARY"]
                valor_field.error_text = None
        
        atualizarStatus()

    def atualizarStatus():
        if not status_container:
            return
            
        campos_preenchidos = sum([
            1 if fornecedor["cnpj"] else 0,
            1 if fornecedor["codigo_produto"] else 0,
            1 if fornecedor["valor_produto"] else 0
        ])
        
        if fornecedor["processando"]:
            status_color = th.get("WARNING", "#F59E0B")
            status_text = "Processando..."
            status_icon = ft.ProgressRing(width=12, height=12, stroke_width=2, color=status_color)
        elif campos_preenchidos == 3:
            cnpj_digits = fornecedor["cnpj"].replace(".", "").replace("/", "").replace("-", "")
            if len(cnpj_digits) == 14:
                status_color = th.get("SUCCESS", "#10B981")
                status_text = "Pronto para processar"
                status_icon = ft.Icon("check_circle", color=status_color, size=14)
            else:
                status_color = th.get("ERROR", "#EF4444")
                status_text = "CNPJ inválido"
                status_icon = ft.Icon("error", color=status_color, size=14)
        elif campos_preenchidos > 0:
            status_color = th.get("INFO", "#3B82F6")
            status_text = f"{campos_preenchidos}/3 campos preenchidos"
            status_icon = ft.Icon("edit", color=status_color, size=14)
        else:
            status_color = th["TEXT_SECONDARY"]
            status_text = "Aguardando dados"
            status_icon = ft.Icon("info", color=status_color, size=14)
        
        status_container.content = ft.Row([
            status_icon,
            ft.Text(status_text, color=status_color, size=12, weight="w500")
        ], spacing=6)

    cnpj_field = ft.TextField(
        label="CNPJ da Empresa",
        hint_text="00.000.000/0000-00",
        value=fornecedor["cnpj"],
        on_change=onCnpjChange,
        max_length=18,
        bgcolor=th["BACKGROUNDSCREEN"],
        color=th["TEXT"],
        border_color=th["TEXT_SECONDARY"],
        focused_border_color=th["PRIMARY_COLOR"],
        prefix_icon="business",
        border_radius=12,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        text_size=14,
        label_style=ft.TextStyle(color=th["TEXT_SECONDARY"], size=12),
        hint_style=ft.TextStyle(color=th["TEXT_SECONDARY"]),
        cursor_color=th["PRIMARY_COLOR"]
    )

    codigo_field = ft.TextField(
        label="Código do Produto",
        hint_text="Digite o código numérico",
        value=fornecedor["codigo_produto"],
        on_change=onCodigoChange,
        bgcolor=th["BACKGROUNDSCREEN"],
        color=th["TEXT"],
        border_color=th["TEXT_SECONDARY"],
        focused_border_color=th["PRIMARY_COLOR"],
        prefix_icon="qr_code_2",
        border_radius=12,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        text_size=14,
        label_style=ft.TextStyle(color=th["TEXT_SECONDARY"], size=12),
        hint_style=ft.TextStyle(color=th["TEXT_SECONDARY"]),
        cursor_color=th["PRIMARY_COLOR"]
    )

    valor_field = ft.TextField(
        label="Valor do Produto (R$)",
        hint_text="100,00",
        value=fornecedor["valor_produto"],
        on_change=onValorChange,
        bgcolor=th["BACKGROUNDSCREEN"],  # Ajustar cor de fundo
        color=th["TEXT"],  # Ajustar cor do texto
        border_color=th["TEXT_SECONDARY"],  # Ajustar cor da borda
        focused_border_color=th["PRIMARY_COLOR"],  # Ajustar cor da borda focada
        prefix_icon="attach_money",
        suffix_text="BRL",
        border_radius=12,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=12),
        text_size=14,
        label_style=ft.TextStyle(color=th["TEXT_SECONDARY"], size=12),
        hint_style=ft.TextStyle(color=th["TEXT_SECONDARY"]),
        cursor_color=th["PRIMARY_COLOR"]
    )
    
    botao_processar = ft.ElevatedButton(
        content=ft.Row([
            ft.ProgressRing(width=18, height=18, stroke_width=2, color="white") if fornecedor["processando"] else ft.Icon(name="calculate", size=18, color="white"),
            ft.Text(
                "Processando..." if fornecedor["processando"] else "Processar Fornecedor", 
                color="white", 
                weight="w600",
                size=14
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        on_click=lambda _: on_processar(fornecedor["id"]),
        bgcolor=th["TEXT_SECONDARY"],
        disabled=True,
        width=float("inf"),
        height=48,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            elevation=2,
            shadow_color=th["PRIMARY_COLOR"],
            animation_duration=200
        )
    )
    
    botao_remover = ft.IconButton(
        icon="delete_outline",
        icon_color=th.get("ERROR", "#EF4444"),
        icon_size=20,
        tooltip="Remover este fornecedor",
        on_click=lambda _: on_remover(fornecedor["id"]),
        visible=total > 1 and fornecedor["id"] != "1", 
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.HOVERED: f"{th.get('ERROR', '#EF4444')}15"},
            shape=ft.CircleBorder(),
            overlay_color={ft.ControlState.PRESSED: f"{th.get('ERROR', '#EF4444')}25"}
        )
    )
    
    header_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Icon("business_center", color="white", size=16),
                    ft.Text(f"Fornecedor {fornecedor['id']}", color="white", size=13, weight="w600")
                ], spacing=6),
                bgcolor=th["PRIMARY_COLOR"],
                padding=ft.padding.symmetric(horizontal=14, vertical=8),
                border_radius=20,
            ),
            
            ft.Container(expand=True),
            
            ft.Container(
                content=ft.Text(f"{index + 1}/{total}", 
                               color=th["PRIMARY_COLOR"], 
                               size=11, 
                               weight="w600"),
                bgcolor=f"{th['CARD']}",
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                border_radius=12,
                border=ft.border.all(1, f"{th['TEXT']}30")
            ),
            
            botao_remover
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        margin=ft.margin.only(bottom=16)
    )
    
    status_container = ft.Container(
        content=ft.Row([
            ft.Icon("info", color=th["TEXT_SECONDARY"], size=14),
            ft.Text("Aguardando dados", color=th["TEXT_SECONDARY"], size=12, weight="w500")
        ], spacing=6),
        bgcolor=f"{th['TEXT_SECONDARY']}10",
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border_radius=8,
        border=ft.border.all(1, f"{th['TEXT_SECONDARY']}20"),
        margin=ft.margin.only(bottom=20)
    )
    
    divider = ft.Container(
        height=1,
        bgcolor=f"{th['TEXT_SECONDARY']}",
        margin=ft.margin.symmetric(vertical=16)
    )
    
    validarCampos()
    
    return ft.Card(
        elevation=4,
        shadow_color=f"{th['PRIMARY_COLOR']}",  
        color=f"{th['PRIMARY_COLOR']}",
        content=ft.Container(
            bgcolor=th["CARD"],
            padding=24,
            border_radius=16,
            border=ft.border.all(1, f"{th['PRIMARY_COLOR']}"),
            content=ft.Column([
                header_card,
                status_container,
                
                # Seção de campos
                ft.Container(
                    content=ft.Column([
                        cnpj_field,
                        ft.Container(height=8),
                        codigo_field,
                        ft.Container(height=8),
                        valor_field,
                    ], spacing=0),
                    margin=ft.margin.only(bottom=20)
                ),
                
                divider,
                botao_processar
                
            ], spacing=0)
        )
    )