import numpy as np
import copy

k_max = 3


def VNS(s, k):
    if k <= 0:
        print("ERRO! Vizinhança", k, "não existe.")
        return
    
    nova_solucao = k_vizinhanca(s, k)
    print("nova solução: ", nova_solucao)
    
    valor_s = sum(s)
    if verifica_paridade(s):
        print("Solução gerada respeita paridade.")
        novo_valor_s = sum(nova_solucao)
        if novo_valor_s > valor_s:
            print("Melhor solução encontrada: ", novo_valor_s)
            valor_s = novo_valor_s
        else: # Solução nova é pior que a antiga: Máximo local
            VNS(s, max(k+1, k_max))
    else: # Solução nova é pior que a antiga (porque não é par): Máximo local
        VNS(s, max(k+1, k_max))


# Muda k vértices para gerar uma nova solução.
def k_vizinhanca(s, k):
    for n in range(k):
        # Escolhe um vértice aleatório da solução
        vert = np.random.randint(num_vertices)
        while s[vert] == 1 and sum(s) != len(s):
            vert = np.random.randint(num_vertices)
        # print("vertice escolhido: ", vert)
        
        # Inverte o seu valor
        # if s[vert] == 0:
        s[vert] = 1
        # else:
        #     s[vert] = 0

    return s


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
    possivel_solucao = np.random.choice([0, 1], size=(num_vertices))
    while sum(possivel_solucao)%2 != 0:
        possivel_solucao = np.random.choice([0, 1], size=(num_vertices))
    print("possivel solucao: {}".format(possivel_solucao))
    melhor_solucao = 0
    VNS(possivel_solucao, 1)


if __name__ == "__main__":
    main()

