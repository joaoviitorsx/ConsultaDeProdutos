from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.Config.database.db import sqlalchemy_url

Base = declarative_base()

class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, nullable=False)
    cnpj = Column(String(14), nullable=False)
    razaoSocial = Column(String(255), nullable=False)
    cnae = Column(String(10), nullable=True)
    uf = Column(String(2), nullable=True)
    simples = Column(Boolean, default=False)
    decreto = Column(Boolean, default=False)

class FornecedorModel:
    def __init__(self, db_url=None):
        self.db_url = db_url or sqlalchemy_url()
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def listarTodos(self):
        session = self.Session()
        try:
            fornecedores = session.query(Fornecedor).all()
            return [
                {
                    "id": f.id,
                    "empresa_id": f.empresa_id,
                    "cnpj": f.cnpj,
                    "razaoSocial": f.razaoSocial,
                    "cnae": f.cnae or "",
                    "uf": f.uf or "",
                    "simples": f.simples,
                    "decreto": f.decreto
                }
                for f in fornecedores
            ]
        finally:
            session.close()

    def buscarCNPJ(self, cnpj, empresa_id=None):
        session = self.Session()
        try:
            query = session.query(Fornecedor).filter_by(cnpj=cnpj)
            if empresa_id is not None:
                query = query.filter_by(empresa_id=empresa_id)
            fornecedor = query.first()
            if fornecedor:
                return {
                    "id": fornecedor.id,
                    "empresa_id": fornecedor.empresa_id,
                    "cnpj": fornecedor.cnpj,
                    "razaoSocial": fornecedor.razaoSocial,
                    "cnae": fornecedor.cnae or "",
                    "uf": fornecedor.uf or "",
                    "simples": fornecedor.simples,
                    "decreto": fornecedor.decreto
                }
            return None
        finally:
            session.close()

    def inserir(self, dados):
        session = self.Session()
        try:
            novoFornecedor = Fornecedor(
                empresa_id=dados["empresa_id"],
                cnpj=dados["cnpj"],
                razaoSocial=dados["razaoSocial"],
                cnae=dados.get("cnae", ""),
                uf=dados.get("uf", ""),
                simples=dados.get("simples", False),
                decreto=dados.get("decreto", False)
            )
            session.add(novoFornecedor)
            session.commit()
        finally:
            session.close()

    def atualizar(self, id, dados):
        session = self.Session()
        try:
            fornecedor = session.query(Fornecedor).filter_by(id=id).first()
            if not fornecedor:
                return False
            for campo in ["empresa_id", "cnpj", "razaoSocial", "cnae", "uf", "simples", "decreto"]:
                if campo in dados:
                    setattr(fornecedor, campo, dados[campo])
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print("Erro ao atualizar fornecedor:", e)
            return False
        finally:
            session.close()

    def excluir(self, id):
        session = self.Session()
        try:
            fornecedor = session.query(Fornecedor).filter_by(id=id).first()
            if fornecedor:
                session.delete(fornecedor)
                session.commit()
                return True
            return False
        finally:
            session.close()