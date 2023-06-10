from PPlay.sprite import *
from EatThis.a_star import *
from EatThis.Classes.Point import *
from EatThis.Classes.PowerUp import *
from PPlay.sound import *
import time

class Enemy(Sprite):
    def __init__(self, name, window, maze, save, image_file, frames=1):
        super().__init__(image_file, frames)
        self.name = name
        self.save = save
        self.state = "hungry"  # hungry, afraid e angry
        self.base_fear_time = 5
        self.fear_timer = 0.0
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
        self.is_dying = False
        self.is_dead = False
        self.death_instant = 0
        self.distance_list = []
        self.nearest_point = self.get_next_closest_point()

    def move1(self, target):
        if len(self.maze.list_of_points) == 0:
            print("game over")

        if self.get_matrix_coordinates() == target.get_matrix_coordinates() and target.state == "invulnerable" and not self.is_dead:
            self.die()

        # Detecta se pacman comeu powerup
        if isinstance(self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]], PowerUp):
            self.maze.powerup_num -= 1
            if target.state != "vulnerable":
                target.change_state()


        # pacman comendo os pontos remove pontos normais ou powerups ao serem comidos.
        if isinstance(self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]], Point):
            self.maze.level[self.get_matrix_coordinates()[0]][self.get_matrix_coordinates()[1]] = 0 # deleta o ponto.

            for i in range(len(self.maze.list_of_points)):
                if self.get_matrix_coordinates() == self.maze.list_of_points[i]:
                    del self.maze.list_of_points[i]
                    break



        # Coordenadas do pacman em relação ao 0 da fase
        self.maze_axis = self.get_maze_axis()
        

        #Versão discretizada das coordenadas do pacman com ajuste (+1) para correspondencia a matriz "level".
        self.matrix_coordinates = self.get_matrix_coordinates()
        

        can_go_down = (self.maze.pathing[int(self.matrix_coordinates[0] + 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_up = (self.maze.pathing[int(self.matrix_coordinates[0] - 1)][int(self.matrix_coordinates[1])] == 0)
        can_go_left = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] - 1)] == 0)
        can_go_right = (self.maze.pathing[int(self.matrix_coordinates[0])][int(self.matrix_coordinates[1] + 1)] == 0)



        # ia do pacman baseada no algoritmo flowfield
        if not self.is_dying and not self.is_dead:
            self.animate()

            # Faz pacman voltar ao estado "hungry" após self.fear_timer expirar.
            if self.fear_timer > 0 and self.state == "afraid":
                self.fear_timer -= self.window.delta_time()
            else:
                self.state = "hungry"

            if target.state == "vulnerable" or target.state == "transition":
                self.state = "angry"

            # Estado padrão do pacman
            if self.state == "hungry":
                # Se houverem pontos para ser comidos
                if len(self.maze.list_of_points) > 0:
                    # Decide se é realmente necessário atualizar flowfield (melhora de performance).
                    aux = self.get_next_closest_point()
                    if self.nearest_point != aux:
                        self.nearest_point = aux
                        self.maze.level[self.nearest_point[1][0]][self.nearest_point[1][1]].get_flow_field()

                    self.ia_pacman_follow(self.maze.level[self.nearest_point[1][0]][self.nearest_point[1][1]])
                else:
                    # Segue blinky
                    self.ia_pacman_follow(target)
            elif self.state == "afraid":
                self.ia_pacman_run_away(target)
            elif self.state == "angry":
                self.ia_pacman_follow(target)

            # distância entre os dois pontos => dist = (delta_x**2 + delta_y**2)^0.5
            direct_distance = self.relative_position_of_target(target)[0]**2
            direct_distance += self.relative_position_of_target(target)[1]**2
            direct_distance = direct_distance**0.5

            if direct_distance <= 100 and target.state != "vulnerable":
                self.fear_timer = self.base_fear_time
                self.state = "afraid"

        else:
            if time.time() - self.death_instant >= 2:
                self.is_dead = True

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
        if not self.is_dying:
            self.death_instant = time.time()
            self.is_dying = True
            self.death_rattle()
            self.set_sequence_time(9, 22, 100, False)
        self.vx = 0
        self.vy = 0


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
        """Retorna tupla (linha, coluna)"""
        return (
            int((self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1),
            int((self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1)
            )

    # Função utiliza o atributo maze.list_of_points para resgatar a lista de pontos e cria uma lista de
    # listas chama "distances_list" que armazenam a distancia entre si e os pontos e as coordenadas dos pontos.
    # Ex: Se maze.list_of_points é [(2, 3), (9, 4)]
    # distances_list será algo do tipo: [[5.3, (2, 3)], [20.1, (9, 4)]]
    # distances_list[0] diz "Existe um ponto em (2, 3) que está a 5.3 unidades de distância.
    # distances_list[1] diz "Existe um ponto em (9, 4) que está a 20.1 unidades de distância.
    # A função retorna o elemento com a menor distância, neste caso a função retornaria min_dist = [5.3, (2, 3)]
    # Observação: maze.list_of_points inclue TODOS os pontos, ou seja, pontos normais e powerups.
    def get_next_closest_point(self):
        """
        Retorna uma lista composta da distancia do ponto e uma tupla (linha, coluna) do ponto.
        Saida: [distancia, (ponto_linha, ponto_coluna)]

        :returns [float distancia, (int ponto_linha, int ponto_coluna)]
        """
        distances_list = []
        min_dist = [42.0, (0, 0)]
        for i in range(len(self.maze.list_of_points)):
            distances_list.append((self.points_distance(self.maze.list_of_points[i]), self.maze.list_of_points[i]))
            if min_dist[0] > distances_list[i][0]:
                min_dist = distances_list[i]
        self.distance_list = distances_list
        return min_dist


    def points_distance(self, tupla):
        return ((self.matrix_coordinates[0] - tupla[0]) ** 2 + (self.matrix_coordinates[1] - tupla[1]) ** 2)**0.5

    def death_rattle(self):
        DeathCry = Sound("Assets/SFX/PacmanDeath.mp3")
        DeathCry.set_volume(self.save.SFX_vol * self.save.Master_vol)
        DeathCry.play()
