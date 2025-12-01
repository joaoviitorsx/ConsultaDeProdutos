from fpdf import FPDF
import datetime
import unicodedata

class RelatorioPDF(FPDF):
    def __init__(self, orientation='L', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(auto=True, margin=15)
    
    def limparTexto(self, texto):
        if not texto:
            return ""
        
        texto = str(texto)
        
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sem_acentos = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
        
        substituicoes = {'ç': 'c', 'Ç': 'C','°': 'o', '™': '','®': '', '©': '','"': '"', '"': '"',''': "'", ''': "'",'–': '-', '—': '-','…': '...'}
            
        for original, substituto in substituicoes.items():
            texto_sem_acentos = texto_sem_acentos.replace(original, substituto)
        
        texto_limpo = ''.join(c for c in texto_sem_acentos if ord(c) < 128)
        
        return texto_limpo

    def header(self):
        try:
            self.image("src/Assets/images/icone.png", 10, 8, 25)
        except:
            self.set_fill_color(15, 98, 254)
            self.rect(10, 8, 25, 25, 'F')
        
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.limparTexto("Assertivus Contabil"), ln=True, align="C")
        
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, self.limparTexto("Relatorio Mensal das Consultas"), ln=True, align="C")
        
        self.set_font("Arial", "", 10)
        data_emissao = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 6, f"Gerado em: {data_emissao}", ln=True, align="C")
        
        self.ln(8)
        self.set_draw_color(15, 98, 254)
        self.line(10, self.get_y(), 287, self.get_y())
        self.ln(10)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(15, 98, 254)
        self.line(10, self.get_y(), 287, self.get_y())
        
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

    def truncarText(self, text, max_length):
        texto_limpo = self.limparTexto(text)
        if len(texto_limpo) > max_length:
            return texto_limpo[:max_length-3] + "..."
        return texto_limpo

    def tabelaCabecalho(self):
        self.set_fill_color(15, 98, 254)
        self.set_text_color(255)
        self.set_font("Arial", "B", 7)

        larguras = {
            "Data": 18,
            "Fornecedor": 28,
            "CNPJ": 24,
            "UF": 8,
            "CNAE": 16,
            "Regime": 24,
            "Produto": 32,
            "Codigo": 26,
            "NCM": 14,
            "Aliq.Prod": 14,
            "Valor Base": 18,
            "Aliq.Aplic": 14,
            "Valor Final": 20
        }
        
        colunas = ["Data", "Fornecedor", "CNPJ", "UF", "CNAE", "Regime", "Produto", "Codigo", "NCM", "Aliq.Prod", "Valor Base", "Aliq.Aplic", "Valor Final"]
                  
        for col in colunas:
            self.cell(larguras[col], 10, self.limparTexto(col), border=0, align="C", fill=True)
        
        self.ln()
        
        self.set_draw_color(15, 98, 254)
        self.line(10, self.get_y(), 287, self.get_y())
        self.ln(3)

    def dados(self, item, fill_color=None):
        self.set_text_color(0)
        self.set_font("Arial", "", 7)
        
        if fill_color:
            self.set_fill_color(fill_color[0], fill_color[1], fill_color[2])
        
        larguras = [18, 28, 24, 8, 16, 24, 32, 26, 14, 14, 18, 14, 20]
        
        dados = [
            self.limparTexto(item["data"]),
            self.truncarText(item["fornecedor"], 26),
            self.limparTexto(item["cnpj"]),
            self.limparTexto(item["uf"]),
            self.limparTexto(item["cnae"]),
            self.truncarText(item["regime"], 22),
            self.truncarText(item["produto"], 30),
            self.limparTexto(item["codigo"]),
            self.limparTexto(item["ncm"]),
            self.limparTexto(str(item["aliquotaProduto"])),
            f"R$ {item['valor_base']:.2f}",
            self.limparTexto(str(item["aliquota"])),
            f"R$ {item['valor_final']:.2f}"
        ]
        
        fill = fill_color is not None
        
        for i, valor in enumerate(dados):
            self.cell(larguras[i], 8, str(valor), border=0, align="C", fill=fill)
        
        self.ln()

    def gerarTabela(self, dados):
        if not dados:
            self.set_font("Arial", "", 12)
            self.cell(0, 10, "Nenhum dado encontrado para gerar o relatorio.", ln=True, align="C")
            return
            
        self.tabelaCabecalho()
        
        for i, item in enumerate(dados):
            if self.get_y() > 180:
                self.add_page()
                self.tabelaCabecalho()
            
            fill_color = (248, 249, 250) if i % 2 == 0 else None
            self.dados(item, fill_color)
        
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 287, self.get_y())

    def gerarResumo(self, dados):
        if not dados:
            return
        
        if self.get_y() > 160:
            self.add_page()
            
        self.ln(10)
        
        self.set_font("Arial", "B", 12)
        self.set_text_color(15, 98, 254)
        self.cell(0, 8, "RESUMO DO RELATORIO", ln=True, align="C")
        self.ln(5)
        
        total_registros = len(dados)
        total_valor_base = sum(float(item["valor_base"]) for item in dados)
        total_valor_final = sum(float(item["valor_final"]) for item in dados)
        total_impostos = total_valor_final - total_valor_base
        
        self.set_font("Arial", "", 10)
        self.set_text_color(0)
        
        y_inicial = self.get_y()
        self.set_fill_color(245, 247, 250)
        self.rect(10, y_inicial, 277, 25, 'F')
        
        self.set_xy(15, y_inicial + 5)
        self.cell(135, 6, f"Total de registros: {total_registros}", ln=False)
        self.cell(137, 6, f"Valor base total: R$ {total_valor_base:.2f}", ln=True)
        
        self.set_x(15)
        self.cell(135, 6, f"Valor final total: R$ {total_valor_final:.2f}", ln=False)
        self.cell(137, 6, f"Total de impostos: R$ {total_impostos:.2f}", ln=True)

def gerarPdfDados(dados, caminho_pdf_final):
    try:
        pdf = RelatorioPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        
        pdf.gerarTabela(dados)
        pdf.gerarResumo(dados)
        
        pdf.output(caminho_pdf_final)
        
    except Exception as e:
        raise Exception(f"Erro ao gerar PDF: {str(e)}")