from PPlay.sprite import *
from EatThis.Classes.Blast import *

class Bomb(Sprite):
    def __init__(self, game_image, maze, player):
        super().__init__(game_image, frames=2)
        self.timer = 0
        self.explode_time = 5
        self.exploded = False
        self.maze = maze
        self.window = player.window
        self.set_position(player.x + player.width/2 - self.width/2, player.y + player.height/2 - self.height/2)
        self.set_total_duration(1000)
        self.set_sequence(0, 2, True)

    def explode(self):
        self.exploded = True
        blast_list = []
        blast = Blast("Assets\Sprites\VFX\explosion.png")
        blast.set_position(self.x, self.y)
        blast_list.append(blast)
        blast_radius = self.generate_blast_radius()
        
        #desenha as explosões para cima, para baixo, para a esquerda e para a direita
        for i in range(blast_radius[0]):
            blast = Blast("Assets\Sprites\VFX\explosion.png")
            blast.set_position(self.x, self.y - i*20)
            blast_list.append(blast)

        for i in range(blast_radius[1]):
            blast = Blast("Assets\Sprites\VFX\explosion.png")
            blast.set_position(self.x, self.y + i*20)
            blast_list.append(blast)

        for i in range(blast_radius[2]):
            blast = Blast("Assets\Sprites\VFX\explosion.png")
            blast.set_position(self.x - i*20, self.y)
            blast_list.append(blast)

        for i in range(blast_radius[3]):
            blast = Blast("Assets\Sprites\VFX\explosion.png")
            blast.set_position(self.x + i*20, self.y)
            blast_list.append(blast)

        print(len(blast_list))
        return blast_list

    def generate_blast_radius(self):
        bomb_coordinates = self.get_matrix_coordinates() #coordenadas da bomba
        level = self.maze.pathing #usa a matriz pathing para verificar quais células devem ser afetadas pela explosão da bomba

        #contadores de quantas células em cada direção serão afetadas pela explosão. Ex se 'cima' = 2, 
        # as duas células acima da bomba serão afetadas pela explosão
        up = 0
        down = 0
        right = 0
        left = 0

        #checa se tem corredor para cima
        matrix_cell = level[bomb_coordinates[0] - 1][bomb_coordinates[1]]
        while(matrix_cell != 1):
            up += 1
            matrix_cell = level[bomb_coordinates[0] - 1 - up][bomb_coordinates[1]]

        #checa se tem corredor para baixo
        matrix_cell = level[bomb_coordinates[0] + 1][bomb_coordinates[1]]
        while(matrix_cell != 1):
            down += 1
            matrix_cell = level[bomb_coordinates[0] + 1 + down][bomb_coordinates[1]]

        #checa se tem corredor para a direita
        matrix_cell = level[bomb_coordinates[0]][bomb_coordinates[1] + 1]
        while(matrix_cell != 1):
            right += 1
            matrix_cell = level[bomb_coordinates[0]][bomb_coordinates[1] + 1 + right]

        #checa se tem corredor para a esquerda
        matrix_cell = level[bomb_coordinates[0]][bomb_coordinates[1] - 1]
        while(matrix_cell != 1):
            left += 1
            matrix_cell = level[bomb_coordinates[0]][bomb_coordinates[1] - 1 - left]
        
        return [up, down, left, right]

    def get_matrix_coordinates(self):
        """Retorna tupla (linha, coluna)"""
        return (
            int((self.y - (self.window.height / 2 - self.maze.half_maze_height) + self.height / 2) // self.maze.wall.width + 1),
            int((self.x - (self.window.width / 2 - self.maze.half_maze_width) + self.width / 2) // self.maze.wall.width + 1)
            )
