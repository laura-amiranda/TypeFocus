from game import jogar
from crud import cadastrar_jogador, editar_jogador, deletar_jogador, carregar_jogadores
from colorama import Fore, Style, init
init(autoreset=True)

def menu():
    jogador = None
    
    while True:
        print(f"\n{Fore.MAGENTA}======= {Fore.MAGENTA}TYPEFOCUS{Fore.MAGENTA} =======")
        print("1 - Cadastrar ou Entrar")
        
        if jogador:
            nome = jogador['nome']
            print(f"2 - Jogar")
        else:
            print("2 - Jogar")
            
        print("3 - Editar cadastro")
        print("4 - Deletar cadastro")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            jogador = cadastrar_jogador()
        elif opcao == "2":
            if jogador:
              
                jogadores_salvos = carregar_jogadores()
                if jogador["nome"] in jogadores_salvos:
                    jogar(jogador["nome"])
                else:
                    print(f"\n{Fore.RED}Cadastro deletado! Faça um novo.")
                    jogador = None  
            else:
                print(f"\n{Fore.MAGENTA}Faça seu cadastro primeiro!")
        elif opcao == "3":
            editar_jogador()
        elif opcao == "4":
            if jogador:
                nome_deletado = jogador["nome"]
                deletar_jogador()
              
                jogadores_salvos = carregar_jogadores()
                if nome_deletado not in jogadores_salvos:
                    jogador = None  
                    print(f"\n{Fore.RED}Seu cadastro foi deletado.")
            else:
                deletar_jogador()
        elif opcao == "5":
            print("\nSaindo do TypeFocus. Até a próxima!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
