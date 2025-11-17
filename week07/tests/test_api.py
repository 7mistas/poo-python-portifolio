import pytest
import logging
from api import app as flask_app    
from pathlib import Path
from chat import Chat

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def app():
    """
    Fixture que cria uma instância da aplicação Flask para testes.
    Configura o ambiente de teste e usa banco de dados separado.
    """



