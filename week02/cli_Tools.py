# Para ultilização futura no README.MD: 
"""
Importa o modulo pathlib para referenciar o caminho para "students.json".

Importa as feramentas para leitura dos dados e definição de argumentos.

Importa um outro script para uso da sua função calculate_average().
"""
from pathlib import Path
import json, argparse
import grades

def main():
    """
    Função para execução da lógica do script.
    
    Args: 
        (): Executa a função.

    Returns:
        (none): Não há retorno na função, só execução no CLI.

    """
    # Argumento de "média minima", a ser definido pelo usuario.
    parser = argparse.ArgumentParser(description="Filtra alunos por média minima.")
    parser.add_argument("--minimo", type=float, default=7.0, help= "Media minima.")
    args = parser.parse_args()
   
    # Define o caminho do Json sempre apontando para o diretório local.
    json_path = Path(__file__).parent / "students.json"
    # Função para fechar o JSON após a ultilização do mesmo.
    with json_path.open("r", encoding="utf-8") as f:
        # Lê as informações do JSON e atribui a alunos.
        alunos = json.load(f)

    # Então, para cada aluno em alunos.
    for aluno in alunos:
        # A divisão da soma pela quantidade de notas de cada aluno.
        media = grades.calculate_average(aluno["notas"])
        # Comparação entre resultado da média dos alunos com o minimo definido.
        if media >= args.minimo:
            # Se sim?! Parabéns!
            print(f"O aluno {aluno['nome']}, foi aprovado com {media:.2f}.")
            # Se não, valeu, tenta na próxima!
        else: 
            print(f"O aluno {aluno['nome']}, foi reprovado com {media:.2f}.")
if __name__ == "__main__":
    main()
