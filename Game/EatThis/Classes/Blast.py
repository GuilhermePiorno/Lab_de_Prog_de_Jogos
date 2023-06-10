from PPlay.sprite import *
from time import *

class Blast(Sprite):
    def __init__(self, image_file):
        super().__init__(image_file, frames=1)
        self.delta_time = 2
        self.creation_instant = time()
        self.exists = True

    def disappear(self):
        if((time() - self.creation_instant) > self.delta_time):
            self.exists = False