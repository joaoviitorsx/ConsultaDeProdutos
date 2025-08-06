from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from src.Models.consultaModel import Consulta
from datetime import datetime

class ConsultaRelatorioService:
    def __init__(self, db_url):
        from sqlalchemy import create_engine
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def buscarConsultasPorPeriodo(self, empresa_id: int, mes: int, ano: int):
        session = self.Session()
        try:
            consultas = session.query(Consulta).filter(
                Consulta.empresa_id == empresa_id,
                Consulta.dataConsulta >= datetime(ano, mes, 1),
                Consulta.dataConsulta < datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1)
            ).order_by(desc(Consulta.dataConsulta)).all()

            def consulta_to_dict(c):
                return {
                    "id": c.id,
                    "usuario_id": c.usuario_id,
                    "empresa_id": c.empresa_id,
                    "cnpjFornecedor": c.cnpjFornecedor,
                    "nomeFornecedor": c.nomeFornecedor,
                    "codigoProduto": c.codigoProduto,
                    "produto": c.produto,
                    "valorBase": c.valorBase,
                    "uf": c.uf,
                    "regime": c.regime,
                    "aliquotaAplicada": c.aliquotaAplicada,
                    "adicionalSimples": c.adicionalSimples,
                    "valorFinal": c.valorFinal,
                    "dataConsulta": c.dataConsulta.isoformat() if c.dataConsulta else None,
                    "cnae": c.cnae,
                    "ncm": c.ncm,
                    "aliquotaProduto": c.aliquotaProduto,
                    "decreto": c.decreto
                }

            return [consulta_to_dict(c) for c in consultas]
        finally:
            session.close()
