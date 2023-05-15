from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from EatThis.procedural_map import *
from EatThis.map_fill import *
from EatThis.classes import *


# TODO: Criar uma superclasse chamada jogador, assim é possível instanciar blinky através de:
#  blinky = Player("./Sprites/Blinky.png", 8) e utilizar atributos novos como blinky.vx, blinky.vy e etc.

"""
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
"""

# Inicialização.
janela = Window(1280, 720)
teclado = Window.get_keyboard()
walltype = 'Curved_20'
TesteDebugMapa = False
buffer = 0  # Buffer para pressionar botão direcional.
cmd = ''
grid_toggle = False

# Background Music.
bgm = Sound("music/Unreal Super Hero 3 by Kenet & Rez.mp3")
bgm.set_volume(5)
bgm.set_repeat(True)
bgm.play()

# Criação da fase inicial
createlevel()
level = fill_level(walltype, janela)

# Extrai tamanho do bloco de parede a partir da variável walltype.
# TODO: Arrumar um jeito de não iniciar blocos e variáveis "atoa".
wall = GameImage("Sprites/Walls/" + walltype + "/Wall_URDL.png")
half_maze_width = (28 * wall.width) / 2
half_maze_height = (31 * wall.height) / 2

# Cria o sprite de Blinky e define o número de frames de sua animação.
# blinky = Sprite("./Sprites/Blinky.png", 8)
blinky = Player("./Sprites/Blinky.png", 8)
blinky.set_position(janela.width / 2 - half_maze_width + (wall.width * 1.5 - blinky.width / 2),
                    janela.height / 2 - half_maze_height + (wall.height * 1.5 - blinky.height / 2))
blinky.set_sequence_time(0, 8, 100, True)
blinky.set_sequence(0, 1, True)
facing = 'AFK'

# Portal_Esquerdo
portal_esquerdo = Sprite("Sprites/Walls/" + walltype + "/Portal_L.png", 3)
portal_esquerdo.set_sequence_time(0, 3, 100, True)
portal_esquerdo.set_sequence(0, 3, True)
portal_esquerdo.set_position(janela.width / 2 - half_maze_width - wall.width,
                             janela.height / 2 - half_maze_height + 13.5 * wall.height - 1)

# Portal_Direito
portal_direito = Sprite("Sprites/Walls/" + walltype + "/Portal_D.png", 3)
portal_direito.set_sequence_time(0, 3, 100, True)
portal_direito.set_sequence(0, 3, True)
portal_direito.set_position(janela.width / 2 + half_maze_width,
                            janela.height / 2 - half_maze_height + 13.5 * wall.height - 1)

