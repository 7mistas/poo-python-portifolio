import os
import logging
import getpass
import requests
import traceback
import questionary
from dotenv import load_dotenv
from datetime import datetime
from src.logger import setup_logging
from src.cloud_config import Cloud_Config
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from pyfiglet import Figlet

console = Console(force_terminal=True, color_system="truecolor")
f = Figlet(font='graffiti')

log = logging.getLogger(__name__)

load_dotenv()

BASE_URL = os.getenv("API_URL")
if not BASE_URL:
    log.warning("A variável de ambiente não foi definida.")
    exit 
TOKEN_GLOBAL = None

def menu_login():
    """
    Exibe o banner "Chat☁️ AWS" em ASCII.
    """
    ascii_art = f.renderText('<ChatAWS>')

    banner = Text(ascii_art, style="bold cyan")
    console.print(banner)

    opcoes_menu = [
            questionary.Choice(title= "Fazer Login", value=1),
            questionary.Choice(title= "Criar Conta", value=2),
            questionary.Choice(title= "Simular Deploy AWS", value=3),
            questionary.Separator(),
            questionary.Choice(title= "Sair", value=0),
    ]
    
    try:
        opcao_select = questionary.select(
                "Escolha uma opção:",
                choices = opcoes_menu,
                use_shortcuts=True
                ).ask()

        if opcao_select is None:
            log.info("Seleção cancelada pelo usuário")
            return -1

        log.info("Opção selecionada para o menu de login")
        return opcao_select

    except Exception as e:
        log.error("Erro inesperado do menu %s", {e})
        return -1

    except ValueError:
        log.error("Opção inválida, somente números permitidos!")
        console.print("[ERRO!] Somente números são válidos!")

def menu_chat(usuario_logado: str):
    """
    Exibe o menu com opções para o usuario.
    """
    
    opcoes_menu = [
            questionary.Choice(
                title=f" >>> Logado como: [{usuario_logado}] <<<",
                disabled=True),
            questionary.Choice(title= "Informações do usuário", value=1),
            questionary.Choice(title= "Enviar mensagem", value=2),
            questionary.Choice(title= "Histórico", value=3),
            questionary.Choice(title= "Buscar mensagem", value=4),
            questionary.Separator(),
            questionary.Choice(title= "Sair da conta", value=5),
    ]
    
    try:
        opcao_select = questionary.select(
                 "Escolha uma opção:",
                choices =opcoes_menu,
                use_shortcuts=True
                ).ask()

        if opcao_select is None:
            log.info("Seleção cancelada pelo usuário")
            return -1

        log.info("Opção selecionada para o menu de chat")
        return opcao_select

    except Exception as e:
        log.error("Erro inesperado do menu %s", {e})
        return -1

    except ValueError:
        log.error("Opção inválida, somente números permitidos!")
        console.print("[ERRO!] Somente números são válidos!")

