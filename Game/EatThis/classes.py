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

    # Ignorar as 2 property e setter abaixo, apenas testando uma forma de incorporar a atualização de parâmetros
    # como blinky_newaxis_x, blinky_newaxis_y, new_x e new_y dentro do próprio objeto player.
    # Funciona, mas isto é uma otimização para mais tarde.
    # TODO: Incorporar parâmetros externos relacionados a classe jogador.

    # Quando objeto.x é chamado, a classe retorna o parametro interno _x.
    @property
    def x(self):
        return self._x

    # Quando blinky.map_x é chamado, ele retorna o valor do parametro interno ._map_x
    @property
    def map_x(self):
        return self._map_x

    # Quando é atribuido um valor a x, ex: blinky.x = 10
    # o valor é atribuido ao parâmetro interno _x e o parametro _map_x recebe o valor deslocado.
    @x.setter
    def x(self, value):
        self._x = value
        self._map_x = self.x - (1280/2 - 28*20/2) + 13

    # Observação: Ainda não sei exatamente os limites e funcionamento interno do @obj.setter e @property
    # aprendi hoje que se chamam "decoradores". Mas parecem cumprir com objetivo. (limpar o código)
    # Porém não é necessário para o funcionamento, então será deixado para mais tarde; vide o "to do" acima.


#   Criar uma classe para todos os elementos do mapa para tirar vantagem
#   para utilizar um atributo e obter melhores comparações.

#   Atualmente objetos são comparados apenas se são 0 ou não zero, ao introduzir "pontos" que pacman come
#   isto pode/vai mudar e todos os espaços da matriz serão objetos, espaços vazios ou paredes, é necessário
#   então uma forma de diferencia-los pois if level[arg1][arg2] != 0 apenas checa por zeros e não é capaz
#   de diferenciar objetos.
#   A classe deve ser criada como a classe players mas adicionando um atributo "self.type".
#   A partir daí podemos definir 1 para "walkable", 2 para "wall", 3 para "ponto normal", 4 para "power-up"
#   e comparar simples através de algo tipo: if level[arg1][arg2].type == 1 or para saber se é um espaço vazio.

class NormalPoint():
    def __init__(self):
        pass

class PowerUp():
    def __init__(self):
        pass

class Shot():
    def __init__(self):
        pass