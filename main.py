def menu():
    while True:
        print("\n=== DIGITE FOCO ===")
        print("1 - Jogar")
        print("2 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            jogar()
        elif opcao == "2":
            print("Até mais! ;)")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()
