from pydantic import BaseModel

class LoginRequest(BaseModel):
    usuario: str
    senha: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    data: dict = None
    token: str = None