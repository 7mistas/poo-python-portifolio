import logging
import sqlite3
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

db_msg_log = logging.getLogger("ChatAWS.Msg") 

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
        db_msg_log.info("Iniciando Database de mensagens e criando tabela...")
        self.criar_tabelas()
    def conectar(self) -> sqlite3.Connection:
        """
        Cria um caminho absoluto e retorna uma nova conexão com o Banco de Dados.

        Returns: 
            sqlite3.Connection: Conexão ativa com o SQLite. 
        """
        caminho_base = Path(__file__).parent
        caminho_completo = caminho_base / self.db_nome

        return sqlite3.connect(caminho_completo)

    def criar_tabelas(self):
        """
        Cria a tabela mensagens se ela não existir.
        Garante  que o esquema de dados esteja correto.
        """

        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mensagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    timestamp TEXT TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()
            db_msg_log.info("Tabela 'mensagens' criada com sucesso!")
        except Exception as e:
            db_msg_log.error("Erro na criação da tabela de mensagem: %s", e)
            if conn:
                conn.rollback

        finally:
            if conn:
                conn.close()

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
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO mensagens (usuario, mensagem, timestamp)
                VALUES(?, ?, ?)''', (usuario, mensagem, datetime.now()))
            conn.commit()
            db_msg_log.info("Mensagem do usuario inserida com sucesso %s às %s", usuario, datetime.now())
            return True

        except Exception as e:
            db_msg_log.error("Erro ao inserir mensagem na tabela: %s", e)
            if conn:
                conn.rollback()

            return False

        finally:
            if conn:
                conn.close()

    def listar_mensagens(self, limite: int = 50) -> List[Tuple]:
        """
        Busca e retorna mensagens mais recentes do banco de dados.

        Args:
            limite (int, Optional): O máximo de mensagens que pode retornar. Padrao 50.

        Returns:
            List [Tuple]: Retorna uma lista de tuplas com os dados de cada mensagens.
        """
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, usuario, mensagem, timestamp
                FROM mensagens
                ORDER BY timestamp DESC
                LIMIT ?
                ''', (limite,))

            mensagens = cursor.fetchall()
            db_msg_log.info("Até número de %s mensagens foram listadas", limite)
            return mensagens

        except Exception as e:
            db_msg_log.info("Iniciando Database de mensagens e criando tabelas...")
            return []

        finally:
            if conn:
                conn.close()

    def buscar_usuario(self, usuario: str) -> List[Tuple]:
        """
        Busca e retorna uma lista de mensagens do usuario atual.

        Args:
            usuario (str): Nome do usuario atual.

        Returns:
            List [Tuple]: Uma lista de tuplas com as mensagens do usuario.
        """
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            # Lógica de busca parcial (%{usuario}%)
            cursor.execute('''
                SELECT id, usuario, mensagem, timestamp
                FROM mensagens
                WHERE usuario LIKE ?
                ORDER BY timestamp ASC
                ''', (f'%{usuario}%',))

            mensagens = cursor.fetchall()
            db_msg_log.info("A busca pelo %s foi bem sucedida", usuario)
            return mensagens

        except Exception as e:
            db_msg_log.error("Falha ao buscar o usuario $s: %s", usuario, e)
            return []
        
        finally:
            if conn:
                conn.close()

    def deletar_mensagem(self, id_mensagem: str ) -> bool:
        """
        Deleta uma mensagem pelo ID do usuário.

        Args:
            id_mensagem (str): O ID da mensagem que será deletada.

        Returns:
            bool: True sa a mensagem for deletada do banco,
            False caso contrário
        """
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM mensagens WHERE id = ?', (id_mensagem,))

            conn.commit()
            db_msg_log.info("A mensagem do ID: $s foi deleta com sucesso!", id_mensagem)
            return True

        except Exception as e:
            db_msg_log.error("Erro ao deletar mensagem do ID $s: %s", id_mensagem, e)
            if conn:
                conn.rollback()
            return False

        finally:
            if conn:
                conn.close()
        
    def deletar_chat(self) -> bool: # Fechado na ultima versão.
        """
        Deleta todas as mensagens do chat.

        Returns:
            bool: True se todas mensagens forem deletadas do banco,
            False caso o contrário.
        """
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM mensagens')

            conn.commit()
            db_msg_log.info("Todas as mensagens foram deletadas com sucesso!")
            return True

        except Exception as e:
            db_msg_log.error("Erro ao deletar todas as mensagens")
            if conn:
                conn.rollback()
            return False

        finally:
            if conn:
                conn.close()
