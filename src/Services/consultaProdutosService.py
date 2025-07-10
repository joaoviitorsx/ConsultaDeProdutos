from src.Models.produtoModel import ProdutoModel

class ConsultaProdutosService:
    def __init__(self, db_path):
        self.produto_model = ProdutoModel(db_path)

    def consultar_produto(self, codigo_produto):
        return self.produto_model.buscar_por_codigo(codigo_produto)

    def calcular_valor_final(self, valor_produto, aliquota, regime, decreto=False):
        valor = float(valor_produto)
        icms = valor * (aliquota / 100)
        if regime == "Simples Nacional":
            pis = cofins = adicional = 0
        else:
            pis = valor * 0.0165
            cofins = valor * 0.076
            adicional = valor * 0.03 if decreto else 0
        total = valor + icms + pis + cofins + adicional
        return {
            "valor_produto": valor,
            "icms": icms,
            "pis": pis,
            "cofins": cofins,
            "adicional": adicional,
            "valor_total": total
        }