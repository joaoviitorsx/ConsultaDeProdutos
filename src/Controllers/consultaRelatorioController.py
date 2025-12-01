from fastapi import APIRouter, Query, HTTPException
from src.Services.consultaRelatorioService import ConsultaRelatorioService
from src.Config.database.db import sqlalchemy_url

router = APIRouter()
service = ConsultaRelatorioService(sqlalchemy_url())

@router.get("/consultas-relatorio")
def get_consultas_relatorio(
    empresa_id: int = Query(..., description="ID da empresa"),
    mes: int = Query(..., ge=1, le=12, description="Mês da consulta"),
    ano: int = Query(..., description="Ano da consulta")
):
    try:
        print(f"Recebida requisição - empresa_id: {empresa_id}, mes: {mes}, ano: {ano}")
        resultado = service.buscarConsultasPorPeriodo(empresa_id, mes, ano)
        print(f"Retornando {len(resultado)} consultas")
        return resultado
    except Exception as e:
        import traceback
        print("Erro ao buscar consultas:", e)
        print("Traceback completo:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
