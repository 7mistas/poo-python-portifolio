""" Modulo que importa a biblioteca Decimal, para aplcação monetária"""
from decimal import Decimal
from bank import Conta

"""
Classe filha que tem seus atributos de limite e métodos para verificar as transações. 
"""
class Conta_poupanca(Conta):
    def __init__(self) -> None:
        super().__init__()
        self.limite_deposito = 10000
        self.limite_saque = 500
    
    """ Função para verificar as condições de deposito. """
    def depositar(self, valor: Decimal) -> Decimal:
        if valor > self.limite_deposito:
            return self.saldo_atual

        return super().depositar(valor)

    """ Função para verificar as condições de saque. """
    def sacar(self, valor: Decimal) -> Decimal:
        if valor > self.limite_saque:
            return self.saldo_atual

        if self.saldo_atual - valor < 0:
            return self.saldo_atual

        return super().sacar(valor)    
