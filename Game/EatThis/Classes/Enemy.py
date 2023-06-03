from PPlay.sprite import *
from EatThis.a_star import *
from EatThis.Classes.Point import *
from EatThis.Classes.PowerUp import *
import time

class Enemy(Sprite):
    def __init__(self, window, maze, image_file, frames=1):
        super().__init__(image_file, frames)
        self.vx = 0
        self.vy = 0
        self.base_speed = 100
        self.cmd = ''
        self.window = window
        self.maze = maze
        self.facing = 'AFK'
        self.maze_axis = (self.x - (window.width / 2 - maze.half_maze_width) + self.width / 2, 
                          self.y - (window.height / 2 - maze.half_maze_height) + self.height / 2)
        self.matrix_coordinates = (
            (self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1,
            (self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1
            )
        self.cmdstr = ''
        self.keyboard = self.window.get_keyboard()
        self.image_file = image_file
        self.is_dead = False
        self.death_instant = 0


    def move1(self, target):

        
        # pacman comendo os pontos normais
        if(isinstance(self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]], Point)):
            self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]] = 0

        # pacman comendo os powerups
        if(isinstance(self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]], PowerUp)):
            self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]] = 0
            # mudar estado do pacman e do blinky
            print("Comeu powerup")
            self.maze.powerup_num -= 1
            if(self.maze.powerup_num == 0):
                #teste morte do pacman
                self.die()
            print(self.maze.powerup_num)

        # Coordenadas do pacman em relação ao 0 da fase
        self.maze_axis = self.get_maze_axis()
        

        #Versão discretizada das coordenadas do pacman com ajuste (+1) para correspondencia a matriz "level".
        # antigo self.matrix_position e self.get_matrix_position()
        self.matrix_coordinates = self.get_matrix_coordinates()
        

        can_go_down = (self.maze.pathing[int(self.matrix_coordinates[0] + 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_up = (self.maze.pathing[int(self.matrix_coordinates[0] - 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_left = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] - 1)] == 0)
        can_go_right = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] + 1)] == 0)


        # ia do pacman baseada na posição relativa
        #self.ia_pacman_1(target)

        # ia do pacman baseada no algoritmo a*
        # self.ia_pacman_2(target, maze_graph)

        # ia do pacman baseada no algoritmo flowfield
        if not self.is_dead:
            self.animate()
            self.ia_pacman_follow(target)
            # dist = (delta_x**2 + delta_y**2)^0.5
            direct_distance = self.relative_position_of_target(target)[0]**2
            direct_distance += self.relative_position_of_target(target)[1]**2
            direct_distance = direct_distance**0.5

            if direct_distance <= 100:
                self.ia_pacman_run_away(target)
        else:
            if time.time() - self.death_instant >= 10:
                self.hide()


        # pacman controlado pelo jogador, para testes
        #self.ia_pacman_testes()

    
        # Determina as tolerâncias de movimento (até quantos pixels errados pacman aceita para fazer curva)
        delta_x = 1
        delta_y = 1
        x_window = (self.matrix_coordinates[1] - 0.5) * self.maze.wall.width - delta_x < self.maze_axis[0] < (self.matrix_coordinates[1] - 0.5) * self.maze.wall.width + delta_x
        y_window = (self.matrix_coordinates[0] - 0.5) * self.maze.wall.height - delta_y < self.maze_axis[1] < (self.matrix_coordinates[0] - 0.5) * self.maze.wall.height + delta_y
        # Movimento VERTICAL (REQUERIMENTO DE POSIÇÃO HORIZONTAL)
        if x_window:
            if self.cmd == 'd' and can_go_down:
                self.cmd = ''
                self.vx = 0
                self.vy = self.base_speed
            if self.cmd == 'u' and can_go_up:
                self.cmd = ''
                self.vx = 0
                self.vy = -self.base_speed

        # Movimento HORIZONTAL (REQUERIMENTO DE POSIÇÃO VERTICAL)
        if y_window:
            if self.cmd == 'r' and can_go_right:
                self.cmd = ''
                self.vx = self.base_speed
                self.vy = 0
            if self.cmd == 'l' and can_go_left:
                self.cmd = ''
                self.vx = -self.base_speed
                self.vy = 0

        # Checa condição de colisão de pacman com parede em x
        if not can_go_right and self.vx > 0 and self.maze_axis[0] >= (self.matrix_coordinates[1] - 0.5) * self.maze.wall.width:
            self.vx = 0
        if not can_go_left and self.vx < 0 and self.maze_axis[0] <= (self.matrix_coordinates[1] - 0.5) * self.maze.wall.width:
            self.vx = 0

        # Checa condição de colisão de pacman com parede em y
        if not can_go_up and self.vy < 0 and self.maze_axis[1] <= (self.matrix_coordinates[0] - 0.5) * self.maze.wall.height:
            self.vy = 0
        if not can_go_down and self.vy > 0 and self.maze_axis[1] >= (self.matrix_coordinates[0] - 0.5) * self.maze.wall.height:
            self.vy = 0


        # Checa colisão de com portal esquerdo.
        if self.maze_axis[0] < 0 + self.maze.wall.width / 2:  # aka: 0 + 20/2 = 10
            self.x += 2 * self.maze.half_maze_width - self.maze.wall.width

        # Checa colisão de com portal direito.
        if self.maze_axis[0] > 28 * self.maze.wall.width - self.maze.wall.width / 2:  # aka: 28*20 - 20/2 550
            self.x -= 2 * self.maze.half_maze_width - self.maze.wall.width


    def ia_pacman_1(self, target):
        relative_x_pacman_blinky, relative_y_pacman_blinky = self.relative_position_of_target(target)

        #ia 'burra' do pacman
        #com essa lógica de movimentação, o pacman fica frequentemente 'preso' correndo contra paredes. Talvez implementar
        #alguma funcionalidade que impeça ele de ficar correndo contra uma parede por mais de algum tempo máximo
        if abs(relative_x_pacman_blinky) > abs(relative_y_pacman_blinky):
            # se movimentará na direção horizontal
            if relative_x_pacman_blinky>0:
                #vai para a direita
                self.cmd = 'r'
            else:
                #vai para a esquerda
                self.cmd = 'l'
        else:
            #se movimentará na direção vertical
            if relative_y_pacman_blinky>0:
                #vai para baixo
                self.cmd = 'd'
            else:
                #vai para cima
                self.cmd = 'u'

    def ia_pacman_2(self, target, maze_graph):

        # cria o caminho (no grafo) do pacman até o blinky
        graph_path = a_star(maze_graph, self.get_matrix_coordinates(), target.get_matrix_coordinates())
        graph_path.append(target.get_matrix_coordinates()) # gambiarra: deve dar pra fazer isso dentro da função
        self.cmdstr = matrix_path(graph_path, self.get_matrix_coordinates())
        if len(self.cmdstr) != 0:
            self.cmd = self.cmdstr[0].lower()
        else:
            self.vx = 0
            self.vy = 0

    def ia_pacman_testes(self):
        if self.keyboard.key_pressed("W"):
            self.cmd = 'u'
        if self.keyboard.key_pressed("S"):
            self.cmd = 'd'
        if self.keyboard.key_pressed("D"):
            self.cmd = 'r'
        if self.keyboard.key_pressed("A"):
            self.cmd = 'l'
    
    def animate(self):
        # Mudança de animação nas 4 direções cardinais.
        if self.vy < 0 and self.facing != 'U':
            self.facing = 'U'
            self.set_sequence(6, 8, True)
        if self.vy > 0 and self.facing != 'D':
            self.facing = 'D'
            self.set_sequence(4, 6, True)
        if self.vx < 0 and self.facing != 'L':
            self.facing = 'L'
            self.set_sequence(2, 4, True)
        if self.vx > 0 and self.facing != 'R':
            self.facing = 'R'
            self.set_sequence(0, 2, True)

    def die(self):
        self.death_instant = time.time()
        self.is_dead = True
        self.vx = 0
        self.vy = 0
        self.set_sequence_time(9, 22, 200, False)

    def relative_position_of_target(self, target):
        return target.x - self.x, target.y - self.y

    def get_maze_axis(self):
        return (self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2, 
                self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2)


    def ia_pacman_follow(self, target):
        # Consulta a "sinkmatrix" para determinar a direção de movimento.
        # A matriz sink é uma matriz de mesma dimensão que a matriz "level" que contém valores de "distancia" de cada célula até o blinky.
        if target.sinkmatrix[self.matrix_coordinates[0] + 1][self.matrix_coordinates[1]] < \
                target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1]]:
            self.cmd = 'd'
        if target.sinkmatrix[self.matrix_coordinates[0] - 1][self.matrix_coordinates[1]] < \
                target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1]]:
            self.cmd = 'u'
        if target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1] - 1] < \
                target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1]]:
            self.cmd = 'l'
        if target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1] + 1] < \
                target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1]]:
            self.cmd = 'r'

    def ia_pacman_run_away(self, target):
        # Inversão do conceito de ia_pacman_follow
        # "menor que" é trocado por "maior que" e "0 >" é adicionado a equação para evitar
        # que fugir para a parede seja uma opção.
        direcoes = ['d', 'u', 'l', 'r']
        offsets = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        for i in range(4):
            if [self.matrix_coordinates[0] + offsets[i][0], self.matrix_coordinates[1] + offsets[i][1]] != [15, 1] and \
                    [self.matrix_coordinates[0] + offsets[i][0], self.matrix_coordinates[1] + offsets[i][1]] != [15, 28]:
                if 0 > target.sinkmatrix[self.matrix_coordinates[0] + offsets[i][0]][self.matrix_coordinates[1] + offsets[i][1]] > \
                        target.sinkmatrix[self.matrix_coordinates[0]][self.matrix_coordinates[1]]:
                    self.cmd = direcoes[i]


    def get_matrix_coordinates(self):
        return (
            int((self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1),
            int((self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1)
            )

