"""Demonstração de POO com herança e polimorfismo simples"""
class Animal:
    """
    Classe com atributos de nome e idade do Animal.

    """
    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome
        self.idade = idade

    """ Função que imprime a fala do Animal"""
    def falar(self) -> str:
        return f"O {self.nome} está falando"
"""
Classe Filha para definir Cachorro
"""
class Cachorro(Animal):
    def __init__(self, nome: str, idade: int) -> None:
        super().__init__(nome, idade)
    """Função """
    def falar(self) -> str:
        return f"O {self.nome} latiu!"
"""
Classe Filha para definir Gato
"""
class Gato(Animal):
    def __init__(self, nome: str, idade: int) -> None:
    """ Função para sobrescrever método da Classe Mãe"""    
    def falar(self) -> str:
        return f"O {self.nome} miou!"
"""
Classe Filha para definir Passaro
"""
class Passaro(Animal):
    def __init__(self, nome: str, idade: int ) -> None:
        super().__init__(nome, idade)
    """ Função para sobrescrever o método da Classe Mãe"""    
    def falar(self) -> str:
        return f"O {self.nome} piou!"

""" Instância para teste"""
def main():
    meu_cachorro = Cachorro("Buddy", 3)
    print(meu_cachorro.falar())

    meu_gato = Gato("Leon", 2)
    print(meu_gato.falar())

    meu_passaro = Passaro("Pablo", 4)
    print(meu_passaro.falar())

if __name__ == "__main__":
    main()
