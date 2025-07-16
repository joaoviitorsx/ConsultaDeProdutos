import httpx
from src.Models.produtoModel import ProdutoModel

BACKEND_URL = "http://localhost:8000/api"

async def buscarFornecedorApi(cnpj):
    cnpjLimpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_URL}/consulta-fornecedor/{cnpjLimpo}")
            resp.raise_for_status()
            data = resp.json().get("data")
            if not data:
                raise ValueError("Fornecedor não encontrado.")
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("CNPJ não encontrado.")
            raise
        except Exception as e:
            raise ValueError(f"Erro ao buscar fornecedor: {str(e)}")

async def buscarProdutoApi(codigo_produto):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_URL}/produto", params={"codigo_produto": codigo_produto})
            resp.raise_for_status()
            data = resp.json()
            if not data:
                raise ValueError("Produto não encontrado.")
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError("Código do produto não encontrado.")
            raise
        except Exception as e:
            raise ValueError(f"Erro ao buscar produto: {str(e)}")

class ConsultaProdutosService:
    def __init__(self, db_url):
        self.produtoModel = ProdutoModel(db_url)

    def consultarProdutos(self, codigoProduto):
        return self.produtoModel.buscarCodigo(codigoProduto)

    def calcularImposto(self, valor_produto, aliquota, regime, decreto=False, uf=None, categoria_fiscal=None):
        """
        Regras fiscais:
        - Se fornecedor é do CE e decreto se aplica, zera impostos.
        - Se for do CE e não isento, usa alíquota do banco.
        - Se for de fora do CE, busca alíquota da tabela decreto com base na UF e categoria fiscal.
        - Se alíquota for ST ou ISENTO, não calcula imposto.
        - Se fornecedor é Simples, soma 3% ao valor final.
        """
        valor = float(valor_produto)

        # Regra 1: Produto isento por decreto estadual (somente CE)
        if uf == "CE" and decreto:
            return {
                "aliquota_utilizada": "0%",
                "regra_aplicada": "Decreto 29.560/08 (isenção total)",
                "valor_imposto": 0.0,
                "valor_final": valor,
                "icms": 0.0,
                "adicional_simples": 0.0
            }

        # Regra 2: Produto com ST ou ISENTO (independente da UF)
        if isinstance(aliquota, str) and aliquota.strip().upper() in ["ST", "ISENTO"]:
            return {
                "aliquota_utilizada": aliquota,
                "regra_aplicada": "Isento ou Substituição Tributária",
                "valor_imposto": 0.0,
                "valor_final": valor,
                "icms": 0.0,
                "adicional_simples": 0.0
            }

        # Regra 3: Fornecedor de fora do CE → buscar alíquota na tabela decreto
        if uf != "CE" and categoria_fiscal:
            aliquota = self.produtoModel.decreto(uf, categoria_fiscal)
            if aliquota is None:
                raise ValueError(f"Não foi encontrada alíquota para UF={uf} e categoria={categoria_fiscal}")

        # Conversão e aplicação de alíquota
        aliquota = float(str(aliquota).replace('%', '').replace(',', '.'))
        icms = valor * (aliquota / 100)
        adicional_simples = 0.0
        regra = "Alíquota padrão"
        aliquota_final = aliquota

        if regime.lower() == "simples nacional":
            adicional_simples = valor * 0.03
            regra = "Simples Nacional (3% adicional)"

        valor_imposto = icms + adicional_simples
        valor_final = valor + valor_imposto

        return {
            "aliquota_utilizada": aliquota_final,
            "regra_aplicada": regra,
            "valor_imposto": valor_imposto,
            "valor_final": valor_final,
            "icms": icms,
            "adicional_simples": adicional_simples,
        }