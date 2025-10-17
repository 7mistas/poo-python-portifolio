# Função para verificar a idade.
def pode_dirigir(idade):

    # Idade mínima para dirigir.
    IDADE_MINIMA = 18

    # Compara o valor de idade com a meta mínima.
    if idade >= IDADE_MINIMA:
        print("Voce pode dirigir")
    else:
        print("Você não pode dirigir! ")
# Entrada da idade do usuário.
sua_idade = int(input("Digite sua idade: "))
# Executa a função.
pode_dirigir(sua_idade)