from crud import cadastrar_jogador, editar_jogador, deletar_jogador
from game import jogar, mostrar_ranking_sessao, mostrar_ranking_historico

def menu():
    while True:
        print("\n=== TYPEFOCUS ===")
        print("1 - Jogar")
        print("2 - Editar cadastro")
        print("3 - Deletar cadastro")
        print("4 - Mostrar ranking da sessão")
        print("5 - Mostrar ranking histórico (comparativo)")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            jogador = cadastrar_jogador()
            if jogador:
                jogar(jogador["nome"])
        elif opcao == "2":
            editar_jogador()
        elif opcao == "3":
            deletar_jogador()
        elif opcao == "4":
            mostrar_ranking_sessao()
        elif opcao == "5":
            mostrar_ranking_historico()
        elif opcao == "6":
            print("\nSaindo do TypeFocus...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
