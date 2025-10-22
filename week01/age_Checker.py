def pode_dirigir(idade: int) -> int:
    """ 
    Função para verificação da idade do usuário.
    
    Args:
        (idade: int): Recebe o valor inteiro da idade.
    Returns:
        int: Comparação do valor da idade em relação a minima permitida.
    """
    IDADE_MINIMA = 18
    return idade >= IDADE_MINIMA

#  Tentativa da entrada da idade e tratamento de erro.
try:
    # Entrada da idade por input no CLI.
    sua_idade = int(input("Digite sua idade: "))
    # Compara o valor de idade com a meta mínima.
    if pode_dirigir(sua_idade):
        print("Voce pode dirigir!")
    else:
        print("Você não pode dirigir! ")
except ValueError:
    print("Erro: Somente numeros são válidos!")
