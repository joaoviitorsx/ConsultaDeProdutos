from src.Config.database.db import conectarBanco, fecharBanco
from src.Utils.cnpj import buscarInformacoesApi
from src.Utils.validadores import removedorCaracteres

async def buscarFornecedorCnpj(cnpj: str) -> dict | None:
    cnpj = removedorCaracteres(cnpj)
    
    print(f"[🔍] Buscando {cnpj} na API")
    resultado = await buscarInformacoesApi(cnpj)
    
    if resultado and len(resultado) == 5:
        razao_social, cnae_codigo, isento, uf, simples_valor = resultado
        
        if razao_social and razao_social.strip():
            fornecedor = {
                "cnpj": cnpj,
                "razao_social": razao_social.strip(),
                "cnae": cnae_codigo,
                "uf": uf,
                "simples": simples_valor,
                "decreto": isento
            }
            
            print(f"[✔] Fornecedor {cnpj} encontrado na API")
            return fornecedor
        else:
            print(f"[Error] Razão social vazia para CNPJ {cnpj}")
    else:
        print(f"[Error] Resultado inválido da API para CNPJ {cnpj}")
    
    print(f"[Error] Fornecedor {cnpj} não encontrado")
    return None

async def salvarFornecedor(fornecedor: dict):
    conexao = conectarBanco()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT cnpj FROM fornecedores WHERE cnpj = %s", (fornecedor["cnpj"],))
        if cursor.fetchone():
            print(f"[Info] Fornecedor {fornecedor['cnpj']} já existe no banco")
            return
            
        cursor.execute("""
            INSERT INTO fornecedores (cnpj, razao_social, cnae, uf, simples, decreto)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            fornecedor["cnpj"],
            fornecedor["razao_social"],
            fornecedor["cnae"],
            fornecedor["uf"],
            fornecedor["simples"],
            fornecedor["decreto"]
        ))
        conexao.commit()
        print(f"[Info] Fornecedor {fornecedor['cnpj']} salvo no banco.")
    except Exception as e:
        print(f"[ERRO] ao salvar fornecedor: {e}")
        conexao.rollback()
    finally:
        fecharBanco(conexao)