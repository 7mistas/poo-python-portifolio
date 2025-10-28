class Animal:
    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome
        self.idade = idade

    def falar(self) -> str:
        return "O {self.nome} está falando"

class Cachorro(Animal):
    def __init__(self, nome: str, idade: int) -> None:
        super().__init__(nome, idade)

    def falar(self) -> str:
        return "O {self.nome} latiu!"

class Gato(Animal):
    def __init__(self, nome: str, idade: int) -> None:
        super().__init__(nome, idade)
    
    def falar(self) -> str:
        return "O {self.nome} miou!"

class Pasaro(Animal):
    def __init__(self, nome: str, idade: int ) -> None:
        super().__init__(nome, idade)
        
    def falar(self) -> str:
        return "O {self.nome} piou!"

def main():
    cachorro_latiu = Cachorro.falar
    print(cachorro_latiu)

    gato_miou = Gato.falar
    print(gato_miou)

    passaro_piou = Passaro.falar
    print(passaro_piou)

def __name__ == "__main__":
    main()
