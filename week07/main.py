import os
import logging
import getpass
from chat import Chat
from logger import setup_logging
from cloud_config import Cloud_Config
from rich.console import Console
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
    ascii_art = f.renderText('{ChatAWS}')

    banner = Text(ascii_art)
    console.print(banner)

    console.print("=" * 71, style="grey70")
    console.print("1 - Fazer Login")
    console.print("2 - Criar Conta")
    console.print("3 - Simular Deploy AWS")
    console.print("0 - Sair")
    console.print("=" * 71, style="grey70")
    try:
        opcao_str = input("Escolha uma opção: ").strip()
        opcao = int(opcao_str)
        console.print("=" * 71, style="grey70")
        log.info("Opção valida para o menu de login")
        return opcao
    

    except ValueError:
        log.error("Opção inválida, somente números permitidos!")
        print("[ERRO!] Somente números são válidos!")


def menu_chat():
    """
    Exibe o menu com opções para o usuario.
    """
    while True:
        console.print("=" * 71, style='grey70')
        console.print(" " * 20, "Menu chat 💬")
        console.print("=" * 71, style='grey70')
        console.print("1 - Informações do usuário")
        console.print("2 - Enviar mensagem")
        console.print("3 - Histórico")
        console.print("4 - Buscar mensagens")
        console.print("5 - Trocar usuário")
        console.print("0 - Sair")
        console.print("=" * 71, style="grey70")
    
        try:
            opcao_str = input("Escolha uma opção: ").strip()
            opcao = int(opcao_str)
            log.info("Opção valida para o menu de login")
            return opcao 

        except ValueError:
            log.error("Opção inválida, somente números permitidos!")
            print("[ERRO!] Somente números são válidos!")
            continue

def main():
    """
    Executa as opções para o usuario selecionar.
    """
    log.info("Aplicação iniciada e logs configurados.")

    chat = Chat()
    cloud = Cloud_Config()

    if cloud:
        print("Conexão bem sucedida com o servidor na nuvem.")
        log.info("Conexão bem sucedida com o servidor na nuvem.")
    else:
        log.warning("[ERRO] Conexão com o servidor na nuvem não estabelecida.")

    # Linha de limpeza do console, antes de iniciar o login.
    os.system('clear' if os.name == 'nt' else 'clear')

    while True:
        opcao = menu_login()

        if opcao == 1:
            console.print("=" * 71, style="grey70")
            print(" " * 20, "Faça o login 🔑")
            console.print("=" * 71, style="grey70")
            usuario = input("Usuário: ").strip()
            try:
                senha = getpass.getpass("Senha: ").strip()
            except Exception as e:
                log.error("Erro de captura da senha: %s", e)
                continue

            sucesso, mensagem = chat.auth.login(usuario, senha)
            print(f"\n{mensagem}\n")

            if sucesso:
                while chat.auth.esta_logado():
                    opcao_chat = menu_chat()

                    if opcao_chat == 1:
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Meu Perfil 👤")
                        console.print("=" * 71, style="grey70")
                        info = chat.auth.exibir_info_usuario()
                        if info:
                            console.print("\n" + "=" * 71, style='grey70')
                            print(f"ID: {info['id']}")
                            print(f"Usuário: {info['usuario']}")
                            print(f"Email: {info['email'] or 'Não informado'}")
                            print(f"Conta criada em: {info['criado_em']}")
                            print(f"Último login: {info['ultimo_login']}")
                            console.print("=" * 71, style='grey70' + "\n")
                        else:
                            print("[ERRO] Não foi possivel carregar as infos do usuário")

                    elif opcao_chat == 2: 
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Enviar Mensagem 📤")
                        console.print("=" * 71, style="grey70")
                        conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                        if conteudo.strip():
                            chat.enviar_mensagem(conteudo)
                        else:
                            print("Mensagens não podem ser vazia!")

                    elif opcao_chat == 3:
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Histórico 📋")
                        console.print("=" * 71, style="grey70")
                        chat.exibir_historico()

                    elif opcao_chat == 4:
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Buscar Mensagens 🔍")
                        console.print("=" * 71, style="grey70")
                        usuario_busca = input("Digite o nome do usuario: ")
                        chat.buscar_mensagens_usuario(usuario_busca)

                    elif opcao_chat == 5:
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Saindo da conta...")
                        console.print("=" * 71, style="grey70")
                        if  chat.auth.logout():
                           break 

                    elif opcao_chat == 0:
                        console.print("=" * 71, style="grey70")
                        print(" " * 20, "Fechando o chat... ❌")
                        console.print("=" * 71, style="grey70")
                        break

                    else:
                        print("[ERRO!] Opção inválida!")
                        continue

        elif opcao == 2:
            console.print("=" * 60, style="grey70")
            print(" " * 15, "Criar Conta 📝")
            console.print("=" * 60, style="grey70")
            usuario = input("Defina seu usuario: ").strip()
            senha = input("Define sua senha (min. 6 caracteres): ").strip()
            email = input("Define seu email: ").strip()
            
            sucesso, mensagem = chat.auth.registrar(usuario, senha, email)
            print(f"\n{mensagem}\n")

        elif opcao == 3: 
            cloud.simular_deploy_aws()

        elif opcao == 0:
            console.print("=" * 60, style="grey70")
            print(" " * 15, "Fechando o chat... ❌")
            console.print("=" * 60, style="grey70")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
