from PPlay.sprite import *

class Trap(Sprite):
    def __init__(self, image_file, player, frames=1):
        super().__init__(image_file, frames)
        self.set_position(player.x + player.width/2 - self.width/2, player.y + player.height/2 - self.height/2)
        self.was_eaten = False