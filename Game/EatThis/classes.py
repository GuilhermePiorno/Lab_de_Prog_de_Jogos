from PPlay.sprite import *


class Player(Sprite):
    def __init__(self, image_file, frames=1):
        # Chama construtor da classe "pai" (sprite).
        super().__init__(image_file, frames)

        # Modificadores de movimento
        self.base_speed = 100
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

    # Ignorar as 2 property e setter abaixo, apenas testando uma forma de incorporar a atualização de parâmetros
    # como blinky_newaxis_x, blinky_newaxis_y, new_x e new_y dentro do próprio objeto player.
    # Funciona, mas isto é uma otimização para mais tarde.
    # TODO: Incorporar parâmetros externos relacionados a classe jogador.

    # Quando objeto.x é chamado, a classe retorna o parametro interno _x.
    @property
    def x(self):
        return self._x

    # Quando blinky.map_x é chamado, ele retorna o valor do parametro interno ._map_x
    @property
    def map_x(self):
        return self._map_x

    # Quando é atribuido um valor a x, ex: blinky.x = 10
    # o valor é atribuido ao parâmetro interno _x e o parametro _map_x recebe o valor deslocado.
    @x.setter
    def x(self, value):
        self._x = value
        self._map_x = self.x - (1280/2 - 28*20/2) + 13

    # Observação: Ainda não sei exatamente os limites e funcionamento interno do @obj.setter e @property
    # aprendi hoje que se chamam "decoradores". Mas parecem cumprir com objetivo. (limpar o código)
    # Porém não é necessário para o funcionamento, então será deixado para mais tarde; vide o "to do" acima.


#   Criar uma classe para todos os elementos do mapa para tirar vantagem
#   para utilizar um atributo e obter melhores comparações.

#   Atualmente objetos são comparados apenas se são 0 ou não zero, ao introduzir "pontos" que pacman come
#   isto pode/vai mudar e todos os espaços da matriz serão objetos, espaços vazios ou paredes, é necessário
#   então uma forma de diferencia-los pois if level[arg1][arg2] != 0 apenas checa por zeros e não é capaz
#   de diferenciar objetos.
#   A classe deve ser criada como a classe players mas adicionando um atributo "self.type".
#   A partir daí podemos definir 1 para "walkable", 2 para "wall", 3 para "ponto normal", 4 para "power-up"
#   e comparar simples através de algo tipo: if level[arg1][arg2].type == 1 or para saber se é um espaço vazio.

