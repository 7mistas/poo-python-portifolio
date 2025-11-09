import logging
from logger import setup_logging()
from chat import Chat
from cloud_config import Cloud_Config

def menu_login():
    print("=" * 18, "CHAT ☁️  AWS", "=" * 19)
    print("=" * 50)
    print("1 - Fazer Login")
    print("2 - Criar Conta")
    print("3 - Simular Deploy AWS")
    print("0 - Sair")
    print("=" * 50)
    try:
        opcao_str = input("Escolha uma opção: ").strip()
        opcao = int(opcao_str)
        return opcao 

    except ValueError:
        print("[ERRO!] Somente numeros são válidos!")


def menu_chat():
    """
    Exibe o menu com opções para o usuario.
    """
    while True:
        print("=" * 50)
        print("==== Menu chat 💬 =====")
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
            return opcao 

        except ValueError:
            print("[ERRO!] Somente numeros são válidos!")
            continue

def main():
    """
    Executa as opções para o usuario selecionar.
    """
    setup_logging()
    app_log = logging.getLogger("ChatAWS")
    app.info("Aplicaão iniciada e logs configurados.")

    chat = Chat()
    cloud = Cloud_Config()

    if cloud:
        print("Conexão bem sucedida com o servidor na nuvem.")
    else:
        print("[ERRO] Conexão com o servidor na nuvem não estabelecida.")

    while True:
        opcao = menu_login()

        if opcao == 1:
            print("==== Faça o login 🔑 ====")
            usuario = input("Usuário: ").strip()
            senha = input("Senha: ").strip()

            sucesso, mensagem = chat.auth.login(usuario, senha)
            print(f"\n{mensagem}\n")

            if sucesso:
                while chat.auth.esta_logado():
                    opcao_chat = menu_chat()

                    if opcao_chat == 1:
                        print("=" * 20, "Meu Perfil 👤", "=" * 20)
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
                        print("=" * 20, "Enviar Mensagem 📤", "=" * 20)
                        conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                        if conteudo.strip():
                            chat.enviar_mensagem(conteudo)
                        else:
                            print("Mensagens não podem ser vazia!")

                    elif opcao_chat == 3:
                        print("=" * 20, "Histórico 📋", "=" * 20)
                        chat.exibir_historico()

                    elif opcao_chat == 4:
                        print("=" * 20, "Buscar Mensagens 🔍", "=" * 20)
                        usuario_busca = input("Digite o nome do usuario: ")
                        chat.buscar_mensagens_usuario(usuario_busca)

                    elif opcao_chat == 5:
                        print("=" * 20, "Saindo da conta...", "=" * 20)
                        if  chat.auth.logout():
                           break 

                    elif opcao_chat == 0:
                        print("=" * 20, "Fechando o chat... ❌", "=" * 20)
                        break

                    else:
                        print("[ERRO!] Opção inválida!")
                        continue

        elif opcao == 2:
            print("=" * 20, "Criar Conta 📝", "=" * 20)
            usuario = input("Defina seu usuario: ").strip()
            senha = input("Define sua senha (min. 6 caracteres): ").strip()
            email = input("Define seu email: ").strip()
            
            sucesso, mensagem = chat.auth.registrar(usuario, senha, email)
            print(f"\n{mensagem}\n")

        elif opcao == 3: 
            cloud.simular_deploy_aws()

        elif opcao == 0:
            print("==== Fechando o chat... ❌ ====")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
