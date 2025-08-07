import os
import threading
import datetime
import sys
import subprocess
import flet as ft

from src.Utils.templatePdf import gerarPdfDados

def gerarPdfRelatorio(page, dados_relatorio, botao_pdf, notificacao):
    if not dados_relatorio:
        notificacao(page, "Aviso", "Nenhum dado disponível para gerar o PDF", tipo="alerta")
        return

    file_picker = next((c for c in page.overlay if isinstance(c, ft.FilePicker)), None)

    if file_picker is None:
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        page.update()

    def salvarEm(caminho_pdf):
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

                dados_formatados = []
                for item in dados_relatorio:
                    try:
                        valor_base = float(str(item.get("valor_base", 0)).replace("R$", "").replace(".", "").replace(",", ".").strip())
                        valor_final = float(str(item.get("valor_final", 0)).replace("R$", "").replace(".", "").replace(",", ".").strip())
                        
                        dados_formatados.append({
                            "data": str(item.get("data", "")),
                            "fornecedor": str(item.get("fornecedor", "")),
                            "cnpj": str(item.get("cnpj", "")),
                            "uf": str(item.get("uf", "")),
                            "cnae": str(item.get("cnae", "")),
                            "regime": str(item.get("regime", "")),
                            "produto": str(item.get("produto", "")),
                            "codigo": str(item.get("codigo", "")),
                            "ncm": str(item.get("ncm", "")),
                            "aliquotaProduto": str(item.get("aliquotaProduto", "")),
                            "valor_base": valor_base,
                            "aliquota": str(item.get("aliquota", "")),
                            "valor_final": valor_final
                        })
                    except (ValueError, TypeError) as e:
                        print(f"Erro ao processar item: {e}")
                        continue

                if not dados_formatados:
                    raise Exception("Nenhum dado válido encontrado para gerar o PDF")

                gerarPdfDados(dados_formatados, caminho_pdf_final)

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
                print(f"Erro detalhado: {ex}")
                notificacao(page, "Erro", f"Erro ao gerar PDF: {str(ex)}", tipo="erro")
            finally:
                botao_pdf.disabled = False
                botao_pdf.content = ft.Row([
                    ft.Icon(name="picture_as_pdf", size=16, color="white"),
                    ft.Text("Gerar PDF", color="white", weight="bold")
                ], spacing=8)
                page.update()

        threading.Thread(target=processar_pdf, daemon=True).start()

    file_picker.on_result = lambda e: salvarEm(e.path) if e.path else notificacao(page, "Aviso", "Salvamento cancelado", tipo="alerta")

    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_padrao = f"relatorio_consultas_{timestamp}"
        
        file_picker.save_file(
            dialog_title="Salvar Relatório como PDF",
            file_name=nome_padrao,
            file_type="custom",
            allowed_extensions=["pdf"]
        )
    except Exception as ex:
        notificacao(page, "Erro", f"Erro ao abrir seletor de arquivo: {ex}", tipo="erro")