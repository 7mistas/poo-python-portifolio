from decimal import Decimal

class Conta:
    def __init__(self, saldo: int) -> None:
        self._saldo = 0

    def depositar(self, valor: int) -> int:
        self.valor += self.saldo
        return self.saldo

    def sacar(self, valor: int) -> int:
        self.valor -= self.saldo
        return self saldo

    @property
    def saldo_atual(self):
        return self.saldo

