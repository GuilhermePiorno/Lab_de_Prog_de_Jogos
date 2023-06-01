from PPlay.sprite import *
from PPlay.gameimage import *

class PowerUp(GameImage):
    def __init__(self, image_file, coordinates):
        super().__init__(image_file)
        self.line = coordinates[0]
        self.column = coordinates[1]
        self.was_eaten = False