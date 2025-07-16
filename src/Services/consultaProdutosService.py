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

async def calcularImposto(codigo_produto, valor_produto, regime, decreto):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BACKEND_URL}/calcular",
            params={
                "codigo_produto": codigo_produto,
                "valor_produto": valor_produto,
                "regime": regime,
                "decreto": decreto
            }
        )
        resp.raise_for_status()
        return resp.json()
    
class ConsultaProdutosService:
    def __init__(self, db_url):
        self.produtoModel = ProdutoModel(db_url)

    def consultarProdutos(self, codigoProduto):
        return self.produtoModel.buscarCodigo(codigoProduto)

    def calcularImposto(self, valor_produto, aliquota, regime, decreto=False):
        """
        - Se fornecedor é Simples, soma 3% à alíquota do produto.
        - Se aliquota for 'ST' ou 'ISENTO', não calcula imposto.
        - Se for do decreto, aplica regra específica (exemplo: multiplica alíquota por 1.2).
        - Else, usa apenas a alíquota do produto.
        """
        valor = float(valor_produto)

        if isinstance(aliquota, str) and aliquota.strip().upper() in ["ST", "ISENTO"]:
            return {
                "aliquota_utilizada": aliquota,
                "regra_aplicada": "Isento/ST",
                "valor_imposto": 0.0,
                "valor_final": valor,
                "icms": 0.0,
                "adicional_simples": 0.0
            }

        aliquota = float(str(aliquota).replace('%', '').replace(',', '.'))
        icms = 0.0
        adicional_simples = 0.0

        if regime.lower() == "simples nacional":
            aliquota_final = aliquota + 3
            regra = "Simples Nacional (+3%)"
            icms = valor * (aliquota / 100)
            adicional_simples = valor * 0.03
        elif decreto:
            aliquota_final = aliquota * 1.2
            regra = "Decreto (aliquota x 1.2)"
            icms = valor * (aliquota_final / 100)
        else:
            aliquota_final = aliquota
            regra = "Alíquota padrão"
            icms = valor * (aliquota_final / 100)

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