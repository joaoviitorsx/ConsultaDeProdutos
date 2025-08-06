# src/Utils/templatePdf.py

from fpdf import FPDF
import datetime

class RelatorioPDF(FPDF):
    def header(self):
        self.image("src/Assets/images/icone.png", 10, 8, 25)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Assertivus Contábil", ln=True, align="C")
        self.set_font("Helvetica", "", 11)
        self.cell(0, 8, "Relatório de Consultas de Produtos", ln=True, align="C")
        self.set_font("Helvetica", "", 9)
        data_emissao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 10, f"Gerado em: {data_emissao}", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def gerar_tabela(self, dados):
        self.set_fill_color(15, 98, 254)
        self.set_text_color(255)
        self.set_font("Helvetica", "B", 8)

        colunas = ["Data", "Hora", "Fornecedor", "CNPJ", "Produto", "Código","Valor Base", "Alíquota", "Regime", "Total"]

        for col in colunas:
            self.cell(22, 8, col, border=1, align="C", fill=True)
        self.ln()

        self.set_text_color(0)
        self.set_font("Helvetica", "", 8)

        for i, item in enumerate(dados):
            fill = i % 2 == 0
            self.set_fill_color(245, 245, 245) if fill else self.set_fill_color(255, 255, 255)

            self.cell(22, 8, item["data"], border=1, fill=True)
            self.cell(22, 8, item["hora"], border=1, fill=True)
            self.cell(22, 8, item["fornecedor"][:15], border=1, fill=True)
            self.cell(22, 8, item["cnpj"], border=1, fill=True)
            self.cell(22, 8, item["produto"][:20], border=1, fill=True)
            self.cell(22, 8, item["codigo"], border=1, fill=True)
            self.cell(22, 8, f"R$ {item['valor_base']:.2f}", border=1, fill=True)
            self.cell(22, 8, item["aliquota"], border=1, fill=True)
            self.cell(22, 8, item["regime"], border=1, fill=True)
            self.cell(22, 8, f"R$ {item['valor_final']:.2f}", border=1, fill=True)
            self.ln()

    def resumo(self, dados):
        self.ln(5)
        self.set_font("Helvetica", "B", 9)
        total_registros = len(dados)
        total_valor = sum(item["valor_final"] for item in dados)
        total_impostos = sum(item["total_impostos"] for item in dados)

        self.cell(0, 6, f"Total de registros: {total_registros}", ln=True)
        self.cell(0, 6, f"Valor total: R$ {total_valor:.2f}", ln=True)
        self.cell(0, 6, f"Total de impostos: R$ {total_impostos:.2f}", ln=True)


def gerar_pdf_com_dados(dados, caminho_pdf_final):
    pdf = RelatorioPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.gerar_tabela(dados)
    pdf.resumo(dados)
    pdf.output(caminho_pdf_final)
