from fastapi import APIRouter, HTTPException
from src.Utils.validadores import removedorCaracteres, validarCnpj
from src.Services.consultaFornecedorService import buscarFornecedorCnpj

router = APIRouter()

@router.get("/consulta-fornecedor/{cnpj}")
async def consulta_fornecedor(cnpj: str):
    try:
        cnpjLimpo = removedorCaracteres(cnpj)
        
        if not validarCnpj(cnpjLimpo):
            raise HTTPException(
                status_code=400, 
                detail="CNPJ inválido: deve conter 14 dígitos numéricos"
            )

        fornecedor = await buscarFornecedorCnpj(cnpjLimpo)
        
        if not fornecedor:
            raise HTTPException(
                status_code=404, 
                detail="Fornecedor não encontrado na base de dados"
            )

        response_data = {
            "cnpj": fornecedor.get("cnpj"),
            "razao_social": fornecedor.get("razao_social"),
            "nome_fantasia": fornecedor.get("razao_social"),
            "cnae": fornecedor.get("cnae"),
            "uf": fornecedor.get("uf"),
            "simples": fornecedor.get("simples", False),
            "isento": fornecedor.get("decreto", False),
            "regime_tributario": "Simples Nacional" if fornecedor.get("simples", False) else "Lucro Real"
        }

        return {
            "success": True,
            "data": response_data,
            "message": "Fornecedor encontrado com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERRO] Controller: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erro interno do servidor"
        )