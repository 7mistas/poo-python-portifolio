from decimal import Decimal
from bank import Conta
from acount_cc import Conta_corrente
from acount_cp import Conta_poupanca

def menu() -> int:
    print(f"=" * 20, "[Conta Bancária]", "=" * 20)
    print(f"=" * 50)
    print("1 - Conta Corrente")
    print("2 - Conta Poupança")
    print("0 - Sair")
    print("=" * 50)
    return int(input("Escolha uma opção: "))

def menu_transacao() -> int:
    print(f"=" * 20, "Escolha a transação", "=" * 20)
    print(f"1 - Deposito")
    print("2 - Saque")
    print("0 - Voltar")
    print(f"=" * 50)
    return int(input("Digite a operação: "))

def main() -> None:
    conta_cc = Conta_corrente()
    conta_cp = Conta_poupanca()

    while True:
        try:
            opcao = menu()
            conta_ativa = None
            nome_conta = ""

            if opcao == 1:
                nome_conta = f"=" * 20, "Conta Corrente", "=" * 20
                conta_ativa = conta_cc

            elif opcao == 2:
                nome_conta = f"=" * 20, "Conta Poupança", "=" * 20
                conta_ativa = conta_cp
            
            elif opcao == 0:
                print(f"=" * 20, "Saindo da Conta...", "=" *20)
                break

            else:
                print("[ERRO!] Opção inválida!")
                continue

            while True:
                sub_opcao = menu_transacao()
                try:
                    if sub_opcao == 1:
                        while True:
                            valor_str = input("Digite seu valor: ").replace(',', '.').strip()
                            if not valor_str:
                                continue
                            try:
                                valor = Decimal(valor_str)
                                conta_ativa.depositar(valor)
                                print(f"O saldo da conta é R$ {conta_ativa.saldo_atual:.2f}.")
                                break
                            except Exception:
                                print("[ERRO!] Digite somente números válidos!")
                                continue

                    elif sub_opcao == 2:
                        while True:
                            valor_str = input("Digite seu valor: ").replace(',', '.').strip()
                            if not valor_str:
                                continue
                            try:
                                valor = Decimal(valor_str)
                                conta_ativa.sacar(valor)
                                print(f"O saldo da conta é R$ {conta_ativa.saldo_atual:.2f}.")
                                break
                            except Exception:
                                print("[ERRO!] Digite somente números válidos!")
                                continue

                    elif sub_opcao == 0:
                        break

                    else:
                        print("[ERRO! Opção inválida!")

                except ValueError:
                    print("[ERRO!] Digite somente números!")
                
            
        except ValueError:
            print("[ERRO!] Digite somente números!")
            
if __name__ == "__main__":
    main()
