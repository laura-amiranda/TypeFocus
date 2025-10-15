PALAVRAS_POR_NIVEL = {
    "facil": [
        "foco",
        "jogo",
        "tecla",
        "mão",
        "dedo",
        "letra",
        "linha",
        "texto",
        "ler",
        "ver",
    ],
    "medio": [
        "python",
        "terminal",
        "digitar",
        "teclado",
        "programa",
        "reflexo",
        "código",
        "desafio",
        "diversão",
        "prática",
    ],
    "dificil": [
        "velocidade",
        "atenção",
        "habilidade",
        "concentração",
        "memória",
        "aprendizado",
        "desempenho",
        "competição",
        "extraordinário",
        "desenvolvimento",
    ],
}

# Lista padrão com progressão gradativa
LISTA_PALAVRAS_PADRAO = (
    PALAVRAS_POR_NIVEL["facil"][:3] +
    PALAVRAS_POR_NIVEL["medio"][:5] +
    PALAVRAS_POR_NIVEL["facil"][3:5] +
    PALAVRAS_POR_NIVEL["medio"][5:] +
    PALAVRAS_POR_NIVEL["dificil"][:4] +
    PALAVRAS_POR_NIVEL["medio"][5:] +
    PALAVRAS_POR_NIVEL["dificil"][4:]
)
