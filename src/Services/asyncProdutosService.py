from sqlalchemy.orm import Session
from src.Models.consultaProdutosModel import Produto, Usuario
from src.Models.apuradorModel import CadastroTributacao, Empresa

def sincroanizarProdutos(cnpj: str, db_empresas: Session, db_consulta: Session):
    """
    1.O usuário loga → consulta tabela usuarios no banco consultaprodutos.
    2.A partir desse usuário, você obtém o CNPJ (usuarios.cnpj).

    Depois:
        Conecta ao banco empresas_db
        Verifica se existe uma empresa com esse mesmo CNPJ
        Se existir, você pega o id (empresa_id) da tabela empresas
        E com esse empresa_id, consulta os dados da tabela cadastro_tributacao para sincronização.
    """
    print(f"🔄 Iniciando sincronização para CNPJ: {cnpj}")

    empresa = db_empresas.query(Empresa).filter(Empresa.cnpj == cnpj).first()
    if not empresa:
        return {
            "message": f"Empresa com CNPJ {cnpj} não encontrada no banco de origem (empresas_db).",
            "produtos_inseridos": 0,
            "produtos_atualizados": 0
        }

    usuario = db_consulta.query(Usuario).filter(Usuario.cnpj == cnpj).first()
    if not usuario or not usuario.empresa_id:
        return {
            "message": f"Usuário com CNPJ {cnpj} não encontrado no banco de destino (consultaprodutos).",
            "produtos_inseridos": 0,
            "produtos_atualizados": 0
        }

    empresa_id_consulta = usuario.empresa_id
    tributacoes = db_empresas.query(CadastroTributacao).filter(
        CadastroTributacao.empresa_id == empresa.id
    ).all()

    novos = 0
    atualizados = 0

    for trib in tributacoes:
        ncm = (trib.ncm or "")[:8]

        existente = db_consulta.query(Produto).filter(
            Produto.empresa_id == empresa_id_consulta,
            Produto.codigo == trib.codigo
        ).first()

        if existente:
            alterado = False

            if existente.produto != trib.produto:
                existente.produto = trib.produto
                alterado = True
            if existente.ncm != ncm:
                existente.ncm = ncm
                alterado = True
            if existente.aliquota != trib.aliquota:
                existente.aliquota = trib.aliquota
                alterado = True
            if existente.categoriaFiscal != trib.categoriaFiscal:
                existente.categoriaFiscal = trib.categoriaFiscal
                alterado = True

            if alterado:
                atualizados += 1
        else:
            novo = Produto(
                empresa_id=empresa_id_consulta,
                codigo=trib.codigo,
                produto=trib.produto,
                ncm=ncm,
                aliquota=trib.aliquota,
                categoriaFiscal=trib.categoriaFiscal
            )
            db_consulta.add(novo)
            novos += 1

    db_consulta.commit()

    print(f"✅ Sincronização finalizada para {cnpj} — Inseridos: {novos} | Atualizados: {atualizados}")

    return {
        "message": "Sincronização concluída com sucesso.",
        "empresa_id": empresa_id_consulta,
        "produtos_inseridos": novos,
        "produtos_atualizados": atualizados
    }
