import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.Utils.path import resourcePath

#load_dotenv()
load_dotenv(dotenv_path=resourcePath(".env"), override=True)

DATABASE_URL_CONSULTA = (
    f"mysql+pymysql://{os.getenv('USUARIO')}:{os.getenv('SENHA')}@"
    f"{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('BANCO')}"
)

engine_consulta = create_engine(
    DATABASE_URL_CONSULTA,
    pool_pre_ping=True,
    pool_recycle=280,
    connect_args={"charset": "utf8mb4"}
)

SessionLocalConsulta = sessionmaker(autocommit=False, autoflush=False, bind=engine_consulta)
BaseConsulta = declarative_base()
