from datetime import datetime
from typing import Optional

class Mensagem:
    def __init__(self, usuario: str, conteudo: str,
            id_msg: Optional[int] = None,
            timestamp: Optional[datetime] = None):
        self.id = id_msg
        self.usuario = usuario
        self.conteudo = conteudo
        self.timestamp = timestamp or datetime.now()

    def formatar(self):
        data_formatada = self.timestamp.strftime("%d/%m/%Y - %H:%M:%S")
        return f"[{self.timestamp}] {self.usuario}: {self.conteudo}"       
                                                                          
    def __str__(self):                                                    
        return self.formatar()       
        
