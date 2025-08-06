# pve_jogo.py
import random
import os
import time
import json
from itertools import combinations
from jogador import jogada_usuario
from maquina_learning import jogada_maquina

# Constantes
VALORES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}
NAIPES = ['♠', '♥', '♦', '♣']
CARTAS = [f"{v}{n}" for v in VALORES.keys() for n in NAIPES]

# Funções auxiliares
def entrada_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ['s', 'sim']: return True
        elif resposta in ['n', 'nao', 'não']: return False
        print("❌ Entrada inválida! Digite 's' para sim ou 'n' para não.")

def valor(carta):
    return VALORES[carta[:-1]]

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def embaralhar_cartas():
    baralho = CARTAS[:]
    random.shuffle(baralho)
    return baralho

def distribuir_cartas(baralho):
    return [baralho.pop() for _ in range(3)]

def mostrar_cartas(cartas):
    return ' | '.join(cartas)

def somas_possiveis(cartas_mesa, alvo):
    possiveis = []
    for i in range(1, len(cartas_mesa)+1):
        for comb in combinations(cartas_mesa, i):
            if sum(valor(c) for c in comb) == alvo:
                possiveis.append(list(comb))
    return possiveis

def contar_pontos(pilhas):
    pontos = {'cartas': len(pilhas), 'ouros': 0, '7ouros': 0, '7s': 0}
    for carta in pilhas:
        if carta[-1] == '♦':
            pontos['ouros'] += 1
            if carta == '7♦': pontos['7ouros'] = 1
        if carta[:-1] == '7': pontos['7s'] += 1
    return pontos

def pontuacao_total(p1, p2):
    pt1 = pt2 = 0
    if p1['cartas'] > p2['cartas']: pt1 += 1
    elif p2['cartas'] > p1['cartas']: pt2 += 1
    if p1['ouros'] > p2['ouros']: pt1 += 1
    elif p2['ouros'] > p1['ouros']: pt2 += 1
    if p1['7ouros']: pt1 += 1
    elif p2['7ouros']: pt2 += 1
    if p1['7s'] > p2['7s']: pt1 += 1
    elif p2['7s'] > p1['7s']: pt2 += 1
    return pt1, pt2

def verifica_final_partida(ponto_user, ponto_maq, ponto_max):
    if ponto_user == ponto_maq: return False
    elif ponto_user >= ponto_max and ponto_user > ponto_maq: return True
    elif ponto_maq >= ponto_max and ponto_maq > ponto_user: return True
    else: return False

def main():
    limpar()
    print("ESCOVA - Usuário vs Máquina")
    ponto_max = int(input("Pontuação máxima para vencer: "))

    placar = {'usuario': 0, 'maquina': 0}
    usuario_comeca = entrada_sim_nao("O usuário será o primeiro a jogar na primeira rodada? (s/n): ")
    fimjogo = verifica_final_partida(placar['usuario'], placar['maquina'], ponto_max)

    while not fimjogo:
        baralho = embaralhar_cartas()
        mesa = [baralho.pop() for _ in range(4)]
        pilha_usuario, pilha_maquina = [], []
        escovas_usuario, escovas_maquina = 0, 0

        while baralho:
            mao_usuario = distribuir_cartas(baralho)
            mao_maquina = distribuir_cartas(baralho)

            for _ in range(3):
                limpar()
                print(f"Usuário: {placar['usuario']}\tMáquina: {placar['maquina']}")
                print(f"Cartas restantes no baralho: {len(baralho)}\n")

                if usuario_comeca:
                    mao_usuario, mesa, capturadas, escova = jogada_usuario(mao_usuario, mesa)
                    pilha_usuario.extend(capturadas)
                    if escova: escovas_usuario += 1
                    time.sleep(1)

                    mao_maquina, mesa, capturadas, escova = jogada_maquina(mao_maquina, mesa)
                    pilha_maquina.extend(capturadas)
                    if escova: escovas_maquina += 1
                    time.sleep(3)
                else:
                    mao_maquina, mesa, capturadas, escova = jogada_maquina(mao_maquina, mesa)
                    pilha_maquina.extend(capturadas)
                    if escova: escovas_maquina += 1
                    time.sleep(3)

                    mao_usuario, mesa, capturadas, escova = jogada_usuario(mao_usuario, mesa)
                    pilha_usuario.extend(capturadas)
                    if escova: escovas_usuario += 1
                    time.sleep(1)

        usuario_comeca = not usuario_comeca
        pilha_maquina.extend(mesa)

        pontos_u = contar_pontos(pilha_usuario)
        pontos_m = contar_pontos(pilha_maquina)

        limpar()
        print("Pontuação da rodada:")
        print("Usuário:")
        print(f" - Total de cartas: {pontos_u['cartas']}")
        print(f" - Ouros: {pontos_u['ouros']}")
        print(f" - 7 de ouros: {'sim' if pontos_u['7ouros'] else 'não'}")
        print(f" - Total de 7s: {pontos_u['7s']}")
        print(f" - Escovas: {escovas_usuario}")

        print("\nMáquina:")
        print(f" - Total de cartas: {pontos_m['cartas']}")
        print(f" - Ouros: {pontos_m['ouros']}")
        print(f" - 7 de ouros: {'sim' if pontos_m['7ouros'] else 'não'}")
        print(f" - Total de 7s: {pontos_m['7s']}")
        print(f" - Escovas: {escovas_maquina}")

        ptu, ptm = pontuacao_total(pontos_u, pontos_m)
        ptu += escovas_usuario
        ptm += escovas_maquina

        placar['usuario'] += ptu
        placar['maquina'] += ptm

        print("\nFIM DA RODADA")
        print(f"Pontos do Usuário 🧠 nesta rodada: {ptu} (Total: {placar['usuario']})")
        print(f"Pontos da Máquina 🤖 nesta rodada: {ptm} (Total: {placar['maquina']})")
        print("\nContinuando daqui 15 segundos...")
        time.sleep(15)

        fimjogo = verifica_final_partida(placar['usuario'], placar['maquina'], ponto_max)

    limpar()
    print(f"🧠 Pontuação Final Usuário: {placar['usuario']}")
    print(f"🤖 Pontuação Final Máquina: {placar['maquina']}")
    if placar['usuario'] >= ponto_max or placar['usuario'] > placar['maquina']:
        print("\n🎉 Você venceu a partida! 🎉")
    elif placar['maquina'] >= ponto_max or placar['usuario'] < placar['maquina']:
        print("\n🤖 A máquina venceu a partida! 🤖")
    else:
        print("\n😲 Jogo terminou empatado! 😲")

if __name__ == "__main__":
    main()
