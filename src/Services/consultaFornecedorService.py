from src.Utils.cnpj import buscarInformacoesApi
from src.Utils.validadores import removedorCaracteres
from src.Models.fornecedorModel import FornecedorModel

async def buscarFornecedorCnpj(cnpj: str) -> dict | None:
    cnpj = removedorCaracteres(cnpj)
    fornecedorModel = FornecedorModel()

    fornecedor = fornecedorModel.buscarCNPJ(cnpj)
    if fornecedor:
        print(f"[✔] Fornecedor {cnpj} encontrado no banco")
        return {
            "cnpj": fornecedor["cnpj"],
            "razao_social": fornecedor["razaoSocial"],
            "cnae": fornecedor["cnae"],
            "uf": fornecedor["uf"],
            "simples": fornecedor["simples"],
            "decreto": fornecedor["decreto"]
        }

    print(f"[🔍] Fornecedor {cnpj} não encontrado no banco, buscando na API...")
    resultado = await buscarInformacoesApi(cnpj)

    if resultado and len(resultado) == 5:
        razaoSocial, cnaeCodigo, uf, simplesValor, isento = resultado

        if razaoSocial and razaoSocial.strip():
            fornecedorApi = {
                "cnpj": cnpj,
                "razaoSocial": razaoSocial.strip(),
                "cnae": cnaeCodigo,
                "uf": uf,
                "simples": simplesValor,
                "decreto": isento,
                "empresa_id": 1
            }

            fornecedorModel.inserir(fornecedorApi)
            print(f"[✔] Fornecedor {cnpj} salvo no banco após consulta API")
            return {
                "cnpj": fornecedorApi["cnpj"],
                "razao_social": fornecedorApi["razaoSocial"],
                "cnae": fornecedorApi["cnae"],
                "uf": fornecedorApi["uf"],
                "simples": fornecedorApi["simples"],
                "decreto": fornecedorApi["decreto"]
            }

    print(f"[Error] Fornecedor {cnpj} não encontrado")
    return None
