from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Controllers.consultaFornecedorController import router as fornecedor_router
from src.Controllers.loginController import router as login_router  # ADICIONADO

app = FastAPI(
    title="API Sistema de Consultas",  # ATUALIZADO
    description="API para consulta de fornecedores e sistema de login",  # ATUALIZADO
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUIR ROTAS
app.include_router(login_router, prefix="/api/auth", tags=["autenticação"])  # ADICIONADO
app.include_router(fornecedor_router, prefix="/api", tags=["fornecedores"])

@app.get("/")
async def root():
    return {
        "message": "API Sistema de Consultas funcionando!",  # ATUALIZADO
        "version": "1.0.0",
        "docs": "Acesse /docs para ver a documentação da API",
        "endpoints": {
            "login": "/api/auth/login",  # ADICIONADO
            "me": "/api/auth/me",  # ADICIONADO
            "logout": "/api/auth/logout",  # ADICIONADO
            "consulta_fornecedor": "/api/consulta-fornecedor/{cnpj}"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API funcionando corretamente"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API...")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🌐 Health Check: http://localhost:8000/health")
    print("🔐 Login: http://localhost:8000/api/auth/login")
    print("👤 Me: http://localhost:8000/api/auth/me")  
    uvicorn.run(app, host="0.0.0.0", port=8000)