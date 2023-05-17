from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from EatThis.procedural_map import *
from EatThis.map_fill import *
from EatThis.classes import *


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

# Cria o sprite de Pacman e define o número de frames de sua animação.
pacman = Sprite("./Sprites/pacman.png", 8)
pacman.set_position(janela.width / 2 + half_maze_width - (wall.width * 1.5 + pacman.width / 2),
                    janela.height / 2 + half_maze_height - (wall.height * 1.5 + pacman.height / 2))
pacman.set_sequence_time(0, 8, 100, True)
pacman.set_sequence(0, 1, True)
pacman_facing = 'AFK'
pacman_vx = 0
pacman_vy = 0
pacman_base_speed = 120

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

    dt = janela.delta_time()

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

    # Mudança de animação de Blinky nas 4 direções cardinais.
    if pacman_vy < 0 and pacman_facing != 'U':
        pacman_facing = 'U'
        pacman.set_sequence(6, 8, True)
    if pacman_vy > 0 and pacman_facing != 'D':
        pacman_facing = 'D'
        pacman.set_sequence(4, 6, True)
    if pacman_vx < 0 and pacman_facing != 'L':
        pacman_facing = 'L'
        pacman.set_sequence(2, 4, True)
    if pacman_vx > 0 and pacman_facing != 'R':
        pacman_facing = 'R'
        pacman.set_sequence(0, 2, True)

    # Código para a geração do mapa para testes.
    if not teclado.key_pressed("N") and not teclado.key_pressed("G") and not teclado.key_pressed("M"):
        TesteDebugMapa = False
    if teclado.key_pressed("N") and not TesteDebugMapa:
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

    if teclado.key_pressed("M") and not TesteDebugMapa:
        if BGM_Toggle:
            BGM_Toggle = False
            bgm.pause()
        else:
            BGM_Toggle = True
            bgm.unpause()
        TesteDebugMapa = True


    # Atualiza buffer de inputs
    buffer += dt

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

    # Coordenadas do pacman em relação ao 0 da fase
    pacman_newaxis_x = pacman.x - (janela.width / 2 - half_maze_width) + pacman.width / 2
    pacman_newaxis_y = pacman.y - (janela.height / 2 - half_maze_height) + pacman.height / 2

    # Versão discretizada das coordenadas do blinky com ajuste (+1) para correspondencia a matriz "level".
    new_x = blinky_newaxis_x // wall.width + 1
    new_y = blinky_newaxis_y // wall.height + 1

    # Versão discretizada das coordenadas do pacman com ajuste (+1) para correspondencia a matriz "level".
    pacman_new_x = pacman_newaxis_x // wall.width + 1
    pacman_new_y = pacman_newaxis_y // wall.height + 1

    can_go_down = level[int(new_y + 1)][int(new_x)] == 0
    can_go_up = level[int(new_y - 1)][int(new_x)] == 0
    can_go_left = level[int(new_y)][int(new_x - 1)] == 0
    can_go_right = level[int(new_y)][int(new_x + 1)] == 0

    pacman_can_go_down = level[int(pacman_new_y + 1)][int(pacman_new_x)] == 0
    pacman_can_go_up = level[int(pacman_new_y - 1)][int(pacman_new_x)] == 0
    pacman_can_go_left = level[int(pacman_new_y)][int(pacman_new_x - 1)] == 0
    pacman_can_go_right = level[int(pacman_new_y)][int(pacman_new_x + 1)] == 0

    relative_x_pacman_blinky = blinky.x - pacman.x
    relative_y_pacman_blinky = blinky.y - pacman.y

    #ia 'burra' do pacman
    #com essa lógica de movimentação, o pacman fica frequentemente 'preso' correndo contra paredes. Talvez implementar
    #alguma funcionalidade que impeça ele de ficar correndo contra uma parede por mais de algum tempo máximo
    if(abs(relative_x_pacman_blinky) > abs(relative_y_pacman_blinky)):
        # se movimentará na direção horizontal
        if(relative_x_pacman_blinky>0):
            #vai para a direita
            pacman_cmd = 'r'
        else:
            #vai para a esquerda
            pacman_cmd = 'l'
    else:
        #se movimentará na direção vertical
        if(relative_y_pacman_blinky>0):
            #vai para baixo
            pacman_cmd = 'd'
        else:
            #vai para cima
            pacman_cmd = 'u'

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

    
    # Determina as tolerâncias de movimento (até quantos pixels errados pacman aceita para fazer curva)
    x_window = (pacman_new_x - 0.5) * wall.width - delta_x < pacman_newaxis_x < (pacman_new_x - 0.5) * wall.width + delta_x
    y_window = (pacman_new_y - 0.5) * wall.height - delta_y < pacman_newaxis_y < (pacman_new_y - 0.5) * wall.height + delta_y
    # Movimento VERTICAL (REQUERIMENTO DE POSIÇÃO HORIZONTAL)
    if x_window:
        if pacman_cmd == 'd' and pacman_can_go_down:
            pacman_cmd = ''
            pacman_vx = 0
            pacman_vy = pacman_base_speed
        if pacman_cmd == 'u' and pacman_can_go_up:
            pacman_cmd = ''
            pacman_vx = 0
            pacman_vy = -pacman_base_speed

    # Movimento HORIZONTAL (REQUERIMENTO DE POSIÇÃO VERTICAL)
    if y_window:
        if pacman_cmd == 'r' and pacman_can_go_right:
            pacman_cmd = ''
            pacman_vx = pacman_base_speed
            pacman_vy = 0
        if pacman_cmd == 'l' and pacman_can_go_left:
            pacman_cmd = ''
            pacman_vx = -pacman_base_speed
            pacman_vy = 0

    # Checa condição de colisão de pacman com parede em x
    if not pacman_can_go_right and pacman_vx > 0 and pacman_newaxis_x >= (pacman_new_x - 0.5) * wall.width:
        pacman_vx = 0
    if not pacman_can_go_left and pacman_vx < 0 and pacman_newaxis_x <= (pacman_new_x - 0.5) * wall.width:
        pacman_vx = 0
    pacman.x += pacman_vx * dt

    # Checa condição de colisão de pacman com parede em y
    if not pacman_can_go_up and pacman_vy < 0 and pacman_newaxis_y <= (pacman_new_y - 0.5) * wall.height:
        pacman_vy = 0
    if not pacman_can_go_down and pacman_vy > 0 and pacman_newaxis_y >= (pacman_new_y - 0.5) * wall.height:
        pacman_vy = 0
    pacman.y += pacman_vy * dt

    # Para debug (S to stop)
    if teclado.key_pressed("P"):
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
    # Move blinky de acordo com sua velocidade no eixo x
    blinky.x += blinky.vx * dt

    # Checa condição de colisão de blinky com parede em y
    if not can_go_up and blinky.vy < 0 and blinky_newaxis_y <= (new_y - 0.5) * wall.height:
        blinky.vy = 0
    if not can_go_down and blinky.vy > 0 and blinky_newaxis_y >= (new_y - 0.5) * wall.height:
        blinky.vy = 0
    # Move blinky de acordo com sua velocidade no eixo y
    blinky.y += blinky.vy * dt

    # Checa colisão de blinky com portal esquerdo.
    if blinky_newaxis_x < 0 + wall.width / 2:  # aka: 0 + 20/2 = 10
        blinky.x += 2 * half_maze_width - wall.width

    # Checa colisão de blinky com portal direito.
    if blinky_newaxis_x > 28 * wall.width - wall.width / 2:  # aka: 28*20 - 20/2 550
        blinky.x -= 2 * half_maze_width - wall.width

    # FPS
    tempo += dt
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
    pacman.draw()
    pacman.update()
    portal_esquerdo.draw()
    portal_esquerdo.update()
    portal_direito.draw()
    portal_direito.update()    
    janela.draw_text("pacman_cmd: " + str(pacman_cmd), 30, 30, 30, color=(255,0,0))
    janela.update()
