from datetime import datetime
from db_msg import Database
from message import Mensagem
from auth import Autenticacao
from typing import List

class Chat:
    """
    Gerencia o login do usuario e suas operações na interações com o banco de dados.
    """
    def __init__(self):
        """
        Inicializa o banco de dados e defini o nome do usuario_atual com o padrão: None.
        """
        self.db = Database("chat.db")
        self.auth = Autenticacao()
        #self.usuario_atual = None


    def enviar_mensagem(self, conteudo: str) -> bool:
        """
        Valida o login e o conteúdo, e envia a mensagem para o banco de dados

        Args:
            conteudo (str): Texto que vai compor a mensagem do usuário.

        Returns:
            bool: True se a mensagem for enviada,
            False caso o contrário.
        """
        # Validações de usuário e conteudo: 
        if not self.auth.esta_logado():
            return False
            print("[ERRO!] Voce precsa estar logado!")

        if not conteudo or conteudo.strip() == "":
            print("[ERRO!] Mensagem vazia!")
            return False

        usuario = self.auth.get_usuario_atual()
        # Insere a mensagem no banco de dados:
        sucesso = self.db.inserir_mensagem(usuario, conteudo.strip())
        if sucesso:
            print("Mensagem enviada!")

        else:
            print("Mensagem não enviada!")

        return sucesso

    
    def carregar_mensagens(self, limite: int = 50) -> List[Mensagem]:
        """
        Carrega os dados e os converte para objetos Mensagem.
        
        Args:
            limite (int): Limite de mensagens que vão ser carregadas. Padrão: None.

        Returns: 
            List[Mensagem]: Retorna a lista de objetos prontos para exibição.
        """
        dados = self.db.listar_mensagens(limite)
        mensagens = []

        for id_msg, usuario, mensagem, data_str in dados:
            if data_str is None:
                continue
            timestamp = datetime.fromisoformat(data_str)
            msg = Mensagem(usuario, mensagem, id_msg, timestamp)
            mensagens.append(msg)

        return mensagens

    def exibir_historico(self, limite: int = 20) -> None:
        """
        Carrega e exibe as mensagens.

        Args:
            limite (int): Número de mensagens para serem exibidas.
        """

        mensagens = self.carregar_mensagens(limite)

        if not mensagens:
            print("[INFO] Nenhuma mensagem no histórico.")
            return

        print("=" * 71)
        print(f"As ultimas {len(mensagens)} mensagens.")
        print("=" * 71)

        for mensagem in mensagens:
            print(mensagem.formatar())
    
    def buscar_mensagens_usuario(self, usuario: str) -> None:
        """Busca mensagens de um usuario expecífico.

        Args:
            usuario (str): O nome do usuario buscado.
        """
            
        dados = self.db.buscar_usuario(usuario)

        if not dados:
            print("[ERRO!] Mesagens não encontradas!")
            return

        print("=" * 71)
        print(f"Mensagens do {usuario}: ")
        print("=" * 71)

        for id_msg, usuario, mensagem, data_str in dados:
            timestamp = datetime.fromisoformat(data_str)
            msg = Mensagem(usuario, mensagem, id_msg, timestamp)
            print(msg.formatar())
            
        print("=" * 71)
        
    def limpar_chat(self): # Desabilitado
        print("Limpando histórico de mensagens")
        self.db.deletar_chat()
