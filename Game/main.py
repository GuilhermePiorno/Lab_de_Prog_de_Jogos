from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.Maze import *
from EatThis.Classes.Enemy import *
from EatThis.Classes.Player import *
from EatThis.a_star import *
from EatThis.debug import *
from EatThis.enemy_spawn import *
from time import *


def play_game(screen_width, screen_height, save):
    print("Hotkeys:")
    print("        B - Bullet-Time")
    print("        P - Pause")
    print("        N - Gera mapa novo")
    print("        G - Liga/Desliga Grid")
    print("        M - Liga/Desliga Música")
    print("        T - Altera modo IA do inimgo")
    print("        V - Altera modo do player")

    # Inicialização.
    janela = Window(screen_width, screen_height)
    janela.set_title("Eat This!")
    teclado = janela.get_keyboard()
    walltypes = ["Curved_20", "Curved_20_Matrix"]
    wall_select = 0
    walltype = walltypes[wall_select]
    debug_timer = 0
    just_pressed = False
    grid_toggle = False
    new_map = False
    bgm_toggle = True
    pause = False
    bullet_time = False
    toggle_mood = False
    toggle_vulnerability = False
    time_ratio = 1
    level_start = True
    level_clock = 0
    # Variáveis que impactam dificuldade!
    powerups_no = 4
    numero_inimigos = 3

    # Background Music.
    sorteio = random.random()
    if sorteio < 0.25:
        song = "Assets/Music/Unreal Super Hero 3 by Kenet & Rez.mp3"
    elif sorteio < 0.5:
        song = "Assets/Music/FLCTR4 (feat. Zabutom).mp3"
    elif sorteio < 0.75:
        song = "Assets/Music/The Arcane Golem.mp3"
    else:
        song = "Assets/Music/The Bat Matriarch.mp3"

    slowmo = [Sound("Assets/SFX/SlowMotionIn.mp3"), Sound("Assets/SFX/SlowMotionOut.mp3")]
    bgm = Sound(song)
    print(f"\nPlaying: {song[13:len(song) - 4]} \n")
    bgm.set_volume(save.BGM_vol * save.Master_vol)
    bgm.set_repeat(True)
    bgm.play()

    # cria o objeto maze
    maze = Maze(walltype, janela, powerups_no)

    # Cria um blinky "fake" para introdução.
    fake_blinky = Sprite("Assets/Sprites/Characters/Blinky.png", 12)
    fake_blinky_pos = maze.get_spawn_coordinates((15,1), fake_blinky.width, fake_blinky.height)
    fake_blinky.set_position(fake_blinky_pos[0] - 50, fake_blinky_pos[1])
    fake_blinky.set_sequence_time(0, 12, 100, True)
    fake_blinky.set_sequence(0, 2, True)

    # Cria o sprite de Blinky e define o número de frames de sua animação.
    blinky = Player(janela, maze, "Assets/Sprites/Characters/Blinky.png", 12)
    player_start_pos = maze.get_spawn_coordinates((15, 1), blinky.width, blinky.height)
    blinky.set_position(player_start_pos[0], player_start_pos[1])
    blinky.set_sequence_time(0, 12, 100, True)
    blinky.set_sequence(0, 1, True)



    # Enemy Creation
    enemies_list = create_pacmans(janela, maze, numero_inimigos, save)


    # Portal_Esquerdo
    portal_esquerdo = Sprite("Assets/Sprites/Walls/" + walltype + "/Portal_L_mask.png", 3)
    portal_esquerdo.set_sequence_time(0, 3, 100, True)
    portal_esquerdo.set_sequence(0, 3, True)
    portal_esquerdo.set_position(janela.width / 2 - maze.half_maze_width - maze.wall.width - 40,
                                 janela.height / 2 - maze.half_maze_height + 13.5 * maze.wall.height - 1)


    # Portal_Direito
    portal_direito = Sprite("Assets/Sprites/Walls/" + walltype + "/Portal_D_mask.png", 3)
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

        # Se algum carregamento gerar um dt muito grande, considerar dt=0 para evitar movimentos "pulados".
        if dt > 0.1:
            dt = 0
        debug_timer += dt
        level_clock += dt

        if level_start and level_clock >= 2:
            level_start = False

