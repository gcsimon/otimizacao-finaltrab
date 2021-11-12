import numpy as np
import copy

from numpy import random

# FLAGS
debug_prints = False
parar_quando_converge = False
usar_shake = True

max_iteracoes = 999999
file_name = 'instancias\instancias\induced_10_22.dat'

# TODO: Converter para VND: Guardar último resultado de todas as vizinhanças. Se forem o mesmo, convergiu

# Implementação do VNS
def VNS(solucao, num_vizinhancas):
    print("num viz: ", num_vizinhancas)
    if num_vizinhancas<=0:
        print("ERRO!", num_vizinhancas, "não é uma valor válido de vizinhanças.")
        return

    print("VNS")
    if debug_prints:
        print("------------------------------------------------------------------------------")
    else:
        print("...")
    
    vizinhanca_atual = 1
    for i in range(max_iteracoes): 
        score_solucao = sum(solucao)

        if score_solucao < num_vertices:
            # Gera nova solução
            nova_solucao = get_melhor_vizinho(solucao, vizinhanca_atual) # Pega melhor vizinho (precisa percorrer todos)
            if usar_shake and vizinhanca_atual > 1:
                # Dá vizinhanca_atual passos para vizinhos VÁLIDOS (precisa percorrer todos novamente)
                nova_solucao = shake(nova_solucao, vizinhanca_atual)
            score_nova_solucao = sum(nova_solucao)
            if debug_prints:
                print("nova solução: ", nova_solucao)

            # Existe vizinho melhor: atual não é máximo local. Diminui k para encontrar o máximo local
            if score_nova_solucao > score_solucao:
                if debug_prints:
                    print("Uma melhor solução foi encontrada: ", score_nova_solucao)
                    print("Diminuindo k")
                solucao = nova_solucao
                vizinhanca_atual = max(vizinhanca_atual-1, 1)
                if debug_prints:
                    print("k:", vizinhanca_atual)
            else:  # Todos vizinhos são piores: Máximo local. Aumentar k para tentar sair
                if debug_prints:
                    print("Nenhuma melhor solução. Máximo local: ", score_solucao)
                # TODO: trocar esse teste para o teste do VND. Não sei se seria aqui
                if vizinhanca_atual==num_vizinhancas and parar_quando_converge: # Máximo local da maior vizinhança. Muito possivelmente um máximo global
                    print("Convergência em", i, "iterações")
                    break
                if debug_prints:
                    print("Aumentando k")
                vizinhanca_atual = min(vizinhanca_atual+1, num_vizinhancas)
                if debug_prints:
                    print("k:", vizinhanca_atual)
        else:
            print('Melhor solução possível alcançada (todos vértices selecionados)')
            break
            #todos os vertices foram selecionados. melhor solucao possivel
    if debug_prints:
        print("------------------------------------------------------------------------------")
    print("Solução final", solucao)
    print("Valor da solução final ", sum(solucao))


# Percorre todos os vizinhos e retorna o vizinho VÁLIDO (respeita paridade) com maior número de vértices.
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
        y = num_vertices - 1

    while x < num_vertices:
        while y < num_vertices:
            while z < num_vertices:
                if (x==y or x==z or y==z) and vizinhanca==3: # Garante que não altera menos que 3 vértices
                    z+=1
                    continue
                if y==z and vizinhanca==2: # Garante que não altera menos que 2 vértices
                    z+=1
                    continue
                # print(x,y,z)
                vizinho = copy.deepcopy(solucao)
                if vizinhanca >= 3:
                    vizinho[x] = int(not bool(vizinho[x])) # Inverte valor do vértice x
                if vizinhanca >= 2:
                    vizinho[y] = int(not bool(vizinho[y])) # Inverte valor do vértice y
                vizinho[z] = int(not bool(vizinho[z])) # Inverte valor do vértice zz
                if verifica_paridade(vizinho):
                    # print('vizinho', vizinho)
                    if sum(vizinho) > sum(solucao_vizinha_melhor):
                        solucao_vizinha_melhor = copy.deepcopy(vizinho)
                z+=1
            y+=1
        x+=1
    
    return solucao_vizinha_melhor


# Dada uma solução e um índice de vizinhança, dá vizinhanca passos aleatórios para soluções VÁLIDAS.
# Não faria sentido dar um passo para uma solução que não respeita a paridade, então precisamos explorar TODOS os
# vizinhos para depois escolher aleatoriamente entre eles
# TODO: Provavelmente existe uma forma melhor de fazer isso. Talvez trocar pra um vizinho realmente aleatório, mas 
# guardar a última resposta válida do VNS para caso o programa termine. Teria que mudar a lógica do VNS
def shake(solucao, vizinhanca):
    vizinhanca_atual = copy.copy(vizinhanca)
    if debug_prints:
        print("Shake! vizinhança: ", vizinhanca)
    solucao_shake = copy.deepcopy(solucao)
    for i in range(vizinhanca): # Dá vizinhanca passos para vizinhos
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
        if verifica_paridade(solucao_shake):
            vizinhos_validos.append(solucao_shake)
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
                    vizinho = copy.deepcopy(solucao_shake)
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

        # Escolhe aleatoriamente entre os vizinhos válidos
        if debug_prints:
            print(len(vizinhos_validos), "vizinhos validos gerados")
        indice = random.randint(len(vizinhos_validos))
        solucao_shake = vizinhos_validos[indice]

        vizinhanca_atual -= 1
    
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

    # Se tentarmos um valor inicial aleatório válido com muitos vértices, pode demorar
    #muito até conseguir. Melhor começar com um vetor de zeros
    primeira_solucao = np.zeros(num_vertices)
    primeira_solucao = shake(primeira_solucao, 3) # Shake gera vizinhos e só pula para um válido. Podemos usar aqui
    print("primeira solucao: {}".format(primeira_solucao))
    print("valor:", sum(primeira_solucao))
    melhor_solucao = 0
    VNS(primeira_solucao, 3)


if __name__ == "__main__":
    main()

