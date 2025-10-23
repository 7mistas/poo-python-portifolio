class Carro:
    def __init__(self, modelo="N/A", cor="N/A", ano="N/A", status=False):
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.status = status

    def ligar(self):
        if not self.status:
            self.status = True
        return self.status

    def desligar(self):
        if self.status:
            self.status = False
        return carro.status

    def info(self):
        print(f"Modelo: {self.modelo}\n"
                f"Cor: {self.cor}\n"
                f"Ano: {self.ano}\n"       
                f"Status: {self.status}")

def main():
    meu_carro = Carro()
    print("=" * 50)
    meu_carro.modelo = input("Digite o modelo: ")
    meu_carro.cor = input("Digite a cor: ")
    try:
        meu_carro.ano = int(input("Digite o ano do veículo: "))
    except ValueError:
        print("Ano inválido")

    print("=" * 50)
    print("Modelo Definido: ")
    meu_carro.info()

if __name__ == "__main__":
    main()
