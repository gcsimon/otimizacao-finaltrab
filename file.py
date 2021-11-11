import numpy as np

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

#[1, 0, 1, 0, 1, 1, 0]

f.close()