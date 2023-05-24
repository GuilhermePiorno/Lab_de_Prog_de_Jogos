# tutorial: https://www.youtube.com/watch?v=JtiK0DOeI4A&t=153s

from procedural_map import  *


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

    def conections(self, no):
        try:
            return self.graph[no]
        except KeyError:
            return 'WALL'

# cria a matriz do mapa
createlevel()
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

# terceira tarefa: traduzir o caminho no grafo para sequência de comandos ('u', 'd', 'l', 'r') na matriz