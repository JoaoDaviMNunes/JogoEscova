import random
import os
import time

# Constantes
VALORES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
           '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}
NAIPES = ['♠', '♥', '♦', '♣']
CARTAS = [f"{v}{n}" for v in VALORES.keys() for n in NAIPES]

# Funções auxiliares
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

def entrada_sim_nao(mensagem):
    while True:
        resposta = input(mensagem + " (s/n): ").strip().lower()
        if resposta in ['s', 'sim']:
            return True
        elif resposta in ['n', 'nao', 'não']:
            return False
        else:
            print("❌ Entrada inválida! Digite 's' para sim ou 'n' para não.")

def main():
    limpar()
    print("ESCOVA - Jogador vs Jogador")
    ponto_max = int(input("🎯 Pontuação máxima para vencer: "))
    jogador1 = input("👤 Nome do jogador 1: ").strip()
    jogador2 = input("👤 Nome do jogador 2: ").strip()

    placar = {jogador1: 0, jogador2: 0}
    jogador1_comeca = True
    continuar = True

    while placar[jogador1] < ponto_max and placar[jogador2] < ponto_max and continuar:
        baralho = embaralhar_cartas()
        mesa = [baralho.pop() for _ in range(4)]
        pilha1, pilha2 = [], []
        escovas1 = escovas2 = 0

        while baralho:
            mao1 = distribuir_cartas(baralho)
            mao2 = distribuir_cartas(baralho)

            for i in range(3):
                for jogador_nome, mao, pilha, escovas in (
                    ((jogador1, mao1, pilha1, escovas1), (jogador2, mao2, pilha2, escovas2))
                    if jogador1_comeca else
                    ((jogador2, mao2, pilha2, escovas2), (jogador1, mao1, pilha1, escovas1))
                ):
                    limpar()
                    input(f"\n{jogador_nome}, pressione Enter quando estiver pronto para ver sua mão...")
                    limpar()
                    print(f"📊 Placar: {jogador1}: {placar[jogador1]} ⭐ | {jogador2}: {placar[jogador2]} ⭐")
                    print(f"🃏 Cartas restantes no baralho: {len(baralho)}\n")
                    print(f"🪙 Mesa: {mostrar_cartas(mesa)}")
                    print(f"🧠 {jogador_nome}, estas são suas cartas:")
                    for idx, carta in enumerate(mao):
                        print(f"[{idx+1}] {carta}")
                    try:
                        escolha = int(input("Escolha a carta para jogar (número): ")) - 1
                        carta = mao[escolha]
                    except (ValueError, IndexError):
                        while True:
                            try:
                                escolha = int(input("Entrada inválida. Escolha um número válido: ")) - 1
                                carta = mao[escolha]
                                break
                            except (ValueError, IndexError):
                                continue

                    mao.pop(escolha)
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
                        pilha.extend(cartas_pegar + [carta])
                        print(f"🎯 {jogador_nome} capturou: {mostrar_cartas(cartas_pegar)} com {carta}")
                        if not mesa:
                            if jogador_nome == jogador1:
                                escovas1 += 1
                            else:
                                escovas2 += 1
                    else:
                        mesa.append(carta)
                        print(f"⚠️ {jogador_nome} não capturou nada com {carta}")

                    input("Pressione Enter para continuar...")

        # Último jogador leva as cartas restantes
        if jogador1_comeca:
            pilha2.extend(mesa)
        else:
            pilha1.extend(mesa)

        pontos1 = contar_pontos(pilha1)
        pontos2 = contar_pontos(pilha2)
        pontos1_total, pontos2_total = pontuacao_total(pontos1, pontos2)
        pontos1_total += escovas1
        pontos2_total += escovas2

        placar[jogador1] += pontos1_total
        placar[jogador2] += pontos2_total

        limpar()
        print("📈 Pontuação da Rodada:")
        print(f"⭐ {jogador1}: {pontos1_total} pontos")
        print(f"   - Cartas: 🃏 {pontos1['cartas']}, Ouros: ♦ {pontos1['ouros']}, 7♦: {'✅' if pontos1['7ouros'] else '❌'}, Setes: {pontos1['7s']}, Escovas: 🧹 {escovas1}")
        print(f"⭐ {jogador2}: {pontos2_total} pontos")
        print(f"   - Cartas: 🃏 {pontos2['cartas']}, Ouros: ♦ {pontos2['ouros']}, 7♦: {'✅' if pontos2['7ouros'] else '❌'}, Setes: {pontos2['7s']}, Escovas: 🧹 {escovas2}")

        print("\n🎯 Placar total:")
        print(f"{jogador1}: {placar[jogador1]} ⭐")
        print(f"{jogador2}: {placar[jogador2]} ⭐")

        continuar = entrada_sim_nao("Desejam jogar mais uma rodada?")
        jogador1_comeca = not jogador1_comeca

    limpar()
    print("\n🏁 Fim de Jogo 🏁")
    print(f"📊 Pontuação final:")
    print(f"⭐ {jogador1}: {placar[jogador1]} pontos")
    print(f"⭐ {jogador2}: {placar[jogador2]} pontos")
    if placar[jogador1] > placar[jogador2]:
        print(f"\n🏆 {jogador1} venceu a partida! Parabéns! 🎉")
    elif placar[jogador2] > placar[jogador1]:
        print(f"\n🏆 {jogador2} venceu a partida! Parabéns! 🎉")
    else:
        print("\n🤝 A partida terminou empatada! Bem jogado!")

if __name__ == "__main__":
    main()
