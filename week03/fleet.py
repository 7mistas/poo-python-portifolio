"""Importa car.py e a sua class Carro com seus atributos"""
from car import Carro

class Frota:
    """Classe para inicializar uma lista com objetos da class Carro"""
    def __init__(self) -> None:
        """Instancia a lista de carros"""
        self.veiculos = []

    def adicionar_Carro(self, carro: Carro) -> None:
        """Funçao para ADICIONAR um objeto Carro a lista"""
        self.veiculos.append(carro)
        print(f"\n[SUCESSO!] {carro.modelo} adicionado a frota!")

    def remover_Carro(self, modelo: str) -> None:
        """Função para REMOVER um objeto Carro da lista"""
        for carro in self.veiculos:
            if carro.modelo == modelo:
                self.veiculos.remove(carro)
                print(f"\nCarro {modelo} removido!")
                
    def listar_Frota(self) -> None:
        """Função para LISTAR os objetos Carro na lista"""
        if not self.veiculos:
            print("\nA Frota está vazia")
            return

        for i, carro in enumerate(self.veiculos):
            print(f"[{i+1}]")
            mostrar_info = carro.info()
            print(mostrar_info)
            print("=" * 50)

    def total_Carros(self) -> None:
        """Função para contabilizar a quantidade de objetos criados"""
        print(f"O total de carros que passaram pela frota é {Carro.total_carros}")
