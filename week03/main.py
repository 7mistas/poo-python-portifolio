"""
Importa class Carro e seus atributos do arquivo car.py

Importa class Frota e seus atributos do arquivo fleet.py
"""
from car import Carro
from fleet import Frota

def menu() -> int:
    """Inicializa o menu para seleção das opções"""
    print("\n" + "=" * 50)
    print("SISTEMA DE GERENCIMENTO DE FROTA DOS VEICULOS")
    print("\n" + "=" * 50)
    print("1 - Adicionar carro")
    print("2 - Informações do carro")
    print("3 - Remover carro")
    print("4 - Listar veiculos da frota")
    print("5 - Ligar carro")
    print("6 - Desligar carro")
    print("7 - Total de carros")
    print("0 - Sair")
    print("\n" + "=" * 50)
    return int(input("Escolha uma opção: "))

def main() -> None:
    """Inicializa toda a lógica pra execução das opções de seleção"""
    frota = Frota()

    while True:
        opcao = menu()
        try:
            if opcao == 1:
                print("==== ADICIONAR CARRO ====")
                modelo = input("Modelo: ")
                cor = input("Cor: ")
                try:
                    ano = int(input("Ano: "))
                    novo_carro = Carro(modelo, cor, ano)
                    frota.adicionar_Carro(novo_carro)
                except ValueError:
                    print("[ERRO!] Ano inválido.")

            elif opcao == 2:
                print("==== INFORMAÇÕES DO CARRO ====")
                modelo = input("Digite o modelo do carro: ")
                encontrado = False
                for carro in frota.veiculos:
                    if carro.modelo == modelo:
                        meu_carro = carro.info()
                        print(meu_carro)
                        encontrado = True
                        break
                if not encontrado:
                    print(f"[ERRO!] Carro {modelo} não foi encontrado!")

            elif opcao == 3:
                print("==== REMOVER O CARRO DA FROTA ====")
                modelo = input("Digite o modelo: ")
                frota.remover_Carro(modelo)

            elif opcao == 4:
                print("==== LISTAR OS CARROS DA FROTA ====")
                minha_frota = frota.listar_Frota()
                print(minha_frota)
                
            elif opcao == 5:
                print("===== LIGAR CARRO ====")
                modelo = input("Digite o modelo: ")
                encontrado = False
                for carro in frota.veiculos:
                    if carro.modelo == modelo:
                        carro.ligar()
                        print(f"O carro está {'Ligado' if carro.status else 'Desligado'}!")
                        encontrado = True
                        break
                if not encontrado:
                    print(f"[ERRO!]O carro {modelo} não foi encontrado!")

            elif opcao == 6:
                print("==== DESLIGAR CARRO ====")
                modelo = input("Digite o modelo: ")
                encontrado = False
                for carro in frota.veiculos:
                    if carro.modelo == modelo:
                        carro.desligar()
                        print(f"Carro está {'Ligado' if carro.status else 'Desligado'}!")
                        encontrado = True
                        break
                if not encontrado: 
                    print(f"O carro {modelo} não foi encontrado!")
            
            elif opcao == 7:
                print("==== Total Carros ====")
                frota.total_Carros()

            elif opcao == 0:
                print("<<< Saindo! >>>")
                break

        except ValueError:
            print("[ERRO!] Opção invalida!")

if __name__ == "__main__":
        main()
