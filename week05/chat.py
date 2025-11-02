from datetime import datetime
from db_msg import Database
from message import Mensagem
from typing import List

class Chat:
    def _init__(self, ):
        self.db = Database()
        self.usuario_atual = None

    def fazer_login(self, usuario: str) -> bool:
        if not usuario or usuario.strip() == "":
            print("[Erro!] Usuário inválido!")
            return False
        self.usuario_atual = usuario
        print(f"Bem vindo, {self.usuario_atual}!")
        return True

    def enviar_mensagem(self, conteudo: str) - bool:
        if not usuario or usuario.strp() == "":
            print("[ERRO!] Voce precisa estar logado!")

        if not conteudo or conteudo.stip() = "":
            print("[ERRO!] Mensagem vazia!")
            return False
    
    def carregar_mensagens(self, limite: int = 50) -> List[Mensagem]:
        dados = self.db.listar_mensagens(limite)
        mensagens = []

        for id_msg, usuario, mensagem, data_str in dados:
            timestamp = datetime.fromisoformat(data_str)
            msg = Mensagem(usuario, mensagem, timestamp)
            mensagens.append(msg)

        return mensagens

    def exibir_historico(self, limite: int = 20) -> None:
        mensagens = self.carregar_mensagens(limite)

        if not mensagens:
            print("[INFO] Nenhuma mensagem no histórico.")
            return

        print("=" * 50)
        print(f"As ultimas {len(mensagens)} mensagens.")
        print("=" * 50)

        for mensagem in mensagens:
            print(msg.formatar())
    
    def buscar_mensagens_usuario(self, usuario: str) -> None:
        dados = self.db.buscar_usuario(usuario)

        if not dados:
            print("[ERRO!] Mesagens não encontradas!")
            return

        print("=" * 50)
        print(f"Mensagens do {usuario}: ")
        print("=" * 50)

        for id_msg, usuario, mensages. timestamp in dados:
            timestamp = datatime.fromisoformat(data_str)
            msg = Mensagem(usuario, conteudo, timestamp)
            print(msg.formatar())
            
        print("=" * 50)
        
