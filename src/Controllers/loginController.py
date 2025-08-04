import os
import jwt
import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.Services.loginService import autenticar, verificarCredenciais
from src.Components.notificacao import notificacao
from src.Models.loginModel import LoginRequest, LoginResponse
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_KEY", "jwt_token")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 8))

API_URL = os.getenv("API_URL")
BACKEND_URL = os.getenv("BACKEND_URL")

async def sincronizarProdutos(cnpj: str, token: str, page):
    print(f"🔄 Verificando necessidade de sincronização para CNPJ: {cnpj}")
    
    if not cnpj:
        print("ℹ️ Usuário sem CNPJ. Sincronização ignorada.")
        notificacao(page, "Sincronização Ignorada", "Usuário sem CNPJ vinculado.", "info")
        return

    try:
        notificacao(page, "Sincronização de Produtos", "Verificando se há atualizações...", "info")
        page.update()

        verificar_response = await asyncio.to_thread(
            lambda: requests.get(
                f"{BACKEND_URL}/verificar-sincronizacao",
                params={"cnpj": cnpj},
                headers={"Authorization": f"Bearer {token}"}
            )
        )

        if verificar_response.status_code == 200:
            data = verificar_response.json()
            if not data.get("necessita_sincronizar", False):
                print("✔️ Nenhuma atualização necessária. Sincronização ignorada.")
                notificacao(page, "Sincronização Atualizada", "Os produtos já estão sincronizados.", "sucesso")
                return
            
            total_produtos = data.get("total_produtos", 0)
        else:
            print(f"⚠️ Erro ao verificar sincronização: {verificar_response.text}")
            notificacao(page, "Erro", "Falha ao verificar necessidade de sincronização.", "erro")
            return

        notificacao(page, "Sincronização em Andamento", f"Iniciando sincronização de {total_produtos} produtos...", "info")
        page.update()
        
        lote = 1000
        offset = 0
        total_inseridos = 0
        total_atualizados = 0
        max_tentativas = 20
        contador_tentativas = 0
        
        while True:
            contador_tentativas += 1
            if contador_tentativas > max_tentativas:
                print(f"⚠️ Sincronização interrompida após {max_tentativas} tentativas")
                break
                
            progress = min(100, int((offset / total_produtos) * 100)) if total_produtos > 0 else 100
            notificacao(page, "Sincronização em Andamento", f"Processando lote {contador_tentativas}... ({progress}%)", "info")
            page.update()
            
            response = await asyncio.to_thread(
                lambda: requests.post(
                    f"{BACKEND_URL}/sincronizar-produtos",
                    json={"offset": offset, "limite": lote},
                    headers={"Authorization": f"Bearer {token}"}
                )
            )
            
            if response.status_code == 200:
                dados = response.json()
                inseridos = dados.get("produtos_inseridos", 0)
                atualizados = dados.get("produtos_atualizados", 0)
                total_inseridos += inseridos
                total_atualizados += atualizados
                
                if dados.get("concluido", False) or (inseridos == 0 and atualizados == 0):
                    break
                
                if offset >= total_produtos:
                    print("✅ Sincronização concluída por limite de produtos")
                    break
                    
                offset += lote
                
                await asyncio.sleep(0.2)
            else:
                print(f"⚠️ Erro na sincronização: {response.text}")
                notificacao(page, "Erro na Sincronização", f"Falha ao sincronizar lote {contador_tentativas}.", "erro")
                return

        print("🔄 Produtos sincronizados com sucesso")
        print(f"- Inseridos: {total_inseridos}")
        print(f"- Atualizados: {total_atualizados}")

        notificacao(
            page,
            "Sincronização Concluída",
            f"{total_inseridos} produto(s) inserido(s) e {total_atualizados} atualizado(s).",
            "sucesso"
        )

    except Exception as e:
        print(f"⚠️ Exceção ao sincronizar produtos: {e}")
        notificacao(page, "Erro", f"Erro inesperado ao sincronizar produtos: {str(e)}", "erro")

async def realizarLogin(page, usuario, senha):
    try:
        response = requests.post(API_URL, json={
            "usuario": usuario,
            "senha": senha
        })

        if response.status_code == 200:
            result = response.json()
            token = result["token"]
            nome = result["data"]["nome"]

            page.selected_empresa_id = result["data"].get("empresa_id")
            page.session.set("usuario_id", result["data"].get("id"))

            page.usuario_info = {
                "nome": result["data"].get("nome"),
                "empresa_id": result["data"].get("empresa_id"),
                "cnpj": result["data"].get("cnpj")
            }

            notificacao(page, "Login realizado", f"Bem-vindo, {nome}!", "sucesso")

            cnpj = result["data"].get("cnpj")
            await sincronizarProdutos(cnpj, token, page)
            
            page.go("/dashboard")

        elif response.status_code == 401:
            notificacao(page, "Login inválido", "Usuário ou senha incorretos.", "erro")
        elif response.status_code == 400:
            notificacao(page, "Dados inválidos", "Verifique os dados informados.", "erro")
        else:
            notificacao(page, "Erro inesperado", response.text, "erro")

    except Exception as e:
        print(f"[ERRO] ao realizar login: {e}")
        notificacao(page, "Erro de rede", "Falha ao conectar com o servidor. Tente novamente.", "erro")

    page.update()

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

        dadosUsuario = verificarCredenciais(request.usuario, request.senha)

        if not dadosUsuario:
            print(f"❌ Login falhou para: {request.usuario}")
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos"
            )

        tokenData = {
            "sub": dadosUsuario["usuario"],
            "user_id": dadosUsuario["id"],
            "empresa_id": dadosUsuario["empresa_id"],
            "cnpj": dadosUsuario.get("cnpj"),
            "nome": dadosUsuario["nome"]
        }

        acessToken = criarAcessToken(tokenData)

        print(f"✅ Login bem-sucedido para: {request.usuario}")

        return LoginResponse(
            success=True,
            message="Login realizado com sucesso",
            data={
                "id": dadosUsuario["id"],
                "usuario": dadosUsuario["usuario"],
                "nome": dadosUsuario["nome"],
                "empresa_id": dadosUsuario["empresa_id"],
                "cnpj": dadosUsuario.get("cnpj")
            },
            token=acessToken
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
            "nome": current_user.get("nome"),
            "cnpj": current_user.get("cnpj")
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
