# TypeFocus
![image](https://github.com/user-attachments/assets/aa96f5fe-3276-4e8c-9248-b69c44e0424e)

## Projeto Typefocus - PISI1
**Jogo de reflexo para auxiliar pessoas com TDAH**

### Nossa proposta
O projeto TypeFocus busca auxiliar pessoas com TDAH e dificuldades de concentração a treinarem foco, velocidade de digitação e atenção. 
A ideia é usar um joguinho simples no terminal, que apresenta palavras para o jogador digitar com a maior rapidez e acertividade possível. 
Para além disso, a inclusão de grupos minoritários nos canais digitais é um dos pilares que sustentam a idealização desse projeto.

### Área de aplicação
1. Finalidade: reduzir as dificuldades de foco e atenção em pessoas com TDAH.
2. Solução -> jogo simples no terminal que treina:
- Atenção sustentada;
- Tempo de reação;
- Motivação com feedback imediato.

## Como jogar?

1. Abra o terminal e execute o arquivo principal com:
2. Digite seu nome, sobrenome, idade e se tem TDAH ou não.
3. Quando o TypeBot aparecer, escolha o nível de dificuldade:
- Fácil: palavras curtas, ótimo para começar.
- Médio: palavras médias, ritmo equilibrado.
- Difícil: palavras longas, exige mais foco.
- Padrão: a dificuldade aumenta gradualmente conforme o jogador acerta.
4. O jogo mostra uma palavra e inicia uma contagem regressiva de 3, 2, 1 antes de liberar a digitação.
5. Digite a palavra exatamente igual.
- Se errar, o jogo pede para tentar novamente.
- Se o tempo ultrapassar 60 segundos, a rodada é encerrada automaticamente.
6. Quando acerta, o jogo mostra o tempo e a pontuação com base no seu desempenho.
7. No final, você pode escolher entre:
- Jogar novamente;
- Trocar de dificuldade;
- Encerrar o jogo.
8. O mascote TypeBot se despede com uma mensagem personalizada, encerrando a sessão.

## Releases

### Requisitos para Primeira
- RF001 – Menu inicial com botão "Jogar"
- RF002 – Escolher palavra aleatória
- RF003 – Contagem regressiva (3,2,1)
- RF004 – Entrada do jogador + timer
- RF005 – Exibir tempo + pontuação
- RF006 – Opção de jogar novamente ou sair
- RF007 – Cadastrar nome do jogador
- RF008 – Escolha de nível de dificuldade
- RF009 – Mascote


### Requisitos para Segunda
- RF010 – Escolha o idioma
- RF011 – Sistema de streaks (combos)
- RF012 – Ranking comparativo
- RF013 – Estatísticas + mensagens motivacionais
- RF014 – Feedback em tempo real (sem ENTER)
- RF015 - Histórico dos jogadores

## Linguagem

**Python 3.12**

### Bibliotecas
- **time** → controle do tempo de digitação e da contagem regressiva.
- **random** → sorteio aleatório das palavras.
- **json** → salvar e carregar os dados dos jogadores.
- **os** → verificação da existência do arquivo `jogadores.json`.

### Estruturas
- **Estruturas de decisão:** `if`, `elif`, `else` – usadas para validações de dados e fluxos de erro.
- **Estruturas de repetição:** `while` – mantém o menu e o jogo rodando até o jogador encerrar.
- **Listas:** armazenam as palavras disponíveis no jogo.
- **Dicionários:** armazenam informações de cada jogador (nome, idade, TDAH).
- **Funções:** utilizadas em todo o projeto para modularizar o código e facilitar a manutenção.
