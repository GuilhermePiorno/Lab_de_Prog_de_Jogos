from PPlay.sprite import *
from queue import LifoQueue

class Enemy(Sprite):
    def __init__(self, window, level, image_file, frames=1):
        super().__init__(image_file, frames)
        self.vx = 0
        self.vy = 0
        self.base_speed = 100
        self.cmd = ''
        self.window = window
        self.level = level
        self.facing = 'AFK'
        self.maze_axis = (self.x - (window.width / 2 - level.half_maze_width) + self.width / 2, 
                          self.y - (window.height / 2 - level.half_maze_height) + self.height / 2)
        self.matrix_position = (self.maze_axis[0] // level.wall.width + 1, self.maze_axis[1] // level.wall.width + 1)
        self.cmdstr = ''
        self.cmd_stack = LifoQueue()
        self.changed_cell = False

    def move1(self, target, cmdstr):
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
        
        # Coordenadas do pacman em relação ao 0 da fase
        self.maze_axis = self.get_maze_axis()
        
        #Versão discretizada das coordenadas do pacman com ajuste (+1) para correspondencia a matriz "level".
        self.matrix_position = self.get_matrix_position()
        
        can_go_down = (self.level.level[int(self.matrix_position[1] + 1)][int(self.matrix_position[0])] == 0)
        can_go_up = (self.level.level[int(self.matrix_position[1] - 1)][int(self.matrix_position[0])] == 0)
        can_go_left = (self.level.level[int(self.matrix_position[1])][int(self.matrix_position[0] - 1)] == 0)
        can_go_right = (self.level.level[int(self.matrix_position[1])][int(self.matrix_position[0] + 1)] == 0)

        # ia do pacman baseada na posição relativa
        #self.ia_pacman_1(target)

        # ia do pacman baseada no algoritmo a*
        self.ia_pacman_2(target, cmdstr)
    
        # Determina as tolerâncias de movimento (até quantos pixels errados pacman aceita para fazer curva)
        delta_x = 1
        delta_y = 1
        x_window = (self.matrix_position[0] - 0.5) * self.level.wall.width - delta_x < self.maze_axis[0] < (self.matrix_position[0] - 0.5) * self.level.wall.width + delta_x
        y_window = (self.matrix_position[1] - 0.5) * self.level.wall.height - delta_y < self.maze_axis[1] < (self.matrix_position[1] - 0.5) * self.level.wall.height + delta_y
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
        if not can_go_right and self.vx > 0 and self.maze_axis[0] >= (self.matrix_position[0] - 0.5) * self.level.wall.width:
            self.vx = 0
        if not can_go_left and self.vx < 0 and self.maze_axis[0] <= (self.matrix_position[0] - 0.5) * self.level.wall.width:
            self.vx = 0

        # Checa condição de colisão de pacman com parede em y
        if not can_go_up and self.vy < 0 and self.maze_axis[1] <= (self.matrix_position[1] - 0.5) * self.level.wall.height:
            self.vy = 0
        if not can_go_down and self.vy > 0 and self.maze_axis[1] >= (self.matrix_position[1] - 0.5) * self.level.wall.height:
            self.vy = 0

    def ia_pacman_1(self, target):
        relative_x_pacman_blinky, relative_y_pacman_blinky = self.relative_position_of_target(target)

        #ia 'burra' do pacman
        #com essa lógica de movimentação, o pacman fica frequentemente 'preso' correndo contra paredes. Talvez implementar
        #alguma funcionalidade que impeça ele de ficar correndo contra uma parede por mais de algum tempo máximo
        if(abs(relative_x_pacman_blinky) > abs(relative_y_pacman_blinky)):
            # se movimentará na direção horizontal
            if(relative_x_pacman_blinky>0):
                #vai para a direita
                self.cmd = 'r'
            else:
                #vai para a esquerda
                self.cmd = 'l'
        else:
            #se movimentará na direção vertical
            if(relative_y_pacman_blinky>0):
                #vai para baixo
                self.cmd = 'd'
            else:
                #vai para cima
                self.cmd = 'u'

    def ia_pacman_2(self, target, cmdstr):
        #print('cmdstr: ' + cmdstr)
        #print('self.cmdstr: ' + self.cmdstr)
        #print(self.cmdstr == cmdstr)
        if(self.changed_cell or (self.cmdstr == cmdstr)):
            self.cmd = self.get_cmd_from_cmdstack(cmdstr)
        self.changed_cell = False
        #print(self.cmd)

    def get_cmd_from_cmdstack(self, cmdstr):
        if(self.cmd_stack.empty()):
            for i in range(-1, (-1)*len(cmdstr)-1, -1):
                self.cmd_stack.put(cmdstr[i])

        if(self.cmdstr != cmdstr):
            self.cmdstr = cmdstr
            self.cmd_stack = LifoQueue()
            for i in range(-1, (-1)*len(cmdstr)-1, -1):
                self.cmd_stack.put(cmdstr[i])
            return self.cmd_stack.get().lower()
        else:
            if self.cmd_stack.qsize() != 0:
                return self.cmd_stack.get().lower()

    def relative_position_of_target(self, target):
        return (target.x - self.x, target.y - self.y)
    
    def changed_matrix_cell(self, last_matrix_position):
        if(last_matrix_position != self.get_matrix_position()):
            return True
        else:
            return False

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
