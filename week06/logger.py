import logging
import os

def setup_logging():
    """ 
    Configura o sistema de logging para o console (INFO) e o arquivo (DEBUG).
    O nome 'ChatAWS' permite que tdos os arquivos usem o mesmo sistema. 
    """

    # Pega o logger principal.
    logger = logging.getLogger("ChatAWS")
    logger.setLevel(logging.DEBUG)

    # Havendo handlers, não adiciona novamente (duplicação).
    if not logger.handlers:
        return

    # Formato definido.
    formatter = logging.Formatter("[%(asctime)s] %(name)s: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Handler com infos parciais para o console. (INFO: O usuário visualiza)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler com info total para o arquivo. (DEBUG: Tudo dentro do arquivo)
    file_handler = logging.StreamHandler()
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Adiciona os handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
