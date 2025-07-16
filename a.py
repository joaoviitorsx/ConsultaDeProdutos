import bcrypt

senha = "123"
senha = senha.encode('utf-8')
salt = bcrypt.gensalt()
hashSenha = bcrypt.hashpw(senha, salt)

print("Hash gerado para inserir no banco:")
print(hashSenha.decode())