from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.Config.database.db import sqlalchemy_url

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    razaoSocial = Column(String(255), nullable=True)
    empresa_id = Column(Integer, nullable=True)
    ativo = Column(Boolean, default=True)

class UsuarioModel:
    def __init__(self, db_url=None):
        self.db_url = db_url or sqlalchemy_url()
        self.engine = create_engine(self.db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def listarTodos(self):
        session = self.Session()
        try:
            usuarios = session.query(Usuario).all()
            return [
                {
                    "id": u.id,
                    "usuario": u.usuario,
                    "razaoSocial": u.razaoSocial or "",
                    "empresa_id": u.empresa_id,
                    "ativo": u.ativo
                }
                for u in usuarios
            ]
        finally:
            session.close()

    def buscarUsuario(self, usuario):
        session = self.Session()
        try:
            user = session.query(Usuario).filter_by(usuario=usuario).first()
            if user:
                return {
                    "id": user.id,
                    "usuario": user.usuario,
                    "razaoSocial": user.razaoSocial or "",
                    "empresa_id": user.empresa_id,
                    "ativo": user.ativo
                }
            return None
        finally:
            session.close()

    def inserir(self, dados):
        session = self.Session()
        try:
            novoUsuario = Usuario(
                usuario=dados["usuario"],
                senha=dados["senha"],
                razaoSocial=dados.get("razaoSocial", ""),
                empresa_id=dados.get("empresa_id"),
                ativo=dados.get("ativo", True)
            )
            session.add(novoUsuario)
            session.commit()
        finally:
            session.close()

    def atualizar(self, id, dados):
        session = self.Session()
        try:
            usuario = session.query(Usuario).filter_by(id=id).first()
            if not usuario:
                return False
            for campo in ["usuario", "senha", "razaoSocial", "empresa_id", "ativo"]:
                if campo in dados:
                    setattr(usuario, campo, dados[campo])
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print("Erro ao atualizar usuário:", e)
            return False
        finally:
            session.close()

    def excluir(self, id):
        session = self.Session()
        try:
            usuario = session.query(Usuario).filter_by(id=id).first()
            if usuario:
                session.delete(usuario)
                session.commit()
                return True
            return False
        finally:
            session.close()