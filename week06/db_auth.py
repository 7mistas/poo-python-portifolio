import bcrypt
import sqlite3
import pathlib import Path

class Database_Auth:
    def __init__(self, db_nome: str = "chat.db"):
        self.db_nome = "db_auth.db"
        self.criar_tabela_usuarios()

    def conectar(self) -> sqlite3.Connetion:
        caminho_base = Path(__file__).parent
        caminho_completo = caminho_base / self.db_nome
        return sqlite3.connect(caminho_completo)

    def criar_tabela_usuarios(self):
        conn = self.conectar()
        cursor = conn.cusrsor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRYMARY KEY AUTOINCREMENT
                usuario TEXT UNIQUE NOT NULL,
                hash_senha TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ultimo_login TIMESTAMP
            )
        ''')

    def gerar_hash(self, senha: str) -> str:
        senha_bytes = senha.encore('utf-8')
        salt = bcrypt.gensalt()

        hash_bytes = bcrypt.hashpw(senha_bytes, salt)

        return hash_bytes.decode('utf-8')   

    def verificar_a_senha(self, senha: str, hash_armazenado: str) -> bool:
        senha_bytes = senha.encore('utf-8')
        hash_bytes = hash_armazenado('utf-8')

        return bcrypt.checkpw(senha_bytes, hash_bytes)

    def registrar_usuario(self, usuario: str, senha: str:, email: str = "") -> Tuple[bool, str]:
        # Validações:
        if not usuario or len(username) < 3:
            return False, "Nome do usuário deve ter mínimo 3 caracteres"
        if not senha or len(senha) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres"

        try:
            conn.connect()
            cursor = conn.cursor()

            # Verifica se o usuário já existe no banco de dados:
            cursor.execute('SELECT id FROM WHERE usuario = ?' (usuario,))
            if cursor.fetchone():
                conn.close
                return False 
            
            hash_senha = self.gerar_senha()

            # Insere o usuário no banco de dados:
            cursor.execute('''
                INSERT INTO usuarios (usuario, hash_senha, email)
                VALUE (?, ?, ?)
                ''', (usuario, senha, email))

            conn.commit()
            conn.close()

            print(f"[INFO] {usuário] registrado com sucesso!")
            return True, "Usuario criado com sucesso"
        
        except Exception as e:
            print(f"[ERRO] O usuário não foi registrado: {e}")
            return False, "Usuário não registrado"

    def autenticar_usuario(self, usuario: str, senha: str) -> Tuple[bool, str]:
        try:
            conn.connect()
            cursor = conn.cursor()

            # Busca o usuário:
            cursor.execute('''
                SELECT id FROM usuarios WHERE usuario = ?
                ''', (usuario,)) 

                resultado = cursor.fetchone()

                if not resultado:
                    conn.close()
                    return False, Nonw
                
                user_id, hash_senha = resultado

                if not self.verificar_senha(senha, hash_senha):
                    # Atualiza o ultimo login.
                    cursor.execute('''
                        UPDATE usuarios
                        SET ultimo_login = ?
                        WHERE id = ?
                        ''', (datetime.now().isoformat(), user_id))
                    
                    conn.commit()
                    conn.close()

                    print(f"{usuario} logado!")
                    return False, None

                else:
                    print("[AVISO] Falha no login do usuário!")
                    return False, None
            except Exception as e: 
                print(f"[ERRO] Erro ao efetuar o login: {e}")
                return False, None

    def obter_info(self, user_id: int) -> Optional[dict]:
        try:
            conn.connect()
            cursor = conn.conect()

            cursor.execute('''
            SELECT id, usuario, email, criado_em, ultimo_login
            FROM usuarios
            WHERE id ?
            ''', (user_id))

            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return{
                    'id': resultado[0],
                    'usuario': resultado[1],
                    'email': resultado[2],
                    'criado_em': resultado[3],
                    'ultimo_login': resultado[4]
                }

            return None

        except Exeception as e:
            print(f"[ERRO] Ao buscar usuário!")
            return None




