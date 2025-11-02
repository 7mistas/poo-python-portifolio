import sqlite3

class Database:
    def __init__(self, db_nome: str = "chat.db"):
        self.db_nome = db_nome
        self.criar_tabelas()
    
    def conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                timestamp TIMESTAMP DEFAUT CURRENT_TIMESTAMP)''')            
    def inserir_mensagem(self) -> bool:
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO mensagens (usuario, mensagem, timestamp)
                VALUES(?, ?, ?, ))''', )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERRO!] Ao inserir a mensaem.")
            return False

    def listar_mensagens(self, limite: int = 10) -> List[Tuple]:
        try:
            conn = self.conectar
            cursor = conn.cursor
            cursor.execute('''
                SELECT id, usuario, mensagem, timesatamp
                FROM mensagens
                ORDER BY timestamp DESC
                LIMIT ?
                ''', (limite,))

            mensagens = cursor.fetchall()
            conn.close()

            return list(mensagens)
        except Exception as e:
            print("[ERRO!] Erro ao listar as mensagens: {e}")
            return []

    def buscar_usuario(self, usuario: str) -> List[Tuple]:
        try:
            conn = self.conectar
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, usuario, mensagem, timesatamp
                FROM mensagens
                WHERE usuario LIKE ?
                ORDER BY timestamp ASC
                ''', (f'%{usuario}%',))

            mensagens = cursor.fetchall()
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


