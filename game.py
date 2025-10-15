import time
import random
from colorama import Fore, Style, init
from palavras import LISTA_PALAVRAS
from utils import contagem_regressiva, calcular_pontos
init(autoreset=True)

def jogar(nome):
    palavras_disponiveis = LISTA_PALAVRAS.copy()
    palavras_usadas = set()
    jogar_novamente = "s"

    while jogar_novamente.lower() == "s":
        if len(palavras_disponiveis) == 0:
            print("\nNão há mais palavras disponíveis para jogar.")
            break

        palavra = random.choice(palavras_disponiveis)
        palavras_disponiveis.remove(palavra)
        palavras_usadas.add(palavra)

        print(f"\nPrepare-se, {nome}!")
        print(f"A palavra é: {Fore.RED}{palavra}")
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
            print(f"\nBoa, {nome}! Tempo: {tempo_total}s | Pontos: {pontos}")
        else:
            pontos = 0
            print(f"\nRodada encerrada sem acerto. Pontos: {pontos}")

        while True:
            jogar_novamente = input("\nDeseja jogar novamente? (s/n): ").strip().lower()
            if jogar_novamente in ["s", "n"]:
                break
            else:
                print("Digite apenas 's' ou 'n'.")

    print(f"\nObrigada por jogar o TypeFocus, {nome}!")
