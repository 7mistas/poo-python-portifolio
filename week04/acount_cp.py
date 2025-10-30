from decimal import Decimal
from bank import Conta

class Conta_poupanca(Conta):
    def __init__(self, numero: int, limite_deposito: Decimal, limite_saque: Decimal) -> None:
        super().__init__(self, _saldo: Decimal, saldo_atual: Decimal)
        self.numero = numero
        self.limite_deposito = 1000
        self.limite_saque = 500

    def depositar(self, valor: Decimal) -> Decimal:
        if self.valor <= self.limite_deposito:
            self.valor += self._saldo
            return self._saldo

    def sacar(self, valor: Decimal) -> Decimal:
        if self.valor > self.limite_saque:
            return self.saldo_atual

        if self.saldo_atual - self.valor < 0:
            return self.saldo_atual

        else: 
            novo_saldo = self.saldo_atual - self.valor
            return novo_saldo

