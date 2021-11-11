import numpy as np

def add_vertice(novaMatriz, matriz_dusgu, verticesSelecionados, index):
    for j in range(num_vertices):
        if(verticesSelecionados[j] == 1):
            novaMatriz[index][j] = matriz_dusgu[index][j]
            novaMatriz[j][index] = matriz_dusgu[j][index]


def read_file():
    file_name = 'instancias\instancias\induced_7_10.dat'

    f = open(file_name, "r")
    primeira_linha =  f.readline()
    num_vertices = int(primeira_linha.split(" ")[0])
    num_arestas = int(primeira_linha.split(" ")[1])

    print("qtd vertices: {}".format(num_vertices))
    print("qtd arestas: {}".format(num_arestas))

    matriz_dusgu = np.zeros((num_vertices, num_vertices))

    for line in f.readlines():
        primeiro = int(line.split(" ")[0].split()[0])
        segundo = int(line.split(" ")[1].split()[0])
        matriz_dusgu[primeiro-1][segundo-1] = 1
        matriz_dusgu[segundo-1][primeiro-1] = 1
    print(matriz_dusgu)

    f.close()

    return num_vertices, matriz_dusgu

def test_parity(matrix, size):
    is_even = True
    for i in range(size):
        sum = 0
        for j in range(size):
            sum += matrix[i][j]
        if sum%2 != 0:
            is_even = False

    return is_even

if __name__ == "__main__":

    num_vertices, matriz_dusgu = read_file()
    
    novaMatriz = np.copy(matriz_dusgu)
    verticesSelecionados = np.random.choice([0, 1], size=(num_vertices))

    for i in range(num_vertices):
        if(verticesSelecionados[i] == 1):
            add_vertice(novaMatriz, matriz_dusgu, verticesSelecionados, i)

    print(novaMatriz)
    print(verticesSelecionados)

    print("é par?", test_parity(novaMatriz, num_vertices))



