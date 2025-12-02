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
        if palavra.lower().startswith(typed.lower()):
            indicador = "" 
        else:
            indicador = "  <-- erro aqui"
            sem_erros = False

        sys.stdout.write('\r' + " " * (len("Digite a palavra (sem ENTER): ") + len(palavra) + 20) + '\r')
        sys.stdout.write("Digite a palavra (sem ENTER): " + typed + indicador)
        sys.stdout.flush()


        if typed.lower() == palavra.lower():
            tempo_total = round(time.time() - start, 2)
            print()  
            return typed, tempo_total, sem_erros, False
        if len(typed) > len(palavra):
            sem_erros = False
