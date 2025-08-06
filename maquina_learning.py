import json
import time
import os
import random
import matplotlib.pyplot as plt
from pve_jogo import mostrar_cartas, somas_possiveis, valor

Q_FILE = "qtable_scopa.json"

# Carregar ou criar a Q-table
def load_qtable():
    if os.path.exists(Q_FILE):
        with open(Q_FILE, "r") as f:
            return json.load(f)
    return {}

def save_qtable(qtable):
    with open(Q_FILE, "w") as f:
        json.dump(qtable, f)

Q_TABLE = load_qtable()

def state_key(mao, mesa):
    return f"{sorted(mao)}|{sorted(mesa)}"

def possiveis_jogadas(mao, mesa):
    jogadas = []
    for carta in mao:
        capturas = somas_possiveis(mesa, 15 - valor(carta))
        if capturas:
            for comb in capturas:
                jogadas.append((carta, comb))
        else:
            jogadas.append((carta, []))
    return jogadas

def melhor_jogada(chave, jogadas):
    if chave not in Q_TABLE:
        Q_TABLE[chave] = {str([j[0]] + j[1]): 0 for j in jogadas}
    if random.random() < 0.3:  # Exploração
        return random.choice(jogadas)
    return max(jogadas, key=lambda j: Q_TABLE[chave].get(str([j[0]] + j[1]), 0))

def atualizar_qtable(chave, jogada, recompensa):
    jogada_str = str([jogada[0]] + jogada[1])
    valor_antigo = Q_TABLE[chave].get(jogada_str, 0)
    Q_TABLE[chave][jogada_str] = valor_antigo + 0.1 * (recompensa - valor_antigo)

def calcular_recompensa(carta, capturas, mesa_antes, mesa_depois):
    recompensa = 0

    # Recompensa por capturar cartas boas
    if capturas:
        if any(c[:-1] == '7' for c in capturas):
            recompensa += 3
        if any(c[-1] == '♦' for c in capturas):
            recompensa += 2
        recompensa += len(capturas) * 0.5

    # Escova (zerar mesa)
    if not mesa_depois and capturas:
        recompensa += 2

    # Penalidade se deixar mesa fácil para o oponente
    if len(mesa_depois) == 1 and valor(mesa_depois[0]) <= 3:
        recompensa -= 1

    return recompensa

def explicar_jogada_maquina(carta, capturas, mesa_antes, mesa_depois):
    print("\n🤖 Explicação da jogada da máquina:")

    if capturas:
        motivos = []

        if any(c[:-1] == '7' for c in capturas):
            motivos.append("capturar um 7, que vale ponto")

        if any(c[-1] == '♦' for c in capturas):
            motivos.append("capturar um ouros (♦), que é importante")

        if '7♦' in capturas:
            motivos.append("capturar o 7 de ouros (7♦), que vale ponto exclusivo")

        if not mesa_depois:
            motivos.append("fazer uma escova (zerar a mesa), que dá ponto direto")

        if len(capturas) >= 3:
            motivos.append("capturar várias cartas de uma vez, aumentando sua pilha")

        if motivos:
            print(f"- A máquina usou {carta} para capturar {mostrar_cartas(capturas)} porque quis:")
            for m in motivos:
                print(f"  • {m}")
        else:
            print(f"- A máquina usou {carta} para capturar {mostrar_cartas(capturas)} por estratégia geral.")
    else:
        print(f"- A máquina descartou {carta} porque não havia combinação válida.")
        if len(mesa_depois) == 1 and valor(mesa_depois[0]) <= 3:
            print("  • Tentou deixar uma carta difícil para o jogador capturar.")
        else:
            print("  • Foi uma jogada neutra para minimizar perdas.")

