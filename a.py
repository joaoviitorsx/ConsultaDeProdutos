import bcrypt

senha = "123"
senha_bytes = senha.encode('utf-8')
salt = bcrypt.gensalt()
hash_senha = bcrypt.hashpw(senha_bytes, salt)

print("Hash gerado para inserir no banco:")
print(hash_senha.decode())