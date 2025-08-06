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
        - Se fornecedor for fora do CE, ignora alíquota do banco e usa tabela decreto (categoriaFiscal + UF).
        - Se fornecedor é Simples, soma 3% ao valor final.
        """
        valor = float(valor_produto)

        # print("DEBUG - INÍCIO cálculo de imposto")
        # print(f"Valor do produto: {valor}")
        # print(f"UF fornecedor: {uf}")
        # print(f"Regime tributário: {regime}")
        # print(f"Categoria Fiscal: {categoriaFiscal}")
        # print(f"Alíquota do produto (banco): {aliquota}")
        # print(f"Decreto aplica? {'Sim' if decreto else 'Não'}")

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

        # Regra 3: Fornecedor fora do CE → usar tabela decreto
        if uf and uf != "CE" and categoriaFiscal:
            aliquota_decreto = self.produtoModel.decreto(uf, categoriaFiscal)
            print(f"🔸 Alíquota via decreto encontrada: {aliquota_decreto}")
            if aliquota_decreto is None:
                raise ValueError(f"Não foi encontrada alíquota para UF={uf} e categoria={categoriaFiscal}")
            aliquota_convertida = float(str(aliquota_decreto).replace('%', '').replace(',', '.'))
            regra = "Alíquota via tabela decreto"
        else:
            # Caso CE (sem isenção ou ST) → usa alíquota do produto
            try:
                aliquota_convertida = float(str(aliquota).replace('%', '').replace(',', '.'))
                regra = "Alíquota padrão"
            except ValueError:
                raise ValueError("Alíquota inválida no banco de dados.")

        # Cálculo de imposto
        icms = valor * (aliquota_convertida / 100)
        adicional_simples = 0.0

        if regime.lower() == "simples nacional":
            adicional_simples = valor * 0.03
            regra += " + Simples Nacional (3%)"

        valor_imposto = icms + adicional_simples
        valor_final = valor + valor_imposto

        print("🟩 RESULTADO DO CÁLCULO:")
        print(f"🔹 Aliquota utilizada: {aliquota_convertida:.2f}%")
        print(f"🔹 ICMS: {icms:.2f}")
        print(f"🔹 Adicional Simples: {adicional_simples:.2f}")
        print(f"🔹 Valor final: {valor_final:.2f}")
        print(f"📌 Regra aplicada: {regra}")

        return {
            "aliquota_utilizada": f"{aliquota_convertida:.2f}%",
            "regra_aplicada": regra,
            "valor_imposto": round(valor_imposto, 2),
            "valor_final": round(valor_final, 2),
            "icms": round(icms, 2),
            "adicional_simples": round(adicional_simples, 2),
        }

