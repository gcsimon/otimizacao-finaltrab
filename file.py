import numpy as np
import copy

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
print("possivel solucao: {}".format(possivel_solucao))

# matriz somente com os vertices selecionados
matriz_reduzida = copy.deepcopy(matriz_dusgu)
elementos_a_zerar = [i for i, e in enumerate(possivel_solucao) if e == 0]
for element in elementos_a_zerar:
    for line in range(num_vertices):
        matriz_reduzida[line][element] = 0
        matriz_reduzida[element][line] = 0
# print(matriz_dusgu)
# print()
print(matriz_reduzida)

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
    print('eh par')
else:
    print('eh impar')





