import os
import httpx
from src.Models.produtoModel import ProdutoModel
from src.Models.consultaModel import ConsultaModel
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

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

async def buscarProdutoApi(codigo_produto: str, empresa_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{BACKEND_URL}/produto",
                params={"codigo_produto": codigo_produto, "empresa_id": empresa_id}
            )
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
        self.consultaModel = ConsultaModel(db_url)

    def consultarProdutos(self, codigo_produto: str, empresa_id: int) -> dict:
        return self.produtoModel.buscarCodigo(codigo_produto, empresa_id)
    
    def salvarConsultaUsuario(self, dados: dict):
        self.consultaModel.salvarConsulta(dados)

    def calcularImposto(self, valor_produto, aliquota, regime, decreto=False, uf=None, categoriaFiscal=None):
        """
        Regras fiscais:
        - Se fornecedor é do CE e decreto se aplica, zera impostos.
        - Se alíquota for ST ou ISENTO, não calcula imposto.
        - Em todos os casos, exceto isenções, validar a alíquota via tabela decreto (categoriaFiscal + UF).
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
                "regra_aplicada": "Isento ou ST",
                "valor_imposto": 0.0,
                "valor_final": valor,
                "icms": 0.0,
                "adicional_simples": 0.0
            }

        # Regra 3: Validação da alíquota com a tabela decreto, apenas para fora do CE
        if categoriaFiscal and uf and uf != "CE":
            aliquotaDecreto = self.produtoModel.decreto(uf, categoriaFiscal)
            if aliquotaDecreto is not None:
                aliquota = aliquotaDecreto
            else:
                raise ValueError(f"Não foi encontrada alíquota para UF={uf} e categoria={categoriaFiscal}")

        # Conversão e aplicação de alíquota
        aliquota = float(str(aliquota).replace('%', '').replace(',', '.'))
        icms = valor * (aliquota / 100)
        simplesNacional = 0.0
        regra = "Alíquota padrão"
        aliquotaFinal = aliquota

        if regime.lower() == "simples nacional":
            simplesNacional = valor * 0.03
            regra = "Simples Nacional (3% adicional)"

        valorImposto = icms + simplesNacional
        valorFinal = valor + valorImposto

        return {
            "aliquota_utilizada": aliquotaFinal,
            "regra_aplicada": regra,
            "valor_imposto": valorImposto,
            "valor_final": valorFinal,
            "icms": icms,
            "adicional_simples": simplesNacional,
        }
