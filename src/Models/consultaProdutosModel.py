from src.Config.database.dbConsultaProdutos import BaseConsulta
from sqlalchemy import Column, Integer, String, Boolean

class Produto(BaseConsulta):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer)
    codigo = Column(String(32))
    produto = Column(String(255))
    ncm = Column(String(8))
    aliquota = Column(String(10))
    categoriaFiscal = Column(String(40))

class Usuario(BaseConsulta):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    usuario = Column(String)
    senha = Column(String)
    razaoSocial = Column(String)
    empresa_id = Column(Integer)
    ativo = Column(Boolean)
    cnpj = Column(String)