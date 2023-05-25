from PPlay.gameimage import *
from EatThis.procedural_map import *


class Maze():
    def __init__(self, walltype, window):
        self.window = window
        self.keyboard = self.window.get_keyboard()
        self.walltype = walltype
        self.wall = GameImage("Sprites/Walls/" + self.walltype + "/Wall_URDL.png")
        self.half_maze_height = (self.wall.height * 31) / 2
        self.half_maze_width = (self.wall.width * 28) / 2
        createlevel()
        self.level = self.fill_level()

    def fill_level(self):
        """ Preenche a matriz com os objectos de paredes de pontos. \n
        Fill the matrix with wall and points'objects. \n
        Examples: matrix = SetLevelObjects(Curved_20, janela)

        :param walltype: string argument named after the folder which contains it.
        :param janela: pplay's window object needs to be passed on since without it objects with image are not created.
        :return: matrix[31][28]
        """

        self.level = [[1]*30 for _ in range(33)]

        with open('maze.txt', mode='r', encoding='utf-8') as fin:
            fin.readline() #pula a primeira linha vazia
            for i in range(31):
                linha = fin.readline()
                for j in range(28):
                    if(linha[j] != "|"):
                        self.level[i+1][j+1] = 0

        # Altera o sprite das paredes para fazerem sentido
        deslocamento_xy = [-1, 0, 1, 0, -1]
        deslocamento_diagonal = [-1, 1, 1, -1, -1]
        for i in range(1, 32):  # linhas 0 e 32 estão sempre vazias
            for j in range(1, 29):  # colunas 0 e 29 estão sempre vazias
                if self.level[i][j] == 1:
                    wall_direction = ''
                    for k in range(4):
                        if self.level[i + deslocamento_xy[k]][j + deslocamento_xy[k + 1]] != 0:
                            if k == 0:
                                wall_direction += 'U'
                            elif k == 1:
                                wall_direction += 'R'
                            elif k == 2:
                                wall_direction += 'D'
                            elif k == 3:
                                wall_direction += 'L'
                    if wall_direction == 'URDL':
                        for k in range(4):
                            if self.level[i + deslocamento_diagonal[k]][j + deslocamento_diagonal[k + 1]] == 0:
                                if k == 0:
                                    wall_direction = 'UR'
                                elif k == 1:
                                    wall_direction = 'RD'
                                elif k == 2:
                                    wall_direction = 'DL'
                                elif k == 3:
                                    wall_direction = 'UL'

                    wall = GameImage("Sprites/Walls/" + self.walltype + "/Wall_" + wall_direction + ".png")
                    # wall.width and wall.height should be the same anyway (wall blocks are squares)

                    # offset measurement for half of the matrix's PLOTTED width (columns - 2 == len(level["any"] - 2).
                    half_maze_width = (len(self.level[0]) - 2) / 2 * wall.width
                    # x offset for column (j) in the matrix
                    x_offset = (j - 1) * wall.width
                    maze_x = self.window.width / 2 - half_maze_width + x_offset

                    # offset measurement for half of the matrix's PLOTTED height (lines - 2 == len(level["any"] - 2).
                    half_maze_height = (len(self.level) - 2) / 2 * wall.height
                    # y offset for column (i) in the matrix
                    y_offset = (i - 1) * wall.height
                    maze_y = self.window.height / 2 - half_maze_height + y_offset

                    wall.set_position(maze_x, maze_y)
                    self.level[i][j] = wall
                    if i == 14 and j == 1:
                        wall = GameImage("./Sprites/Walls/" + self.walltype + "/Wall_UL.png")
                        wall.set_position(maze_x, maze_y)
                    elif i == 14 and j == 28:
                        wall = GameImage("./Sprites/Walls/" + self.walltype + "/Wall_UR.png")
                        wall.set_position(maze_x, maze_y)

                    if i == 16 and j == 1:
                        wall = GameImage("./Sprites/Walls/" + self.walltype + "/Wall_DL.png")
                        wall.set_position(maze_x, maze_y)
                    elif i == 16 and j == 28:
                        wall = GameImage("./Sprites/Walls/" + self.walltype + "/Wall_RD.png")
                        wall.set_position(maze_x, maze_y)
                    self.level[i][j] = wall

        self.level[15][1] = 0
        self.level[15][28] = 0
        return self.level
    
    def draw(self):
        for i in range(1, 32):
            for j in range(1, 29):
                if self.level[i][j] != 0:
                    self.level[i][j].draw()
