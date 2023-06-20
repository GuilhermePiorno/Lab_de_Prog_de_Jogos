from PPlay.sprite import *
from EatThis.Classes.Point import *

class Shot(Sprite):
    def __init__(self, image_file, shooter, frames):
        super().__init__(image_file, frames)
        self.direction = shooter.facing
        self.base_speed = max(abs(shooter.vx), abs(shooter.vy)) + 40
        self.hit_enemy = False
        self.hit_wall = False
        self.out_of_bounds = False
        self.window = shooter.window
        self.maze = shooter.maze
        self.set_total_duration(1000)
        if(shooter.facing == "U"):
            #tiro para cima
            self.vx = 0
            self.vy = -self.base_speed
            self.set_position((shooter.x + shooter.width/2) - self.width/2, shooter.y - self.height)
            self.set_sequence(6, 8, True)
        elif(shooter.facing == "D"):
            #tiro para baixo
            self.vx = 0
            self.vy = self.base_speed
            self.set_position((shooter.x + shooter.width/2) - self.width/2, shooter.y + shooter.height)
            self.set_sequence(4, 6, True)
        elif(shooter.facing == "L"):
            #tiro para a esquerda
            self.vx = -self.base_speed
            self.vy = 0
            self.set_position(shooter.x - self.width, shooter.y + shooter.height/2 - self.height/2)
            self.set_sequence(2, 4, True)
        elif(shooter.facing == "R"):
            #tiro para a direita
            self.vx = self.base_speed
            self.vy = 0
            self.set_position(shooter.x + shooter.width, shooter.y + shooter.height/2 - self.height/2)
            self.set_sequence(0, 2, True)
        else:
            #blinky afk - está crashando o jogo
            pass

    def check_collision_with_wall(self):
        coordinate = self.get_matrix_coordinates()
        if(not(isinstance(self.maze.level[coordinate[0]][coordinate[1]], Point) or self.maze.level[coordinate[0]][coordinate[1]] == 0)):
            self.hit_wall = True

    def check_inside_maze_boundary(self):
        coordinate = self.get_matrix_coordinates()
        if(coordinate[0] > 30 or coordinate[0] < 1 or coordinate[1] > 28 or coordinate[1] < 1):
            self.out_of_bounds = True

    def get_matrix_coordinates(self):
        return ( 
            int((self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1),
            int((self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1)
            )
