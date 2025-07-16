from src.Models.fornecedorModel import FornecedorModel

class FornecedorService:
    def __init__(self, model: FornecedorModel):
        self.model = model

    def listar(self):
        return self.model.listarTodos()

    def adicionar(self, dados):
        if self.model.buscarCodigo(dados["codigo"]):
            raise ValueError("Já existe um produto com este código.")
        self.model.inserir(dados)

    def editar(self, id, dados):
        fornecedorExistente = self.model.buscarCodigo(dados["codigo"])
        if fornecedorExistente and fornecedorExistente["id"] != id:
            raise ValueError("Código já utilizado por outro produto.")
        self.model.atualizar(id, dados)

    def excluir(self, id):
        self.model.excluir(id)
