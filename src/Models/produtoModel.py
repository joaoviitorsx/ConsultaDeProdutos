from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Table, MetaData, select
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

class ProdutoModel:
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
            produto = session.query(Produto).filter_by(id=id).first()
            if not produto:
                return False
            for campo in ["empresa_id", "codigo", "produto", "ncm", "aliquota", "categoriaFiscal"]:
                if campo in dados:
                    setattr(produto, campo, dados[campo])
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print("Erro ao atualizar produto:", e)
            return False
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

    def decreto(self, uf: str, categoria_fiscal: str) -> float | None:
        categoria_map = {
            "20RegraGeral": "20RegraGeral",
            "7CestaBasica": "7CestaBasica",
            "12CestaBasica": "12CestaBasica",
            "28BebidaAlcoolica": "28BebidaAlcoolica"
        }

        nome_coluna = categoria_map.get(categoria_fiscal)
        if not nome_coluna:
            raise ValueError(f"Categoria fiscal '{categoria_fiscal}' inválida.")

        metadata = MetaData()
        decreto_table = Table("decreto", metadata, autoload_with=self.engine)

        with self.engine.connect() as conn:
            stmt = select(decreto_table.c[nome_coluna]).where(decreto_table.c.uf == uf)
            result = conn.execute(stmt).fetchone()
            return result[0] if result else None
