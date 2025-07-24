import os
import bcrypt
import aiohttp
import traceback
from src.Config import theme
from dotenv import load_dotenv
from sqlalchemy import text
from src.Config.database.dbConsultaProdutos import SessionLocalConsulta

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
    try:
        with SessionLocalConsulta() as session:
            result = session.execute(text("""
                SELECT id, usuario, senha, razaoSocial, cnpj, empresa_id
                FROM usuarios
                WHERE usuario = :usuario AND ativo = TRUE
            """), {"usuario": usuario}).mappings().first()

            if not result:
                print(f"❌ Usuário '{usuario}' não encontrado ou inativo")
                return None

            senha_hash_banco = result["senha"]

            if not senha_hash_banco:
                print("⚠️ Hash da senha está vazio ou None")
                return None

            if isinstance(senha_hash_banco, str):
                senha_hash_banco = senha_hash_banco.encode()

            if bcrypt.checkpw(senha.encode(), senha_hash_banco):
                print(f"✅ Login válido para: {usuario}")
                return {
                    "id": result["id"],
                    "usuario": result["usuario"],
                    "nome": result.get("razaoSocial", "Usuário"),
                    "empresa_id": result["empresa_id"],
                    "cnpj": result.get("cnpj")
                }
            else:
                print("❌ Senha incorreta para: {usuario}")
                return None

    except Exception as e:
        print(f"[ERRO] ao autenticar usuário: {e}")
        traceback.print_exc()
        return None