class AuthError(Exception):
    """Exceção base para erros de autenticação (login, registro)."""
    pass

class DatabaseError(Exception):
    """Exceção para erros do banco de dados (conexão, sintaxe SQL)."""
    pass

class ChatError(Exception):
    """Exceção para erros no chat (mensagem vazia, opção incorreta)."""
    pass
