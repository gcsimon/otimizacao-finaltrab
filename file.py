import numpy as np
import copy

k_max = 1
iterations = 999


def VNS(solucao, num_vizinhancas):
    print("num viz: ", num_vizinhancas)
    if num_vizinhancas <= 0:
        print("ERRO! Vizinhança", num_vizinhancas, "não existe.")
        return
    for i in range(iterations): 
        if sum(solucao) < len(solucao):
            nova_solucao = k_vizinhanca(solucao, num_vizinhancas)
            print("nova solução: ", nova_solucao)
            if verifica_paridade(nova_solucao):
                score_solucao = sum(solucao)
                score_nova_solucao = sum(nova_solucao)
                if score_nova_solucao > score_solucao and verifica_paridade(nova_solucao):
                    print("Uma melhor solução foi encontrada: ", score_nova_solucao)
                    solucao = nova_solucao
                else:  # Solução nova é pior que a antiga: Máximo local
                    num_vizinhancas = min(num_vizinhancas + 1, k_max)
                    continue
            # Solução nova é pior que a antiga (porque não é par): Máximo local
            else:
                num_vizinhancas = min(num_vizinhancas, k_max)
                continue
        else:
            print('Solucao topzera. Todos vertices selecionados')
            #todos os vertices foram selecionados. melhor solucao possivel
    print("solucao final", solucao)
    print("Valor solucao final ", sum(solucao))

# Muda k vértices para gerar uma nova solução.
def k_vizinhanca(solucao, num_vizinhancas):
    solucao_vizinha_melhor = copy.deepcopy(solucao)
    for i in range(len(solucao)):
        vizinho = copy.deepcopy(solucao)
        vizinho[i] = int(not bool(vizinho[i]))
        if verifica_paridade(vizinho):
            print('solucaozita', vizinho)
            if sum(vizinho) > sum(solucao_vizinha_melhor):
                solucao_vizinha_melhor = copy.deepcopy(vizinho)
    return solucao_vizinha_melhor



def verifica_paridade(solucao):
    # matriz somente com os vertices selecionados
    matriz_reduzida = copy.deepcopy(matriz_dusgu)
    elementos_a_zerar = [i for i, e in enumerate(solucao) if e == 0]
    for element in elementos_a_zerar:
        for line in range(num_vertices):
            matriz_reduzida[line][element] = 0
            matriz_reduzida[element][line] = 0
    # print(matriz_dusgu)
    # print()
    # print("matriz reduzida: \n", matriz_reduzida)

    # verifica se solução é par

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

    file_name = 'instancias\instancias\induced_7_10.dat'

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

    #possivel selecao de vertices
    primeira_solucao = np.random.choice([0, 1], size=(num_vertices))
    while not verifica_paridade(primeira_solucao):
        primeira_solucao = np.random.choice([0, 1], size=(num_vertices))
    print("primeira solucao: {}".format(primeira_solucao))
    melhor_solucao = 0
    VNS(primeira_solucao, 1)


if __name__ == "__main__":
    main()

