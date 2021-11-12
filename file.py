import numpy as np
import copy

from numpy import random

# FLAGS
debug_prints = False
usar_shake = True

max_iteracoes = 99999
file_name = 'instancias\instancias\induced_10_22.dat'

# Implementação do VNS
def VNS(solucao, num_vizinhancas):
    print("num viz: ", num_vizinhancas)
    if num_vizinhancas<=0:
        print("ERRO!", num_vizinhancas, "não é uma valor válido de vizinhanças.")
        return

    print("------------------------------------------------------------------------------")
    print("                                   VNS")
    print("------------------------------------------------------------------------------")
    if not debug_prints:
        print("...")
    
    # Vetor com a última solução válida de cada vizinhança.
    # Inicializa a vizinhança 1 com uma cópia da solução, as outras com vetores zerados.
    # (As vizinhanças não podem começar com a mesma solução por causa do teste do VND)
    solucoes_validas = []
    for i in range(num_vizinhancas):
        solucoes_validas.append(np.zeros(num_vertices))
    solucoes_validas[0] = (copy.deepcopy(solucao))
    
    vizinhanca_atual = 1
    i = 0
    while i < max_iteracoes: 
        score_solucao = 0
        for s in solucoes_validas:
            score_s = sum(s)
            if score_s > score_solucao:
                score_solucao = score_s
        
        if debug_prints:
            if i > 0:
                print("---------------------------------------")
            print("Soluções válidas:", solucoes_validas)
            print("Maior score válido:", score_solucao)

        # Gera nova solução
        nova_solucao = get_melhor_vizinho(solucao, vizinhanca_atual) # Melhor vizinho VÁLIDO (precisa percorrer todos)
        score_nova_solucao = 0
        if nova_solucao is None:
            nova_solucao = solucao
            score_nova_solucao = sum(nova_solucao)
        else: # Solução é válida
            score_nova_solucao = sum(nova_solucao)
            if score_nova_solucao == num_vertices: # Todos os vertices foram selecionados. melhor solucao possivel
                print('Melhor solução possível alcançada (todos vértices selecionados)')
                break
            solucoes_validas[vizinhanca_atual-1] = copy.deepcopy(nova_solucao) # Guarda solução válida
        if debug_prints:
            print("nova solução: ", nova_solucao)

        # Existe vizinho melhor: atual não é máximo local. Diminui k para encontrar o máximo local
        if score_nova_solucao > score_solucao:
            if debug_prints:
                print("Uma melhor solução foi encontrada: ", nova_solucao)
                print("score: ", score_nova_solucao)
                print("k: ", vizinhanca_atual)
                print("i: ", i)
            if usar_shake:  solucao = shake(nova_solucao, vizinhanca_atual)
            else:   solucao = nova_solucao
            vizinhanca_atual = max(vizinhanca_atual-1, 1)
            if debug_prints:
                print("diminuindo k para:", vizinhanca_atual)
        else:  # Todos vizinhos são piores: Máximo local. Aumentar k para tentar sair
            vizinhanca_atual = min(vizinhanca_atual+1, num_vizinhancas)
            if usar_shake:  solucao = shake(nova_solucao, vizinhanca_atual)
            if debug_prints:
                print("Nenhuma melhor solução. Máximo local: ", score_solucao)
                print("Aumentando k para:", vizinhanca_atual)
        
        # Testa critério de parada do VND
        todas_solucoes_iguais = True
        for soluc in solucoes_validas:
            if not (soluc == solucoes_validas[0]).all():
                todas_solucoes_iguais = False
        if todas_solucoes_iguais:
            print("Convergência em", i+1, "iterações")
            break

        i+=1
    
    if debug_prints:
        print("------------------------------------------------------------------------------")
    if i == max_iteracoes:
        print("Timeout após", i, "iterações.")
    
    # Encontra melhor solução entre as vizinhanças
    solucao_final = np.zeros(num_vertices)
    score_solucao_final = 0
    for s in solucoes_validas:
        score_s = sum(s)
        if score_s > score_solucao_final:
            score_solucao_final = score_s
            solucao_final = s
    print("Solução final:", solucao_final)
    print("Valor da solução final ", score_solucao_final)


