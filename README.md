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

### Primeira Versão
1. O sistema escolhe uma palavra aleatória de uma lista.
2. A palavra é exibida na tela e inicia uma contagem regressiva de 3, 2, 1.
3. Após a contagem, o campo de digitação é liberado e o cronômetro começa.
4. O jogador digita a palavra e confirma com ENTER -> só é aceito se a palavra estiver correta.
5. O jogo exibe o tempo final e a pontuação baseada no desempenho.
6. O jogador pode escolher entre jogar novamente ou sair.

### Segunda Versão
1. O jogador insere seu nome e escolhe o modo (padrão, fácil, médio ou difícil).
2. O sistema sorteia uma palavra de acordo com o modo escolhido.
3. A palavra é exibida na tela e inicia uma contagem regressiva de 3, 2, 1.
4. Após a contagem, o campo de digitação é liberado e o cronômetro começa.
5. O jogador digita -> o jogo verifica em tempo real se a palavra está correta (sem ENTER).
6. Ao acertar a palavra, o cronômetro para automaticamente.
7. O sistema calcula e exibe:
- Tempo da partida;
- Pontuação (com bônus de streaks em acertos consecutivos);
- Melhor tempo do jogador;
- Média de desempenho;
- Total de partidas jogadas;
- Ranking comparativo com resultados anteriores.
7. São exibidas mensagens motivacionais para incentivar o jogador.
8. O jogador pode escolher entre jogar novamente ou encerrar.

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
- RF0115 - Histórico dos jogadores

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