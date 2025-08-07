import flet as ft
import threading
import time

def notificacao(page: ft.Page, titulo: str, mensagem: str, tipo: str = "info"):
    tipos = {
        "sucesso": {"bg": "#1fb355", "text": "white", "icon": "check_circle"},
        "erro": {"bg": "#db3e3e", "text": "white", "icon": "error"},
        "info": {"bg": "#3474dc", "text": "white", "icon": "info"},
        "alerta": {"bg": "#db8f0b", "text": "white", "icon": "warning"},
    }

    estilo = tipos.get(tipo, tipos["info"])

    if not hasattr(page, "overlay"):
        page.overlay = []

    def notificaoDinamica(titulo, mensagem):
        chars_por_linha_titulo = 45
        linhas_titulo = max(1, len(titulo) // chars_por_linha_titulo + (1 if len(titulo) % chars_por_linha_titulo > 0 else 0))
        altura_titulo = linhas_titulo * 18

        chars_por_linha_mensagem = 50
        linhas_mensagem = max(1, len(mensagem) // chars_por_linha_mensagem + (1 if len(mensagem) % chars_por_linha_mensagem > 0 else 0))
        altura_mensagem = linhas_mensagem * 16

        altura_conteudo = altura_titulo + altura_mensagem + 2
        altura_final = max(26, altura_conteudo) + 32 + 16
        return max(80, min(altura_final, 200))

    altura_dinamica = notificaoDinamica(titulo, mensagem)

    notificacoes_existentes = [
        item for item in page.overlay
        if isinstance(item, ft.Container) and hasattr(item, 'content') and isinstance(item.content, ft.Card)
    ]

    posicao_acumulada = 20 + altura_dinamica + 10
    for notif in notificacoes_existentes:
        notif.bottom = posicao_acumulada
        notif.animate_position = ft.Animation(400, "easeOut")
        altura_existente = getattr(notif, 'altura_notificacao', 80)
        posicao_acumulada += altura_existente + 10

    texto_titulo = ft.Text(titulo, color=estilo["text"], weight="bold", size=15, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS)
    texto_mensagem = ft.Text(mensagem, color=estilo["text"], size=13, max_lines=5, overflow=ft.TextOverflow.ELLIPSIS)

    card = ft.Container(
        content=ft.Card(
            elevation=6,
            content=ft.Container(
                padding=16,
                bgcolor=estilo["bg"],
                border_radius=12,
                content=ft.Row([
                    ft.Icon(estilo["icon"], color=estilo["text"], size=26),
                    ft.Column([texto_titulo, texto_mensagem], spacing=2, expand=True)
                ], spacing=12, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
            )
        ),
        width=420,
        height=altura_dinamica,
        right=20,
        bottom=20,
        opacity=0,
        animate_opacity=ft.Animation(400, "easeOut"),
        animate_offset=ft.Animation(400, "easeOut"),
        animate_position=ft.Animation(400, "easeOut"),
        offset=ft.Offset(0.5, 0)
    )
    
    card.altura_notificacao = altura_dinamica
    page.overlay.append(card)
    page.update()

    def animar_entrada():
        time.sleep(0.1)
        card.opacity = 1
        card.offset = ft.Offset(0, 0)
        page.update()

    def animar_saida():
        time.sleep(4)
        card.opacity = 0
        card.offset = ft.Offset(0.5, 0)
        page.update()
        time.sleep(0.5)
        try:
            if card in page.overlay:
                page.overlay.remove(card)

                notificacoes_restantes = [
                    item for item in page.overlay
                    if isinstance(item, ft.Container) and hasattr(item, 'content') and isinstance(item.content, ft.Card)
                ]

                posicao_atual = 20
                for notif in notificacoes_restantes:
                    notif.bottom = posicao_atual
                    altura_notif = getattr(notif, 'altura_notificacao', 80)
                    posicao_atual += altura_notif + 10

                page.update()
        except:
            pass

    threading.Thread(target=animar_entrada).start()
    threading.Thread(target=animar_saida).start()

def notificarProgresso(page: ft.Page, titulo: str, mensagem: str, tipo: str = "info"):
    estilo = {
        "bg": "#3474dc",
        "text": "white",
        "icon": "info"
    }

    texto_titulo = ft.Text(titulo, color=estilo["text"], weight="bold", size=15)
    texto_mensagem = ft.Text(mensagem, color=estilo["text"], size=13, max_lines=5, overflow=ft.TextOverflow.ELLIPSIS)
    progresso_texto = ft.Text("0%", color=estilo["text"], size=12)
    progresso_ring = ft.ProgressRing(color=estilo["text"], width=16, height=16, stroke_width=2)

    coluna = ft.Column(
        controls=[
            texto_titulo,
            texto_mensagem,
            ft.Row([progresso_ring, progresso_texto], spacing=6, alignment=ft.MainAxisAlignment.START)
        ],
        spacing=2
    )

    card = ft.Container(
        content=ft.Card(
            elevation=6,
            content=ft.Container(
                padding=16,
                bgcolor=estilo["bg"],
                border_radius=12,
                content=ft.Row([
                    ft.Icon(estilo["icon"], color=estilo["text"], size=26),
                    coluna
                ], spacing=12)
            )
        ),
        width=420,
        height=110,
        right=20,
        bottom=20,
        opacity=1,
        offset=ft.Offset(0, 0),
        animate_position=ft.Animation(400, "easeOut"),
        animate_opacity=ft.Animation(400, "easeOut")
    )

    card.altura_notificacao = 110
    card.texto_mensagem = texto_mensagem
    card.progresso_texto = progresso_texto

    notificacoes_existentes = [
        item for item in page.overlay
        if isinstance(item, ft.Container) and hasattr(item, 'content') and isinstance(item.content, ft.Card)
    ]

    posicao_acumulada = 20
    for notif in notificacoes_existentes:
        notif.bottom = posicao_acumulada
        notif.animate_position = ft.Animation(400, "easeOut")
        altura = getattr(notif, 'altura_notificacao', 80)
        posicao_acumulada += altura + 10

    card.bottom = posicao_acumulada
    page.overlay.append(card)
    page._notificacao_progresso = card
    page.update()


def atualizarProgresso(mensagem: str, progresso: int, page: ft.Page):
    if hasattr(page, "_notificacao_progresso"):
        card = page._notificacao_progresso
        card.texto_mensagem.value = mensagem
        card.progresso_texto.value = f"{progresso}%"
        page.update()


def removerProgresso(page: ft.Page):
    if hasattr(page, "_notificacao_progresso"):
        try:
            card = page._notificacao_progresso
            if card in page.overlay:
                page.overlay.remove(card)
            del page._notificacao_progresso
            page.update()
        except:
            pass