# Percorre todos os vizinhos e retorna o vizinho VÁLIDO (respeita paridade) com maior número de vértices. Retorna None
# caso não haja vizinho maior válido.
# Complexidade O(N^vizinhanca)
def get_melhor_vizinho(solucao, vizinhanca):
    if debug_prints:
        print("Gerando", num_vertices*vizinhanca, "vizinhos na vizinhança", vizinhanca, "...")
    solucao_vizinha_melhor = copy.deepcopy(solucao)
    x = 0
    y = 0
    z = 0
    if vizinhanca < 3:
        x = num_vertices-1
    if vizinhanca < 2:
        y = num_vertices-1

    while x < num_vertices:
        while y < num_vertices:
            while z < num_vertices:
                if (x==y or x==z or y==z) and vizinhanca==3: # Garante que não altera menos que 3 vértices
                    z+=1
                    continue
                if y==z and vizinhanca==2: # Garante que não altera menos que 2 vértices
                    z+=1
                    continue

                vizinho = copy.deepcopy(solucao)
                if vizinhanca >= 3:
                    vizinho[x] = int(not bool(vizinho[x])) # Inverte valor do vértice x
                if vizinhanca >= 2:
                    vizinho[y] = int(not bool(vizinho[y])) # Inverte valor do vértice y
                vizinho[z] = int(not bool(vizinho[z])) # Inverte valor do vértice z

                if verifica_paridade(vizinho):
                    if sum(vizinho) > sum(solucao_vizinha_melhor):
                        solucao_vizinha_melhor = copy.deepcopy(vizinho)
                z+=1
            y+=1
        x+=1
    
    if not verifica_paridade(solucao_vizinha_melhor):
        return None
    return solucao_vizinha_melhor


# Dada uma solução e um índice de vizinhança, dá vizinhanca passos aleatórios para soluções vizinhas (não
# necessariamente válidas). 
def shake(solucao, vizinhanca):
    solucao_shake = copy.deepcopy(solucao)
    for i in range(vizinhanca): # Dá vizinhanca passos para vizinhos
        vertices_selecionados = []
        # Seleciona vizinhanca vertices para serem invertidos, sem repetir
        for j in range(vizinhanca):
            vert = random.randint(num_vertices)
            while vert in vertices_selecionados:
                vert = random.randint(num_vertices)
            vertices_selecionados.append(vert)
        
        # Inverte os vertices selecionados
        for vert in vertices_selecionados:
            solucao_shake[vert] = int(not bool(solucao_shake[vert]))
    
    return solucao_shake


