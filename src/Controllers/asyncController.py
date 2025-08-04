import traceback
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from src.Config.database.dbEmpresas import SessionLocalEmpresas
from src.Config.database.dbConsultaProdutos import SessionLocalConsulta
from src.Services.asyncProdutosService import sincroanizarProdutos
from src.Controllers.loginController import verificarToken

router = APIRouter()

def getDbEmpresas():
    db = SessionLocalEmpresas()
    try:
        yield db
    finally:
        db.close()

def getDbConsulta():
    db = SessionLocalConsulta()
    try:
        yield db
    finally:
        db.close()

@router.post("/sincronizar-produtos")
def sincronizarProdutosRoute(
    dados: dict = Body(...),
    db_empresas: Session = Depends(getDbEmpresas),
    db_consulta: Session = Depends(getDbConsulta),
    current_user: dict = Depends(verificarToken)
):
    try:
        cnpj = current_user.get("cnpj")
        if not cnpj:
            raise HTTPException(status_code=400, detail="CNPJ não encontrado no token")

        offset = dados.get("offset", 0)
        limite = dados.get("limite", 1000)
        
        resultado = sincroanizarProdutos(
            cnpj, 
            db_empresas, 
            db_consulta, 
            offset=offset, 
            limite=limite
        )
        
        from src.Models.apuradorModel import Empresa, CadastroTributacao
        empresa = db_empresas.query(Empresa).filter(Empresa.cnpj == cnpj).first()
        total_produtos = db_empresas.query(CadastroTributacao).filter(
            CadastroTributacao.empresa_id == empresa.id
        ).count() if empresa else 0
        
        concluido = (offset + limite) >= total_produtos or resultado.get("produtos_inseridos", 0) == 0
        
        return {
            **resultado,
            "concluido": concluido,
            "total_produtos": total_produtos
        }

    except Exception as e:
        print(f"❌ Erro ao sincronizar produtos: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500, 
            content={"erro": f"Erro interno ao sincronizar produtos: {str(e)}"}
        )

@router.get("/verificar-sincronizacao")
def verificarSincronizacao(cnpj: str, db_empresas: Session = Depends(getDbEmpresas), db_consulta: Session = Depends(getDbConsulta)):
    from src.Models.apuradorModel import Empresa, CadastroTributacao
    from src.Models.consultaProdutosModel import Produto, Usuario

    try:
        empresa = db_empresas.query(Empresa).filter(Empresa.cnpj == cnpj).first()
        if not empresa:
            return {"necessita_sincronizar": False, "motivo": "Empresa não encontrada no banco origem."}

        usuario = db_consulta.query(Usuario).filter(Usuario.cnpj == cnpj).first()
        if not usuario:
            return {"necessita_sincronizar": False, "motivo": "Usuário com CNPJ não encontrado no destino."}

        total_origem = db_empresas.query(CadastroTributacao).filter(CadastroTributacao.empresa_id == empresa.id).count()
        total_destino = db_consulta.query(Produto).filter(Produto.empresa_id == usuario.empresa_id).count()

        if total_origem != total_destino:
            return {
                "necessita_sincronizar": True,
                "total_produtos": total_origem, 
                "produtos_origem": total_origem,
                "produtos_destino": total_destino
            }
        
        return {"necessita_sincronizar": False, "total_produtos": total_origem}
    
    except Exception as e:
        print(f"❌ Erro ao verificar sincronização: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro interno ao verificar necessidade de sincronização"}
        )
