from src.Models.produtoModel import ProdutoModel

class ProdutoService:
    def __init__(self, model: ProdutoModel):
        self.model = model

    def listar(self):
        return self.model.listarTodos()

    def adicionar(self, dados):
        if self.model.buscarCodigo(dados["codigo"]):
            raise ValueError("Já existe um produto com este código.")
        self.model.inserir(dados)

    def editar(self, id, dados):
        produtoExistente = self.model.buscarCodigo(dados["codigo"])
        if produtoExistente and produtoExistente["id"] != id:
            raise ValueError("Código já utilizado por outro produto.")
        self.model.atualizar(id, dados)

    def excluir(self, id):
        self.model.excluir(id)
