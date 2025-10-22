def usando_For (nums: int) -> int:
    """ 
    Função com For - Mais simples e automático.

    Args:
        (nums: int): Recebe numeros inteiros de uma lista.

    Returns:
        Retorna a soma de todos os numeros da lista "FOR".
    """
    total = 0
    for numero in nums:
        total += numero
    return total

def usando_While(nums: int) -> int:
    """
    Função com While - Mais complexo e manual.

    Args:
        (nums: int): Recebe numeros inteiros de uma lista.

    Returns: 
        Retorna a soma de todos os numeros da lista.
    """
    total = 0
    indice = 0
    while indice < len(nums):
        total += nums[indice]
        indice += 1
    return total

# Resultado.
print(usando_For([1, 2, 6, 8, 7]))
print("=" * 50)
print(usando_While([9, 89, 78, 57]))
