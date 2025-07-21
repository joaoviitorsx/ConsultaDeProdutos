import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Controllers.consultaFornecedorController import router as fornecedor_router
from src.Controllers.consultaProdutosController import router as produtos_router
from src.Controllers.loginController import router as login_router
from src.Controllers.consultaRelatorioController import router as relatorio_router

app = FastAPI(
    title="API Sistema de Consultas",
    description="API para o software de consulta de produtos",
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

@app.get("/")
async def root():
    return {
        "message": "API Sistema de Consultas funcionando!", 
        "version": "1.0.0",
        "docs": "Acesse /docs para ver a documentação da API",
        "endpoints": {
            "login": "/api/auth/login",
            "me": "/api/auth/me",
            "logout": "/api/auth/logout",
            "consulta_fornecedor": "/api/consulta-fornecedor/{cnpj}",
            "consulta_produto": "/api/produto?codigo_produto=...",
            "calcular": "/api/calcular"
        }
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
    uvicorn.run(app, host="0.0.0.0", port=8000)