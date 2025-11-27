import time
import random
import os
import json
from datetime import datetime
from colorama import Fore, Style, init

from palavras import PALAVRAS_POR_NIVEL, LISTA_PALAVRAS_PADRAO, PALAVRAS_INGLES, PALABRAS_ESPANOL
from utils import contagem_regressiva, calcular_pontos, input_real_time

init(autoreset=True)

RANKING_ARQUIVO = "ranking.json"     
HISTORICO_ARQUIVO = "historico.json"

ranking_sessao = []

def carregar_json_arquivo(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return default
        return default
    except OSError:
        return default

def salvar_json_arquivo(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"Não foi possível salvar {path}: {e}")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_mascote_inicial(idioma='pt'):
    if idioma == 'en':
        prompt = "Press ENTER to start:"
        titulo = "Ready?"
    elif idioma == 'es':
        prompt = "Presiona ENTER para comenzar:"
        titulo = "¿Listo?"
    else:
        prompt = "Pressione ENTER para começar:"
        titulo = "Está preparado?"
    print(f"""
{Fore.WHITE}                    ╭──────────────────────╮
                    │  {titulo:<18}│
                    ╰────╮{Style.RESET_ALL}
{Fore.MAGENTA}        ╔═════╗   ╰───○{Style.RESET_ALL}
{Fore.MAGENTA}        ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
    """)

def exibir_mascote_pronto(idioma='pt'):
    if idioma == 'en':
        prompt = "Press ENTER to start:"
    elif idioma == 'es':
        prompt = "Presiona ENTER para comenzar:"
    else:
        prompt = "Pressione ENTER para começar:"

    if idioma == 'en':
        titulo = 'Ready?'
    elif idioma == 'es':
        titulo = '¿Listo?'
    else:
        titulo = 'Está preparado?'
    print(f"""
{Fore.WHITE}                    ╭──────────────────────╮
                    │  {titulo:<18}│
                    ╰────╮{Style.RESET_ALL}
{Fore.MAGENTA}        ╔═════╗   ╰───○{Style.RESET_ALL}
{Fore.MAGENTA}        ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}        ╚══╦══╝{Style.RESET_ALL}
    """)
    input(f"{Fore.WHITE}{prompt}{Style.RESET_ALL}")
    print()

def exibir_mascote_resultado(acertou, tempo=0, idioma='pt'):
    if idioma == 'en':
        if acertou:
            if tempo < 3:
                mensagem = "Amazing! You're fast!"
            elif tempo < 5:
                mensagem = "Nice! Keep going!"
            else:
                mensagem = "Good job! Keep practicing!"
        else:
            mensagem = "Too bad! Try again!"
    elif idioma == 'es':
        if acertou:
            if tempo < 3:
                mensagem = "¡Increíble! ¡Eres rápido!"
            elif tempo < 5:
                mensagem = "¡Muy bien! ¡Sigue así!"
            else:
                mensagem = "¡Buen trabajo! ¡Practica más!"
        else:
            mensagem = "¡Qué pena! ¡Intenta de nuevo!"
    else:
        if acertou:
            if tempo < 3:
                mensagem = "Incrível! Você é rápido!"
            elif tempo < 5:
                mensagem = "Muito bem! Continue assim!"
            else:
                mensagem = "Bom trabalho! Pratique mais!"
        else:
            mensagem = "Que pena! Tente novamente!"

    print(f"""
{Fore.WHITE}              ╭────────────────────────╮
              │ {mensagem:<26}│
              ╰──╮{Style.RESET_ALL}
{Fore.MAGENTA}    ╔═════╗  ╰─○{Style.RESET_ALL}
{Fore.MAGENTA}    ║ ◉ ◉ ║{Style.RESET_ALL}
{Fore.MAGENTA}    ╚══╦══╝{Style.RESET_ALL}
    """)
    time.sleep(1.2)

def escolher_idioma():
    while True:
        escolha = input("\nDeseja jogar em (P)ortuguês, (I)nglês ou (E)spanhol? ").strip().lower()
        if escolha in ['p', 'pt', 'port', 'portugues']:
            return 'pt'
        elif escolha in ['i', 'en', 'ingles', 'english']:
            return 'en'
        elif escolha in ['e', 'es', 'espanol', 'spanish', 'español']:
            return 'es'
        else:
            print("Opção inválida. Digite P para Português, I para Inglês ou E para Espanhol.")

def escolher_dificuldade():
    print(f"\n{Fore.WHITE}Escolha o nível de dificuldade:")
    print("1 - Fácil ")
    print("2 - Médio ")
    print("3 - Difícil ")
    print("4 - Padrão ")

    while True:
        escolha = input("\nEscolha uma opção (1-4): ").strip()
        if escolha == "1":
            return "facil"
        elif escolha == "2":
            return "medio"
        elif escolha == "3":
            return "dificil"
        elif escolha == "4":
            return "padrao"
        else:
            print(f"{Fore.RED}Opção inválida! Digite um número de 1 a 4.")

def registrar_historico(registro):
    historico = carregar_json_arquivo(HISTORICO_ARQUIVO, [])
    historico.append(registro)
    salvar_json_arquivo(HISTORICO_ARQUIVO, historico)

def atualizar_estatisticas_jogador(nome, tempo):

    from crud import carregar_jogadores, salvar_jogadores
    jogadores = carregar_jogadores()
    if nome in jogadores:
        p = jogadores[nome]
        p['partidas'] = p.get('partidas', 0) + 1
        p['total_tempo'] = p.get('total_tempo', 0.0) + tempo
        if (p.get('melhor_tempo') is None) or (tempo < p.get('melhor_tempo')):
            p['melhor_tempo'] = tempo
            bateu_recorde = True
        else:
            bateu_recorde = False
        jogadores[nome] = p
        salvar_jogadores(jogadores)
        return bateu_recorde, p
    return False, None

def mostrar_ranking_sessao():
    global ranking_sessao
    print("\nRanking da sessão:")
    if not ranking_sessao:
        print("Ainda não há resultados na sessão.")
        return
    sorted_r = sorted(ranking_sessao, key=lambda x: x['pontos'], reverse=True)
    for i, item in enumerate(sorted_r[:10], start=1):
        print(f"{i}. {item['nome']} — {item['pontos']} pts (palavra: {item.get('palavra','-')})")

def mostrar_ranking_historico():
    historico = carregar_json_arquivo(HISTORICO_ARQUIVO, [])
    if not historico:
        print("\nAinda não há histórico salvo.")
        return

    melhor_por_jogador = {}
    for r in historico:
        n = r.get('nome')
        pontos = r.get('pontos', 0)
        if n not in melhor_por_jogador or pontos > melhor_por_jogador[n]:
            melhor_por_jogador[n] = pontos
    sorted_melhor = sorted(melhor_por_jogador.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking histórico (melhor resultado por jogador):")
    for i, (nome, pts) in enumerate(sorted_melhor[:10], start=1):
        print(f"{i}. {nome} — {pts} pts")

def pedir_feedback(idioma='pt'):
    if idioma == 'en':
        prompt = "Leave a short feedback about the game (or press Enter to skip): "
    elif idioma == 'es':
        prompt = "Deja un comentario corto sobre el juego (o presiona Enter para omitir): "
    else:
        prompt = "Deixe um comentário sobre o jogo (ou pressione Enter para pular): "
    fb = input(prompt).strip()
    return fb

def jogar(nome):
    limpar_tela()
    idioma = escolher_idioma()
    exibir_mascote_inicial(idioma)
    nivel = escolher_dificuldade()

    if idioma == 'en':
        if nivel == 'padrao':
            palavras_disponiveis = []
            for l in PALAVRAS_INGLES.values():
                palavras_disponiveis.extend(l)
        else:
            palavras_disponiveis = PALAVRAS_INGLES[nivel].copy()
    elif idioma == 'es':
        if nivel == 'padrao':
            palavras_disponiveis = []
            for l in PALABRAS_ESPANOL.values():
                palavras_disponiveis.extend(l)
        else:
            palavras_disponiveis = PALABRAS_ESPANOL[nivel].copy()
    else:
        if nivel == 'padrao':
            palavras_disponiveis = LISTA_PALAVRAS_PADRAO.copy()
        else:
            palavras_disponiveis = PALAVRAS_POR_NIVEL[nivel].copy()

    if nivel == "padrao":
        if idioma == 'en':
            print(f"\n{Fore.MAGENTA}Standard mode selected - difficulty will increase!")
        elif idioma == 'es':
            print(f"\n{Fore.MAGENTA}Modo estándar seleccionado - ¡la dificultad aumentará!")
        else:
            print(f"\n{Fore.MAGENTA}Modo Padrão selecionado - a dificuldade aumenta gradativamente!")
    else:
        print(f"\n{Fore.MAGENTA}Nível {nivel.upper()} selecionado!")

    time.sleep(1.0)
    limpar_tela()
    exibir_mascote_pronto(idioma)

    palavras_usadas = set()
    jogar_novamente = "s"
    streak = 0 

    pontos = 0
    tempo_total = 0

    while jogar_novamente.lower() == "s":
        if len(palavras_disponiveis) == 0:
            if idioma == 'en':
                print("\nNo more words available.")
            elif idioma == 'es':
                print("\nNo hay más palabras disponibles.")
            else:
                print("\nNão há mais palavras disponíveis para jogar.")
            break

        limpar_tela()
        palavra = random.choice(palavras_disponiveis)
        palavras_disponiveis.remove(palavra)
        palavras_usadas.add(palavra)

        if idioma == 'en':
            print(f"\nThe word is: {Fore.RED}{palavra}{Style.RESET_ALL}\n")
        elif idioma == 'es':
            print(f"\nLa palabra es: {Fore.RED}{palavra}{Style.RESET_ALL}\n")
        else:
            print(f"\nA palavra é: {Fore.RED}{palavra}{Style.RESET_ALL}\n")

        contagem_regressiva()

        tentativa, tempo_total, sem_erros, tempo_estourado = input_real_time(palavra, tempo_limite=60)

        if tempo_estourado:
            pontos = 0
            acertou = False
            streak = 0
        elif tentativa == palavra:
            streak += 1
            bateu_recorde, jogador_info = atualizar_estatisticas_jogador(nome, tempo_total)
            pontos = calcular_pontos(tempo_total, sem_erros=sem_erros, streak=streak, bateu_recorde=bateu_recorde)
            acertou = True
        else:
            pontos = 0
            acertou = False
            streak = 0

        feedback = pedir_feedback(idioma)

        registro = {
            "nome": nome,
            "idioma": "ingles" if idioma == 'en' else ("espanhol" if idioma == 'es' else "portugues"),
            "nivel": nivel,
            "palavra": palavra,
            "tempo": tempo_total,
            "pontos": pontos,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "streak": streak,
            "feedback": feedback
        }
        registrar_historico(registro)

        global ranking_sessao
        ranking_sessao.append({"nome": nome, "pontos": pontos, "palavra": palavra, "tempo": tempo_total})

        limpar_tela()
        if acertou:
            if idioma == 'en':
                print(f"\nTime: {tempo_total}s | Points: {pontos} | Combo: {streak}")
            elif idioma == 'es':
                print(f"\nTiempo: {tempo_total}s | Puntos: {pontos} | Combo: {streak}")
            else:
                print(f"\nTempo: {tempo_total}s | Pontos: {pontos} | Combo atual: {streak}")
            exibir_mascote_resultado(True, tempo_total, idioma)
        else:
            if idioma == 'en':
                print(f"\nRound ended without success. Points: {pontos}")
            elif idioma == 'es':
                print(f"\nRonda finalizada sin acierto. Puntos: {pontos}")
            else:
                print(f"\nRodada encerrada sem acerto. Pontos: {pontos}")
            exibir_mascote_resultado(False, tempo_total, idioma)
            streak = 0

        session_scores = [r['pontos'] for r in ranking_sessao if r['nome'] == nome]
        if session_scores:
            melhor = max(session_scores)
            media = round(sum(session_scores)/len(session_scores), 2)
            if idioma == 'en':
                print(f"\nSession stats — Best: {melhor} pts | Average: {media} pts | Games: {len(session_scores)}")
            elif idioma == 'es':
                print(f"\nEstadísticas de la sesión — Mejor: {melhor} pts | Promedio: {media} pts | Partidas: {len(session_scores)}")
            else:
                print(f"\nEstatísticas da sessão — Melhor: {melhor} pts | Média: {media} pts | Partidas: {len(session_scores)}")

        if acertou:
            if tempo_total < 2:
                msg = {"pt": "Reflexo incrível! Continue assim!", "en": "Lightning reflex! Keep it up!", "es": "¡Reflejo increíble! ¡Sigue así!"}
            elif tempo_total < 4:
                msg = {"pt": "Mandou bem, continue!", "en": "Nice! Keep going!", "es": "¡Buen trabajo! ¡Sigue así!"}
            elif tempo_total < 6:
                msg = {"pt": "Tá indo bem, mas pode ser mais rápido.", "en": "You're doing well, but you can be faster.", "es": "Vas bien, pero puedes ser más rápido."}
            else:
                msg = {"pt": "Concentre-se mais na próxima!", "en": "Focus more next time!", "es": "¡Concéntrate más la próxima vez!"}
            print(msg.get(idioma, msg['pt']))
        else:
            msg_fail = {"pt": "Não desanime — tente novamente!", "en": "Don't give up — try again!", "es": "¡No te rindas — inténtalo de nuevo!"}
            print(msg_fail.get(idioma, msg_fail['pt']))

        while True:
            prompt = {"pt": "\nDeseja jogar novamente? (s/n): ", "en": "\nPlay again? (y/n): ", "es": "\n¿Jugar de nuevo? (s/n): "}
            resp = input(prompt.get(idioma,'\nDeseja jogar novamente? (s/n): ')).strip().lower()
            if idioma == 'en':
                if resp in ['y','n']:
                    jogar_novamente = 's' if resp == 'y' else 'n'
                    break
                else:
                    print("Digite 'y' ou 'n'.")
            else:
                if resp in ['s','n']:
                    jogar_novamente = resp
                    break
                else:
                    print("Digite apenas 's' ou 'n'.")

        if jogar_novamente == "s":
            change_lang_prompts = {
                'pt': "Deseja trocar de idioma? (s/n): ",
                'en': "Change language? (y/n): ",
                'es': "¿Cambiar idioma? (s/n): "
            }
            resp_lang = input(change_lang_prompts.get(idioma, change_lang_prompts['pt'])).strip().lower()
            wants_change_lang = (resp_lang == 'y') if idioma == 'en' else (resp_lang == 's')
            if wants_change_lang:
                limpar_tela()

                menu = {
                    'pt': {'title': '\nP) Português  I) Inglês  E) Espanhol', 'prompt': 'Digite P, I ou E: '},
                    'en': {'title': '\nP) Português  I) English  E) Español', 'prompt': 'Type P, I or E: '},
                    'es': {'title': '\nP) Português  I) English  E) Español', 'prompt': 'Teclea P, I o E: '}
                }
                m = menu.get(idioma, menu['pt'])
                while True:
                    print(m['title'])
                    escolha = input(m['prompt']).strip().lower()
                    if escolha in ['p','pt','port','portugues']:
                        novo_idioma = 'pt'
                        break
                    if escolha in ['i','en','ingles','english']:
                        novo_idioma = 'en'
                        break
                    if escolha in ['e','es','espanol','spanish','español']:
                        novo_idioma = 'es'
                        break
                    if idioma == 'en':
                        print('Invalid option. Type P, I or E.')
                    else:
                        print('Opção inválida. Digite P, I ou E.')
                idioma = novo_idioma
                exibir_mascote_inicial(idioma)

                if idioma == 'en':
                    if nivel == 'padrao':
                        palavras_disponiveis = []
                        for valores in PALAVRAS_INGLES.values():
                            palavras_disponiveis.extend(valores)
                    else:
                        palavras_disponiveis = PALAVRAS_INGLES.get(nivel, []).copy()
                elif idioma == 'es':
                    if nivel == 'padrao':
                        palavras_disponiveis = []
                        for valores in PALABRAS_ESPANOL.values():
                            palavras_disponiveis.extend(valores)
                    else:
                        palavras_disponiveis = PALABRAS_ESPANOL.get(nivel, []).copy()
                else:
                    if nivel == 'padrao':
                        palavras_disponiveis = LISTA_PALAVRAS_PADRAO.copy()
                    else:
                        palavras_disponiveis = PALAVRAS_POR_NIVEL.get(nivel, []).copy()
                palavras_usadas = set()

            trocar = input("Deseja trocar de dificuldade? (s/n): ").strip().lower()
            if trocar == "s":
                limpar_tela()
                exibir_mascote_inicial(idioma)
                nivel = escolher_dificuldade()
                if idioma == 'en':
                    if nivel == 'padrao':
                        palavras_disponiveis = []
                        for l in PALAVRAS_INGLES.values():
                            palavras_disponiveis.extend(l)
                    else:
                        palavras_disponiveis = PALAVRAS_INGLES[nivel].copy()
                elif idioma == 'es':
                    if nivel == 'padrao':
                        palavras_disponiveis = []
                        for l in PALABRAS_ESPANOL.values():
                            palavras_disponiveis.extend(l)
                    else:
                        palavras_disponiveis = PALABRAS_ESPANOL[nivel].copy()
                else:
                    if nivel == 'padrao':
                        palavras_disponiveis = LISTA_PALAVRAS_PADRAO.copy()
                    else:
                        palavras_disponiveis = PALAVRAS_POR_NIVEL[nivel].copy()
                palavras_usadas = set()
                print(f"\n{Fore.MAGENTA}Dificuldade alterada para {nivel.upper()}!")
                time.sleep(1.5)

    limpar_tela()
    exibir_mascote_resultado(True if pontos>0 else False, tempo_total, idioma)
    if idioma == 'en':
        print(f"\nGood bye, {nome}!")
    elif idioma == 'es':
        print(f"\n¡Adiós, {nome}!")
    else:
        print(f"\nAté logo, {nome}!")
    time.sleep(1.0)
