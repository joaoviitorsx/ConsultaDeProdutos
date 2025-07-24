from src.Config.database.dbEmpresas import BaseEmpresas
from sqlalchemy import Column, Integer, String

class CadastroTributacao(BaseEmpresas):
    __tablename__ = "cadastro_tributacao"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, index=True)
    codigo = Column(String(60))
    produto = Column(String(255))
    ncm = Column(String(20))
    aliquota = Column(String(10))
    categoriaFiscal = Column(String(40))

class Empresa(BaseEmpresas):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(20), unique=True, index=True)
    razao_social = Column(String(100))