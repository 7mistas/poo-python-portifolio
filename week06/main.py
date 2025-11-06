from chat import Chat
from cloud_config import Cloud_Config

def menu_login():
    print("=" * 20 + "CHAT AWS")
    print("=" * 50)
    print("1 - Fazer Login")
    print("2 - Criar Conta")
    print("3 - Simular Deploy AWS")
    print("0 - Sair")
    print("=" * 50)
    return input("Escolha uma opção: ").strip()

def menu_chat():
    """
    Exibe o menu com opções para o usuario.
    """
    while True:
        print("=" * 50)
        print("==== Menu chat 💬 =====")
        print("1 - Enviar mensagem")
        print("2 - Listar mensagens")
        print("3 - Buscar mensagens pelo usuário")
        print("4 - Trocar usuário")
        print("5 - Limpar o chat")
        print("0 - Sair")
        print("=" * 50)
    
        try:
            opcao_str = input("Escolha uma opção: ").strip()
            opcao = int(opcao_str)
            return opcao 

        except ValueError:
            print("[ERRO!] Somente numeros são válidos!")

def main():
    """
    Executa as opções para o usuario selecionar.
    """
    chat = Chat()
    cloud = Cloud_Config()

    if cloud:
        print("Conexão bem sucedida com o servidor na nuvem.")
    else:
        print("[ERRO] Conexão com o servidor na nuvem não estabelecida.")


    while True:
        print("==== Bem vindo ao chat ====")
        usuario = input("Digite seu nome para entrar: ")
        if chat.fazer_login(usuario):
            break

    while True:
        opcao = menu_chat()

        if opcao == 1:
            print("==== Faça o login 🔑 ====")
            usuario = input("Usuário: ").strip
            senha = input("Senha: ").strip

            sucesso, mensagem = chat.auth.login(usuario, senha)
            print(f"\n{mensagem}")

            if sucesso:
                while chat.auth.esta_logado():
                    opcao_chat = menu_chat()

                if opcao == 1:
                    print("=== Meu Perfil 👤 ====")
                    info = chat.auth.get_usuario_atual(self)
                    if info:
                        print(f"\n{'=' * 60}")
                        print(f"ID: {info['id']}")
                        print(f"Usuário: {info['username']}")
                        print(f"Email: {info['email'] or 'Não informado'}")
                        print(f"Conta criada em: {info['criado_em']}")
                        print(f"Último login: {info['ultimo_login']}")
                        print(f"{'=' * 60}\n")


                if opcao == 2: 
                    print("==== Enviar Mensagem 📤 ====")
                    conteudo = input(f"Digite a sua mensagem, {usuario}: ")
                    chat.enviar_mensagem(conteudo)

                elif opcao == 3:
                    print("==== Histórico 📋 ====")
                    chat.exibir_historico()

                elif opcao == 4:
                    print("==== Buscar Mensagens 🔍 ====")
                    usuario_busca = input("Digite o nome do usuario: ")
                    chat.buscar_mensagens_usuario(usuario_busca)

                elif opcao == 5:
                    print("==== Sando da conta... ↩️  ====")
                    novo_usuario = input("Digite o novo usuario: ")
                    if  chat.fazer_login(novo_usuario):
                        usuario = novo_usuario

                elif opcao == 0:
                    print("==== Fechando o chat... ❌ ====")
                    break

                else:
                    print("[ERRO!] Opção inválida!")
                    continue

        elif opcao == 2:
            print("==== Criar Conta 📝 ====")
            usuario = input("Defina seu usuario: ").strip
            senha = input("Define sua senha (min. 6 caracteres): ").strip
            email = input("Define seu email: ").strip
            
            sucesso, mensagem = chat.auth.registrar(usuario, senha, email)
            print("\nmensagem")

        elif opcao == 3: 
            cloud.simular_deploy_aws()

        elif opcao == 0:
            print("==== Saindo do app ❌ ====")
            break

if __name__ == "__main__":
    main()
