import sqlite3
from datetime import datetime
from typing import List, Tuple
from pathlib import Path

class Database:
    def __init__(self, db_nome: str):
        self.db_nome = db_nome
        self.criar_tabelas()
    
    def conectar(self) -> sqlite3.Connection:
        caminho_base = Path(__file__).parent
        caminho_completo = caminho_base / self.db_nome

        return sqlite3.connect(caminho_completo)

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def inserir_mensagem(self, usuario, mensagem) -> bool:
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            #timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO mensagens (usuario, mensagem)
                VALUES(?, ?)''', (usuario, mensagem))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(e)
            print(f"[ERRO!] Ao inserir a mensagem: {str(e)}")
            return False

    def listar_mensagens(self, limite: int = 50) -> List[Tuple]:
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
            conn.close()
            return mensagens

        except Exception as e:
            print(f"[ERRO!] Erro ao listar as mensagens: {e}")

    def buscar_usuario(self, usuario: str) -> List[Tuple]:
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, usuario, mensagem, timesatamp
                FROM mensagens
                WHERE usuario LIKE ?
                ORDER BY timestamp ASC
                ''', (f'%{usuario}%',))

            mensagens = cursor.fetchall()
            print(mensagens)
            conn.closed()
            return mensagens
        except Exception as e:
            print(f"[ERRO!] Erro ao buscar o usuário!: {e}")
            return []

    def deletar_mensagem(self, id_mensagem: str) -> bool:
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM mensagens WHERE id = ?', (id_mensagem,))

            conn.commit()
            conn.closed()
            return True
        except Exception as e:
            print(f"[ERRO!] Ao deletar a mensagem: {e}")
            return False
        
    def limpar_chat(self) -> bool:
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM mensagens')

            conn.commit()
            conn.closed()
            return True
        except Exception as e:
            print(f"[ERRO!] Ao deletar todas as mensagens: {e}")  
            return False


