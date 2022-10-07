from passlib.context import CryptContext

#criando contexto
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')
#se for deprecated, faça o tratamento automático

#hash é a impressão digital da senha
def checar_senha(senha: str, hash_senha: str) -> bool:
    
    """
    Função para verificar se a senha está correta, 
    comparando a senha em texto puro, informada pelo
    usuário, e o hash da senha que está salvo no bd
    durante a criação da conta.
    """
    
    return CRIPTO.verify(senha, hash_senha)


#gerador de hash
def gerar_hash_senha(senha: str) -> str:

    """
    Função que gera e retorna o hash da senha
    """
    return CRIPTO.hash(senha)
