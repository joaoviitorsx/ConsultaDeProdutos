import os
import threading
import datetime
import sys
import subprocess
import flet as ft

from src.Utils.templatePdf import gerar_pdf_com_dados

def gerarPdfRelatorio(page, dados_relatorio, botao_pdf, notificacao):
    file_picker = next((c for c in page.overlay if isinstance(c, ft.FilePicker)), None)

    if file_picker is None:
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        page.update()

    def salvar_em(caminho_pdf):
        botao_pdf.disabled = True
        botao_pdf.content = ft.Row([
            ft.ProgressRing(width=16, height=16, stroke_width=2, color="white"),
            ft.Text("Gerando...", color="white")
        ], spacing=8)
        page.update()

        def processar_pdf():
            try:
                if not caminho_pdf.lower().endswith(".pdf"):
                    caminho_pdf_final = caminho_pdf + ".pdf"
                else:
                    caminho_pdf_final = caminho_pdf

                gerar_pdf_com_dados(dados_relatorio, caminho_pdf_final)

                def abrir(ev=None):
                    page.close(dialog)
                    try:
                        if sys.platform == "win32":
                            os.startfile(caminho_pdf_final)
                        else:
                            subprocess.Popen(["open", caminho_pdf_final])
                    except Exception as ex:
                        notificacao(page, "Erro", f"Erro ao abrir PDF: {ex}", tipo="erro")

                def fechar(ev=None):
                    page.close(dialog)

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("PDF gerado com sucesso!"),
                    content=ft.Text(f"Arquivo salvo em:\n{caminho_pdf_final}"),
                    actions=[
                        ft.TextButton("Abrir", on_click=abrir),
                        ft.TextButton("Fechar", on_click=fechar)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.open(dialog)
                notificacao(page, "Sucesso", "PDF gerado com sucesso!", tipo="sucesso")

            except Exception as ex:
                notificacao(page, "Erro", f"Erro ao gerar PDF: {ex}", tipo="erro")
            finally:
                botao_pdf.disabled = False
                botao_pdf.content = ft.Row([
                    ft.Icon(name="picture_as_pdf", size=16, color="white"),
                    ft.Text("Gerar PDF", color="white", weight="bold")
                ], spacing=8)
                page.update()

        threading.Thread(target=processar_pdf, daemon=True).start()

    file_picker.on_result = lambda e: salvar_em(e.path) if e.path else notificacao(page, "Aviso", "Salvamento cancelado", tipo="alerta")

    try:
        file_picker.save_file(
            dialog_title="Salvar Relatório como PDF",
            file_type="custom",
            allowed_extensions=["pdf"]
        )
    except Exception as ex:
        notificacao(page, "Erro", f"Erro ao abrir seletor de arquivo: {ex}", tipo="erro")
