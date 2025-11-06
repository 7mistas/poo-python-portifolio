from chat import Chat

def menu():
    """
    Exibe o menu com opções para o usuario.
    """
    while True:
        print("=" * 50)
        print("Menu chat: ")
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

    while True:
        print("==== Bem vindo ao chat ====")
        usuario = input("Digite seu nome para entrar: ")
        if chat.fazer_login(usuario):
            break

    while True:
        opcao = menu()

        if opcao == 1: 
            print("==== Enviar Mensagem ====")
            conteudo = input(f"Digite a sua mensagem, {usuario}: ")
            chat.enviar_mensagem(conteudo)

        elif opcao == 2:
            print("==== Histórico ====")
            chat.exibir_historico()

        elif opcao == 3:
            print("==== Buscar Mensagens do Usuário ====")
            usuario_busca = input("Digite o nome do usuario: ")
            chat.buscar_mensagens_usuario(usuario_busca)

        elif opcao == 4:
            print("==== Saindo... ====")
            novo_usuario = input("Digite o novo usuario: ")
            if  chat.fazer_login(novo_usuario):
                usuario = novo_usuario
        
        elif opcao == 5:
            print("=== Limpar o chat ====")
            chat.limpar_chat()

        elif opcao == 0:
            print("Fechando o chat... ")
            break

        else:
            print("[ERRO!] Opção inválida!")
            continue
    
if __name__ == "__main__":
    main()
