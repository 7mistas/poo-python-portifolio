from decimal import Decimal
from bank import Conta

class Conta_corrente(Conta):
    def __init__(self, numero: int, limite_saque: Decimal, limite_deposito: Decimal) -> None:
        super().__init__(self, _saldo: Decimal, saldo_atual: Decimal)
        self.numero = numero
        self.limite_saque = 1000
        self.limite_deposito = 3000

    def depositar(self, valor: Decimal) -> Decimal:
        if self.limite_depoosito > self.saldo_atual:
            self.valor += self._saldo
            return self.saldo_atual

    def saque(self, valor: Decimal) -> Decimal:
        if self.valor > self.limite_saque:
            return self.saldo_atual

        if self.valor - self.saldo_atual < 0:
            return self.saldo_atual

        else:
            novo_saldo = self.valor - self_saldo
            return novo_saldo

