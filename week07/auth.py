from db_auth import Database_Auth
from typing import Optional, Tuple
from exceptions import AuthError, DatabaseError

class Autenticacao:
    def __init__(self):
        self.db_auth = Database_Auth()
        self.usuario_logado: Optional[str] = None
        self.id_logado: Optional[int] = None

    def registrar(self, usuario: str, senha: str, email: str = "") -> Tuple[bool, str]:
        self.db_auth.registrar_usuario(usuario, senha, email)

    def login(self, usuario: str, senha: str) -> Tuple[bool, str]:
        autenticado, user_id = self.db_auth.autenticar_usuario(usuario, senha)
        
        self.id_logado = user_id
        self.usuario_logado = usuario

    def logout(self):
        if self.usuario_logado:
            log.info(f"Usuario {self.usuario_logado} desconectado!")
        else:
            log.warning("Tentativa de logout sem usuario logado.")

        self.id_logado = None
        self.usuario_logado = None

    def esta_logado(self) -> bool:
        return self.usuario_logado is not None
 
    def get_usuario_atual(self) -> Optional[str]:
        return self.usuario_logado

    def exibir_info_usuario(self) -> Optional[dict]:
        if self.id_logado:
           return self.db_auth.obter_info(self.id_logado)
        return None
