from fastapi import APIRouter, Query
from src.Services.consultaProdutosService import ConsultaProdutosService

router = APIRouter()
service = ConsultaProdutosService("CAMINHO_PARA_SEU_BANCO.db")

@router.get("/produto")
def get_produto(codigo_produto: str):
    produto = service.consultar_produto(codigo_produto)
    if not produto:
        return {"erro": "Produto não encontrado"}
    return produto

@router.post("/calcular")
def calcular_valor(codigo_produto: str, valor_produto: float, regime: str, decreto: bool = False):
    produto = service.consultar_produto(codigo_produto)
    if not produto:
        return {"erro": "Produto não encontrado"}
    resultado = service.calcular_valor_final(valor_produto, produto["aliquota"], regime, decreto)
    return resultado