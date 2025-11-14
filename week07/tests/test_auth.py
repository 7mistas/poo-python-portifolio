import pytest
import logging
from auth import Autenticacao
from exceptions import AuthError

@pytest.fixture
def db_auth_mock(mocker):
    '''
    Cria um mock para assumir ser Database_Auth.
    '''
    mock = mocker.MagicMock()
    return mock

@pytest.fixture
def auth_inst(db_auth_mock):
    '''
    Cria uma instância da Autenticação e injeta o mock(Database_Auth).
    '''
    return Autenticacao(db_auth_mock)

def registrar_senha_curta(auth_inst, db_auth_mock):
    '''
    Testa o registro do usuário com senha menor que (6) caracteres.

    '''

    with pytest.raises(AuthError, match = "A senha tem que no minimo 6 caracteres"):
        auth_registrar("")

def teste_login_invalido(auth_inst, db_auth_mock):
    '''
    Testa o login lançando um "erro" para lançar um AuthError.
    '''

    with pytest.raises(AuthError):
        auth_inst.login("usuario_invalido", "777!777")
    assert auth_inst.id_logado is None
    assert auth_inst.usuario_logado is None