# Inicia variáveis para o FPS.
FPS = 0
tempo = 0
cont = 0
# Game-loop
while True:
    # Leitura de Entradas
    # Mudança de animação de Blinky nas 4 direções cardinais.
    if blinky.vy < 0 and facing != 'U':
        facing = 'U'
        blinky.set_sequence(6, 8, True)
    if blinky.vy > 0 and facing != 'D':
        facing = 'D'
        blinky.set_sequence(4, 6, True)
    if blinky.vx < 0 and facing != 'L':
        facing = 'L'
        blinky.set_sequence(2, 4, True)
    if blinky.vx > 0 and facing != 'R':
        facing = 'R'
        blinky.set_sequence(0, 2, True)

    # Código para a geração do mapa para testes.
    if not teclado.key_pressed("A") and not teclado.key_pressed("G"):
        TesteDebugMapa = False
    if teclado.key_pressed("A") and not TesteDebugMapa:
        createlevel()
        level = fill_level(walltype, janela)
        TesteDebugMapa = True

    if teclado.key_pressed("G") and not TesteDebugMapa:
        if grid_toggle:
            grid_toggle = False
            walltype = walltype.split("_")[0] + "_" + walltype.split("_")[1]
        else:
            grid_toggle = True
            walltype += '_Matrix'
        TesteDebugMapa = True
        level = fill_level(walltype, janela)

    # Atualiza buffer de inputs
    buffer += janela.delta_time()

    if teclado.key_pressed("UP"):
        buffer = 0
        cmd = 'u'

    if teclado.key_pressed("DOWN"):
        buffer = 0
        cmd = 'd'

    if teclado.key_pressed("RIGHT"):
        buffer = 0
        cmd = 'r'

    if teclado.key_pressed("LEFT"):
        buffer = 0
        cmd = 'l'

    # Coordenadas do blinky em relação ao 0 da fase
    blinky_newaxis_x = blinky.x - (janela.width / 2 - half_maze_width) + blinky.width / 2
    blinky_newaxis_y = blinky.y - (janela.height / 2 - half_maze_height) + blinky.height / 2

    # Versão discretizada das coordenadas com ajuste (+1) para correspondencia a matriz "level".
    new_x = blinky_newaxis_x // wall.width + 1
    new_y = blinky_newaxis_y // wall.height + 1

    can_go_down = level[int(new_y + 1)][int(new_x)] == 0
    can_go_up = level[int(new_y - 1)][int(new_x)] == 0
    can_go_left = level[int(new_y)][int(new_x - 1)] == 0
    can_go_right = level[int(new_y)][int(new_x + 1)] == 0

    # Determina as tolerâncias de movimento (até quantos pixels errados blinky aceita para fazer curva)
    delta_x = 1
    delta_y = 1
    x_window = (new_x - 0.5) * wall.width - delta_x < blinky_newaxis_x < (new_x - 0.5) * wall.width + delta_x
    y_window = (new_y - 0.5) * wall.height - delta_y < blinky_newaxis_y < (new_y - 0.5) * wall.height + delta_y
    # Condição para aceitar qualquer input de movimento.
    if buffer < 0.5:
        # Movimento VERTICAL (REQUERIMENTO DE POSIÇÃO HORIZONTAL)
        if x_window:
            if cmd == 'd' and can_go_down:
                cmd = ''
                blinky.vx = 0
                blinky.vy = blinky.base_speed
            if cmd == 'u' and can_go_up:
                cmd = ''
                blinky.vx = 0
                blinky.vy = -blinky.base_speed

        # Movimento HORIZONTAL (REQUERIMENTO DE POSIÇÃO VERTICAL)
        if y_window:
            if cmd == 'r' and can_go_right:
                cmd = ''
                blinky.vx = blinky.base_speed
                blinky.vy = 0
            if cmd == 'l' and can_go_left:
                cmd = ''
                blinky.vx = -blinky.base_speed
                blinky.vy = 0

    # Para debug (S to stop)
    if teclado.key_pressed("S"):
        blinky.vx = blinky.vy = 0

    # TODO: As vezes blinky anda demais antes de sua velocidade ser reduzida a zero,
    #  similar ao problema de deslizamento do pong. Este problema foi remediado colocando a atualização de posição
    #  após o check de reset e devido as velocidades baixas, mas caso a velocidade suba acima de 350 o problema retorna.
    #  Velocidades acima de 350 são ruins de jogar, então o problema foi temporariamente ignorado.
    # Checa condição de colisão de blinky com parede em x
    if not can_go_right and blinky.vx > 0 and blinky_newaxis_x >= (new_x - 0.5) * wall.width:
        blinky.vx = 0
    if not can_go_left and blinky.vx < 0 and blinky_newaxis_x <= (new_x - 0.5) * wall.width:
        blinky.vx = 0
    blinky.x += blinky.vx * janela.delta_time()

    # Checa condição de colisão de blinky com parede em y
    if not can_go_up and blinky.vy < 0 and blinky_newaxis_y <= (new_y - 0.5) * wall.height:
        blinky.vy = 0
    if not can_go_down and blinky.vy > 0 and blinky_newaxis_y >= (new_y - 0.5) * wall.height:
        blinky.vy = 0
    blinky.y += blinky.vy * janela.delta_time()

    # Checa colisão de blinky com portal esquerdo.
    if blinky_newaxis_x < 0 + wall.width / 2:  # aka: 0 + 20/2 = 10
        blinky.x += 2 * half_maze_width - wall.width

    # Checa colisão de blinky com portal direito.
    if blinky_newaxis_x > 28 * wall.width - wall.width / 2:  # aka: 28*20 - 20/2 550
        blinky.x -= 2 * half_maze_width - wall.width

    # FPS
    tempo += janela.delta_time()
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0

    janela.set_background_color((0, 0, 0))
    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))

    for i in range(33):
        for j in range(1, 29):
            if level[i][j] != 0:
                level[i][j].draw()

    blinky.draw()
    blinky.update()
    portal_esquerdo.draw()
    portal_esquerdo.update()
    portal_direito.draw()
    portal_direito.update()
    janela.update()
