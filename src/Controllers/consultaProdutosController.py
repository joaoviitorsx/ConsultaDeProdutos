from fastapi import APIRouter, HTTPException, Query
from src.Services.consultaProdutosService import ConsultaProdutosService, buscarFornecedorApi
from src.Config.database.db import sqlalchemy_url

db_url = sqlalchemy_url()
router = APIRouter()
service = ConsultaProdutosService(db_url)

@router.get("/produto")
def get_produto(codigo_produto: str, empresa_id: int):
    produto = service.consultarProdutos(codigo_produto, empresa_id)
    if not produto or not produto.get("id"):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/calcular")
async def calcular_valor(
    codigo_produto: str,
    valor_produto: float,
    empresa_id: int = Query(..., description="ID da empresa do usuário logado"),
    cnpj_fornecedor: str = Query(..., description="CNPJ do fornecedor sem máscara")
):
    produto = service.consultarProdutos(codigo_produto, empresa_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    try:
        fornecedor = await buscarFornecedorApi(cnpj_fornecedor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    resultado = service.calcularImposto(
        valor_produto=valor_produto,
        aliquota=produto["aliquota"],
        regime=fornecedor.get("regime", "Outro"),
        decreto=fornecedor.get("isento", False),
        uf=fornecedor.get("uf", ""),
        categoriaFiscal=produto.get("categoriaFiscal", "")
    )

    return {
        "produto": {
            "codigo": produto["codigo"],
            "descricao": produto["produto"],
            "aliquota": produto["aliquota"],
            "categoriaFiscal": produto.get("categoriaFiscal", "")
        },
        "fornecedor": {
            "cnpj": fornecedor.get("cnpj"),
            "uf": fornecedor.get("uf"),
            "simples": fornecedor.get("simples"),
            "isento": fornecedor.get("isento"),
            "regime": fornecedor.get("regime")
        },
        "calculo": resultado
    }

