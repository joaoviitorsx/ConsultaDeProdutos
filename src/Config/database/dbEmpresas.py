import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.Utils.path import resourcePath

#load_dotenv()
load_dotenv(dotenv_path=resourcePath(".env"), override=True)

DATABASE_URL_EMPRESAS = (
    f"mysql+pymysql://{os.getenv('USER_EMPRESAS')}:{os.getenv('PASSWORD_EMPRESAS')}@"
    f"{os.getenv('HOST_EMPRESAS')}:{os.getenv('PORT_EMPRESAS')}/{os.getenv('NAME_EMPRESAS')}"
)

engine_empresas = create_engine(
    DATABASE_URL_EMPRESAS,
    pool_pre_ping=True,
    pool_recycle=280,
    connect_args={"charset": "utf8mb4"}
)

SessionLocalEmpresas = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_empresas
)

BaseEmpresas = declarative_base()
