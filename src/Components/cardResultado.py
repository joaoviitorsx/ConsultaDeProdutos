import flet as ft
from src.Config import theme
from src.Utils.validadores import formatador

def melhorOpcao(resultados: list[dict]) -> None:
    if len(resultados) > 1:
        menor_valor = min(r.get("valor_final", float("inf")) for r in resultados)
        melhor_marcado = False
        for r in resultados:
            if not melhor_marcado and r.get("valor_final", 0) == menor_valor:
                r["melhor_opcao"] = True
                melhor_marcado = True
            else:
                r["melhor_opcao"] = False
    elif resultados:
        resultados[0]["melhor_opcao"] = True

def CardResultado(resultado: dict) -> ft.Card:
    th = theme.get_theme()

    cores = {
        "melhor_opcao": th.get("SUCCESS", "#10B981"),
        "melhor_opcao_light": th.get("SUCCESS_LIGHT", "#34D399"),
        "sucesso": th.get("SUCCESS", "#10B981"),
        "alerta": th.get("ERROR", "#EF4444"),
        "neutro": th.get("TEXT_SECONDARY", "#6B7280"),
        "borda_sutil": f"{th.get('TEXT_SECONDARY', '#6B7280')}30",
        "azul_corporativo": th.get("INFO", "#3B82F6"),
        "cinza_escuro": th.get("TEXT", "#111827"),
        "card_produto": f"{th.get('PRIMARY_COLOR', '#2563EB')}08",
        "primary": th.get("PRIMARY_COLOR", "#2563EB"),
        "card": th.get("CARD", "#FFFFFF"),
        "text": th.get("TEXT", "#111827"),
        "text_secondary": th.get("TEXT_SECONDARY", "#6B7280"),
    }

    cor_borda = cores["melhor_opcao"] if resultado.get("melhor_opcao") else cores["borda_sutil"]
    cor_principal = cores["melhor_opcao"] if resultado.get("melhor_opcao") else cores["text"]

    badge = ft.Container(
        content=ft.Row([
            ft.Icon(name="verified", color="white", size=16),
            ft.Text("MELHOR OPÇÃO", color="white", size=12, weight="w700"),
        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=cores["melhor_opcao"],
        padding=ft.padding.symmetric(horizontal=14, vertical=6),
        border_radius=6,
        border=ft.border.all(1, cores["melhor_opcao_light"]),
        visible=resultado.get("melhor_opcao", False)
    )

    header = ft.Row([
        ft.Column([
            ft.Text(resultado.get("razao", ""), size=15, weight="w700", color=cores["cinza_escuro"], max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ft.Row([
                ft.Text(f"CNPJ: {resultado.get('cnpj', '')}", size=10, color=cores["neutro"], weight="w500"),
                ft.Container(width=8),
                ft.Text(f"UF: {resultado.get('uf', '')}", size=10, color=cores["neutro"], weight="w500"),
            ], spacing=4),
            ft.Row([
                ft.Icon("business", color=cores["neutro"], size=12),
                ft.Text(resultado.get("regime", ""), size=10, color=cores["neutro"], weight="w500"),
            ], spacing=4),
        ], spacing=2, expand=True),
        badge
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    produto_card = ft.Container(
        content=ft.Row([
            ft.Icon("inventory_2", color=cores["primary"], size=22),
            ft.Column([
                ft.Text(resultado.get("nome_produto", "Produto não encontrado"), size=13, weight="w600", color=cores["primary"]),
                ft.Text(f"NCM: {resultado.get('ncm', '---')}", size=11, color=cores["text_secondary"]),
            ], spacing=2),
        ], spacing=10),
        bgcolor=cores["card_produto"],
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        margin=ft.margin.only(bottom=8)
    )

    valores = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("Valor Base", size=11, color=cores["neutro"]),
                ft.Text(formatador(resultado.get("valor_produto", 0)), size=15, weight="w700", color=cores["cinza_escuro"]),
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=cores["card"],
            border_radius=8,
            border=ft.border.all(1, cores["borda_sutil"]),
            expand=True
        ),
        ft.Container(width=8),
        ft.Container(
            content=ft.Column([
                ft.Text("Valor Final", size=11, color=cores["neutro"]),
                ft.Text(formatador(resultado.get("valor_final", 0)), size=16, weight="w700", color=cor_principal),
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=f"{cor_principal}08" if resultado.get("melhor_opcao") else cores["card"],
            border_radius=8,
            border=ft.border.all(2, cor_principal) if resultado.get("melhor_opcao") else ft.border.all(1, cores["borda_sutil"]),
            expand=True
        ),
    ], spacing=8)

    aliquota_banco = str(resultado.get('aliquota_banco', '')).upper()
    percentual_aliquota = str(resultado.get('percentual_aliquota', '')).upper()
    is_sem_imposto = aliquota_banco in ["ST", "ISENTO"] or percentual_aliquota in ["ST", "ISENTO"]

    if is_sem_imposto:
        impostos_produto_texto = "Sem Impostos"
        aliquota_label = f"Alíquota: {aliquota_banco}"
    else:
        impostos_produto_texto = f"+{percentual_aliquota}% | R$ {formatador(resultado.get('valor_aliquota', 0))}"
        aliquota_label = f"Alíquota: {aliquota_banco}%"

    regime = str(resultado.get("regime", "")).strip().lower()
    adicional_aplicado = resultado.get("adicional_aplicado", False)

    if isinstance(adicional_aplicado, str):
        adicional_aplicado = adicional_aplicado.strip().lower() in ["true", "1", "sim"]
    elif isinstance(adicional_aplicado, (int, float)):
        adicional_aplicado = adicional_aplicado != 0
    else:
        adicional_aplicado = bool(adicional_aplicado)

    if "simples" in regime:
        adicional_status = "Sim" if adicional_aplicado else "Não"
        adicional_status_color = cores["sucesso"] if adicional_aplicado else cores["text_secondary"]
    else:
        adicional_status = "Não se aplica"
        adicional_status_color = cores["text_secondary"]

    impostos_cards = ft.Row([
        ft.Container(
            expand=True,
            content=ft.Column([
                ft.Row([
                    ft.Icon("percent", color=cores["primary"], size=16),
                    ft.Text("Impostos do Produto", size=11, weight="w600", color=cores["primary"]),
                ], spacing=4),
                ft.Text(aliquota_label, size=11, color=cores["text"]),
                ft.Text(impostos_produto_texto, size=12, color=cores["sucesso"] if resultado.get("aliquota_aplicada") and not is_sem_imposto else cores["text_secondary"]),
            ], spacing=4, alignment=ft.CrossAxisAlignment.START),
            bgcolor=cores["card"],
            border_radius=8,
            border=ft.border.all(1, cores["borda_sutil"]),
            padding=ft.padding.all(12),
        ),
        ft.Container(width=8),
        ft.Container(
            expand=True,
            content=ft.Column([
                ft.Row([
                    ft.Icon("add", color=cores["sucesso"], size=16),
                    ft.Text("Adicional Simples", size=11, weight="w600", color=cores["sucesso"]),
                ], spacing=4),
                ft.Text(adicional_status, size=11, color=adicional_status_color),
                ft.Text(
                    f"+{resultado.get('percentual_adicional', '0')}% | R$ {formatador(resultado.get('valor_adicional_simples', 0))}",
                    size=12,
                    color=cores["sucesso"] if adicional_aplicado and "simples" in regime else cores["text_secondary"]
                ),
            ], spacing=4, alignment=ft.CrossAxisAlignment.START),
            bgcolor=cores["card"],
            border_radius=8,
            border=ft.border.all(1, cores["borda_sutil"]),
            padding=ft.padding.all(12),
        ),
        ft.Container(width=8),
        ft.Container(
            expand=True,
            content=ft.Column([
                ft.Row([
                    ft.Icon("gavel", color=cores["primary"], size=16),
                    ft.Text("Decreto", size=11, weight="w600", color=cores["primary"]),
                ], spacing=4),
                ft.Text(
                    "Sim" if resultado.get("decreto") else "Não",
                    size=12,
                    color=cores["sucesso"] if resultado.get("decreto") else cores["text_secondary"]
                ),
                ft.Text("", size=12, color=cores["text_secondary"])
            ], spacing=4, alignment=ft.CrossAxisAlignment.START),
            bgcolor=cores["card"],
            border_radius=8,
            border=ft.border.all(1, cores["borda_sutil"]),
            padding=ft.padding.all(12),
        ),
    ], spacing=8)

    return ft.Card(
        elevation=8 if resultado.get("melhor_opcao") else 4,
        shadow_color=f"{cor_principal}20" if resultado.get("melhor_opcao") else "#00000010",
        surface_tint_color=f"{cor_principal}05" if resultado.get("melhor_opcao") else None,
        content=ft.Container(
            bgcolor=cores["card"],
            border=ft.border.all(2, cor_borda),
            padding=18,
            border_radius=12,
            content=ft.Column([
                header,
                produto_card,
                valores,
                impostos_cards
            ], spacing=10)
        )
    )

