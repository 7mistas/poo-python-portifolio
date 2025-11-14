import os
import logging
import getpass
import traceback
import questionary
from chat import Chat
from logger import setup_logging
from exceptions import AuthError, DatabaseError
from cloud_config import Cloud_Config
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from pyfiglet import Figlet

# Inicia o modulo de console do Rich para gráfico na CLI.
console = Console(force_terminal=True, color_system="truecolor")
f = Figlet(font='graffiti')

# Inicia o modulo de logs do ChatAWS.
setup_logging()
log = logging.getLogger(__name__)

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
            questionary.Choice(title= "Buscar Mensagem", value=4),
            questionary.Choice(title= "Trocar usuário", value=5),
            questionary.Separator(),
            questionary.Choice(title= "Retornar ao login", value=0),
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
    log.info("Aplicação iniciada e logs configurados.")

    chat = Chat()
    cloud = Cloud_Config()

    if cloud:
        log.info("Conexão bem sucedida com o servidor na nuvem.")
    else:
        log.warning("[ERRO] Conexão com o servidor na nuvem não estabelecida.")

    # Linha de limpeza do console, antes de iniciar o login.
    os.system('clear' if os.name == 'nt' else 'clear')

    while True:
        opcao = menu_login()

        if opcao == 1:
            console.print("=" * 71, style="grey70")
            console.print(" " * 20, "Digite seus dados 🔑")
            console.print("=" * 71, style="grey70")
            usuario = input("Uuário: ").strip()
            senha = getpass.getpass("Senha: ").strip()
            try:
                chat.auth.login(usuario, senha)
                log.info("Senha autorizada")

                while chat.auth.esta_logado():
                    opcao_chat = menu_chat(chat.auth.usuario_logado)

                    if opcao_chat == 1:
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Meu Perfil 👤")
                        console.print("=" * 71, style="grey70")
                        info = chat.auth.exibir_info_usuario()
                        if info:
                            console.print("\n" + "=" * 71, style='grey70')
                            console.print(f"ID: {info['id']}")
                            console.print(f"Usuário: {info['usuario']}")
                            console.print(f"Email: {info['email'] or 'Não informado'}")
                            console.print(f"Conta criada em: {info['criado_em']}")
                            console.print(f"Último login: {info['ultimo_login']}")
                            console.print("=" * 71, style='grey70' + "\n")
                        else:
                            console.print("Não foi possivel carregar as infos do usuário")
                            log.error("[ERRO] Não foi possivel carregar as infos do usuário")

                    elif opcao_chat == 2: 
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Enviar Mensagem 📤")
                        console.print("=" * 71, style="grey70")
                        conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                        if conteudo.strip():
                            chat.enviar_mensagem(conteudo)
                        else:
                            console.info("Mensagens não podem ser vazia!")

                    elif opcao_chat == 3:
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Histórico 📋")
                        console.print("=" * 71, style="grey70")
                        lista_mensagens = chat.carregar_mensagens(limite=20)
                        if not lista_mensagens:
                            console.print("Nenhuma mensagem no histórico.")
                        else:
                            console.print(f"As ultimas {len(lista_mensagens)} mensagem(ns) do histórico.")
                            for msg in lista_mensagens:
                                console.print(msg.formatar())

                        console.print("=" * 71, style="grey70")

                    elif opcao_chat == 4:
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Buscar Mensagens 🔍")
                        console.print("=" * 71, style="grey70")
                        usuario_busca = input("Digite o nome do usuario: ")
                        chat.buscar_mensagens_usuario(usuario_busca)

                    elif opcao_chat == 5:
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Saindo da conta...")
                        console.print("=" * 71, style="grey70")
                        if chat.auth.logout():
                            log.info("Logout bem sucedido")
                            break 

                    elif opcao_chat == 0:
                        console.print("=" * 71, style="grey70")
                        console.print(" " * 20, "Fechando o chat... ❌")
                        console.print("=" * 71, style="grey70")
                        break

                    else:
                        log.info("Opção inválida digitada pelo usuário!")
                        console.print("Opção inválida!")
                        continue

            except (AuthError, DatabaseError) as e:
                log.warning("Falha no login: %s", e)
                console.print("[Erro] Na tentativa de login do usuário")
                traceback.print_exc()
                

            except Exception as e:
                log.critical("Falha critica no chat após login: %s", e)
                console.print("[Erro]Falha no sistema após login: %s", e)
                traceback.print_exc()

        elif opcao == 2:
            console.print("=" * 71, style="grey70")
            console.print(" " * 15, "Criar Conta 📝")
            console.print("=" * 71, style="grey70")
            usuario = input("Defina seu usuario: ").strip()
            senha = input("Define sua senha (min. 6 caracteres): ").strip()
            email = input("Define seu email: ").strip()
            
            try:
                chat.auth.registrar(usuario, senha, email)
                console.print(f"\nUsuário criado com sucesso!\n")

            except (AuthError, DatabaseError) as e:
                log.warning("Falha ao criar o usuario: %s", e)
                console.print("[Erro] Ao criar conta do usuário", e)
                traceback.print_exc()

            except Exception as e:
                log.critical("Falha critica na criação do usuario: %s", e)
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
