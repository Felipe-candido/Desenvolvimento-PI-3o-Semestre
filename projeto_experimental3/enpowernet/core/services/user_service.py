def construir_nome_exibicao(nome_usuario):
    nome = nome_usuario.split(' ')
    
    if len(nome) == 1:
        return nome[0]

    nome_exibicao = nome[0] + ' ' + nome[-1] 

    return nome_exibicao

def construir_numero_telefone(numero_usuario):
    numero_usuario = ''.join(filter(str.isdigit, numero_usuario))
    
    if len(numero_usuario) not in (10, 11):
        raise ValueError("Número de telefone deve ter 10 ou 11 dígitos.")

    ddd = numero_usuario[:2] 
    numero_principal = numero_usuario[2:] 
    
    if len(numero_principal) == 8:
        return f"({ddd}) {numero_principal[:4]}-{numero_principal[4:]}"  
    elif len(numero_principal) == 9:
        return f"({ddd}) {numero_principal[:5]}-{numero_principal[5:]}"  
