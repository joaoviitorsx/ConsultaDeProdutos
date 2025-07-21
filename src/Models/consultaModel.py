from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.Config.database.db import sqlalchemy_url

Base = declarative_base()

class Consulta(Base):
    __tablename__ = 'consultas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, nullable=False)
    empresa_id = Column(Integer, nullable=False)
    cnpjFornecedor = Column(String(18), nullable=False)
    nomeFornecedor = Column(String(60), nullable=True)
    codigoProduto = Column(String(32), nullable=False)
    produto = Column(String(60), nullable=True)
    valorBase = Column(Float, nullable=False)
    uf = Column(String(2), nullable=True)
    regime = Column(String(40), nullable=True)
    aliquotaAplicada = Column(String(10), nullable=True)
    adicionalSimples = Column(Float, nullable=True)
    valorFinal = Column(Float, nullable=False)
    dataConsulta = Column(DateTime, default=datetime.utcnow)

class ConsultaModel:
    def __init__(self, db_url=None):
        self.db_url = db_url or sqlalchemy_url()
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def salvarConsulta(self, dados: dict):
        session = self.Session()
        try:
            nova = Consulta(**dados)
            session.add(nova)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
