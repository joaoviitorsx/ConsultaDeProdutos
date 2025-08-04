import os
import threading
import datetime
import sys
import subprocess
import flet as ft

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle

def gerarPdfRelatorio(page, dados_relatorio, botao_pdf, notificacao):
    file_picker = None
    for control in page.overlay:
        if isinstance(control, ft.FilePicker):
            file_picker = control
            break
    
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

                c = canvas.Canvas(caminho_pdf_final, pagesize=A4)
                width, height = A4

                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "Relatório de Consultas Tributárias")
                
                c.setFont("Helvetica", 10)
                data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                c.drawString(50, height - 70, f"Gerado em: {data_hora}")
                
                dados_tabela = [[
                    "Data", "Fornecedor", "CNPJ", "Produto",
                    "Código", "Valor Base", "Alíquota", "Regime", "Total"
                ]]

                for item in dados_relatorio:
                    dados_tabela.append([
                        item["data"],
                        item["fornecedor"][:30],
                        item["cnpj"],
                        item["produto"][:30],
                        item["codigo"],
                        f"R$ {item['valor_base']:.2f}",
                        item["aliquota"],
                        item["regime"],
                        f"R$ {item['valor_final']:.2f}"
                    ])

                tabela = Table(dados_tabela, repeatRows=1, hAlign='LEFT')
                tabela.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F62FE")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                    *[("BACKGROUND", (0, i), (-1, i), colors.white) 
                      for i in range(2, len(dados_tabela), 2)]
                ]))

                largura, altura = tabela.wrapOn(c, width - 80, height - 120)
                tabela.drawOn(c, 40, height - 100 - altura)
                
                if len(dados_relatorio) > 0:
                    valor_total = sum(item["valor_final"] for item in dados_relatorio)
                    impostos_total = sum(item["total_impostos"] for item in dados_relatorio)
                    
                    y_pos = height - 120 - altura - 30
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(40, y_pos, f"Total de registros: {len(dados_relatorio)}")
                    c.drawString(40, y_pos - 15, f"Valor total: R$ {valor_total:.2f}")
                    c.drawString(40, y_pos - 30, f"Total de impostos: R$ {impostos_total:.2f}")

                c.showPage()
                c.save()

                def abrirPdf(ev=None):
                    page.close(dialog)
                    try:
                        if sys.platform == "win32":
                            os.startfile(caminho_pdf_final)
                        else:
                            subprocess.Popen(["open", caminho_pdf_final])
                    except Exception as ex:
                        notificacao(page, "Erro", f"Erro ao abrir PDF: {ex}", tipo="erro")

                def fecharDialog(ev=None):
                    page.close(dialog)

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("PDF gerado com sucesso!"),
                    content=ft.Text(f"Arquivo salvo em:\n{caminho_pdf_final}"),
                    actions=[
                        ft.TextButton("Abrir", on_click=abrirPdf),
                        ft.TextButton("Fechar", on_click=fecharDialog)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                
                page.open(dialog)
                notificacao(page, "Sucesso", f"PDF gerado com sucesso", tipo="sucesso")
                
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

    def onPathSelect(e):
        if e.path is None:
            notificacao(page, "Aviso", "Salvamento cancelado", tipo="alerta")
            return
        salvar_em(e.path)

    file_picker.on_result = onPathSelect
    
    try:
        file_picker.save_file(
            dialog_title="Salvar Relatório como PDF",
            file_type="custom",
            allowed_extensions=["pdf"]
        )
    except Exception as ex:
        notificacao(page, "Erro", f"Erro ao abrir seletor de arquivo: {ex}", tipo="erro")
        
        botao_pdf.disabled = False
        botao_pdf.content = ft.Row([
            ft.Icon(name="picture_as_pdf", size=16, color="white"),
            ft.Text("Gerar PDF", color="white", weight="bold")
        ], spacing=8)
        page.update()