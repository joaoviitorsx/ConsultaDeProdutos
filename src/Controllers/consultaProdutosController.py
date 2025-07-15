from fastapi import APIRouter, HTTPException
from src.Services.consultaProdutosService import ConsultaProdutosService
from src.Config.database.db import sqlalchemy_url

db_url = sqlalchemy_url()
router = APIRouter()
service = ConsultaProdutosService(db_url)

@router.get("/produto")
def get_produto(codigo_produto: str):
    produto = service.consultarProdutos(codigo_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/calcular")
def calcular_valor(
    codigo_produto: str,
    valor_produto: float,
    regime: str,
    decreto: bool = False
):
    produto = service.consultarProdutos(codigo_produto)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    resultado = service.calcularImposto(
        valor_produto=valor_produto,
        aliquota=produto["aliquota"],
        regime=regime,
        decreto=decreto
    )
    return resultado