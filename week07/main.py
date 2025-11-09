import getpass
import logging
import os
from logger import setup_logging
from chat import Chat
from cloud_config import Cloud_Config

# Inicia o modulo de logs do ChatAWS.
setup_logging()
log = logging.getLogger(__name__)

def menu_login():
    print("=" * 50)
    print(" " * 18, "CHAT ☁️  AWS")
    print("=" * 50)
    print("1 - Fazer Login")
    print("2 - Criar Conta")
    print("3 - Simular Deploy AWS")
    print("0 - Sair")
    print("=" * 50)
    try:
        opcao_str = input("Escolha uma opção: ").strip()
        opcao = int(opcao_str)
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
        print("=" * 50)
        print(" " * 18, "Menu chat 💬")
        print("=" * 50)
        print("1 - Informações do usuário")
        print("2 - Enviar mensagem")
        print("3 - Histórico")
        print("4 - Buscar mensagens")
        print("5 - Trocar usuário")
        print("0 - Sair")
        print("=" * 50)
    
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
            print("=" * 50)
            print(" " * 15, "Faça o login 🔑")
            print("=" * 50)
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
                        print("=" * 50)
                        print(" " * 15, "Meu Perfil 👤")
                        print("=" * 50)
                        info = chat.auth.exibir_info_usuario()
                        if info:
                            print(f"\n{'=' * 50}")
                            print(f"ID: {info['id']}")
                            print(f"Usuário: {info['usuario']}")
                            print(f"Email: {info['email'] or 'Não informado'}")
                            print(f"Conta criada em: {info['criado_em']}")
                            print(f"Último login: {info['ultimo_login']}")
                            print(f"{'=' * 50}\n")
                        else:
                            print("[ERRO] Não foi possivel carregar as infos do usuário")

                    elif opcao_chat == 2: 
                        print("=" * 50)
                        print(" " * 15, "Enviar Mensagem 📤")
                        print("=" * 50)
                        conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                        if conteudo.strip():
                            chat.enviar_mensagem(conteudo)
                        else:
                            print("Mensagens não podem ser vazia!")

                    elif opcao_chat == 3:
                        print("=" * 50)
                        print(" " * 18, "Histórico 📋")
                        print("=" * 50)
                        chat.exibir_historico()

                    elif opcao_chat == 4:
                        print("=" * 50)
                        print(" " * 15, "Buscar Mensagens 🔍")
                        print("=" * 50)
                        usuario_busca = input("Digite o nome do usuario: ")
                        chat.buscar_mensagens_usuario(usuario_busca)

                    elif opcao_chat == 5:
                        print("=" * 50)
                        print(" " * 15, "Saindo da conta...")
                        print("=" * 50)
                        if  chat.auth.logout():
                           break 

                    elif opcao_chat == 0:
                        print("=" * 50)
                        print(" " * 15, "Fechando o chat... ❌")
                        print("=" * 50)
                        break

                    else:
                        print("[ERRO!] Opção inválida!")
                        continue

        elif opcao == 2:
            print("=" * 50)
            print(" " * 15, "Criar Conta 📝")
            print("=" * 50)
            usuario = input("Defina seu usuario: ").strip()
            senha = input("Define sua senha (min. 6 caracteres): ").strip()
            email = input("Define seu email: ").strip()
            
            sucesso, mensagem = chat.auth.registrar(usuario, senha, email)
            print(f"\n{mensagem}\n")

        elif opcao == 3: 
            cloud.simular_deploy_aws()

        elif opcao == 0:
            print("=" * 50)
            print(" " * 15, "Fechando o chat... ❌")
            print("=" * 50)
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
