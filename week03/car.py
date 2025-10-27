class Carro:
    """ Classe Carro que cria objetos com os seguintes atributos abaixo"""
    total_carros = 0
    def __init__(self, modelo: str, cor: str, ano: int, status: bool = False) -> None:
        """Inicializa o objeto da class Carro e seus atributos"""        
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.status = status
        Carro.total_carros += 1

    def ligar(self) -> bool:
        """Função para LIGAR o objeto Carro, mudando seu valor booleano"""
        if not self.status:
            self.status = True
        return self.status

    def desligar(self) -> bool:
        """Função para DESLIGAR o objeto Carro, mudando seu valor booleano"""
        if self.status:
            self.status = False
        return self.status

    def info(self) -> str:
        """Função para LISTAR os atributos dos objetos"""
        return(f"Modelo: {self.modelo}\n"
                f"Cor: {self.cor}\n"
                f"Ano: {self.ano}\n"       
                f"Status: {'Ligado' if self.status else 'Desligado'}")

