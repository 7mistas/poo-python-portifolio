""" Modulo para importar a biblioteca Decimal, para aplicação monetária"""
from decimal import Decimal
""" Modulo que importa de bank.py a Classe Mãe"""
from bank import Conta

"""
Classe Filha que contém atributos de limites, e métodos de verificação para as transações.
"""
class Conta_corrente(Conta):
    def __init__(self) -> None:
        super().__init__()
        self.limite_saque = 2000
        self.limite_deposito = 20000

    """ Função para verificar as condições de deposito """
    def depositar(self, valor: Decimal) -> Decimal:
        if valor <= 0:
            return self.saldo_atual

        if valor > self.limite_deposito:
            return self.saldo_atual

        return super().depositar(valor)

    """ Função para verificar as condições de saque """
    def sacar(self, valor: Decimal) -> Decimal:
        if valor > self.limite_saque:
            return self.saldo_atual

        if self.saldo_atual - valor < 0:
            return self.saldo_atual

        return super().sacar(valor)
