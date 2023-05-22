from PPlay.sprite import *

class Player(Sprite):
    def __init__(self, janela, level, image_file, frames=1):
        super().__init__(image_file, frames)