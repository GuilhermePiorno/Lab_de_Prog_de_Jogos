# tutorial: https://www.youtube.com/watch?v=JtiK0DOeI4A
# https://brilliant.org/wiki/a-star-search/

from procedural_map import  *
import numpy as np
from queue import PriorityQueue
import time

class MazeGraph:
    def __init__(self, maze):
        self.matrix = maze
        self.lines = len(maze)
        self.columns = len(maze[0])
        self.graph = {}

    def add_node(self, coordinates):
        self.graph[coordinates] = []

    def add_conection(self, coordinates1, coordinates2):
        self.graph[coordinates1].append(coordinates2)
        #self.grafo[coordenadas2].append(coordenadas1)

    def create_graph(self):
        for i in range(self.lines):
            for j in range(self.columns):
                if self.matrix[i][j] == 0:  # Verifica se é um caminho
                    coordinates = (i, j)
                    self.add_node(coordinates)
                    # Verifica as células adjacentes (acima, abaixo, à esquerda e à direita)
                    # para criar as conexões entre os nós
                    if i > 0 and self.matrix[i - 1][j] == 0:  # Célula acima
                        self.add_conection(coordinates, (i - 1, j))
                    if i < self.lines - 1 and self.matrix[i + 1][j] == 0:  # Célula abaixo
                        self.add_conection(coordinates, (i + 1, j))
                    if j > 0 and self.matrix[i][j - 1] == 0:  # Célula à esquerda
                        self.add_conection(coordinates, (i, j - 1))
                    if j < self.columns - 1 and self.matrix[i][j + 1] == 0:  # Célula à direita
                        self.add_conection(coordinates, (i, j + 1))

    def get_neighbours(self, node):
        try:
            # retorna as conexões do nó em questão
            return self.graph[node]
        except KeyError:
            # trata o erro de quando o nó não existe no dicionário do grafo, o que significa que as coordenadas desse 
            # nó são na verdade paredes
            pass

def return_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    
    path.reverse()
    return path

def a_star(graph, start_node, target_node):
    # variável para gravar a ordem na qual os nós foram visitados
    count = 0
    # A Priority Queue é uma fila baseada em prioridade. Nesse caso, a prioridade é baseada na ordem decrescente do f_score de cada nó
    open_set = PriorityQueue()
    # adicionao nó inicial (correspondente à posição do pacman no labirinto) na fila, junto com seu f_score (0, pois é o nó inicial) e a ordem que foi colocado na lista (0)
    open_set.put((0, count, start_node))
    came_from = {} # guarda o caminho que fizemos
    g_score = {node: np.Infinity for node in graph.graph} # cria um dicionário com o g_score de cada nó do grafo. O valor inicial é atribuído como infinito
    g_score[start_node] = 0 # atribui o valor 0 ao g_score do nó inicial
    f_score = {node: np.Infinity for node in graph.graph} # cria um dicionário com o f_score de cada nó do grafo. O valor inicial é atribuído como infinito
    f_score[start_node] = h(start_node, target_node)  # o f_score do nó inicial é dado apenas pela função heurística, pois o g_score do nó inicial é sempre 0
    
    open_set_hash = {start_node} # usado para checar quais nós estão ou não na priority queue

    while not open_set.empty(): # o algoritmo roda até que o open set esteja vazio
        current = open_set.get()[2] # pega o nó do open_set. Essa operação sempre pega o nó com menor f_score. Se houver empate, pega o nó que foi inserido primeiro
        open_set_hash.remove(current)

        if current == target_node:
            #achou o caminho
            path = return_path(came_from, target_node)
            return path
        
        for neighbour in graph.get_neighbours(current):
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour, target_node)
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
    return False

# função heurística: 'Manhattan distance'
def h(node, target_node):
    delta_lines = abs(node[0] - target_node[0])
    delta_columns = abs(node[1] - target_node[1])
    return delta_lines + delta_columns

def matrix_path(graph_path, start_node):
    pacman_commands = ''
    current_node = start_node
    for node in graph_path:
        #checa se deve ir para a esquerda
        if((current_node[0] == node[0]) and (current_node[1] == (node[1] + 1))):
            pacman_commands += 'L'
        #checa se deve ir para a direita
        elif((current_node[0] == node[0]) and (current_node[1] == (node[1] - 1))):
            pacman_commands += 'R'
        #checa se deve ir para baixo
        elif(((current_node[0] + 1) == node[0]) and (current_node[1] == node[1])):
            pacman_commands += 'D'
        #checa se deve ir para cima
        elif(((current_node[0] - 1) == node[0]) and (current_node[1] == node[1])):
            pacman_commands += 'U'
        
        current_node = node
    
    return pacman_commands


# cria a matriz do mapa
#createlevel()
maze = [[1]*30 for _ in range(33)]

with open('maze.txt', mode='r', encoding='utf-8') as fin:
    fin.readline() #pula a primeira linha vazia
    for i in range(31):
        linha = fin.readline()
        for j in range(28):
            if(linha[j] != "|"):
                maze[i+1][j+1] = 0

# primeira tarefa: transformar a matriz do jogo em um grafo
maze_graph = MazeGraph(maze)
maze_graph.create_graph()

# segunda tarefa: aplicar o algoritmo a* no grafo e obter o caminho até o destino
target = (2, 2) # posição do blinky na matriz
start = (18, 15) # posição do pacman na matriz

t1 = time.time()
graph_path = a_star(maze_graph, start, target)
graph_path.append(target) # gambiarra: deve dar pra fazer isso dentro da função
print(graph_path)
# terceira tarefa: traduzir o caminho no grafo para sequência de comandos ('u', 'd', 'l', 'r') na matriz
pacman_cmds = matrix_path(graph_path, start)
print(pacman_cmds)
t2 = time.time()
dt = t2-t1
print(dt)