import os
import bcrypt
import mysql.connector
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

HOST = os.getenv("HOST")
USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")
BANCO = os.getenv("BANCO")
PORT = int(os.getenv("PORT", 3306))

def conectar():
    return mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=BANCO,
        port=PORT
    )

def criar_usuario(usuario, senha, razaoSocial, empresa_id, ativo, cnpj):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode()
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, senha, razaoSocial, empresa_id, ativo, cnpj)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (usuario, senha_hash, razaoSocial, empresa_id, ativo, cnpj))
        conn.commit()
        print(f"Usuário {usuario} criado com sucesso!")
    except mysql.connector.IntegrityError:
        print(f"Usuário {usuario} já existe.")
    finally:
        cursor.close()
        conn.close()

def alterar_senha(usuario_id, nova_senha):
    senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (senha_hash, usuario_id))
    conn.commit()
    if cursor.rowcount:
        print(f"Senha do usuário {usuario_id} alterada com sucesso!")
    else:
        print(f"Usuário com id {usuario_id} não encontrado.")
    cursor.close()
    conn.close()

# Exemplo de uso:
criar_usuario('arissonrafael', 'Dbh7cB', 'Arisson Rafael Avila de Paula', 2, 1, '')
criar_usuario('rodrigocalderan', 'ylZAre', 'Rodrigo Calderan', 2, 1, '')
criar_usuario('iagosantos', 'T68xM3', 'Iago Santos', 2, 1, '')
# Para alterar senha de um usuário existente:
# alterar_senha(3, 'novaSenhaParaID3')