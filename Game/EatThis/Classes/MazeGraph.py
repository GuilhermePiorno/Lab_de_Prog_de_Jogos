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