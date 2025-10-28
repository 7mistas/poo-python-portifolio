"""Demonstração de POO com herança e polimorfismo simples"""
class Animal:
    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome
        self.idade = idade

    def falar(self) -> str:
        return f"O {self.nome} está falando"

class Cachorro(Animal):
    def __init__(self, nome: str, idade: int) -> None:
        super().__init__(nome, idade)

    def falar(self) -> str:
        return f"O {self.nome} latiu!"

class Gato(Animal):
    def __init__(self, nome: str, idade: int) -> None:
        super().__init__(nome, idade)
    
    def falar(self) -> str:
        return f"O {self.nome} miou!"

class Passaro(Animal):
    def __init__(self, nome: str, idade: int ) -> None:
        super().__init__(nome, idade)
        
    def falar(self) -> str:
        return f"O {self.nome} piou!"

def main():
    meu_cachorro = Cachorro("Buddy", 3)
    print(meu_cachorro.falar())

    meu_gato = Gato("Leon", 2)
    print(meu_gato.falar())

    meu_passaro = Passaro("Pablo", 4)
    print(meu_passaro.falar())

if __name__ == "__main__":
    main()
