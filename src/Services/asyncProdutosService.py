from sqlalchemy.orm import Session
from src.Models.consultaProdutosModel import Produto, Usuario
from src.Models.apuradorModel import CadastroTributacao, Empresa

def sincroanizarProdutos(cnpj: str, db_empresas: Session, db_consulta: Session, offset=0, limite=1000):
    """
    Sincroniza produtos do banco empresas_db para o banco consultaprodutos em lotes.
    
    args:
        cnpj: CNPJ da empresa
        db_empresas: Sessão do banco de dados de origem
        db_consulta: Sessão do banco de dados de destino
        offset: Posição inicial para busca (paginação)
        limite: Quantidade máxima de registros por lote
    
    return:
        Dict com estatísticas da sincronização
    """
    print(f"🔄 Iniciando sincronização para CNPJ: {cnpj} - Offset: {offset}, Limite: {limite}")

    empresa = db_empresas.query(Empresa).filter(Empresa.cnpj == cnpj).first()
    if not empresa:
        return {
            "message": f"Empresa com CNPJ {cnpj} não encontrada no banco de origem (empresas_db).",
            "produtos_inseridos": 0,
            "produtos_atualizados": 0,
            "lote_atual": offset // limite + 1 if limite > 0 else 1
        }

    usuario = db_consulta.query(Usuario).filter(Usuario.cnpj == cnpj).first()
    if not usuario or not usuario.empresa_id:
        return {
            "message": f"Usuário com CNPJ {cnpj} não encontrado no banco de destino (consultaprodutos).",
            "produtos_inseridos": 0,
            "produtos_atualizados": 0,
            "lote_atual": offset // limite + 1 if limite > 0 else 1
        }

    empresa_id_consulta = usuario.empresa_id
    
    tributacoes = db_empresas.query(CadastroTributacao).filter(
        CadastroTributacao.empresa_id == empresa.id
    ).offset(offset).limit(limite).all()
    
    total_registros = db_empresas.query(CadastroTributacao).filter(
        CadastroTributacao.empresa_id == empresa.id
    ).count()

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

    lote_atual = offset // limite + 1 if limite > 0 else 1
    total_lotes = (total_registros + limite - 1) // limite if limite > 0 else 1
    progresso = min(100, int((offset + len(tributacoes)) / total_registros * 100)) if total_registros > 0 else 100
    
    concluido = (offset + limite >= total_registros) or len(tributacoes) < limite

    print(f"✅ Sincronização do lote {lote_atual}/{total_lotes} ({progresso}%) para {cnpj} — Inseridos: {novos} | Atualizados: {atualizados}")

    return {
        "message": "Sincronização do lote concluída com sucesso.",
        "empresa_id": empresa_id_consulta,
        "produtos_inseridos": novos,
        "produtos_atualizados": atualizados,
        "lote_atual": lote_atual,
        "total_lotes": total_lotes,
        "progresso": progresso,
        "concluido": concluido,
        "total_registros": total_registros
    }