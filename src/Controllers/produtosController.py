from src.Services.produtoService import ProdutoService
from src.Models.produtoModel import ProdutoModel
from src.Config.database.db import sqlalchemy_url

class ProdutoController:
    def __init__(self, db_url=None):
        self.db_url = db_url or sqlalchemy_url()
        self.model = ProdutoModel(self.db_url)
        self.service = ProdutoService(self.model)

    def listar(self):
        return self.service.listar()

    def adicionar(self, dados):
        try:
            self.service.adicionar(dados)
        except ValueError as e:
            return str(e)
        return None

    def editar(self, id, dados):
        try:
            self.service.editar(id, dados)
        except ValueError as e:
            return str(e)
        return None

    def excluir(self, id):
        self.service.excluir(id)
