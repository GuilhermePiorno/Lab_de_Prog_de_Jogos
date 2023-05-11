from PPlay.window import *
from PPlay.sprite import *
from generator import *
from PPlay.gameimage import *

janela = Window(1280, 720)

# Cria o sprite de Blinky e define o número de frames de sua animação.
blinky = Sprite("./Sprites/Blinky.png", 8)


# Chama o maze generator e armazena o labirinto em maze.txt
createlevel()

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
                    if level[i + deslocamento_xy[k]][j + deslocamento_xy[k + 1]] != 0:
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

                wall = GameImage("Sprites/Walls/Curved_20/Wall_" + wall_direction + ".png")
                # wall.width and wall.height should be the same anyway (wall blocks are squares)

                # offset measurement for half of the matrix's PLOTTED width (columns - 2 == len(level["any"] - 2).
                half_maze_width = (len(level[0]) - 2) / 2 * wall.width
                # x offset for column (j) in the matrix
                x_offset = (j - 1) * wall.width
                maze_x = janela.width / 2 - half_maze_width + x_offset

                # offset measurement for half of the matrix's PLOTTED height (lines - 2 == len(level["any"] - 2).
                half_maze_height = (len(level) - 2) / 2 * wall.height
                # y offset for column (i) in the matrix
                y_offset = (i - 1) * wall.height
                maze_y = janela.height / 2 - half_maze_height + y_offset

                wall.set_position(maze_x, maze_y)
                level[i][j] = wall

# O intervalo de frames parece funcionar fechado/aberto -> [Frame_Inicial, Frame Final)
# ex: example.set_sequence_time(0, 1, _total_duration_, _loop_boolean_) mostra apenas o frame 0.
# Duração total da animação em ms, cada animação será mostrada por t/n onde n é o número de frames de animação.
blinky.set_position(janela.width/2 - half_maze_width + wall.width/1.5, janela.height/2 - half_maze_height + wall.height/1.5)
#blinky.set_position(janela.width/2 - half_maze_width + 2 * wall.width - blinky.width / 2,
#                    janela.height/2 - half_maze_height + 2 * wall.height - blinky.height / 2)
blinky.set_sequence_time(0, 8, 100, True)

teclado = Window.get_keyboard()
facing = 'AFK'
# Game-loop
blinky.set_sequence(0, 1, True)

FPS = 0
tempo = 0
cont = 0
vel_x = 0
vel_y = 0

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

    # TODO: Remover ou modularizar esta funcionalidade de gerar mapas para teste.
    #  |========================DEMO MAPS======DELETE ME AFTERWARDS
    if not teclado.key_pressed("a"):
        a = 0
    if teclado.key_pressed("a") and not a:
        a = 1
        createlevel()
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
                            if level[i + deslocamento_xy[k]][j + deslocamento_xy[k + 1]] != 0:
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

                        wall = GameImage("Sprites/Walls/Curved_20_Matrix/Wall_" + wall_direction + ".png")
                        # offset measurement for half of the matrix's PLOTTED width (columns - 2 == len(level["any"] - 2).
                        half_maze_width = (len(level[0]) - 2) / 2 * wall.width
                        # x offset for column (j) in the matrix
                        x_offset = (j - 1) * wall.width
                        maze_x = janela.width / 2 - half_maze_width + x_offset

                        # offset measurement for half of the matrix's PLOTTED height (lines - 2 == len(level["any"] - 2).
                        half_maze_height = (len(level) - 2) / 2 * wall.height
                        # y offset for column (i) in the matrix
                        y_offset = (i - 1) * wall.height
                        maze_y = janela.height / 2 - half_maze_height + y_offset

                        wall.set_position(maze_x, maze_y)
                        level[i][j] = wall
    #  |========================DEMO MAPS======DELETE ME AFTERWARDS

    # Movimento básico para teste de animação, descomente para habilitar.
    if teclado.key_pressed("RIGHT"):
        vel_x = 100
        vel_y = 0
    if teclado.key_pressed("LEFT"):
        vel_x = -100
        vel_y = 0
    if teclado.key_pressed("UP"):
        vel_x = 0
        vel_y = -100
    if teclado.key_pressed("DOWN"):
        vel_x = 0
        vel_y = 100
    if teclado.key_pressed("S"):
        vel_x = vel_y = 0

    blinky.x += vel_x * janela.delta_time()
    blinky.y += vel_y * janela.delta_time()

    # FPS
    tempo += janela.delta_time()
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0

    # Inicialização de objetos
    janela.set_background_color((0, 0, 0))
    # Escreve FPS na tela.
    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))

    # Debug de mudança de sistema de coordenadas.
    # Posição real
    debug_text = "Posição: (" + str(f'{blinky.x:.2f}') + "; " + str(f'{blinky.y:.2f}') + ")"
    janela.draw_text(debug_text, 15, 15, size=25, color=(255, 255, 0))
    # Posição em relação ao 0 da matriz
    eixo_matriz_x = blinky.x - (janela.width/2 - half_maze_width)
    eixo_matriz_y = blinky.y - (janela.height / 2 - half_maze_height)
    debug_text2 = "Eixo Matriz: (" + str(f'{eixo_matriz_x:.2f}') + "; " + str(f'{eixo_matriz_y:.2f}' + ")")
    janela.draw_text(debug_text2, 15, 45, size=25, color=(255, 255, 0))
    # Posição em relação ao novo eixo a ser utilizado
    new_x = (blinky.x - (janela.width/2 - half_maze_width + wall.width/1.5))//wall.width + 2
    new_y = (blinky.y - (janela.height / 2 - half_maze_height + wall.height / 1.5)) // wall.width + 2
    debug_text3 = "New Axis: (" + str(f'{new_x:.2f}') + "; " + str(f'{new_y:.2f}') + ")"
    janela.draw_text(debug_text3, 15, 75, size=25, color=(255, 255, 0))
    # Draw
    # level[1][5].draw()

    for i in range(33):
        for j in range(1, 29):
            if level[i][j] != 0:
                level[i][j].draw()
    blinky.draw()
    blinky.update()
    janela.update()
