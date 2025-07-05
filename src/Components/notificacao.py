import flet as ft
import threading
import time

def notificacao(page: ft.Page, titulo: str, mensagem: str, tipo: str = "info"):
    tipos = {
        "sucesso": {"bg": "#22c55e", "text": "white", "icon": "check_circle"},
        "erro": {"bg": "#ef4444", "text": "white", "icon": "error"},
        "info": {"bg": "#3b82f6", "text": "white", "icon": "info"},
        "alerta": {"bg": "#f59e0b", "text": "white", "icon": "warning"},
    }

    estilo = tipos.get(tipo, tipos["info"])

    card = ft.Container(
        content=ft.Card(
            elevation=6,
            content=ft.Container(
                padding=16,
                bgcolor=estilo["bg"],
                border_radius=12,
                content=ft.Row(
                    controls=[
                        ft.Icon(estilo["icon"], color=estilo["text"], size=26),
                        ft.Column([
                            ft.Text(titulo, color=estilo["text"], weight="bold", size=15),
                            ft.Text(mensagem, color=estilo["text"], size=13)
                        ], spacing=2, expand=True)
                    ],
                    spacing=12
                )
            )
        ),
        width=420,
        height=80,
        right=20,
        bottom=20,
        opacity=0,
        animate_opacity=ft.Animation(400, "easeOut"),
        animate_offset=ft.Animation(400, "easeOut"),
        offset=ft.Offset(0.5, 0)
    )

    if not hasattr(page, "overlay"):
        page.overlay = []

    for c in page.overlay:
        if isinstance(c, ft.Container) and hasattr(c, 'content'):
            return

    page.overlay.append(card)
    page.update()

    def animar_entrada():
        time.sleep(0.1)
        card.opacity = 1
        card.offset = ft.Offset(0, 0)
        page.update()

    def animar_saida():
        time.sleep(3)
        card.opacity = 0
        card.offset = ft.Offset(0.5, 0) 
        page.update()
        time.sleep(0.5)
        try:
            if card in page.overlay:
                page.overlay.remove(card)
                page.update()
        except:
            pass

    threading.Thread(target=animar_entrada).start()
    threading.Thread(target=animar_saida).start()