# Dada uma solução e um índice de vizinhança, expande todos os vizinhos da solução na vizinhança. Dentre eles, retorna
# o válido de maior score. Caso não exista nenhum vizinho válido, tenta uma vizinhança abaixo. Caso chegue na primeira
# vizinhança ainda sem encontrar um válido, retorna uma solução sem nenhum vértice selecionado.
def vizinho_valido_aleatorio(solucao, vizinhanca):
    if vizinhanca <= 1:
        print("Não foram encontrados vizinhos válidos, retornando um vetor de zeros.")
        return np.zeros(num_vertices)
    
    vizinhanca_atual = copy.copy(vizinhanca)
    if debug_prints:
        print("Escolhendo vizinho aleatório! vizinhança: ", vizinhanca)
    solucao_aleatoria = copy.deepcopy(solucao)
    if debug_prints:
        print("Gerando", num_vertices*vizinhanca_atual, "vizinhos na vizinhança", vizinhanca_atual, "...")
    x = 0
    y = 0
    z = 0
    if vizinhanca_atual < 3:
        x = num_vertices-1
    if vizinhanca_atual < 2:
        y = num_vertices - 1

    vizinhos_validos = []
    if verifica_paridade(solucao_aleatoria):
        vizinhos_validos.append(solucao_aleatoria)
    while x < num_vertices:
        while y < num_vertices:
            while z < num_vertices:
                if (x==y or x==z or y==z) and vizinhanca_atual==3: # Garante que não altera menos que 3 vértices
                    z+=1
                    continue
                if y==z and vizinhanca_atual==2: # Garante que não altera menos que 2 vértices
                    z+=1
                    continue
                # print(x,y,z)
                vizinho = copy.deepcopy(solucao_aleatoria)
                if vizinhanca_atual >= 3:
                    vizinho[x] = int(not bool(vizinho[x])) # Inverte valor do vértice x
                if vizinhanca_atual >= 2:
                    vizinho[y] = int(not bool(vizinho[y])) # Inverte valor do vértice y
                vizinho[z] = int(not bool(vizinho[z])) # Inverte valor do vértice zz
                if verifica_paridade(vizinho):
                    vizinhos_validos.append(vizinho)
                z+=1
            y+=1
        x+=1

    if debug_prints:
        print(len(vizinhos_validos), "vizinhos validos gerados")
    if len(vizinhos_validos) == 0:
        print("Não há vizinho válido para", solucao, "na vizinhança", vizinhanca)
        return vizinho_valido_aleatorio(solucao, vizinhanca-1)

    # Escolhe aleatoriamente entre os vizinhos válidos
    indice = random.randint(len(vizinhos_validos))
    solucao_shake = vizinhos_validos[indice]
    
    return solucao_shake


# Verifica se a solução é válida (se a soma das conexões de cada vértice é par)
def verifica_paridade(solucao):
    # matriz somente com os vertices selecionados
    matriz_reduzida = copy.deepcopy(matriz_dusgu)
    elementos_a_zerar = [i for i, e in enumerate(solucao) if e == 0]
    for element in elementos_a_zerar:
        for line in range(num_vertices):
            matriz_reduzida[line][element] = 0
            matriz_reduzida[element][line] = 0

    eh_par = True
    for line in range(num_vertices):
        sum = 0
        for column in range(num_vertices):
            sum += matriz_reduzida[line][column]
        if sum % 2 == 1:
            eh_par = False
            break
    if eh_par:
        return True
    else:
        return False




def main():
    global matriz_dusgu
    global num_vertices
    global num_arestas

    f = open(file_name, "r")
    primeira_linha =  f.readline()
    num_vertices = int(primeira_linha.split(" ")[0])
    num_arestas = int(primeira_linha.split(" ")[1])

    print("qtd vertices: {}".format(num_vertices))
    print("qtd arestas: {}".format(num_arestas))

    # preenche matriz a partir da instancia
    matriz_dusgu = np.zeros((num_vertices, num_vertices))
    for line in f.readlines():
        primeiro = int(line.split(" ")[0].split()[0])
        segundo = int(line.split(" ")[1].split()[0])
        matriz_dusgu[primeiro-1][segundo-1] = 1
        matriz_dusgu[segundo-1][primeiro-1] = 1
    f.close()

    print("Matriz criada")

    # Só gerar um número aleatório e torcer que ele seja válido vai demorar muito quando existirem muitos vértices. A
    # função vizinho_valido_aleatorio alivia este problema.
    # primeira_solucao = np.full(num_vertices, 1)
    primeira_solucao = np.full(num_vertices, 0)
    # Escolhe um vizinho aleatório válido
    primeira_solucao = vizinho_valido_aleatorio(primeira_solucao, 2)
    print("primeira solucao: {}".format(primeira_solucao))
    print("valor:", sum(primeira_solucao))
    melhor_solucao = 0
    VNS(primeira_solucao, 3)


if __name__ == "__main__":
    main()

