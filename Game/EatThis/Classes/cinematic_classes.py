from PPlay.sprite import *



class Actor(Sprite):
    resizer = pygame.transform.scale
    def __init__(self, image_file, frames=1):
        # Chama construtor da classe "pai" (sprite).
        super().__init__(image_file, frames)

        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.f = ""
        self.size = [self.width, self.height]
        self.original_image = pygame.image.load(image_file).convert_alpha()
        self.img = self.resizer(self.original_image, self.size)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.Rect(self.x, self.y, self.width, self.height)

    def change_size(self, factor):
        self.size[1] += factor
        self.size[0] = self.size[1] * self.width//self.height
        self.img = self.resizer(self.original_image, self.size)
        # self.rect = self.image.get_rect(center=(self.x+self.width/2, self.y+self.height/2))
        self.rect = self.img.get_rect(center=(self.x+self.width/2, self.y+(self.height/2)))
        # print(self.original_image.get_width() - self.img.get_width())
        # self.x -= 1



        # self.rect = self.rect.move([0, -0.6])
        # self.rect[1] -= 1
        # self.rect[0] -= 1

        # rect_x = self.x + self.width / 2
        # rect_y = self.y + self.height / 2
        # self.rect = self.image.get_rect(center=(rect_x, rect_y))
        # print(self.rect)
        # print(vector_x, vector_y)

    def change_transparency(self, alpha):
        self.img.fill((255,255,255,alpha), None, pygame.BLEND_RGBA_MULT)
