import time
from pve_jogo import mostrar_cartas, somas_possiveis, valor

def jogada_maquina(mao_maquina, mesa):
    print(f"\n----------------\n\nMesa: {mostrar_cartas(mesa)}")
    print("Máquina pensando...")
    time.sleep(1)

    for carta in mao_maquina:
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
            mao_maquina.remove(carta)
            cartas_pegar = melhores_jogadas[0][1]
            for c in cartas_pegar:
                mesa.remove(c)
            print(f"Máquina capturou: {mostrar_cartas(cartas_pegar)} com {carta}")
            mesa_vazia = not mesa
            return mao_maquina, mesa, cartas_pegar + [carta], mesa_vazia

    carta = mao_maquina.pop(0)
    mesa.append(carta)
    print(f"Máquina não capturou nada com {carta}")
    return mao_maquina, mesa, [], False
