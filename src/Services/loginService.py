import os
import bcrypt
import aiohttp
from src.Config import theme
from src.Config.database.db import conectarBanco, fecharBanco
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")

async def autenticar(usuario: str, senha: str) -> tuple[int | None, dict]:
    timeout = aiohttp.ClientTimeout(total=30)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            payload = {"usuario": usuario, "senha": senha}
            async with session.post(API_URL, json=payload, ssl=False) as resp:
                data = await resp.json()
                return resp.status, data
    except Exception as e:
        return None, {"error": str(e)}
    
def verificarCredenciais(usuario: str, senha: str) -> dict | None:
    print(f"Verificando credenciais para: {usuario}")
    
    conexao = conectarBanco()
    
    if not conexao:
        print("Falha na conexão com o banco")
        return None

    try:
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT id, usuario, senha, razaoSocial, empresa_id FROM usuarios WHERE usuario = %s AND ativo = TRUE"
        cursor.execute(query, (usuario,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Usuário encontrado: {usuario}")
            print(f"Dados: ID={resultado['id']}, Razão Social={resultado.get('razaoSocial', 'N/A')}")
            
            senha_hash_banco = resultado["senha"]
            
            if bcrypt.checkpw(senha.encode(), senha_hash_banco.encode()):
                dados_usuario = {
                    "id": resultado["id"],
                    "usuario": resultado["usuario"],
                    "nome": resultado.get("razaoSocial", "Usuário"), 
                    "empresa_id": resultado["empresa_id"]
                }
                print(f"Login válido para: {usuario}")
                return dados_usuario
            else:
                print(f"Senha incorreta para: {usuario}")
                return None
        else:
            print(f"Usuário '{usuario}' não encontrado ou inativo")
            return None

    except Exception as e:
        print(f"[ERRO] ao autenticar usuário: {e}")
        return None
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            fecharBanco(conexao)