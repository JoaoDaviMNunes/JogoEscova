import time
from pve_jogo import valor, mostrar_cartas, somas_possiveis

def jogada_usuario(mao_usuario, mesa):
    print(f"\n----------------\n\nMesa: {mostrar_cartas(mesa)}")
    print("Suas cartas:")
    for idx, carta in enumerate(mao_usuario):
        print(f"[{idx+1}] {carta}")

    while True:
        try:
            escolha = int(input("Escolha a carta para jogar (número): ")) - 1
            carta = mao_usuario[escolha]
            break
        except (ValueError, IndexError):
            print("Entrada inválida. Escolha um número válido.")

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
        print(f"Você capturou: {mostrar_cartas(cartas_pegar)} com {carta}")
        mesa_vazia = not mesa
        return mao_usuario, mesa, cartas_pegar + [carta], mesa_vazia
    else:
        mesa.append(carta)
        print(f"Você não capturou nada com {carta}")
        return mao_usuario, mesa, [], False