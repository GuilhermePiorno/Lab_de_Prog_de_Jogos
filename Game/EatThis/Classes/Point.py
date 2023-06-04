from PPlay.sprite import *
from PPlay.gameimage import *
from copy import deepcopy

class Point(GameImage):
    def __init__(self, image_file, coordinates, window, path):
        super().__init__(image_file)
        self.line = coordinates[0]
        self.column = coordinates[1]
        self.was_eaten = False
        self.sinkmatrix = None
        self.maze_pathing = path
        self.window = window

    def get_matrix_coordinates(self):
        return (
            int((self.y - (self.window.height / 2 - 360) + self.height / 2) // 20 + 1),
            int((self.x - (self.window.width / 2 - 640) + self.width / 2) // 20 + 1)
            )


    def get_flow_field(self, lista=None):
        # A função é recursiva, o primeiro if é para quando get_flow_field é chamada pela primeira vez.
        cardinallookups = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        if lista is None:
            # sinkmatrix é uma deepcopy de levelpathing, levelpathing é a matriz de paredes (0s) e caminhos (1s)
            # levelpathing (level.pathing) apenas existe para facilitar a criação de sinkmatrixes.
            self.sinkmatrix = deepcopy(self.maze_pathing)
            targetstart = (self.line, self.column)
            # coloca as coordenadas de blinky na lista neste formato: [[y, x]] aka: [[linha, coluna]]
            # é importante a criação de uma lista para que a função recursiva funcione.
            # durante a recursão a lista é alterada para [[y0, x0], [y1, x1], [y2, x2], ...] que são as coordenadas
            # de cada ponto que está sendo analisado.
            lista = [[targetstart[0], targetstart[1]]]
            # seta a posição de blinky na sinkmatrix para -900
            self.sinkmatrix[lista[0][0]][lista[0][1]] = -900
        # nexttargets é o argumento que será utilizado na recursão. ou seja é a lista de coordenadas que serão analisadas.
        nexttargets = []
        for i in range(len(lista)):  # para cada coordenada na lista
            for j in range(4):      # para cada direção cardeal
                linha = lista[i][0] + cardinallookups[j][0]  # linha = linha + direção cardeal
                coluna = lista[i][1] + cardinallookups[j][1] # coluna = coluna + direção cardeal

                # Correções de out of index e solução para teletransporte ao mesmo tempo.
                if linha > len(self.sinkmatrix) - 1: # se linha está prestes a exceder a matriz, volta para o começo
                    linha = 0
                if coluna > len(self.sinkmatrix[0]) - 1: # se coluna está prestes a exceder a matriz, volta para o começo
                    coluna = 0
                # lados de linha <0 e coluna <0 não precisam ser corrigidos pois o python aceita index negativo.

                if self.sinkmatrix[linha][coluna] == 0: # se a posição é um caminho
                    self.sinkmatrix[linha][coluna] = self.sinkmatrix[lista[i][0]][lista[i][1]] + 1 # seta a posição para o valor da posição anterior + 1
                    nexttargets.append([linha, coluna]) # adiciona a posição na lista de coordenadas a serem analisadas

        if len(nexttargets) != 0: # se a lista de coordenadas a serem analisadas não está vazia
            self.get_flow_field(nexttargets) # recursão
        else:  # se a lista de coordenadas a serem analisadas está vazia quer dizer que o processo chegou ao fim.
            return