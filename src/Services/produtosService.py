from src.Models.produtosModel import ProdutosModel

class ProdutoService:
    def __init__(self, model: ProdutosModel):
        self.model = model

    def listar(self):
        return self.model.listarTodos()

    def adicionar(self, dados):
        if self.model.buscarCodigo(dados["codigo"]):
            raise ValueError("Já existe um produto com este código.")
        self.model.inserir(dados)

    def editar(self, id, dados):
        produto_existente = self.model.buscarCodigo(dados["codigo"])
        if produto_existente and produto_existente["id"] != id:
            raise ValueError("Código já utilizado por outro produto.")
        self.model.atualizar(id, dados)

    def excluir(self, id):
        self.model.excluir(id)
