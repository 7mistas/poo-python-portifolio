#!/usr/bin/env python3

import sys
import os
from typing import Tuple

def checkhealth(url: str = "http://localhost:5000/health", timeout: int =5) -> Tuple[bool, str]:
    """
    Verifica o status operacional da API no Docker.

    Args: 
        url: URL do Endpoint de health

    Returns:
        Tupla(sucesso: bool, mensagem: str)
    """
    try:
        response = requests.get(url, timeout=timeout)

        if response.status_code != 200:
            return false, f"Status code incorreto:{resonse.status_code}"

        data = response.json()

        if not data.get("success"):
            return False, "Campo 'success' não foi validado"

        if data.get("data", {}).get("database") != "connected":
            return False, "Banco de dados não conectado"
        
        return True, "A API está saudavel e operacional"

    except requests.exceptions.Timeout:
        return False, "Timeout ao conectar na API"
    except requests.exceptions.ConnectionError:
        return False, "Não foi possivel conectar a API"
    except Exception as e:
        return False, f"Não foi possivel conectar a API: {str(e)}" 
    
if __name__=="__main__":
    sucesso, mensagem = check_health()

    print(mensagem)

    sys.exit(0 if sucesso else 1)
