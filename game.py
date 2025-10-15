import time
import random
import os
from colorama import Fore, Style, init
from palavras import PALAVRAS_POR_NIVEL, LISTA_PALAVRAS_PADRAO
from utils import contagem_regressiva, calcular_pontos
init(autoreset=True)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_mascote_inicial():
    print(f"""
{Fore.WHITE}                    ╭────────────────────────────╮
                    │ Olá! Sou o TypeBot!        │
                    │ Vamos treinar sua          │
                    │ velocidade de digitação?   │
                    │ Escolha um nível abaixo.   │
                    ╰────╮{Style.RESET_ALL}
{Fore.MAGENTA}        ╔═════╗   ╰───○{Style.RESET_ALL}
{Fore.MAGENTA}        ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}           ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╔══╩══╗{Style.RESET_ALL}
{Fore.MAGENTA}        ║     ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}       ╔═══╬═══╗{Style.RESET_ALL}
{Fore.MAGENTA}       ║   ║   ║{Style.RESET_ALL}
{Fore.MAGENTA}      ═╩═══╩═══╩═{Style.RESET_ALL}
{Fore.MAGENTA}      ▓▓       ▓▓{Style.RESET_ALL}
    """)


def exibir_mascote_pronto():
    print(f"""
{Fore.WHITE}                    ╭──────────────────────╮
                    │  Está preparado?     │
                    ╰────╮{Style.RESET_ALL}
{Fore.MAGENTA}        ╔═════╗   ╰───○{Style.RESET_ALL}
{Fore.MAGENTA}        ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}           ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╔══╩══╗{Style.RESET_ALL}
{Fore.MAGENTA}        ║     ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}       ╔═══╬═══╗{Style.RESET_ALL}
{Fore.MAGENTA}       ║   ║   ║{Style.RESET_ALL}
{Fore.MAGENTA}      ═╩═══╩═══╩═{Style.RESET_ALL}
{Fore.MAGENTA}      ▓▓       ▓▓{Style.RESET_ALL}
    """)
    input(f"{Fore.WHITE}Pressione ENTER para começar:{Style.RESET_ALL}")
    print()


def exibir_mascote_resultado(acertou, tempo=0):
    if acertou:
        if tempo < 3:
            mensagem = "Incrível! Você é rápido!"
        elif tempo < 5:
            mensagem = "Muito bem! Continue assim!"
        else:
            mensagem = "Bom trabalho! Pratique mais!"

        print(f"""
{Fore.WHITE}              ╭────────────────────────╮
              │ {mensagem:<26}│
              ╰──╮{Style.RESET_ALL}
{Fore.MAGENTA}    ╔═════╗  ╰─○{Style.RESET_ALL}
{Fore.MAGENTA}    ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}       ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╔══╩══╗{Style.RESET_ALL}
{Fore.MAGENTA}    ║     ║{Style.RESET_ALL}
        """)
    else:
        print(f"""
{Fore.YELLOW}              ╭────────────────────────╮
              │  Que pena!             │
              │  Tente novamente!      │
              ╰──╮{Style.RESET_ALL}
{Fore.MAGENTA}    ╔═════╗  ╰─○{Style.RESET_ALL}
{Fore.MAGENTA}    ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}       ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╔══╩══╗{Style.RESET_ALL}
{Fore.MAGENTA}    ║     ║{Style.RESET_ALL}
        """)

    time.sleep(1.5)


def exibir_mascote_despedida(nome):
    print(f"""
{Fore.WHITE}              ╭──────────────────────────╮
              │  Até logo, {nome[:12]:<12}!   │
              │  Foi ótimo treinar com │
              │  você! Volte sempre!   │
              ╰──╮{Style.RESET_ALL}   {Fore.MAGENTA}👋{Style.RESET_ALL}
{Fore.MAGENTA}    ╔═════╗  ╰─○{Style.RESET_ALL}
{Fore.MAGENTA}    ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╚══╦══╝{Style.RESET_ALL}
{Fore.MAGENTA}       ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╔══╩══╗{Style.RESET_ALL}
{Fore.MAGENTA}    ║     ║{Style.RESET_ALL}
    """)
    time.sleep(5)


