# Função para verificar a idade.
def pode_dirigir(idade):

    # Idade mínima para dirigir.
    IDADE_MINIMA = 18

    # Retorno do valor em 
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