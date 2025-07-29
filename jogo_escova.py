import random
import os
import time

# Constantes
VALORES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}
NAIPES = ['♠', '♥', '♦', '♣']
CARTAS = [f"{v}{n}" for v in VALORES.keys() for n in NAIPES]

# Funções auxiliares
def entrada_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ['s', 'sim', 'Sim']:
            return 's'
        elif resposta in ['n', 'nao', 'não', 'Nao', 'Não']:
            return 'n'
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
    from itertools import combinations
    possiveis = []
    for i in range(1, len(cartas_mesa)+1):
        for comb in combinations(cartas_mesa, i):
            if sum(valor(c) for c in comb) == alvo:
                possiveis.append(list(comb))
    return possiveis

def escolher_jogada_maquina(mao, mesa):
    for carta in mao:
        jogadas = somas_possiveis(mesa, 15 - valor(carta))
        melhores_jogadas = []
        for comb in jogadas:
            prioridade = 0
            if any(c[:-1] == '7' for c in comb): prioridade += 3
            if any(c[-1] == '♦' for c in comb): prioridade += 2
            prioridade += len(comb)
            melhores_jogadas.append((prioridade, comb))
        if melhores_jogadas:
            melhores_jogadas.sort(reverse=True, key=lambda x: x[0])
            return carta, melhores_jogadas[0][1]
    return mao[0], []  # descarta carta aleatória

def contar_pontos(pilhas):
    pontos = {'cartas': len(pilhas), 'ouros': 0, '7ouros': 0, '7s': 0}
    for carta in pilhas:
        if carta[-1] == '♦':
            pontos['ouros'] += 1
            if carta == '7♦':
                pontos['7ouros'] = 1
        if carta[:-1] == '7':
            pontos['7s'] += 1
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

def main():
    # Jogo principal
    print("ESCOVA - Usuário vs Máquina")
    ponto_max = int(input("Pontuação máxima para vencer: "))

    placar = {'usuario': 0, 'maquina': 0}

    while placar['usuario'] < ponto_max and placar['maquina'] < ponto_max:
        baralho = embaralhar_cartas()
        mesa = [baralho.pop() for _ in range(4)]
        pilha_usuario, pilha_maquina = [], []
        escovas_usuario, escovas_maquina = 0, 0

        while baralho:
            mao_usuario = distribuir_cartas(baralho)
            mao_maquina = distribuir_cartas(baralho)

            for i in range(3):
                limpar()
                print(f"Cartas restantes no baralho: {len(baralho)}")
                print(f"Mesa: {mostrar_cartas(mesa)}")
                print("Suas cartas:")
                for idx, carta in enumerate(mao_usuario):
                    print(f"[{idx+1}] {carta}")

                try:
                    escolha = int(input("Escolha a carta para jogar (número): ")) - 1
                    carta = mao_usuario[escolha]
                except (ValueError, IndexError):
                    while True:
                        try:
                            escolha = int(input("Entrada inválida. Escolha um número válido: ")) - 1
                            carta = mao_usuario[escolha]
                            break
                        except (ValueError, IndexError):
                            continue

                mao_usuario.pop(escolha)
                jogadas = somas_possiveis(mesa, 15 - valor(carta))
                melhores_jogadas = []
                for comb in jogadas:
                    prioridade = 0
                    if any(c[:-1] == '7' for c in comb): prioridade += 3
                    if any(c[-1] == '♦' for c in comb): prioridade += 2
                    prioridade += len(comb)
                    melhores_jogadas.append((prioridade, comb))

                if melhores_jogadas:
                    melhores_jogadas.sort(reverse=True, key=lambda x: x[0])
                    cartas_pegar = melhores_jogadas[0][1]
                    for c in cartas_pegar:
                        mesa.remove(c)
                    pilha_usuario.extend(cartas_pegar + [carta])
                    print(f"Você capturou: {mostrar_cartas(cartas_pegar)} com {carta}")
                    if not mesa:
                        escovas_usuario += 1
                else:
                    mesa.append(carta)
                    print(f"Você não capturou nada com {carta}")

                time.sleep(2)

                # Jogada da máquina
                print("\nMáquina pensando...")
                time.sleep(1)
                carta_m, pegou = escolher_jogada_maquina(mao_maquina, mesa)
                print(f"Máquina jogou: {carta_m}")
                mao_maquina.remove(carta_m)
                if pegou:
                    for c in pegou:
                        mesa.remove(c)
                    pilha_maquina.extend(pegou + [carta_m])
                    print(f"Máquina capturou: {mostrar_cartas(pegou)} com {carta_m}")
                    if not mesa:
                        escovas_maquina += 1
                else:
                    mesa.append(carta_m)
                    print(f"Máquina não capturou nada com {carta_m}")

                time.sleep(3)

        # Sobras na mesa vão para quem jogou por último (máquina)
        pilha_maquina.extend(mesa)

        # Contar pontos
        pontos_u = contar_pontos(pilha_usuario)
        pontos_m = contar_pontos(pilha_maquina)

        print("\nPontuação da rodada:")
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

        # Mostrar placar
        print("\nFIM DA RODADA")
        print(f"Pontos do Usuário nesta rodada: {ptu} (Total: {placar['usuario']})")
        print(f"Pontos da Máquina nesta rodada: {ptm} (Total: {placar['maquina']})")
        inp = entrada_sim_nao("\nContinuar para a próxima rodada? (s/n): ")
        if inp == 'n':
            break

    limpar()
    print(f"Total: {placar['usuario']}")
    print(f"Total: {placar['maquina']}")
    if placar['usuario'] >= ponto_max:
        print("🎉 Você venceu a partida!")
    else:
        print("🤖 A máquina venceu a partida!")

if __name__ == "__main__":
    main()