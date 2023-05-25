from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from EatThis.procedural_map import *
from EatThis.map_fill import *
#from EatThis.Classes.classes import Player
from EatThis.pacman_moves import *
import random
from EatThis.Classes.Level import *
from EatThis.Classes.Enemy import *
from EatThis.Classes.Player import *
import time


print("Hotkeys:")
print("        N - Gera mapa novo")
print("        G - Liga/Desliga Grid")
print("        M - Liga/Desliga Música")

# Inicialização.
janela = Window(1280, 720)
janela.set_title("Eat This!")
teclado = janela.get_keyboard()
walltype = 'Curved_20'
TesteDebugMapa = False
buffer = 0  # Buffer para pressionar botão direcional.
cmd = ''
pacman_cmd = ''
grid_toggle = False
BGM_Toggle = True

# Background Music.
bgm = Sound("music/Unreal Super Hero 3 by Kenet & Rez.mp3")
bgm.set_volume(5)
bgm.set_repeat(True)
bgm.play()

# cria o objeto maze
maze = Level(walltype, janela)

# Cria o sprite de Blinky e define o número de frames de sua animação.
# blinky = Sprite("./Sprites/Blinky.png", 8)
blinky = Player(janela, maze, "./Sprites/Blinky.png", 8)
blinky.set_position(janela.width / 2 - maze.half_maze_width + (maze.wall.width * 1.5 - blinky.width / 2),
                    janela.height / 2 - maze.half_maze_height + (maze.wall.height * 1.5 - blinky.height / 2))
blinky.set_sequence_time(0, 8, 100, True)
blinky.set_sequence(0, 1, True)
# facing = 'AFK'

# Cria o sprite de Pacman e define o número de frames de sua animação.
pacman = Enemy(janela, maze, "./Sprites/pacman.png", 8)
pacman.set_position(janela.width / 2 + maze.half_maze_width - (maze.wall.width * 1.5 + pacman.width / 2),
                    janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pacman.height / 2))
pacman.set_sequence_time(0, 8, 100, True)
pacman.set_sequence(0, 1, True)

# Portal_Esquerdo
portal_esquerdo = Sprite("Sprites/Walls/" + walltype + "/Portal_L.png", 3)
portal_esquerdo.set_sequence_time(0, 3, 100, True)
portal_esquerdo.set_sequence(0, 3, True)
portal_esquerdo.set_position(janela.width / 2 - maze.half_maze_width - maze.wall.width,
                             janela.height / 2 - maze.half_maze_height + 13.5 * maze.wall.height - 1)

# Portal_Direito
portal_direito = Sprite("Sprites/Walls/" + walltype + "/Portal_D.png", 3)
portal_direito.set_sequence_time(0, 3, 100, True)
portal_direito.set_sequence(0, 3, True)
portal_direito.set_position(janela.width / 2 + maze.half_maze_width,
                            janela.height / 2 - maze.half_maze_height + 13.5 * maze.wall.height - 1)

# Inicia variáveis para o FPS.
FPS = 0
tempo = 0
cont = 0
# Game-loop
while True:
    # Leitura de Entradas

    dt = janela.delta_time()

    # Código para a geração do mapa para testes.
    if not teclado.key_pressed("N") and not teclado.key_pressed("G") and not teclado.key_pressed("M"):
        TesteDebugMapa = False
    if teclado.key_pressed("N") and not TesteDebugMapa:
        maze = Level(walltype, janela)
        blinky.level = maze  # Atualiza o level do blinky
        pacman.level = maze  # Atualiza o level do pacman
        TesteDebugMapa = True

    if teclado.key_pressed("G") and not TesteDebugMapa:
        if grid_toggle:
            grid_toggle = False
            walltype = walltype.split("_")[0] + "_" + walltype.split("_")[1]
        else:
            grid_toggle = True
            walltype += '_Matrix'
        TesteDebugMapa = True
        maze.walltype = walltype  # Atualiza o walltype do maze
        maze.level = maze.fill_level()  # Atualiza o level do maze para incluir a walltype nova
    blinky.get_flow_field()
    # print(blinky.sinkmatrix[int(pacman.matrix_position[1])][int(pacman.matrix_position[0])])
    # print(blinky.matrix_position)
    # print(blinky.sinkmatrix)
    print(pacman.matrix_position)
    if teclado.key_pressed("M") and not TesteDebugMapa:
        if BGM_Toggle:
            BGM_Toggle = False
            bgm.pause()
            s = time.time()
            blinky.get_flow_field()
            f = time.time()
            # 0.0004994869232177734
            print(f-s)
        else:
            BGM_Toggle = True
            bgm.unpause()
        TesteDebugMapa = True


    # Atualiza buffer de inputs
    blinky.buffer += dt
    
    blinky.move1()
    blinky.x += blinky.vx * dt
    blinky.y += blinky.vy * dt

    pacman.move1(blinky)
    pacman.x += pacman.vx * dt
    pacman.y += pacman.vy * dt

    # FPS
    tempo += dt
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0

    janela.set_background_color((0, 0, 0))
    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))
    maze.draw()
    blinky.draw()
    blinky.update()
    pacman.draw()
    pacman.update()
    portal_esquerdo.draw()
    portal_esquerdo.update()
    portal_direito.draw()
    portal_direito.update()    
    janela.draw_text("pacman_cmd: " + str(pacman.cmd), 30, 30, 30, color=(255,0,0))
    janela.update()
