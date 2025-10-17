# Importa um (regex) modulo de expressões regulares.
import re

# Função para contar as palavras de um texto simples.
def counter_words(text):
    # Converte o texto para letras minusulas. (ignore case)
    text_lower = text.lower()

    # Extrai as palavras (remove as pontuações. do texto)
    words = re.findall(r'\w+', text_lower)

    # Conta a frequência de cada palavra no texto
    word_freq = {}
    
    # Para cada palavra que estiver no texto...
    for word in words:
        # Se a palavra estiver no texto...
        if word in word_freq:
            # Incrementa uma palavra ao dic
            word_freq[word] += 1
        # Se não...
        else:
            # Adiciona a palavra(chave) e sua primeira vez(valor) ao dic
            word_freq[word] = 1
    # Exibe o resultado
    print (word_freq)

# Texto simples demonstrativo.    
view_text = "Olá, eu, eu, eu sei o que você quer!?"
# Executando a função.
counter_words(view_text)
