from PPlay import sprite


class Player(sprite.Sprite):
    def __init__(self, image_file, frames=1):
        # Chama construtor da classe "pai" (sprite).
        sprite.Sprite.__init__(self, image_file, frames)

        # Modificadores de movimento
        self.base_speed = 100
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

#   Criar uma classe para todos os elementos do mapa para tirar vantagem
#   para utilizar um atributo e obter melhores comparações.

#   Atualmente objetos são comparados apenas se são 0 ou não zero, ao introduzir "pontos" que pacman come
#   isto pode/vai mudar e todos os espaços da matriz serão objetos, espaços vazios ou paredes, é necessário
#   então uma forma de diferencia-los pois if level[arg1][arg2] != 0 apenas checa por zeros e não é capaz
#   de diferenciar objetos.
#   A classe deve ser criada como a classe players mas adicionando um atributo "self.type".
#   A partir daí podemos definir 1 para "walkable", 2 para "wall", 3 para "ponto normal", 4 para "power-up"
#   e comparar simples através de algo tipo: if level[arg1][arg2].type == 1 or para saber se é um espaço vazio.

