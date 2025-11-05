from datetime import datetime
from typing import Optional

class Mensagem:
    def __init__(self, usuario: str, conteudo: str,
            id_msg: Optional[int] = None,
            timestamp: Optional[datetime] = None):
        self.id = id_msg
        self.usuario = usuario
        self.conteudo = conteudo
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

    def formatar(self):
        data_formatada = self.timestamp.strftime("%d/%m/%Y - %H:%M:%S")
        return f"[{data_formatada}] {self.usuario}: {self.conteudo}"       
    def __str__(self):                                                    
        return self.formatar()       