# TODO: talvez seja bom atribuir uma posição em relação a apenas um eixo de coordenadas e criar métodos dentro das 
# classes para converter entre os diferentes sistemas de coordenadas 
# TODO: como estamos migrando para orientação a objetos, talvez seja melhor criar uma classe para o mapa também, para que 
# possamos passar o mapa como um parâmetro na inicialização do pacman e do blinky
class Enemy(Sprite):
    def __init__(self, janela, level, image_file, frames=1):
        super().__init__(image_file, frames)

        self.base_speed = 50
        self.vx = 0
        self.vy = 0
        self.cmd = ''
        self.janela = janela
        self.level = level
        self.facing = 'AFK'

        wall_width = 20
        wall_height = 20
        half_maze_width = (28 * wall_width) / 2
        half_maze_height = (31 * wall_height) / 2

        #coordenadas em relação ao canto superior esquerdo do mapa
        self.newaxis_x = self.x - (self.janela.width / 2 - half_maze_width) + self.width / 2
        self.newaxis_y = self.y - (self.janela.height / 2 - half_maze_height) + self.height / 2

        #coordenadas discretas na matriz level
        self.new_x = self.newaxis_x // wall_width + 1
        self.new_y = self.newaxis_y // wall_height + 1

        #direções para as quais pacman pode ir
        self.can_go_down = self.level[int(self.new_y + 1)][int(self.new_x)] == 0
        self.can_go_up = self.level[int(self.new_y - 1)][int(self.new_x)] == 0
        self.can_go_left = self.level[int(self.new_y)][int(self.new_x - 1)] == 0
        self.can_go_right = self.level[int(self.new_y)][int(self.new_x + 1)] == 0

    def animate(self):
        # Mudança de animação de pacman nas 4 direções cardinais.
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

    def relative_position_of_target(self, target):
        relative_position_x = target.x - self.x
        relative_position_y = target.y - self.y
        return (relative_position_x, relative_position_y)
        
    def move(self, target):
        self.animate()
        if(abs(self.relative_position_of_target(target)[0]) > abs(self.relative_position_of_target(target)[1])):
            # se movimentará na direção horizontal
            if(self.relative_position_of_target(target)[0]>0):
                #vai para a direita
                self.cmd = 'd'
            else:
                #vai para a esquerda
                self.cmd = 'l'
        else:
            #se movimentará na direção vertical
            if(self.relative_position_of_target(target)[1]>0):
                #vai para baixo
                self.cmd = 'd'
            else:
                #vai para cima
                self.cmd = 'u'
        
        #checa para quais direções pacman pode ir
        self.can_go_down = self.level[int(self.new_y + 1)][int(self.new_x)] == 0
        self.can_go_up = self.level[int(self.new_y - 1)][int(self.new_x)] == 0
        self.can_go_left = self.level[int(self.new_y)][int(self.new_x - 1)] == 0
        self.can_go_right = self.level[int(self.new_y)][int(self.new_x + 1)] == 0

        # Determina as tolerâncias de movimento (até quantos pixels errados blinky aceita para fazer curva)
        delta_x = 1
        delta_y = 1
        wall_width = 20
        wall_height = 20
        x_window = (self.new_x - 0.5) * wall_width - delta_x < self.newaxis_x < (self.new_x - 0.5) * wall_width + delta_x
        y_window = (self.new_y - 0.5) * wall_height - delta_y < self.newaxis_y < (self.new_y - 0.5) * wall_height + delta_y
        # Condição para aceitar qualquer input de movimento.
        if x_window:
            if self.cmd == 'd' and self.can_go_down:
                self.cmd = ''
                self.vx = 0
                self.vy = self.base_speed
            if self.cmd == 'u' and self.can_go_up:
                self.cmd = ''
                self.vx = 0
                self.vy = -self.base_speed

        # Movimento HORIZONTAL (REQUERIMENTO DE POSIÇÃO VERTICAL)
        if y_window:
            if self.cmd == 'r' and self.can_go_right:
                self.cmd = ''
                self.vx = self.base_speed
                self.vy = 0
            if self.cmd == 'l' and self.can_go_left:
                self.cmd = ''
                self.vx = -self.base_speed
                self.vy = 0

        if not self.can_go_right and self.vx > 0 and self.newaxis_x >= (self.new_x - 0.5) * wall_width:
            self.vx = 0
        if not self.can_go_left and self.vx < 0 and self.newaxis_x <= (self.new_x - 0.5) * wall_width:
            self.vx = 0
        # Move blinky de acordo com sua velocidade no eixo x
        # self.x += self.vx * dt

        # Checa condição de colisão de blinky com parede em y
        if not self.can_go_up and self.vy < 0 and self.newaxis_y <= (self.new_y - 0.5) * wall_height:
            self.vy = 0
        if not self.can_go_down and self.vy > 0 and self.newaxis_y >= (self.new_y - 0.5) * wall_height:
            self.vy = 0
        # Move blinky de acordo com sua velocidade no eixo y
        # self.y += self.vy * dt


class Point(Sprite):
    def __init__(self, image_file, frames=1):
        # Chama construtor da classe "pai" (sprite).
        super().__init__(image_file, frames)

class PowerUp():
    def __init__(self):
        pass

class Shot():
    def __init__(self):
        pass