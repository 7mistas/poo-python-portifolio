# Importa a biblioteca para leitura do arquivo Json.
import json

# Função para calcular as notas somadas dos alunos.
def calculate_average(notas):
    # Retorno do valor das médias das notas.
    return sum(notas) / len(notas)

# Força o arquivo ser fechado após a leitura.
with open("/home/mista/poo-python-portifolio/week02/students.json", "r", encoding="utf-8") as f:
    # Leitura do json.
    alunos = json.load(f)

# Para cada aluno listado no Json.
for aluno in alunos:
    # A média é calculada para cada nota somada.
    media = calculate_average(aluno["notas"])
    # Se a media for maior ou igual a 7.
    if media >= 7:
        # O CLI exbe a mensagem com o reu
        print(f"{aluno['nome']} aprovado com média: {media:.2f}")
    else: 
        print(f"{aluno['nome']} reprovado com média: {media:.2f}")
