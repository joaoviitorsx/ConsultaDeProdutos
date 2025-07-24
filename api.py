import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Controllers.consultaFornecedorController import router as fornecedor_router
from src.Controllers.consultaProdutosController import router as produtos_router
from src.Controllers.loginController import router as login_router
from src.Controllers.consultaRelatorioController import router as relatorio_router
from src.Controllers.asyncController import router as async_router

app = FastAPI(
    title="API Assertivus Contabil",
    description="API para os softwares de gestão contábil e fiscal da Assertivus Contabil",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router, prefix="/api/auth", tags=["autenticação"])
app.include_router(fornecedor_router, prefix="/api", tags=["fornecedores"])
app.include_router(produtos_router, prefix="/api", tags=["produtos"])
app.include_router(relatorio_router, prefix="/api", tags=["relatorios"])
app.include_router(async_router, prefix="/api", tags=["sincronizacao"])

@app.get("/")
async def root():
    return {
        "message": "API Sistema de Consultas funcionando!", 
        "version": "1.0.0",
        "docs": "Acesse /docs para ver a documentação da API",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API funcionando corretamente"}

if __name__ == "__main__":
    print("🚀 Iniciando API")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🌐 Health Check: http://localhost:8000/health")
    print("🔐 Login: http://localhost:8000/api/auth/login")
    print("👤 Me: http://localhost:8000/api/auth/me")
    print("🔄 Verificar sincronização: http://localhost:8000/api/verificar-sincronizacao?cnpj=SEUCNPJ")
    print("🛠️  Executar sincronização: http://localhost:8000/api/sincronizar-produtos")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
