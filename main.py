import os
from game import jogar
from crud import (
    cadastrar_jogador,
    editar_jogador,
    deletar_jogador,
    carregar_jogadores
)
from colorama import Fore, Style, init
init(autoreset=True)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    jogador = None
    
    while True:
        limpar_tela()
        print(f"\n{Fore.MAGENTA}======= TYPEFOCUS =======")
        print("1 - Cadastrar ou Entrar")
        
        if jogador:
            nome = jogador['nome']
            print(f"2 - Jogar - Logado como: {nome}")
        else:
            print("2 - Jogar")
            
        print("3 - Editar cadastro")
        print("4 - Deletar cadastro")
        print("5 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            limpar_tela()
            jogador = cadastrar_jogador()
            input("\nPressione ENTER para continuar:")
        elif opcao == "2":
            if jogador:
                jogadores_salvos = carregar_jogadores()
                if jogador["nome"] in jogadores_salvos:
                    jogar(jogador["nome"])
                else:
                    limpar_tela()
                    print(f"\n{Fore.RED}Cadastro deletado! Faça um novo.")
                    jogador = None
                    input("\nPressione ENTER para continuar:")
            else:
                limpar_tela()
                print(f"\n{Fore.MAGENTA}Faça seu cadastro primeiro!")
                input("\nPressione ENTER para continuar:")
        elif opcao == "3":
            limpar_tela()
            editar_jogador()
            input("\nPressione ENTER para continuar:")
        elif opcao == "4":
            limpar_tela()
            if jogador:
                nome_deletado = jogador["nome"]
                deletar_jogador()
                jogadores_salvos = carregar_jogadores()
                if nome_deletado not in jogadores_salvos:
                    jogador = None
                    print(f"\n{Fore.RED}Seu cadastro foi deletado.")
            else:
                deletar_jogador()
            input("\nPressione ENTER para continuar:")
        elif opcao == "5":
            limpar_tela()
            print("\nSaindo do TypeFocus. Até a próxima!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\nPressione ENTER para continuar:")


if __name__ == "__main__":
    menu()
