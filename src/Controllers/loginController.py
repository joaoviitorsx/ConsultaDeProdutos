
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.Services.loginService import autenticar
from src.Components.notificacao import notificacao
from fastapi import APIRouter, HTTPException, Depends
from src.Services.loginService import verificarCredenciais
from src.Models.loginModel import LoginRequest, LoginResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_KEY", "jwt_token")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 8))

async def realizarLogin(page, usuario, senha):
        status, data = await autenticar(usuario, senha)
        if status == 200:
            notificacao(page, "Login realizado", f"Bem-vindo, {data['data']['nome']}!", "sucesso")
            page.go("/dashboard")
        elif status == 401:
            notificacao(page, "Login inválido", "Usuário ou senha incorretos.", "erro")
        elif status == 400:
            notificacao(page, "Dados inválidos", "Verifique os dados informados.", "erro")
        elif status is None:
            notificacao(page, "Erro de rede", data.get("error", "Erro desconhecido"), "erro")
        else:
            notificacao(page, "Erro inesperado", str(data), "erro")

        page.update()
        return data 

def criarAcessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ Token JWT criado com sucesso (expira em {ACCESS_TOKEN_EXPIRE_MINUTES} minutos)")
        return encoded_jwt
    except Exception as e:
        print(f"❌ Erro ao criar token JWT: {e}")
        raise HTTPException(status_code=500, detail="Erro ao gerar token")

def verificarToken(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        
        if usuario is None:
            print("❌ Token sem usuário válido")
            raise HTTPException(status_code=401, detail="Token inválido")
        
        print(f"✅ Token válido para usuário: {usuario}")
        return payload
        
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        print("❌ Token inválido")
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/login", response_model=LoginResponse)
async def realizaLogin(request: LoginRequest):
    try:
        print(f"🔑 Tentativa de login para: {request.usuario}")
        
        if not request.usuario or not request.senha:
            print("❌ Campos obrigatórios não preenchidos")
            raise HTTPException(
                status_code=400,
                detail="Usuário e senha são obrigatórios"
            )

        dados_usuario = verificarCredenciais(request.usuario, request.senha)
        
        if not dados_usuario:
            print(f"❌ Login falhou para: {request.usuario}")
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos"
            )

        token_data = {
            "sub": dados_usuario["usuario"],
            "user_id": dados_usuario["id"],
            "empresa_id": dados_usuario["empresa_id"],
            "nome": dados_usuario["nome"]
        }
        
        access_token = criarAcessToken(token_data)
        
        print(f"✅ Login bem-sucedido para: {request.usuario}")

        return LoginResponse(
            success=True,
            message="Login realizado com sucesso",
            data={
                "id": dados_usuario["id"],
                "usuario": dados_usuario["usuario"],
                "nome": dados_usuario["nome"],
                "empresa_id": dados_usuario["empresa_id"]
            },
            token=access_token
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [ERRO] Login Controller: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor"
        )

@router.get("/me")
async def obterUsuario(current_user: dict = Depends(verificarToken)):
    try:
        print(f"📋 Solicitação de dados do usuário: {current_user.get('sub')}")
        
        return {
            "success": True,
            "data": {
                "usuario": current_user.get("sub"),
                "user_id": current_user.get("user_id"),
                "empresa_id": current_user.get("empresa_id"),
                "nome": current_user.get("nome")
            }
        }
    except Exception as e:
        print(f"❌ Erro ao obter usuário atual: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/logout")
async def logout():
    print("🚪 Logout realizado")
    return {
        "success": True,
        "message": "Logout realizado com sucesso"
    }

@router.post("/refresh")
async def carregarToken(current_user: dict = Depends(verificarToken)):
    try:
        print(f"🔄 Renovando token para: {current_user.get('sub')}")
        
        new_token_data = {
            "sub": current_user.get("sub"),
            "user_id": current_user.get("user_id"),
            "empresa_id": current_user.get("empresa_id"),
            "nome": current_user.get("nome")
        }
        
        new_token = criarAcessToken(new_token_data)
        
        return {
            "success": True,
            "message": "Token renovado com sucesso",
            "token": new_token
        }
        
    except Exception as e:
        print(f"❌ Erro ao renovar token: {e}")
        raise HTTPException(status_code=500, detail="Erro ao renovar token")

@router.post("/validate")
async def validarToken(current_user: dict = Depends(verificarToken)):
    return {
        "success": True,
        "message": "Token válido",
        "data": {
            "usuario": current_user.get("sub"),
            "expira_em": current_user.get("exp")
        }
    }