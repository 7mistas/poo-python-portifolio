"""Modulo que importa os arquivos car.py e fleet para o teste"""
from car import Carro
from fleet import Frota

def main() -> None:
    """Inicializa a demo"""
    print("==== INICIANDO DEMONSTRAÇÃO DA FROTA ====")

    print("==== Instanciando os carros... ====!")
    carro_a = Carro("Focus", "Red", 2005)
    carro_b = Carro("Punto", "Branco", 2000)
    carro_c = Carro("Gol", "Cinza", 1985)
    carro_d = Carro("Viper", "Preto", 2015)
    
    print("==== Criando a frota... ====")
    minha_frota = Frota()

    print("==== Adicionando os carros à Frota inicial... ====")
    minha_frota.adicionar_Carro(carro_a)
    minha_frota.adicionar_Carro(carro_b)
    minha_frota.adicionar_Carro(carro_c)
    minha_frota.adicionar_Carro(carro_d)

    print("==== Testando Info Carro...====")
    meu_carro = carro_a.info()
    print(meu_carro)

    print("==== Listando frota inicial... ====")
    minha_frota.listar_Frota()

    print("==== Testando ligar o carro... ====")
    carro_a.ligar()
    print(f"Status do carro {carro_a.modelo} após ligar {carro_a.status}")

    print("==== Removendo o carro... ====")
    minha_frota.remover_Carro("Fusca")
    minha_frota.remover_Carro("Gol")

    print("==== Listando frota final... ====")
    minha_frota.listar_Frota()

    print(f"==== Total de carros da frota demo [{Carro.total_carros}] ====")

if __name__ == "__main__":
    main()