def escolher_dificuldade():
    print(f"\n{Fore.WHITE}Escolha o nível de dificuldade:")
    print("1 - Fácil ")
    print("2 - Médio ")
    print("3 - Difícil ")
    print("4 - Padrão ")

    while True:
        escolha = input("\nEscolha uma opção (1-4): ").strip()
        if escolha == "1":
            return "facil", PALAVRAS_POR_NIVEL["facil"].copy()
        elif escolha == "2":
            return "medio", PALAVRAS_POR_NIVEL["medio"].copy()
        elif escolha == "3":
            return "dificil", PALAVRAS_POR_NIVEL["dificil"].copy()
        elif escolha == "4":
            return "padrao", LISTA_PALAVRAS_PADRAO.copy()
        else:
            print(f"{Fore.RED}Opção inválida! Digite um número de 1 a 4.")


def jogar(nome):
    limpar_tela()
    exibir_mascote_inicial()
    
    nivel, palavras_disponiveis = escolher_dificuldade()
    
    if nivel == "padrao":
        print(
            f"\n{Fore.MAGENTA}Modo Padrão selecionado - "
            f"a dificuldade aumenta gradativamente!"
        )
    else:
        print(f"\n{Fore.MAGENTA}Nível {nivel.upper()} selecionado!")
    
    time.sleep(1.5)
    
    limpar_tela()
    exibir_mascote_pronto()
    
    palavras_usadas = set()
    jogar_novamente = "s"

    while jogar_novamente.lower() == "s":
        if len(palavras_disponiveis) == 0:
            print("\nNão há mais palavras disponíveis para jogar.")
            break

        limpar_tela()
        
        palavra = random.choice(palavras_disponiveis)
        palavras_disponiveis.remove(palavra)
        palavras_usadas.add(palavra)

        print(
            f"\nA palavra é: "
            f"{Fore.RED}{palavra}{Style.RESET_ALL}\n"
        )
        
        contagem_regressiva()

        inicio = time.time()
        tempo_total = 0
        tentativa = ""

        while True:
            tentativa = input("\nDigite a palavra: ").strip()
            fim = time.time()
            tempo_total = round(fim - inicio, 2)

            if tempo_total > 60:
                print("\nTempo esgotado! Você demorou mais de 60 segundos.")
                tentativa = ""
                break

            if not tentativa:
                print("Campo vazio! Tente novamente.")
                continue

            if tentativa != palavra:
                print(f"{Fore.RED}Palavra incorreta! Envie novamente.")
                continue
            else:
                break

        if tentativa == palavra:
            pontos = calcular_pontos(tempo_total, sem_erros=True)
            limpar_tela()
            print(f"\nTempo: {tempo_total}s | Pontos: {pontos}")
            exibir_mascote_resultado(True, tempo_total)
        else:
            pontos = 0
            limpar_tela()
            print(f"\nRodada encerrada sem acerto. Pontos: {pontos}")
            exibir_mascote_resultado(False)

        while True:
            jogar_novamente = input(
                "\nDeseja jogar novamente? (s/n): "
            ).strip().lower()
            if jogar_novamente in ["s", "n"]:
                break
            else:
                print("Digite apenas 's' ou 'n'.")
        
        if jogar_novamente == "s":
            trocar = input(
                "Deseja trocar de dificuldade? (s/n): "
            ).strip().lower()
            if trocar == "s":
                limpar_tela()
                exibir_mascote_inicial()
                nivel, novas_palavras = escolher_dificuldade()
                novas_filtradas = [
                    p for p in novas_palavras
                    if p not in palavras_usadas
                ]
                if not novas_filtradas:
                    print(
                        f"\n{Fore.YELLOW}Nenhuma nova palavra disponível "
                        f"nesse nível. Escolha outro nível ou "
                        f"continue no atual."
                    )
                    time.sleep(1.8)
                else:
                    palavras_disponiveis = novas_filtradas
                    print(
                        f"\n{Fore.MAGENTA}Dificuldade alterada "
                        f"para {nivel.upper()}!"
                    )
                    _ = input("\nPressione ENTER para continuar:")
                    limpar_tela()
                    exibir_mascote_pronto()

    limpar_tela()
    exibir_mascote_despedida(nome)
