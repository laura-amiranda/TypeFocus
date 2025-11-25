import time
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def contagem_regressiva():
    print("\nPreparando em...")
    for i in range(3, 0, -1):
        print(f"{Fore.MAGENTA}{i}{Fore.RESET}")
        time.sleep(1)

def calcular_pontos(tempo, sem_erros=True, streak=0, bateu_recorde=False):
    """
    Calcula pontos conforme esquema:
    - <2s => 100
    - 2-4 => 70
    - 4-6 => 50
    - 6-8 => 30
    - >8 => 10
    Bônus:
    - sem_erros: +20
    - streak: +10 por combo (por rodada)
    - bateu_recorde: +30
    """
    if tempo < 2:
        pontos = 100
    elif tempo < 4:
        pontos = 70
    elif tempo < 6:
        pontos = 50
    elif tempo < 8:
        pontos = 30
    else:
        pontos = 10

    if sem_erros:
        pontos += 20

    pontos += streak * 10

    if bateu_recorde:
        pontos += 30

    return pontos

def getch():
    """
    Lê um único caractere do terminal sem precisar pressionar ENTER.
    Funciona em Windows (msvcrt) e em Unix (tty/termios).
    """
    try:
        import msvcrt
        ch = msvcrt.getwch()
        return ch
    except ImportError:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def input_real_time(palavra, tempo_limite=60):
    """
    Lê a digitação sem ENTER, mostra progresso, verifica erro em tempo real.
    Retorna (tentativa, tempo_total, sem_erros, tempo_estourado)
    """
    start = time.time()
    typed = ""
    sem_erros = True

    sys.stdout.write("\nDigite a palavra (sem ENTER): ")
    sys.stdout.flush()

    while True:
        if time.time() - start > tempo_limite:
            print("\n\nTempo esgotado! Você demorou mais de 60 segundos.")
            return "", round(time.time() - start, 2), False, True

        ch = getch()

        if ch in ("\r", "\n"):
            continue

        if ch in ('\x08', '\x7f'):
            if len(typed) > 0:
                typed = typed[:-1]
                sys.stdout.write('\r' + " " * (len("Digite a palavra (sem ENTER): ") + len(palavra) + 20) + '\r')
                sys.stdout.write("Digite a palavra (sem ENTER): " + typed)
                sys.stdout.flush()
            continue

        if ch == '\x03':
            raise KeyboardInterrupt

        typed += ch
        if palavra.startswith(typed):
            indicador = "" 
        else:
            indicador = "  <-- erro aqui"
            sem_erros = False

        sys.stdout.write('\r' + " " * (len("Digite a palavra (sem ENTER): ") + len(palavra) + 20) + '\r')
        sys.stdout.write("Digite a palavra (sem ENTER): " + typed + indicador)
        sys.stdout.flush()

        if typed == palavra:
            tempo_total = round(time.time() - start, 2)
            print()  
            return typed, tempo_total, sem_erros, False

        if len(typed) > len(palavra):
            sem_erros = False
