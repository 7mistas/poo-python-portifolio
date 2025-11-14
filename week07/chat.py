import logging
from datetime import datetime
from db_msg import Database
from message import Mensagem
from auth import Autenticacao
from typing import List, Tuple

log = logging.getLogger(__name__)

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
            log.warning("Tentativa de envio de mensagem sem login.")
            raise AuthError("[ERRO!] Voce precsa estar logado!")

        if not conteudo or conteudo.strip() == "":
            log.warning("Tentativa de envio de mensagem vazia.")
            raise ChatError("[ERRO!] A mensagem não pode ser vazia!")

        try:
            # Insere a mensagem no banco de dados:
            self.db.inserir_mensagem(self.auth.usuario_logado, conteudo)
        except DatabaseError as e:
            log.error("Erro ao inserir mensagem no banco de dados: %s", e)
            raise DatabaseError("Falha ao salvar a mensagem: %s",e)
    
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

    def exibir_historico(self, limite: int = 20) -> List[Mensagem]:
        """
        Carrega as mensagens para exibição do histórico.

        Args:
            limite (int): Número de mensagens para serem exibidas.
        """
        mensagens = self.carregar_mensagens(limite)
        if not mensagens:
            log.info("Nenhuma mensagem no histórico.")
            return []

        return mensagens

    
    def buscar_mensagens_usuario(self, usuario: str) -> List[Mensagem]:
        """Busca mensagens de um usuario expecífico.

        Args:
            usuario (str): O nome do usuario buscado.

        Returns:
            dados(List): retorna uam lista com os dados buscados. 
        """
        dados = self.db.pegar_mensagem_usuario(usuario)
        if not dados:
            log.info("Mesagens não encontradas!")
            
        return dados

    def limpar_chat(self): # Desabilitado
        self.db.deletar_chat()
