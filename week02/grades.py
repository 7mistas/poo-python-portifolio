""" 
Modulo para lidar com o apontamento do diretório na pasta.
Importa a biblioteca para leitura do arquivo Json.

Ele referencia o local de onde o arquivo tem outros:
"""
from pathlib import Path
import json

def calculate_average(notas: float) -> float:
    """
    Função para calculo aritmético das notas.
    Args:
        (notas: float): Recebe valor float numa lista.
    Returns:
        Retorna a média da soma das notas, em relação a quantidade de notas dos alunos.            
    """ 
    return sum(notas) / len(notas)
    
def main():
    """
    Funçao principal que carrega toda a lógica.
    
    Ela imprime no terminal o status caso o aluno esteja (ou não) aprovado, junto da sua média.
    """
    # Atribui a uma váriavel o conteudo do Json apontado.
    json_path = Path(__file__).parent / "students.json"
    # Força o arquivo a ser fechado após a leitura do mesmo.
    with json_path.open("r", encoding="utf-8") as f:
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
# Chama a função para execução do código.
if __name__ == "__main__":
    main()
