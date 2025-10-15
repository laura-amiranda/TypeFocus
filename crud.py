import json
import os

ARQUIVO_JOGADORES = "jogadores.json"

def carregar_jogadores():
    if os.path.exists(ARQUIVO_JOGADORES):
        with open(ARQUIVO_JOGADORES, "r") as f:
            return json.load(f)
    return {}

def salvar_jogadores(jogadores):
    with open(ARQUIVO_JOGADORES, "w") as f:
        json.dump(jogadores, f, indent=4)

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
        print(f"\nSeu cadastro foi encontrado, {nome}. Login realizado.")
        return {"nome": nome, "idade": jogadores[nome]["idade"], "tdah": jogadores[nome]["tdah"]}
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

        jogadores[nome] = {"idade": idade, "tdah": "sim" if tdah == "s" else "não"}
        salvar_jogadores(jogadores)
        print(f"\nVocê foi cadastrado com sucesso, {nome}.")
        return {"nome": nome, "idade": idade, "tdah": tdah}

def editar_jogador():
    jogadores = carregar_jogadores()
    nome = input("\nDigite seu nome completo para editar: ").strip().title()

    if nome in jogadores:
        print(f"\nEditando seu cadastro, {nome}:")
        novo_nome = input("Novo nome completo (ou Enter para manter): ").strip().title()
        nova_idade = input("Nova idade (ou Enter para manter): ").strip()
        novo_tdah = input("Tem TDAH? (s/n ou Enter para manter): ").strip().lower()

        if novo_nome:
            if validar_nome(novo_nome):
                jogadores[novo_nome] = jogadores.pop(nome)
                nome = novo_nome
            else:
                print("Nome inválido, alteração ignorada.")

        if nova_idade:
            if validar_idade(nova_idade):
                jogadores[nome]["idade"] = nova_idade
            else:
                print("Idade inválida, alteração ignorada.")

        if novo_tdah in ["s", "n"]:
            jogadores[nome]["tdah"] = "sim" if novo_tdah == "s" else "não"

        salvar_jogadores(jogadores)
        print(f"\nSeu cadastro foi atualizado com sucesso, {nome}!")
    else:
        print("\nJogador não encontrado.")

def deletar_jogador():
    jogadores = carregar_jogadores()
    nome = input("\nDigite seu nome completo caso deseje deletar: ").strip().title()

    if nome in jogadores:
        del jogadores[nome]
        salvar_jogadores(jogadores)
        print(f"\nSeu cadastro foi removido, {nome}.")
    else:
        print("\nJogador não encontrado.")
