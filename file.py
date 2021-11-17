import numpy as np
import copy as cp

ITERATIONS = 10000
TIME_OUT = ITERATIONS*10
BONUS = 1
NEIGHBORS = 1

class Graph:
    def __init__(self, matrix, vertices, num_vertices):
        self.matrix = matrix
        self.vertices = vertices
        self.num_vertices = num_vertices
        self.is_even = False
        self.score = 0
    def __str__(self):
        return "Matriz:\n" + str(self.matrix) + "\nVertices:\n" + str(self.vertices)

def read_file():
    #file_name = 'instancias\instancias\induced_7_10.dat'
    file_name = 'instancias\instancias\induced_10_22.dat'
    #file_name = 'instancias\instancias\induced_50_122.dat'

    f = open(file_name, "r")
    primeira_linha =  f.readline()
    num_vertices = int(primeira_linha.split(" ")[0])
    num_arestas = int(primeira_linha.split(" ")[1])

    matriz_dusgu = np.zeros((num_vertices, num_vertices))

    for line in f.readlines():
        primeiro = int(line.split(" ")[0].split()[0])
        segundo = int(line.split(" ")[1].split()[0])
        matriz_dusgu[primeiro-1][segundo-1] = 1
        matriz_dusgu[segundo-1][primeiro-1] = 1

    f.close()

    return Graph(matriz_dusgu, np.ones(num_vertices), num_vertices)

def apply_vertice_vec(graph, original_graph, vertices):
    for i in range(graph.num_vertices):
        for j in range(graph.num_vertices):
            if(vertices[j] == 1 and vertices[i] == 1):
                graph.matrix[i][j] = original_graph.matrix[i][j]
                graph.matrix[j][i] = original_graph.matrix[j][i]
            else:
                graph.matrix[i][j] = 0
                graph.matrix[j][i] = 0
    graph.vertices = vertices
    graph.is_even = test_parity(graph)
    graph.score = calculate_score(graph)

def add_vertice(graph, original_graph, index):
    for j in range(graph.num_vertices):
        if(graph.vertices[j] == 1):
            graph.matrix[index][j] = original_graph.matrix[index][j]
            graph.matrix[j][index] = original_graph.matrix[j][index]
    graph.vertices[index] = 1

def remove_vertice(graph, index):
    for j in range(graph.num_vertices):
        graph.matrix[index][j] = 0
        graph.matrix[j][index] = 0
    graph.vertices[index] = 0

def test_parity(graph):
    is_even = True
    for i in range(graph.num_vertices):
        sum = 0
        for j in range(graph.num_vertices):
            sum += graph.matrix[i][j]
        if sum%2 != 0:
            is_even = False

    return is_even

def create_solution(original_graph):
    new_graph = cp.deepcopy(original_graph)
    vertices_vec = np.random.choice([0, 1], size=(original_graph.num_vertices))

    apply_vertice_vec(new_graph, original_graph, vertices_vec)

    return new_graph

def calculate_score(graph):
    score = 0
    for i in range(graph.num_vertices):
        score += 1 if sum(graph.matrix[i]) % 2 == 0 else 0
    return score + sum(graph.vertices)
    #return sum(graph.vertices) + (BONUS if graph.is_even else 0)

def selectNeighbor(graph, original_graph):
    #neighbors = original_graph.num_vertices // 3
    neighbors = NEIGHBORS
    index_list = np.zeros(neighbors, dtype=int)
    possible_indexes = list(range(original_graph.num_vertices))
    for i in range(neighbors):
        index_list[i] = np.random.choice(possible_indexes)
        possible_indexes.remove(index_list[i])
    
    new_graph = cp.deepcopy(graph)
    for index in index_list:
        if(new_graph.vertices[index] == 0):
            add_vertice(new_graph, original_graph, index)
        else:
            remove_vertice(new_graph, index)

    new_graph.is_even = test_parity(new_graph)
    new_graph.score = calculate_score(new_graph)

    return new_graph

def lahc(original_graph):
    solution_A = Graph(np.zeros((original_graph.num_vertices, original_graph.num_vertices)), np.zeros(original_graph.num_vertices), original_graph.num_vertices)
    final_solution = cp.deepcopy(solution_A)
    sols = []
    for i in range(original_graph.num_vertices):
        sols.append(solution_A.score)
    i = 0
    while((i < ITERATIONS or not final_solution.is_even) and i < TIME_OUT):
        solution_B = selectNeighbor(solution_A, original_graph)
        v = i % original_graph.num_vertices
        if solution_B.score >= sols[v]:
            solution_A = cp.deepcopy(solution_B)
            if(solution_A.is_even and sum(solution_A.vertices) > sum(final_solution.vertices)):
                final_solution = cp.deepcopy(solution_A)
                print("ultima solucao: ", sum(final_solution.vertices))
        sols[v] = solution_A.score
        i += 1

    if(i == TIME_OUT):
        print("TIME OUT")
    if(not final_solution.is_even):
        print("NO SOLUTIONS FOUND")
        print(max(sols))
        return max(sols)

    print("final:\n", final_solution)
    #print("final score:", final_solution.score)
    print("vertices:", sum(final_solution.vertices))
    return final_solution


if __name__ == "__main__":
    original_graph = read_file()
    #print("neighbors:", original_graph.num_vertices//3)
    #print("original:\n", original_graph)
    solution = lahc(original_graph)
    




