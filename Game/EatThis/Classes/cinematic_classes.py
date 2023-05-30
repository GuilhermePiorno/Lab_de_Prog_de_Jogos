from PPlay.sprite import *

# TODO classe similar a classe Player, criada separadamente para evitar conflitos devido a
#  futuras alterações na classe Player. Considerar unificação das classes no futuro.
class Actor(Sprite):
    def __init__(self, image_file, frames=1):
        # Chama construtor da classe "pai" (sprite).
        super().__init__(image_file, frames)

        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.f = ""