def jogada_maquina(mao_maquina, mesa):
    print(f"\n----------------\n\nMesa: {mostrar_cartas(mesa)}")
    print("Máquina pensando...")
    time.sleep(1)

    chave = state_key(mao_maquina, mesa)
    jogadas = possiveis_jogadas(mao_maquina, mesa)
    jogada = melhor_jogada(chave, jogadas)
    carta, capturas = jogada

    mesa_antes = mesa[:]
    mao_maquina.remove(carta)

    if capturas:
        for c in capturas:
            mesa.remove(c)
        mesa_vazia = not mesa
        print(f"Máquina capturou: {mostrar_cartas(capturas)} com {carta}")
        explicar_jogada_maquina(carta, capturas, mesa_antes, mesa)
        recompensa = calcular_recompensa(carta, capturas, mesa_antes, mesa)
        atualizar_qtable(chave, jogada, recompensa)
        save_qtable(Q_TABLE)
        return mao_maquina, mesa, [carta] + capturas, mesa_vazia
    else:
        mesa.append(carta)
        print(f"Máquina não capturou nada com {carta}")
        explicar_jogada_maquina(carta, capturas, mesa_antes, mesa)
        recompensa = calcular_recompensa(carta, [], mesa_antes, mesa)
        atualizar_qtable(chave, jogada, recompensa)
        save_qtable(Q_TABLE)
        return mao_maquina, mesa, [], False

# =====================================================================================

def plotar_grafico_conhecimento(qtable_path='qtable_scopa.json'):
    if not os.path.exists(qtable_path):
        print("❌ Arquivo de Q-table não encontrado!")
        return

    with open(qtable_path, 'r') as f:
        qtable = json.load(f)

    estados = list(qtable.keys())
    num_estados = len(estados)
    medias_q = []
    maximos_q = []
    minimos_q = []
    variancias_q = []

    for estado in estados:
        valores = list(qtable[estado].values())
        if not valores:
            medias_q.append(0)
            maximos_q.append(0)
            minimos_q.append(0)
            variancias_q.append(0)
        else:
            medias_q.append(sum(valores) / len(valores))
            maximos_q.append(max(valores))
            minimos_q.append(min(valores))
            variancias_q.append(sum((x - medias_q[-1])**2 for x in valores) / len(valores))

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("📊 Análise do Conhecimento da IA (Q-table)", fontsize=16)

    # 📈 Gráfico 1: Valor médio dos Q-values por estado
    axs[0, 0].plot(range(num_estados), medias_q, color='blue')
    axs[0, 0].set_title("Média dos Q-values por Estado")
    axs[0, 0].set_xlabel("Estado")
    axs[0, 0].set_ylabel("Média")
    axs[0, 0].grid(True, linestyle='--', alpha=0.5)

    # 🔺 Gráfico 2: Máximo vs Mínimo Q-value por estado
    axs[0, 1].plot(range(num_estados), maximos_q, label='Máximo', color='green')
    axs[0, 1].plot(range(num_estados), minimos_q, label='Mínimo', color='red')
    axs[0, 1].set_title("Máximo e Mínimo Q-value por Estado")
    axs[0, 1].legend()
    axs[0, 1].set_xlabel("Estado")
    axs[0, 1].set_ylabel("Q-value")
    axs[0, 1].grid(True, linestyle='--', alpha=0.5)

    # 🎲 Gráfico 3: Variância dos Q-values por estado
    axs[1, 0].plot(range(num_estados), variancias_q, color='orange')
    axs[1, 0].set_title("Variância dos Q-values por Estado")
    axs[1, 0].set_xlabel("Estado")
    axs[1, 0].set_ylabel("Variância")
    axs[1, 0].grid(True, linestyle='--', alpha=0.5)

    # 🧠 Gráfico 4: Densidade dos Q-values (Histograma)
    todos_q_values = [v for d in qtable.values() for v in d.values()]
    axs[1, 1].hist(todos_q_values, bins=30, color='purple', alpha=0.7)
    axs[1, 1].set_title("Distribuição dos Q-values (Histograma)")
    axs[1, 1].set_xlabel("Valor do Q-value")
    axs[1, 1].set_ylabel("Frequência")
    axs[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# gráficos do conhecimento adquirido pela máquina
plotar_grafico_conhecimento()