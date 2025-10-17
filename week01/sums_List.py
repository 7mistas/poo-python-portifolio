# For - Mais simples e automático.
def usando_For (nums):
    total = 0
    for numero in nums:
        total += numero
    return total
# While - Mais complexo e manual.
def usando_While(nums):
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