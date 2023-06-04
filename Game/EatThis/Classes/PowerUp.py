from PPlay.sprite import *
from PPlay.gameimage import *
from EatThis.Classes.Point import *

class PowerUp(Point):
    def __init__(self, image_file, coordinates, window, path):
        super().__init__(image_file, coordinates, window, path)
        self.line = coordinates[0]
        self.column = coordinates[1]
        self.was_eaten = False


