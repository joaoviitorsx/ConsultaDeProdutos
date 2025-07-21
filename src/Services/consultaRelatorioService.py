from src.Models.consultaModel import ConsultaModel, Consulta
from datetime import datetime

class ConsultaRelatorioService:
    def __init__(self, db_url):
        self.model = ConsultaModel(db_url)

    def buscarConsultasPorPeriodo(self, empresa_id: int, mes: str, ano: str) -> list:
        from sqlalchemy import extract
        session = self.model.Session()
        try:
            consultas = (
                session.query(Consulta)
                .filter(
                    Consulta.empresa_id == empresa_id,
                    extract("month", Consulta.dataConsulta) == int(mes),
                    extract("year", Consulta.dataConsulta) == int(ano)
                )
                .order_by(Consulta.dataConsulta.desc())
                .all()
            )
            return [c.__dict__ for c in consultas]
        finally:
            session.close()