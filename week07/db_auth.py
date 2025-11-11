import bcrypt
import logging
import sqlite3
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime
from exceptions import AuthError, DatabaseError

log = logging.getLogger(__name__)

class Database_Auth:
    def __init__(self, db_nome: str = "chat.db"):
        self.db_nome = "db_auth.db"
        log.info("Inicializando Database_Auth e criando tabelas...")
        self.criar_tabela_usuarios()

    def conectar(self) -> sqlite3.Connection:
        caminho_base = Path(__file__).parent
        caminho_completo = caminho_base / self.db_nome

        return sqlite3.connect(caminho_completo)

    def criar_tabela_usuarios(self):
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    hash_senha TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultimo_login TIMESTAMP
                )
            ''')
            conn.commit()
            log.debug("Tabela 'usuarios' verificada/criada.")
        except sqlite3.Erros as e:
            log.error("Falha ao criar tabela no SQLite 'usuarios': %s", e)
            raise DatabaseError(f"Erro no banco de dados: %s", e)
            
        finally:
            conn.close()


    def gerar_hash(self, senha: str) -> str:
        senha_bytes = senha.encode('utf-8')

        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)

        return hash_bytes.decode('utf-8')   

    def verificar_senha(self, senha: str, hash_senha: str) -> bool:
        senha_bytes = senha.encode('utf-8')
        hash_bytes = hash_senha.encode('utf-8')

        return bcrypt.checkpw(senha_bytes, hash_bytes)

    def registrar_usuario(self, usuario: str, senha: str, email: str = ""):

        # Validações:
        if not usuario or len(usuario) < 3:
            raise AuthError("Nome do usuário deve ter mínimo 3 caracteres")
        if not senha or len(senha) < 6:
            raise AuthError("A senha deve ter no mínimo 6 caracteres")

        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            # Verifica se o usuário já existe no banco de dados:
            cursor.execute('SELECT id FROM usuarios WHERE usuario = ?', (usuario,))
            if cursor.fetchone():
                raise AuthError("Usuário já existente!" )
            
            hash_senha = self.gerar_hash(senha)

            # Insere o usuário no banco de dados:
            cursor.execute('''
                INSERT INTO usuarios (usuario, hash_senha, email)
                VALUES (?, ?, ?)
                ''', (usuario, hash_senha, email))

            conn.commit()
            log.info("Usuario %s registrado com sucesso", usuario)
            return True
        
        except sqlite3.Error as e:
            log.error("Usuario %s criado com sucesso: %s", usuario, e)
            if conn:
                log.warning("Desfazendo o registro")
                conn.rollback()
            raise DatabaseError("Usuário não registrado")

        finally:
            if conn:
                conn.close()

    def autenticar_usuario(self, usuario: str, senha: str) -> int:
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            # Busca o usuário:
            cursor.execute('''
                SELECT id, hash_senha FROM usuarios WHERE usuario = ?
                ''', (usuario,)) 

            resultado = cursor.fetchone()

            if not resultado:
                raise DatabaseError("Usuario nao encontrado")
            
            user_id, hash_senha = resultado

            if self.verificar_senha(senha, hash_senha): 

                # Atualiza o ultimo login.
                cursor.execute('''
                    UPDATE usuarios
                    SET ultimo_login = ?
                    WHERE id = ?
                    ''', (datetime.now().isoformat(), user_id))
                
                conn.commit()
                log.info("Usuario %s está autenticado", usuario)
                return user_id

            else:
                log.warning("Falha no login do usuário!")
                return None 

        except sqlite3.Error as e: 
            log.error("Falha no login do usuário %s: %s", usuario, e)
            if conn:
                log.warning("Retornando o login.")
                conn.rollback()
            return None

        finally:
            if conn:
                conn.close()


    def obter_info(self, user_id: int) -> Optional[dict]:
        conn = None
        try:
            conn = self.conectar()
            cursor = conn.cursor()

            cursor.execute('''
            SELECT id, usuario, email, criado_em, ultimo_login
            FROM usuarios
            WHERE id = ?
            ''', (user_id,))

            resultado = cursor.fetchone()

            if resultado:
                return{
                    'id': resultado[0],
                    'usuario': resultado[1],
                    'email': resultado[2],
                    'criado_em': resultado[3],
                    'ultimo_login': resultado[4]
                }

            log.info("Id %s encontrado, Dict gerado", user_id)
            return None

        except sqlite3.Error as e:
            log.error("Id %s não encontrado, Dict não criado: %s", user_id, e)
            return None

        finally:
            if conn:
                conn.close()
