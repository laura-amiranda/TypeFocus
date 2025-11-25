import json
import os

ARQUIVO_JOGADORES = "jogadores.json"

def carregar_jogadores():
    if os.path.exists(ARQUIVO_JOGADORES):
        with open(ARQUIVO_JOGADORES, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_jogadores(jogadores):
    try:
        with open(ARQUIVO_JOGADORES, "w", encoding="utf-8") as f:
            json.dump(jogadores, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"Não foi possível salvar {ARQUIVO_JOGADORES}: {e}")

def validar_nome(nome):
    return nome.replace(" ", "").isalpha()

def validar_idade(idade):
    return idade.isdigit() and int(idade) > 0

def cadastrar_jogador():
    jogadores = carregar_jogadores()

    while True:
        nome = input("\nDigite seu nome completo: ").strip().title()
        if not nome:
            print("O nome não pode ficar vazio.")
            continue
        if not validar_nome(nome):
            print("O nome deve conter apenas letras.")
            continue
        break

    if nome in jogadores:
        print(f"\nJogador {nome} encontrado. Login realizado.")
        return jogadores[nome]
    else:
        while True:
            idade = input("Digite sua idade: ").strip()
            if not idade:
                print("A idade não pode ficar vazia.")
                continue
            if not validar_idade(idade):
                print("A idade deve conter apenas números.")
                continue
            break

        while True:
            tdah = input("Você tem TDAH? (s/n): ").strip().lower()
            if tdah not in ["s", "n"]:
                print("Digite apenas 's' para sim ou 'n' para não.")
                continue
            break

        jogadores[nome] = {
            "nome": nome,
            "idade": int(idade),
            "tdah": True if tdah == "s" else False,
            "melhor_tempo": None,
            "partidas": 0,
            "total_tempo": 0.0
        }
        salvar_jogadores(jogadores)
        print(f"\nJogador {nome} cadastrado com sucesso.")
        return jogadores[nome]

def editar_jogador():
    jogadores = carregar_jogadores()
    nome = input("\nDigite o nome completo que deseja editar: ").strip().title()

    if nome in jogadores:
        print(f"\nEditando cadastro de {nome}:")
        novo_nome = input("Novo nome completo (ou Enter para manter): ").strip().title()
        nova_idade = input("Nova idade (ou Enter para manter): ").strip()
        novo_tdah = input("Tem TDAH? (s/n ou Enter para manter): ").strip().lower()

        if novo_nome:
            if validar_nome(novo_nome):
                jogadores[novo_nome] = jogadores.pop(nome)
                nome = novo_nome
            else:
                print("Nome inválido. Alteração ignorada.")

        if nova_idade:
            if validar_idade(nova_idade):
                jogadores[nome]["idade"] = int(nova_idade)
            else:
                print("Idade inválida. Alteração ignorada.")

        if novo_tdah in ["s", "n"]:
            jogadores[nome]["tdah"] = True if novo_tdah == "s" else False

        salvar_jogadores(jogadores)
        print(f"\nCadastro de {nome} atualizado com sucesso.")
    else:
        print("\nJogador não encontrado.")

def deletar_jogador():
    jogadores = carregar_jogadores()
    nome = input("\nDigite o nome completo do jogador que deseja deletar: ").strip().title()

    if nome in jogadores:
        del jogadores[nome]
        salvar_jogadores(jogadores)
        print(f"\nCadastro de {nome} removido.")
    else:
        print("\nJogador não encontrado.")
