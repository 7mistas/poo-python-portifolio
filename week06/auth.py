from db_auth import Database_Auth
from typing import Optional, Tuple

class Autenticacao:
    def __init__(self):
        self.db_auth = Database_Auth()
        self.usuario_logado: Optional[str] = None
        self.id_logado: Optional[int] = None

    def registrar(self, usuario: str, senha: str, email: str = "") -> Tuple[bool, str]:
        return self.db_auth.registrar_usuario(usuario, senha, email)

    def login(self, usuario: str, senha: str) -> Tuple[bool, str]:
        autenticado, user_id = self.db_auth.autenticar_usuario(usuario, senha)

        if autenticado:
            self.id_logado = user_id
            self.usuario_logado = usuario
            return True, f"Bem vindo {usuario}! ID: {user_id}"

        else:
            return False, f"Usuário ou senha incorretos!"

    def logout(self):
        if self.usuario_logado:
            print(f"Usuario {self.usuario_logado} desconectado!")

        self.id_logado = None
        self.usuario_logado = None

    def esta_logado(self) -> bool:
        return self.usuario_logado is not None

    def get_usuario_atual(self) -> Optional[str]:
        return self.usuario_logado

    def exibir_info_usuario(self) -> Optional[dict]:
        if self.id_logado:
           return self.db.obter_info(self.id_logado)
        return None
