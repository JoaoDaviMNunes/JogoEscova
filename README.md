# 🃏 Escova - Usuário vs Máquina

## 1. 🎮 Nome do Jogo

**Escova**  
Um jogo de cartas clássico no terminal: você contra a máquina!  
Baseado na tradicional "Scopa" italiana, com adaptações 🇧🇷✨

## 2. 🌍 Origem

"Escova" é uma variação brasileira da tradicional **Scopa**, um jogo de cartas italiano.  
Neste jogo, o objetivo é **capturar cartas da mesa somando exatamente 15 pontos**, com estratégias para capturar as cartas mais valiosas.  
O jogo apresentado aqui substitui as cartas de figuras (Valete, Dama e Rei) por números: **8, 9 e 10**, deixando o jogo acessível para qualquer baralho numérico.

## 3. 📋 Instruções do Jogo

### 👤 Jogadores
- 1 jogador humano (você)
- 1 oponente controlado pela máquina 🤖

### 🃏 Baralho
- Cartas de **A (1) até 10**, com os **4 naipes tradicionais**: ♠ ♥ ♦ ♣
- Total: **40 cartas**

### 🎯 Objetivo
Capturar cartas da mesa somando **exatamente 15 pontos** com uma carta da sua mão + combinações da mesa.

### 🔁 Fluxo de Jogo
1. O jogo começa perguntando a **pontuação máxima** que define o vencedor.
2. 4 cartas são colocadas na mesa.
3. A cada rodada, os dois jogadores recebem 3 cartas.
4. A jogada segue alternadamente:
   - O jogador escolhe qual carta jogar.
   - Se for possível fazer 15 com cartas da mesa, as cartas são **capturadas**.
   - Se todas as cartas forem removidas da mesa, é feita uma **escova** (vale ponto extra!).
5. Após o jogador, é a vez da máquina, que joga com base em estratégia:
   - **Prioridade para capturar 7s**, depois **ouros**, depois **mais cartas**.
6. Após acabar o baralho, os pontos da rodada são calculados.

### 🧠 Estratégia da Máquina
A máquina sempre tenta:
1. Combinações com cartas 7.
2. Combinações com cartas do naipe de ouros ♦.
3. Combinação com o **maior número de cartas possíveis**.

### 🕹️ Seleção das Cartas
- O jogador escolhe a carta pelo **índice numérico** (ex: `[1] 3♣`)
- O programa mostra as cartas disponíveis e aguarda a jogada.

## 4. 🧾 Pontuações

Ao final de cada rodada, os seguintes pontos são avaliados:

| Critério             | Pontuação | Observação                                                    |
|----------------------|-----------|----------------------------------------------------------------|
| 🃙 Maior número de cartas | +1        | Total de 40 cartas no jogo. Em caso de empate, **sem ponto**. |
| ♦ Maior número de ouros   | +1        | Total de 10 cartas ♦. Em caso de empate, **sem ponto**.        |
| 7️⃣ Quem pegou o 7♦        | +1        | Apenas **uma carta no jogo**.                                 |
| 7️⃣ Maior número de 7s     | +1        | Total de **4 cartas 7** no jogo. Em caso de empate, **sem ponto**. |
| 🧹 Cada escova          | +1        | Feita ao limpar a mesa com uma jogada.                        |

## 5. 🚀 Como Executar o Jogo

### Pré-requisitos
- Python 3.6 ou superior instalado
- Terminal (CMD, Bash, ou Terminal do VS Code)

### Passos para Jogar contra a Máquina
```
git clone https://github.com/JoaoDaviMNunes/JogoEscova.git
cd JogoEscova
python3 pve_jogo.py
```

### Passos para PVP Local
```
git clone https://github.com/JoaoDaviMNunes/JogoEscova.git
cd JogoEscova
python3 pvp_jogo.py
```

## 6. 👨‍💻 Desenvolvedor

João Nunes

https://github.com/JoaoDaviMNunes

---

Feito com ❤️ para os fãs de jogos clássicos de carta!
