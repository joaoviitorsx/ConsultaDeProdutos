import re

def removedorCaracteres(valor: str) -> str:
    return re.sub(r'\D', '', valor)

def validarCnpj(cnpj: str) -> bool:
    cnpj = removedorCaracteres(cnpj)
    return len(cnpj) == 14 and cnpj.isdigit()
