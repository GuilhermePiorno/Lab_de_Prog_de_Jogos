from PPlay.window import *
from PPlay.sprite import *
from generator import *
from PPlay.gameimage import *

janela = Window(1920, 1080)

# Cria o sprite de Blinky e define o número de frames de sua animação.
blinky = Sprite("./Sprites/Blinky.png", 8)
blinky.set_position(janela.width / 2 - blinky.width / 2, janela.height / 2 - blinky.height / 2)

# Chama o maze generator e armazena o labirinto em maze.txt
# createlevel()

# Acessa o labirinto criado e armazena os sprites criados em uma matriz para depois ser desenhada
with open('maze.txt', mode='r', encoding='utf-8') as fin:
    i = 0
    # linha 0 e linha 32 são vazias.
    level = [[0] * 30 for _ in range(33)]
    for linha in fin:
        for j in range(len(linha)):
            if linha[j] == '|':
                level[i][j + 1] = 1
            else:
                level[i][j + 1] = 0
        i += 1

    # Altera o sprite das paredes para fazerem sentido
    deslocamento_xy = [-1, 0, 1, 0, -1]
    deslocamento_diagonal = [-1, 1, 1, -1, -1]
    for i in range(1, 32):  # linhas 0 e 32 estão sempre vazias
        for j in range(1, 29):  # colunas 0 e 29 estão sempre vazias
            if level[i][j] == 1:
                wall_direction = ''
                for k in range(4):
                    if level[i+deslocamento_xy[k]][j+deslocamento_xy[k+1]] != 0:
                        if k == 0:
                            wall_direction += 'U'
                        elif k == 1:
                            wall_direction += 'R'
                        elif k == 2:
                            wall_direction += 'D'
                        elif k == 3:
                            wall_direction += 'L'
                if wall_direction == 'URDL':
                    for k in range(4):
                        if level[i + deslocamento_diagonal[k]][j + deslocamento_diagonal[k + 1]] == 0:
                            if k == 0:
                                wall_direction = 'UR'
                            elif k == 1:
                                wall_direction = 'RD'
                            elif k == 2:
                                wall_direction = 'DL'
                            elif k == 3:
                                wall_direction = 'UL'

                wall = GameImage("Sprites/Wall_" + wall_direction + ".png")
                # wall = GameImage("Sprites/Wall_RL.png")
                # Como cada bloco é 34x34, 32 garante a sobreposição do último pixel de cada lado.
                wall.set_position((j - 1) * 34, (i - 1) * 34)
                level[i][j] = wall

# O intervalo de frames parece funcionar fechado/aberto -> [Frame_Inicial, Frame Final)
# ex: example.set_sequence_time(0, 1, _total_duration_, _loop_boolean_) mostra apenas o frame 0.
# Duração total da animação em ms, cada animação será mostrada por t/n onde n é o número de frames de animação.
blinky.set_sequence_time(0, 8, 100, True)

teclado = Window.get_keyboard()
facing = 'AFK'
# Game-loop
blinky.set_sequence(0, 1, True)

FPS = 0
tempo = 0
cont = 0

while True:
    # Leitura de Entradas

    # Mudança de animação de Blinky nas 4 direções cardinais.
    if teclado.key_pressed("UP") and facing != 'U':
        facing = 'U'
        blinky.set_sequence(6, 8, True)
    if teclado.key_pressed("DOWN") and facing != 'D':
        facing = 'D'
        blinky.set_sequence(4, 6, True)
    if teclado.key_pressed("LEFT") and facing != 'L':
        facing = 'L'
        blinky.set_sequence(2, 4, True)
    if teclado.key_pressed("RIGHT") and facing != 'R':
        facing = 'R'
        blinky.set_sequence(0, 2, True)

    # Movimento básico para teste de animação, descomente para habilitar.
    blinky.move_key_x(0.1)
    blinky.move_key_y(0.1)

    # FPS
    tempo += janela.delta_time()
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0

    # Inicialização de objetos
    janela.set_background_color((0, 0, 0))

    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))

    # Draw
    # level[1][5].draw()

    for i in range(33):
        for j in range(1, 29):
            if level[i][j] != 0:
                level[i][j].draw()
    blinky.draw()
    blinky.update()
    janela.update()
