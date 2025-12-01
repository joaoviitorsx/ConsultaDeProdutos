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
            # Calcula a data inicial e final do período
            data_inicio = datetime(ano, mes, 1)
            if mes == 12:
                data_fim = datetime(ano + 1, 1, 1)
            else:
                data_fim = datetime(ano, mes + 1, 1)
            
            print(f"Buscando consultas - Empresa: {empresa_id}, Período: {data_inicio} até {data_fim}")
            
            consultas = session.query(Consulta).filter(
                Consulta.empresa_id == empresa_id,
                Consulta.dataConsulta >= data_inicio,
                Consulta.dataConsulta < data_fim
            ).order_by(desc(Consulta.dataConsulta)).all()
            
            print(f"Total de consultas encontradas: {len(consultas)}")

            def consulta_to_dict(c):
                try:
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
                except Exception as e:
                    print(f"Erro ao converter consulta {c.id}: {e}")
                    raise

            resultado = [consulta_to_dict(c) for c in consultas]
            print(f"Consultas convertidas com sucesso: {len(resultado)}")
            return resultado
        except Exception as e:
            print(f"Erro ao buscar consultas por período: {e}")
            raise
        finally:
            session.close()
