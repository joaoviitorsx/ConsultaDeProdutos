from sqlalchemy import create_engine, Column, Integer, String, Float, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, nullable=False)
    codigo = Column(String(32), nullable=False)
    produto = Column(String(40), nullable=False)
    ncm = Column(String(8), nullable=False)
    aliquota = Column(DECIMAL(5, 2), nullable=False)

class ProdutoModel:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def buscarCodigo(self, codigoProduto):
        session = self.Session()
        produto = session.query(Produto).filter_by(codigo=codigoProduto).first()
        session.close()
        if produto:
            return {
                "id": produto.id,
                "empresa_id": produto.empresa_id,
                "codigo": produto.codigo,
                "produto": produto.produto,
                "ncm": produto.ncm,
                "aliquota": produto.aliquota
            }
        return None