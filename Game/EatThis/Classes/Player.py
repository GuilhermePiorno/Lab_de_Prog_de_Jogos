from PPlay.sprite import *
from PPlay.gameimage import *
from EatThis.Classes.Point import *
from copy import deepcopy

class Player(Sprite):
    def __init__(self, window, maze, image_file, frames=1):
        super().__init__(image_file, frames)
        self.state = "invulnerable"
        self.vx = 0
        self.vy = 0
        self.base_speed = 120
        self.cmd = ''
        self.vulnerability_timer = 0
        self.base_vulnerability_time = 2
        self.transition_timer = 0
        self.transition_base_time = 2
        self.window = window
        self.keyboard = self.window.get_keyboard()
        self.maze = maze
        # self.sinkmatrix = self.level.pathing.copy()
        self.sinkmatrix = deepcopy(self.maze.pathing)
        self.buffer = 0
        self.facing = 'AFK'
        self.maze_axis = (self.x - (window.width / 2 - maze.half_maze_width) + self.width / 2,
                          self.y - (window.height / 2 - maze.half_maze_height) + self.height / 2)
        self.matrix_coordinates = (
            (self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1,
            (self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1
            )

    def move1(self):
        # Como primeira ação blinky atualiza sua sinkmatrix/flowfield.
        self.get_flow_field()


        if self.vulnerability_timer > 0:
            self.vulnerability_timer -= self.window.delta_time()

        if self.vulnerability_timer <= 0 and self.state == "vulnerable":
            self.state = "transition"
            #self.set_sequence(8, 12, True)
            self.update_sequence()
            self.state_transition()

        if self.transition_timer > 0:
            self.transition_timer -= self.window.delta_time()
        if self.transition_timer <= 0 and self.state == "transition":
            self.change_state()





        if self.state == "invulnerable":
            # Mudança de animação de Blinky nas 4 direções cardinais.
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




        if self.keyboard.key_pressed("UP"):
            self.buffer = 0
            self.cmd = 'u'
        if self.keyboard.key_pressed("DOWN"):
            self.buffer = 0
            self.cmd = 'd'
        if self.keyboard.key_pressed("RIGHT"):
            self.buffer = 0
            self.cmd = 'r'
        if self.keyboard.key_pressed("LEFT"):
            self.buffer = 0
            self.cmd = 'l'

        # Coordenadas do pacman em relação ao 0 da fase
        self.maze_axis = self.get_maze_axis()

        #Versão discretizada das coordenadas do pacman com ajuste (+1) para correspondencia a matriz "level".
        self.matrix_coordinates = self.get_matrix_coordinates()
        

        can_go_down = (self.maze.pathing[int(self.matrix_coordinates[0] + 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_up = (self.maze.pathing[int(self.matrix_coordinates[0] - 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_left = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] - 1)] == 0)
        can_go_right = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] + 1)] == 0)



        # Determina as tolerâncias de movimento (até quantos pixels errados blinky aceita para fazer curva)
        delta_x = 1
        delta_y = 1

        x_window = (self.matrix_coordinates[1] - 0.5) * self.maze.wall.width - delta_x < self.maze_axis[0] < (
                self.matrix_coordinates[1] - 0.5) * self.maze.wall.width + delta_x
        y_window = (self.matrix_coordinates[0] - 0.5) * self.maze.wall.height - delta_y < self.maze_axis[1] < (
                self.matrix_coordinates[0] - 0.5) * self.maze.wall.height + delta_y

        # Condição para aceitar qualquer input de movimento.
        if self.buffer < 0.5:
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

        # TODO: As vezes blinky anda demais antes de sua velocidade ser reduzida a zero,
        #  similar ao problema de deslizamento do pong. Este problema foi remediado colocando a atualização de posição
        #  após o check de reset e devido as velocidades baixas, mas caso a velocidade suba acima de 350 o problema retorna.
        #  Velocidades acima de 350 são ruins de jogar, então o problema foi temporariamente ignorado.

        # Checa condição de colisão com parede em x
        if not can_go_right and self.vx > 0 and self.maze_axis[0] >= (
                self.matrix_coordinates[1] - 0.5) * self.maze.wall.width:
            self.vx = 0
        if not can_go_left and self.vx < 0 and self.maze_axis[0] <= (
                self.matrix_coordinates[1] - 0.5) * self.maze.wall.width:
            self.vx = 0

        # Checa condição de colisão com parede em y
        if not can_go_up and self.vy < 0 and self.maze_axis[1] <= (
                self.matrix_coordinates[0] - 0.5) * self.maze.wall.height:
            self.vy = 0
        if not can_go_down and self.vy > 0 and self.maze_axis[1] >= (
                self.matrix_coordinates[0] - 0.5) * self.maze.wall.height:
            self.vy = 0

        # Checa colisão de blinky com portal esquerdo.
        if self.maze_axis[0] < 0 + self.maze.wall.width / 2:  # aka: 0 + 20/2 = 10
            self.x += 2 * self.maze.half_maze_width - self.maze.wall.width

        # Checa colisão de blinky com portal direito.
        if self.maze_axis[0] > 28 * self.maze.wall.width - self.maze.wall.width / 2:  # aka: 28*20 - 20/2 550
            self.x -= 2 * self.maze.half_maze_width - self.maze.wall.width

    def get_maze_axis(self):
        return (self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2,
                self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2)


    def get_matrix_coordinates(self):
        return ( 
            int((self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1),
            int((self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1)
            )

    def set_maze_axis(self):
        pass

    def set_matrix_position(self):
        pass

    # Função que atualiza a sinkmatrix de blinky.
    # Idéias interessantes para implementar:
    # Blinky pode simular invisibilidade preenchendo está matriz de zeros ou de valres aleatórios.
    # Por convenção foi utilizado o valor -900 para posição própria então
    def get_flow_field(self, lista=None):
        # A função é recursiva, o primeiro if é para quando get_flow_field é chamada pela primeira vez.
        cardinallookups = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        if lista is None:
            # sinkmatrix é uma deepcopy de levelpathing, levelpathing é a matriz de paredes (0s) e caminhos (1s)
            # levelpathing (level.pathing) apenas existe para facilitar a criação de sinkmatrixes.
            self.sinkmatrix = deepcopy(self.maze.pathing)
            targetstart = self.get_matrix_coordinates()
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

    def change_state(self):
        if self.state == "invulnerable":
            self.state = "vulnerable"
            self.base_speed *= 0.5
            self.vx *= 0.5
            self.vy *= 0.5
            self.vulnerability_timer = self.base_vulnerability_time
        elif self.state == "vulnerable" or self.state == "transition":
            self.base_speed /= 0.5
            self.vx /= 0.5
            self.vy /= 0.5
            self.state = "invulnerable"
        self.update_sequence()

    def state_transition(self):
        self.transition_timer = self.transition_base_time



    def update_sequence(self):
        if self.state == "invulnerable":
            if self.facing == 'U':
                self.set_sequence(6, 8, True)
            if self.facing == 'D':
                self.set_sequence(4, 6, True)
            if self.facing == 'L':
                self.set_sequence(2, 4, True)
            if self.facing == 'R':
                self.set_sequence(0, 2, True)
        if self.state == "vulnerable":
            self.set_sequence(8, 10, True)
        if self.state == "transition":
            self.set_sequence(8, 12, True)
            self.set_total_duration(50)

