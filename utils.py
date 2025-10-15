import time
from colorama import Fore

def contagem_regressiva():
    print("\nPreparando em...")
    for i in range(3, 0, -1):
        print(f"{Fore.RED}{i}{Fore.RESET}")
        time.sleep(1)

def calcular_pontos(tempo, sem_erros=True):
    if tempo < 2:
        pontos_base = 100
    elif tempo < 4:
        pontos_base = 70
    elif tempo < 6:
        pontos_base = 50
    elif tempo < 8:
        pontos_base = 30
    else:
        pontos_base = 10

    bonus = 20 if sem_erros else 0
    return pontos_base + bonus