# <============================================================ DEBUG AREA START
        # Se nada tiver sido pressionado, checa inputs.
        if not just_pressed:
            bullet_time = var_toggle(bullet_time, "B", teclado)
            bgm_toggle = var_toggle(bgm_toggle, "M", teclado)
            pause = var_toggle(pause, "P", teclado)
            grid_toggle = var_toggle(grid_toggle, "G", teclado)
            new_map = var_toggle(new_map, "N", teclado)
            toggle_mood = var_toggle(toggle_mood, "T", teclado)
            toggle_vulnerability =  var_toggle(toggle_vulnerability, "V", teclado)

        # Notação pythonica de atribuição simples com if.
        # variável = valor_se_sim if condicao else valor_se_nao.
        bgm.unpause() if bgm_toggle else bgm.pause()    #---DEBUG------> M

        change_state = time_ratio
        time_ratio = 0.2 if bullet_time else 1          #---DEBUG------> B
        if change_state != time_ratio:
            # 0.2//1 = 0 ou 1//1 = 1, ou seja, alterna entre som de SlowMotionIn ou SlowMotionOut.
            slowmo[int(time_ratio//1)].play()
            bgm.set_volume(save.BGM_vol * save.Master_vol * time_ratio)
            #print(pacman.distance_list)


        if grid_toggle:                                 #---DEBUG------> G
            wall_select += 1
            walltype = walltypes[wall_select % (len(walltypes))]
            maze.walltype = walltype  # Atualiza o walltype do maze
            maze.level = maze.fill_level()  # Atualiza o level do maze para incluir a walltype nova
            grid_toggle = False


            for i in range(numero_inimigos):
                enemies_list[i].get_next_closest_point()
                enemies_list[i].maze.level[enemies_list[i].nearest_point[1][0]][enemies_list[i].nearest_point[1][1]].get_flow_field()



        if new_map:                                     #---DEBUG------> N
            maze = Maze(walltype, janela, powerups_no)
            blinky.maze = maze  # Atualiza o level do blinky

            for i in range(numero_inimigos):
                enemies_list[i].maze = maze
                enemies_list[i].get_next_closest_point()
                enemies_list[i].maze.level[enemies_list[i].nearest_point[1][0]][enemies_list[i].nearest_point[1][1]].get_flow_field()

            new_map = False

        if toggle_mood:                                 # ---DEBUG------> T
            pass


        if toggle_vulnerability:                        # ---DEBUG------> V
            blinky.change_state()
            print(f"Now I'm {blinky.state}!")
            toggle_vulnerability = not toggle_vulnerability


        # Atualiza caso algo tenha sido pressionado.
        just_pressed = check_keys(teclado, "B", "G", "M", "N", "P", "T", "V")
# <============================================================ DEBUG AREA END


        # Atualiza buffer de inputs
        blinky.buffer += dt
        if not pause and not level_start:
            blinky.move1()
            blinky.x += blinky.vx * dt
            blinky.y += blinky.vy * dt
            blinky.update()

            for pacman in enemies_list:
                pacman.move1(blinky)
                pacman.x += pacman.vx * dt * time_ratio
                pacman.y += pacman.vy * dt * time_ratio
                pacman.update()


        for pacman in enemies_list:
            # print(pacman.is_dead)
            if pacman.is_dead:
                enemies_list.remove(pacman)


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
        if not level_start:
            fake_blinky.hide()
            blinky.unhide()
            blinky.draw()
            for pacman in enemies_list:
                pacman.draw()
        else:
            fake_blinky.x += 25 * dt
            blinky.hide()
            if level_clock // 0.1 in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
                for pacman in enemies_list:
                    pacman.draw()

        fake_blinky.draw()
        fake_blinky.update()
        portal_esquerdo.draw()
        portal_esquerdo.update()
        portal_direito.draw()
        portal_direito.update()
        janela.update()






