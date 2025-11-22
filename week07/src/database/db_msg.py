import logging
import sqlite3
from datetime import datetime
from typing import List, Tuple
from pathlib import Path
from src.exceptions import AuthError, DatabaseError

log = logging.getLogger(__name__) 

class Database:
    """
    Gerencia a conexão e as operações CRUD com o banco de dados SQLite.
    """
    def __init__(self, db_nome: str):
        """
        Inicia a instância do banco de dados e cria a tabela das mensagens.
        Args: db_nome: (str): Nome do banco de dados (chat.db)
        """
        self.db_nome = db_nome
        log.info("Iniciando Database de mensagens e criando tabela...")
        self.criar_tabelas()

    def conectar(self) -> sqlite3.Connection:
        """
        Cria um caminho absoluto e retorna uma nova conexão com o Banco de Dados.

        Returns: 
            sqlite3.Connection: Conexão ativa com o SQLite. 
        """
        raiz_projeto = Path(__file__).resolve().parents[2]
        caminho_base = raiz_projeto / 'data'
        caminho_base.mkdir(parents=True, exist_ok=True) 

        return sqlite3.connect(caminho_base / self.db_nome)

    def criar_tabelas(self):
        """
        Cria a tabela mensagens se ela não existir.
        Garante  que o esquema de dados esteja correto.
        """

        try:
            with self.conectar() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mensagens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT NOT NULL,
                        mensagem TEXT NOT NULL,
                        timestamp TEXT TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                log.info("Tabela 'mensagens' criada com sucesso!")

        except sqlite3.Error as e:
            log.error("[Erro] Na criação da tabela de mensagem: %s", e)
            raise DatabaseError("Erro na criação da tabela de mensagens: %s ", e)

    def inserir_mensagem(self, usuario: str, mensagem: str) -> bool:
        """
        Insere uma nova mensagem no banco de dados
        
        Args: 
            usuario(str): Nome do usuario logado.
            mensagem(str): Conteudo da mensagem.

        Returns:
            bool: True se a mensagem foi registrada no banco de dado,
            False caso contrário.
        """
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO mensagens (usuario, mensagem, timestamp)
                    VALUES(?, ?, ?)''', (usuario, mensagem, datetime.now()))
                log.info("Mensagem do usuario inserida com sucesso %s às %s", usuario, datetime.now())

        except sqlite3.Error as e:
            log.error("Erro ao inserir mensagem na tabela: %s", e)
            raise DatabaseError("Erro ao salvar mensagem no banco de dados: %s", e)

    def listar_mensagens(self, limite: int = 50) -> List[Tuple]:
        """
        Busca e retorna mensagens mais recentes do banco de dados.

        Args:
            limite (int, Optional): O máximo de mensagens que pode retornar. Padrao 50.

        Returns:
            List [Tuple]: Retorna uma lista de tuplas com os dados de cada mensagens.
        """
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT id, usuario, mensagem, timestamp
                    FROM mensagens
                    ORDER BY timestamp DESC
                    LIMIT ?
                    ''', (limite,))

                mensagens = cursor.fetchall()
                log.info("Até número de %s mensagens foram listadas", limite)
                return mensagens

        except sqlite3.Error as e:
            log.error("[Erro] Falha na busca das mensagnes no bamco de dados: %s", e)
            raise DatabaseError("Não foi possivel listar as mensagens.")
            return []

    def pegar_mensagem_usuario(self, usuario: str) -> List[Tuple]:
        """
        Busca e retorna uma lista de mensagens do usuario atual.

        Args:
            usuario (str): Nome do usuario atual.

        Returns:
            List [Tuple]: Uma lista de tuplas com as mensagens do usuario.
        """
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()

                # Lógica de busca parcial (%{usuario}%)
                cursor.execute('''
                    SELECT id, usuario, mensagem, timestamp
                    FROM mensagens
                    WHERE usuario LIKE ?
                    ORDER BY timestamp ASC
                    ''', (f'%{usuario}%',))

                mensagens = cursor.fetchall()
                log.info("A busca pelo %s foi bem sucedida", usuario)
                return mensagens

        except sqlite3.Error as e:
            log.error("Falha ao buscar o usuario $s: %s", usuario, e)
            raise DatabaseError("Não foi possivel buscar as mensagens do usuário")
            return []

    def deletar_mensagem(self, id_mensagem: str ) -> bool:
        """
        Deleta uma mensagem pelo ID do usuário.

        Args:
            id_mensagem (str): O ID da mensagem que será deletada.

        Returns:
            bool: True sa a mensagem for deletada do banco,
            False caso contrário
        """
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM mensagens WHERE id = ?', (id_mensagem,))

                log.info("A mensagem do ID: $s foi deleta com sucesso!", id_mensagem)
                return True

        except Sqlite3.Error as e:
            log.error("Erro ao deletar mensagem do ID $s: %s", id_mensagem, e)
            raise DatabaseError("Não foi possivel deletar a mensagem")
            return False
        
    def deletar_chat(self) -> bool: # Fechado na ultima versão.
        """
        Deleta todas as mensagens do chat.

        Returns:
            bool: True se todas mensagens forem deletadas do banco,
            False caso o contrário.
        """
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM mensagens')

                log.info("Todas as mensagens foram deletadas com sucesso!")
                return True

        except sqlite3.Error as e:
            log.error("[Erro] Ao deletar todas as mensagens")
            raise DatabaseError("Não foi possivel deletar todas as mensagens")
            return False
