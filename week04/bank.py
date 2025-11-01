from decimal import Decimal

class Conta:
    def __init__(self) -> None:
        self._saldo = Decimal("0.00")

    def depositar(self, valor: Decimal) -> Decimal:
        self._saldo += valor
        return self._saldo

    def sacar(self, valor: Decimal) -> Decimal:
        self._saldo -= valor
        return self._saldo

    @property
    def saldo_atual(self):
        return self._saldo
