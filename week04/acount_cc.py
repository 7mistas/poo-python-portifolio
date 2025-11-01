from decimal import Decimal
from bank import Conta

class Conta_corrente(Conta):
    def __init__(self) -> None:
        super().__init__()
        self.limite_saque = 2000
        self.limite_deposito = 20000

    def depositar(self, valor: Decimal) -> Decimal:
        if valor <= 0:
            return self.saldo_atual

        if valor > self.limite_deposito:
            return self.saldo_atual

        return super().depositar(valor)

    def sacar(self, valor: Decimal) -> Decimal:
        if valor > self.limite_saque:
            return self.saldo_atual

        if self.saldo_atual - valor < 0:
            return self.saldo_atual

        return super().sacar(valor)
