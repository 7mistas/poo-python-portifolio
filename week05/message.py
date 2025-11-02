class Mensagem:
    def __init__(self, usuario: str, conteudo: str):
        self.usuario = usuario
        self.conteudo = conteudo
        self.timestamp = datetime.now()srttime("%d-%m-%Y %H:%M:%S")

    def formatar(self):      
        returm {
                "usuario" = self.usuario
                "conteudo" = self.conteudo
                "timestamp" = self.timestamp                              
                }                                                         
                                                                          
    def __str__(self):                                                    
        return f"[{self.timestamp}] {sel.usuario}: {self.conteudo}"       
        
