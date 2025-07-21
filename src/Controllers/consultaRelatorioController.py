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
        consultas = service.buscarConsultasPorPeriodo(empresa_id, mes, ano)
        for c in consultas:
            c.pop('_sa_instance_state', None)
        return consultas
    except Exception as e:
        print("Erro ao buscar consultas:", e)
        raise HTTPException(status_code=500, detail=str(e))