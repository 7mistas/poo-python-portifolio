from bank import Conta

class Conta_corrente(Conta):
    def __init__(self, numero: int, limite_saque: int) -> None:
        super().__init__(self, _saldo: int)
        self.numero = numero
        self.limite_saque = 1000
        self.limite_deposito = 3000

    def depositar(self, valor: int) -> int:
        if self.limite_depoosito > self._saldo:
            self.valor += self._saldo
            return self._saldo

    def saque(self, valor: int) -> int:
        if not self.limite_saque += 0:
            self.valor -= self._saldo
            return self._saldo

