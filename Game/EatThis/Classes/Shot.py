from PPlay.sprite import *

class Shot(Sprite):
    def __init__(self, image_file, shooter, frames):
        super().__init__(image_file, frames)
        self.direction = shooter.facing
        self.base_speed = max(abs(shooter.vx), abs(shooter.vy)) + 40
        self.hit_enemy = False
        if(shooter.facing == "U"):
            #tiro para cima
            self.vx = 0
            self.vy = -self.base_speed
            self.set_position((shooter.x + shooter.width/2) - self.width/2, shooter.y - self.height)
        elif(shooter.facing == "D"):
            #tiro para baixo
            self.vx = 0
            self.vy = self.base_speed
            self.set_position((shooter.x + shooter.width/2) - self.width/2, shooter.y + shooter.height)
        elif(shooter.facing == "L"):
            #tiro para a esquerda
            self.vx = -self.base_speed
            self.vy = 0
            self.set_position(shooter.x - self.width, shooter.y + shooter.height/2 - self.height/2)
        elif(shooter.facing == "R"):
            #tiro para a direita
            self.vx = self.base_speed
            self.vy = 0
            self.set_position(shooter.x + shooter.width, shooter.y + shooter.height/2 - self.height/2)
        else:
            #blinky afk - está crashando o jogo
            pass
