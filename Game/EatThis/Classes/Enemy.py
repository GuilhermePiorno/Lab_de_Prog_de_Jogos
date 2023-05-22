from PPlay.sprite import *


class Enemy(Sprite):
    def __init__(self, window, level, image_file, initial_position, frames=1):
        super().__init__(image_file, frames)
        self.vx = 0
        self.vy = 0
        self.base_speed = 100
        self.cmd = ''
        self.window = window
        self.level = level
        self.facing = 'AFK'
        self.maze_axis = (self.x - (window.width / 2 - half_maze_width) + self.width / 2, 
                          self.y - (window.height / 2 - half_maze_heigth) + self.height / 2)
        self.matrix_position = (self.maze_axis[0] // wall.width + 1, self.maze_axis[1] // wall.width + 1)

    def get_maze_axis(self):
        return (self.x - (window.width / 2 - half_maze_width) + self.width / 2, 
                self.y - (window.height / 2 - half_maze_heigth) + self.height / 2)

    def get_matrix_position(self):
        return ((self.x - (window.width / 2 - half_maze_width) + self.width / 2) // wall.width + 1, 
                (self.y - (window.height / 2 - half_maze_heigth) + self.height / 2) // wall.width + 1)

    def set_maze_axis(self):
        pass

    def set_matrix_position(self):
        pass
