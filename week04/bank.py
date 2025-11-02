""" Modulo que importa a biblioteca Decimal, para aplicação monetária """
from decimal import Decimal

"""
Classe com os atributos da conta bancária
"""
class Conta:
    def __init__(self) -> None:
        self._saldo = Decimal("0.00")

    """Função para depositar na conta"""
    def depositar(self, valor: Decimal) -> Decimal:
        self._saldo += valor
        return self._saldo

    """Função para sacar na conta"""
    def sacar(self, valor: Decimal) -> Decimal:
        self._saldo -= valor
        return self._saldo

    @property
    def saldo_atual(self):
        return self._saldo
