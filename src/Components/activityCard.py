import flet as ft
from src.Config import theme

def get_type_color(type_, th):
    return {
        "search": th["PRIMARY_COLOR"],
        "create": "#43A047",  # Ou adicione uma cor de sucesso ao seu tema
        "update": "#FFB300",  # Ou adicione uma cor de warning ao seu tema
        "delete": th["ERROR"],
    }.get(type_, th["TEXT_SECONDARY"])

def get_type_bgcolor(type_, th):
    return {
        "search": th["CARD"],  # Ou crie uma cor clara para fundo
        "create": "#E8F5E9",
        "update": "#FFF8E1",
        "delete": "#FFEBEE",
    }.get(type_, th["CARD"])

def get_type_label(type_):
    return {
        "search": "Consulta",
        "create": "Criado",
        "update": "Atualizado",
        "delete": "Excluído",
    }.get(type_, "Ação")

def get_avatar_fallback(name):
    return "".join([n[0] for n in name.split()]).upper()

def build_activity_row(activity, th):
    return ft.Row([
        ft.Container(
            width=36,
            height=36,
            bgcolor=th["PRIMARY_COLOR"],
            border_radius=18,
            alignment=ft.alignment.center,
            content=ft.Text(
                get_avatar_fallback(activity["user"]),
                color=th["ON_PRIMARY"],
                size=12,
                weight="bold"
            )
        ),
        ft.Column([
            ft.Text(
                f'{activity["user"]} {activity["action"]} ',
                color=th["TEXT"],
                size=14,
                spans=[
                    ft.TextSpan(
                        activity["target"],
                        style=ft.TextStyle(color=th["TEXT_SECONDARY"])
                    )
                ]
            ),
            ft.Text(activity["time"], size=11, color=th["TEXT_SECONDARY"])
        ], spacing=2, expand=True),
        ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            bgcolor=get_type_bgcolor(activity["type"], th),
            border_radius=8,
            content=ft.Text(
                get_type_label(activity["type"]),
                color=get_type_color(activity["type"], th),
                size=12,
                weight="bold"
            )
        )
    ], spacing=12, alignment=ft.MainAxisAlignment.START)

def ActivityCard():
    th = theme.current_theme

    activities = [
        {"id": "1", "user": "João Silva", "action": "consultou fornecedor", "target": "CNPJ: 12.345.678/0001-90", "time": "2 min atrás", "type": "search"},
        {"id": "2", "user": "Maria Santos", "action": "cadastrou produto", "target": "Código: 12345", "time": "5 min atrás", "type": "create"},
        {"id": "3", "user": "Admin", "action": "atualizou usuário", "target": "Carlos Oliveira", "time": "10 min atrás", "type": "update"},
        {"id": "4", "user": "Ana Costa", "action": "gerou relatório", "target": "Relatório Mensal", "time": "15 min atrás", "type": "create"},
        {"id": "5", "user": "Pedro Lima", "action": "comparou produtos", "target": "4 fornecedores", "time": "20 min atrás", "type": "search"},
    ]

    return ft.Container(
        bgcolor=th["CARD_DARK"],
        border=ft.border.all(1, th["BORDER"]),
        border_radius=12,
        padding=20,
        content=ft.Column([
            ft.Text("Atividade Recente", size=18, weight="bold", color=th["TEXT"]),
            ft.Column(
                controls=[build_activity_row(a, th) for a in activities],
                spacing=14
            )
        ], spacing=16)
    )