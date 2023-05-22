from PPlay.sprite import *

class Player(Sprite):
    def __init__(self, window, level, image_file, frames=1):
        super().__init__(image_file, frames)
        self.vx = 0
        self.vy = 0
        self.base_speed = 100
        self.cmd = ''
        self.window = window
        self.keyboard = self.window.get_keyboard()
        self.level = level
        self.buffer = 0
        self.facing = 'AFK'
        self.maze_axis = (self.x - (window.width / 2 - level.half_maze_width) + self.width / 2, 
                          self.y - (window.height / 2 - level.half_maze_height) + self.height / 2)
        self.matrix_position = (self.maze_axis[0] // level.wall.width + 1, self.maze_axis[1] // level.wall.width + 1)

    def move1(self):
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
        self.matrix_position = self.get_matrix_position()
        
        can_go_down = (self.level.level[int(self.matrix_position[1] + 1)][int(self.matrix_position[0])] == 0)
        can_go_up = (self.level.level[int(self.matrix_position[1] - 1)][int(self.matrix_position[0])] == 0)
        can_go_left = (self.level.level[int(self.matrix_position[1])][int(self.matrix_position[0] - 1)] == 0)
        can_go_right = (self.level.level[int(self.matrix_position[1])][int(self.matrix_position[0] + 1)] == 0)

        # Determina as tolerâncias de movimento (até quantos pixels errados blinky aceita para fazer curva)
        delta_x = 1
        delta_y = 1
        x_window = (self.matrix_position[0] - 0.5) * self.level.wall.width - delta_x < self.maze_axis[0] < (self.matrix_position[0] - 0.5) * self.level.wall.width + delta_x
        y_window = (self.matrix_position[1] - 0.5) * self.level.wall.height - delta_y < self.maze_axis[1] < (self.matrix_position[1] - 0.5) * self.level.wall.height + delta_y
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
        if not can_go_right and self.vx > 0 and self.maze_axis[0] >= (self.matrix_position[0] - 0.5) * self.level.wall.width:
            self.vx = 0
        if not can_go_left and self.vx < 0 and self.maze_axis[0] <= (self.matrix_position[0] - 0.5) * self.level.wall.width:
            self.vx = 0

        # Checa condição de colisão com parede em y
        if not can_go_up and self.vy < 0 and self.maze_axis[1] <= (self.matrix_position[1] - 0.5) * self.level.wall.height:
            self.vy = 0
        if not can_go_down and self.vy > 0 and self.maze_axis[1] >= (self.matrix_position[1] - 0.5) * self.level.wall.height:
            self.vy = 0

        # Checa colisão de blinky com portal esquerdo.
        if self.maze_axis[0] < 0 + self.level.wall.width / 2:  # aka: 0 + 20/2 = 10
            self.x += 2 * self.level.half_maze_width - self.level.wall.width

        # Checa colisão de blinky com portal direito.
        if self.maze_axis[0] > 28 * self.level.wall.width - self.level.wall.width / 2:  # aka: 28*20 - 20/2 550
            self.x -= 2 * self.level.half_maze_width - self.level.wall.width

    def get_maze_axis(self):
        return (self.x - (self.window.width / 2 - self.level.half_maze_width) + self.width / 2, 
                self.y - (self.window.height / 2 - self.level.half_maze_height) + self.height / 2)

    def get_matrix_position(self):
        return ((self.x - (self.window.width / 2 - self.level.half_maze_width) + self.width / 2) // self.level.wall.width + 1, 
                (self.y - (self.window.height / 2 - self.level.half_maze_height) + self.height / 2) // self.level.wall.width + 1)

    def set_maze_axis(self):
        pass

    def set_matrix_position(self):
        pass