def main():
    """
    Executa as opções para o usuario selecionar.
    """
    setup_logging()
    log.info("Aplicação iniciada e logs configurados.")
    global TOKEN_GLOBAL

    cloud = Cloud_Config()

    # Linha de limpeza do console, antes de iniciar o login.
    os.system('clear' if os.name == 'nt' else 'clear')

    while True:
        opcao = menu_login()

        if opcao == 1:
            console.print("=" * 71, style="grey70")
            console.print(" " * 20, "Digite seus dados 🔑", style="bold cyan")
            console.print("=" * 71, style="grey70")
            usuario = input("Usuário: ").strip()
            senha = getpass.getpass("Senha: ").strip()
            try:
                response = requests.post(
                        f"{BASE_URL}/auth/login",
                        json={"usuario": usuario, "senha": senha}
                )

                if response.status_code == 200:
                    resposta_json = response.json()
                    TOKEN_GLOBAL = resposta_json['data']['token']
                    log.info("Login para o usuário %s foi realizado com sucesso", usuario)
                    console.print(f"[bold cyan]\nBem vindo, {usuario}!\n[/bold cyan]")

                    while TOKEN_GLOBAL:       
                        opcao_chat = menu_chat(usuario)

                        try:
                            if opcao_chat == 1:
                                console.print("=" * 71, style="grey70")
                                console.print(" " * 20, "Meu Perfil 👤", style="bold cyan")
                                console.print("=" * 71, style="grey70")
                                
                                resp_perfil = requests.get(
                                        f"{BASE_URL}/auth/me",
                                        headers={"Authorization": f"Bearer {TOKEN_GLOBAL}"}
                                )

                                if resp_perfil.status_code == 200:
                                    info = resp_perfil.json().get('data')
                                    console.print("\n" + "=" * 71, style='grey70')
                                    console.print(f"ID: {info['id']}")
                                    console.print(f"Usuário: {info['usuario']}")
                                    console.print(f"Email: {info['email'] or 'Não informado'}")
                                    console.print(f"Conta criada em: {info['criado_em']}")
                                    console.print(f"Último login: {info['ultimo_login']}")
                                    console.print("=" * 71, style='grey70' + "\n")
                                else:
                                    console.print(f"[ERRO] Erro ao buscar perfil: {resp_perfil.json().get('erro')}")
                                    log.error("[ERRO] Não foi possivel carregar as infos do usuário")

                            elif opcao_chat == 2: 
                                console.print("=" * 71, style="grey70")
                                console.print(" " * 20, "Enviar Mensagem 📤")
                                console.print("=" * 71, style="grey70")
                                conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                                resp_msg = requests.post(
                                        f"{BASE_URL}/messages/post",
                                        json={"conteudo": conteudo},
                                        headers={"Authorization": f"Bearer {TOKEN_GLOBAL}"}
                                )
                                if resp_msg.status_code != 201:
                                    console.print(f"[Erro]Falha no servidor: {resp_msg.json().get('erro')}")
                                else:
                                    console.print("\nMensagem enviada" + "\n", style="bold green")

                            elif opcao_chat == 3:
                                console.print("=" * 71, style="grey70")
                                console.print(" " * 20, "Histórico 📋")
                                console.print("=" * 71, style="grey70")
                                resp_hist = requests.get(
                                        f"{BASE_URL}/messages/all",
                                        headers={"Authorization": f"Bearer {TOKEN_GLOBAL}"}
                                )
                                if resp_hist.status_code == 200:
                                    historico = resp_hist.json().get('data',[])
                                    if not historico:
                                        console.print("Nenhuma mensagem no histórico")
                                    else:
                                        for msg in historico:
                                            console.print(msg)
                                            console.print("=" * 71, style="grey70")
                                else:
                                    console.print(f"Erro ao buscar o histórico: {resp_hist.json().get('erro')}")

                            elif opcao_chat == 4:
                                console.print("=" * 71, style="grey70")
                                console.print(" " * 20, "Buscar Mensagens 🔍")
                                console.print("=" * 71, style="grey70")
                                usuario_busca = input("Digite o nome do usuario: ")

                                resp_busca = requests.get(
                                        f"{BASE_URL}/messages/search",
                                        params={"usuario": usuario_busca},
                                        headers={"Authorization": f"Bearer {TOKEN_GLOBAL}"}
                                )

                                if resp_busca.status_code == 200:
                                    mensagens_formatadas = resp_busca.json().get('data', [])
                                    if not mensagens_formatadas:
                                        console.print(f"Nenhuma mensagem encontrada para '{usuario_busca}'.")
                                    else:
                                        for msg in mensagens_formatadas:
                                            console.print(msg)
                                            console.print("=" * 71, style="grey70")
                                else:
                                    console.print(f"Erro ao buscar: {resp_busca.json().get('erro')}")

                            elif opcao_chat == 5:
                                console.print("=" * 71, style="grey70")
                                console.print(" " * 20, "Saindo da conta...")
                                console.print("=" * 71, style="grey70")
                                TOKEN_GLOBAL = None
                                log.info("Logout do usuario %s foi bem sucedido", usuario)
                                break

                            else:
                                log.info("Opção inválida digitada pelo usuário!")
                                console.print("Opção inválida!")
                                continue

                        except(requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
                            log.warning("Falha no login: %s", e)
                            console.print("[Erro] Falha na tentativa de login do usuário: ", e)
                            traceback.print_exc()
                        except Exception as e:
                            log.critical("Falha critica no cliente: %s", e)
                            console.print("[Erro] Fatal inesperado no (Cliente): %s", e)
                            traceback.print_exc()
                else:
                    erro_msg = response.json().get('erro', 'Erro desconhecido')
                    log.warning("Falha no login (Cliente) para %s", usuario, erro_msg)
                    console.print(f"[ERRO] {erro_msg}")

            except requests.exceptions.ConnectionError:
                log.critical("Não foi possivel conectar no endereço: %s", BASE_URL)
                console.print("[Erro] Falha na tentativa de login do usuário: ")
                traceback.print_exc()
            except Exception as e:
                log.critical("[ERRO] Falha critica no chat após login: %s", e)
                console.print("Falha na execução do Cliente: %s", e)
                traceback.print_exc()

        elif opcao == 2:
            console.print("=" * 71, style="grey70")
            console.print(" " * 15, "Criar Conta 📝")
            console.print("=" * 71, style="grey70")
            usuario = input("Defina seu usuario: ").strip()
            senha = input("Define sua senha (min. 6 caracteres): ").strip()
            email = input("Define seu email: ").strip()
            
            try:
                response = requests.post(
                        f"{BASE_URL}/auth/register",
                        json={"usuario": usuario, "senha": senha, "email": email}
                )

                if response.status_code == 201:
                    console.print(f"O usuario {'ussario'}, foi criado com sucesso")
                else:
                    erro_msg = response.json().get('erro', 'Erro desconhecido')
                    console.print(f"[ERRO] {erro_msg}")

            except requests.exceptions.ConnectionError:
                log.critical("Não foi possivel conectar ao servidor API %s", BASE_URL)
                console.print(f"[Erro] Não foi possivel conectar ao servidor: ", e)
                traceback.print_exc()

            except Exception as e:
                log.critical("Falha crit9ica na criação do usuario: %s", e)
                console.print("[ERRO]: Falha na criação da conta: %s", e)
                traceback.print_exc()

        elif opcao == 3: 
            cloud.simular_deploy_aws()

        elif opcao == 0:
            console.print("=" * 71, style="grey70")
            console.print(" " * 15, "Fechando o chat... ❌")
            console.print("=" * 71, style="grey70")
            break

        else:
            console.print("Opção inválida!")

if __name__ == "__main__":
    main()
