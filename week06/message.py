from datetime import datetime
from typing import Optional

class Mensagem:
    """
    Representa um objeto de mensagens com seus atributos.
        """
    def __init__(self, usuario: str, conteudo: str,
            id_msg: Optional[int] = None,
            timestamp: Optional[datetime] = None):
            """
            Inicializa a mensagem. Atribuindo a hora atual caso for None.

            Args:
                usuario (str): Nome do usuario que envia a mensagem.
                conteudo (str): Conteudo da mensagem.
                id_msg (Optinal[int], optional): O ID da mensagem. Padrão: None
                timestamp (Optional[datetime], optional): Data e hora da mensagem. Padrao: None.

            """
            self.id = id_msg
            self.usuario = usuario
            self.conteudo = conteudo
        
            # Lógica para garantir que a data tenha o datetime sempre válido.
            if timestamp is None:
                self.timestamp = datetime.now()
            else:
                self.timestamp = timestamp

    def formatar(self):
        """
        Formata os detalhes da mensagem de maneira legivel pra visualizar.
        
        Returns:
            str: O resultado da função formatar()
        """
        data_formatada = self.timestamp.strftime("%d/%m/%Y - %H:%M:%S")
        return f"[{data_formatada}] {self.usuario}: {self.conteudo}"       
    def __str__(self):                                                    
        return self.formatar()       
