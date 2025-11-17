import logging

def setup_logging():
    """
    Configura o logging 'raiz' (Root Logger) para todo o projeto.
    """

    logging.basicConfig(
            level=logging.INFO, # Nivel de handler mínimo que será exibido.
            format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler("chat_app.log"), 
                logging.StreamHandler()
                ]
            )
