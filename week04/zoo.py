""" Modulo que importa as classes vindo de animals.py"""
from animals import Animal, Cachorro, Gato, Passaro

"""
Classe com lista e metódo para listar os animais do Zoo 
"""
class Zoologico:
    def __init__(self) -> None:
        self.zoo = []

    """ Função para imprimir a lista de animais """
    def mostrar_animais(self) -> str:
        if not self.zoo:
            print("A lista está vazia!")
            return

        for i, animal in enumerate(self.zoo):
            print(f"[{i+1}]")
            meu_zoo = animal.falar()
            print(meu_zoo)
