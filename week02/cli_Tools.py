# Para ultilização futura no README.MD: 

# Importa as feramentas para leitura dos dados e definição de argumentos.
import json, argparse

# Argumento de "média minima", a ser definido pelo usuario.
parser = argparse.ArgumentParser(description="Filtra alunos por média minima.")
parser.add_argument("--minimo", type=float, default=7.0, help= "Media minima.")
args = parser.parse_args()

# Função para fechar o JSON após a ultilização do mesmo.
with open("/home/mista/poo-python-portifolio/week02/students.json", "r", encoding="utf-8") as f:
    # Lê as informações do JSON e atribui a alunos.
    alunos = json.load(f)

# Então, para cada aluno em alunos.
for aluno in alunos:
    # A divisão da soma pela quantidade de notas de cada nota.
    media = sum(aluno["notas"]) / len(aluno["notas"])
    # Comparação entre resultado da média dos alunos com o minimo definido.
    if media >= args.minimo:
        # Se sim?! Parabéns!
        print(f"O aluno {aluno['nome']}, foi aprovado com {media:.2f}.")
        # Se não, valeu, tenta na próxima!
    else: 
        print(f"O aluno {aluno['nome']}, foi reprovado com {media:.2f}.")
