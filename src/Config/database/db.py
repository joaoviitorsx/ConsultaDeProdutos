import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from src.Utils.path import resourcePath

def env():
    #raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    #env_path = os.path.join(raiz, '.env')
    env_path = resourcePath(".env")
    load_dotenv(dotenv_path=env_path, override=True)
    return {
        'host': os.getenv('HOST'),
        'usuario': os.getenv('USUARIO'),
        'senha': os.getenv('SENHA'),
        'banco': os.getenv('BANCO'),
        'port': os.getenv('PORT', '3306')
    }

def conectarBanco():
    try:
        config = env()
        conexao = mysql.connector.connect(
            host=config['host'],
            user=config['usuario'],
            password=config['senha'],
            database=config['banco'],
            port=int(config['port']),
            charset='utf8mb4',
            use_unicode=True,
            autocommit=False,
            connection_timeout=30,
            sql_mode='STRICT_TRANS_TABLES'
        )
        if conexao.is_connected():
            print(f"[SUCESSO] Conexão com o banco {config['banco']}")
            return conexao
    except Error as e:
        print(f"[ERRO] ao conectar ao banco: {e}")
    return None

def fecharBanco(conexao):
    if conexao and conexao.is_connected():
        conexao.close()

def sqlalchemy_url():
    config = env()
    return f"mysql+pymysql://{config['usuario']}:{config['senha']}@{config['host']}:{config['port']}/{config['banco']}"