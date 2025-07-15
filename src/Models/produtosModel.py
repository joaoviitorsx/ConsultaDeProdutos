import traceback
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.Config.database.db import sqlalchemy_url

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, nullable=False)
    codigo = Column(String(32), nullable=False)
    produto = Column(String(40), nullable=False)
    ncm = Column(String(8), nullable=False)
    aliquota = Column(String(12), nullable=False)
    categoriaFiscal = Column("categoriaFiscal", String(40), nullable=True)

class ProdutosModel:
    def __init__(self, db_url=None):
        self.db_url = db_url or sqlalchemy_url()
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def listarTodos(self):
        session = self.Session()
        try:
            produtos = session.query(Produto).all()
            def parse_aliquota(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return val
            return [
                {
                    "id": p.id,
                    "empresa_id": p.empresa_id,
                    "codigo": p.codigo or "Vazio",
                    "produto": p.produto or "Vazio",
                    "ncm": p.ncm or "Vazio",
                    "aliquota": parse_aliquota(p.aliquota) or "0.00",
                    "categoriaFiscal": p.categoriaFiscal or "Vazio"
                }
                for p in produtos
            ]
        finally:
            session.close()

    def buscarCodigo(self, codigoProduto):
        session = self.Session()
        try:
            produto = session.query(Produto).filter_by(codigo=codigoProduto).first()
            if produto:
                try:
                    aliquotaValida = float(produto.aliquota)
                except (ValueError, TypeError):
                    aliquotaValida = produto.aliquota
                return {
                    "id": produto.id,
                    "empresa_id": produto.empresa_id,
                    "codigo": produto.codigo,
                    "produto": produto.produto,
                    "ncm": produto.ncm,
                    "aliquota": aliquotaValida,
                    "categoriaFiscal": produto.categoriaFiscal or ""
                }
            return None
        finally:
            session.close()
            
    def inserir(self, dados):
        session = self.Session()
        try:
            novoProduto = Produto(
                empresa_id=dados["empresa_id"],
                codigo=dados["codigo"],
                produto=dados["produto"],
                ncm=dados["ncm"],
                aliquota=dados["aliquota"],
                categoriaFiscal=dados.get("categoriaFiscal", "")
            )
            print("Inserindo produto com categoriaFiscal:", dados.get("categoriaFiscal"))
            session.add(novoProduto)
            session.commit()
        finally:
            session.close()

    def atualizar(self, id, dados):
        session = self.Session()
        try:
            print("Atualizando produto id =", id, "dados =", dados)
            p = session.query(Produto).filter_by(id=id).first()
            if not p:
                print("Produto não encontrado")
                return False
            p.empresa_id = dados.get("empresa_id", p.empresa_id)
            p.codigo = dados.get("codigo", p.codigo)
            p.produto = dados.get("produto", p.produto)
            p.ncm = dados.get("ncm", p.ncm)
            p.aliquota = dados.get("aliquota", p.aliquota)
            p.categoriaFiscal = dados.get("categoriaFiscal", p.categoriaFiscal)
            print("Valor de p.categoriaFiscal antes do commit:", p.categoriaFiscal)
            session.flush()
            session.commit()
            session.refresh(p)
            print("Commit OK")
            return True
        except Exception as e:
            session.rollback()
            print("Erro ao commitar:", e)
            traceback.print_exc()  # <-- Adicione esta linha
            raise
        finally:
            session.close()

    def excluir(self, id):
        session = self.Session()
        try:
            produto = session.query(Produto).filter_by(id=id).first()
            if produto:
                session.delete(produto)
                session.commit()
                return True
            return False
        finally:
            session.close()