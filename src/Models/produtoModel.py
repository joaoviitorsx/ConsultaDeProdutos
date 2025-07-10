import sqlalchemy

class ProdutoModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def buscarCodigo(self, codigoProduto):
        conexao = sqlalchemy.connect(self.db_path)
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, empresa_id, codigo, produto, ncm, aliquota FROM Produtos WHERE codigo = ?",
            (codigoProduto,)
        )
        row = cursor.fetchone()
        conexao.close()
        if row:
            return {
                "id": row[0],
                "empresa_id": row[1],
                "produto": row[2],
                "ncm": row[3],
                "aliquota": row[4]
            }
        return None