import random
import string

def gerar_senha(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(random.choices(caracteres, k=tamanho))
    return senha

if __name__ == "__main__":
    print("Senha gerada:", gerar_senha())