from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.Maze import *
from EatThis.Classes.Enemy import *
from EatThis.Classes.Player import *
from EatThis.Classes.Shot import *
from EatThis.Classes.Trap import *
from EatThis.Classes.Bomb import *
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
    # print("        T - Altera modo IA do inimgo")
    print("        V - Altera modo do player")
    # Inicialização.
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    fps_msg = "FPS"
    current_stage = f"Stage: {save.stage_no}"
    stage_render = font.render(current_stage, True, 'white')
    credits_rollup = f"credits: {save.credits}"
    janela = Window(screen_width, screen_height)
    janela.set_title("Eat This!")
    teclado = janela.get_keyboard()
    walltypes = ["Curved_20", "Curved_20_Matrix",
                 "Curved_20_Cyan", "Curved_20_Cyan_Matrix",
                 "Curved_20_Salmon", "Curved_20_Purple",
                 "Curved_20_Orange", "Curved_20_White",
                 "Curved_20_Green"]

    # Gera um indice de cor diferente por fase
    aux = 1
    while aux == 1 or aux == 3:
        aux = random.randint(0, 8)
    wall_select = aux

    walltype = walltypes[wall_select]

    # Debuging variables.
    debug_timer = 0
    just_pressed = False
    grid_toggle = False
    new_map = False
    bgm_toggle = True
    bullet_time = False
    toggle_mood = False
    toggle_vulnerability = False

    # Variáveis do jogo.
    level_start = True
    level_clock = 0
    pause = False
    time_ratio = 1
    shots_list = []
    shots_list_max_len = 5
    enemies_list = []
    traps_list = []
    bombs_list = []
    blasts_list = []
    level_finished = False

    # Variáveis que impactam dificuldade.
    powerups_no = 2
    numero_inimigos = 1

    # Background Music.
    song_list = ["Assets/Music/Unreal Super Hero 3 by Kenet & Rez.mp3",
                 "Assets/Music/FLCTR4 (feat. Zabutom).mp3",
                 "Assets/Music/The Arcane Golem.mp3",
                 "Assets/Music/The Bat Matriarch.mp3"]
    sorteio = random.randint(0, 3)
    song = song_list[sorteio]


    slowmo = [Sound("Assets/SFX/SlowMotionIn.mp3"), Sound("Assets/SFX/SlowMotionOut.mp3")]
    bgm = Sound(song)
    print(f"\nPlaying: {song[13:len(song) - 4]} \n")
    bgm.set_volume(save.BGM_vol * save.Master_vol)
    bgm.set_repeat(True)

    if save.stage_no == 1:
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

    # Fade-to-Black sprite
    blackout = Sprite("Assets/Sprites/VFX/Fade_To_Black.png", 10)
    blackout.set_position(0,0)
    blackout.set_sequence_time(0, 10, 100, False)
    blackout.pause()

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
            #shot_fireball = var_toggle(shot_fireball, "SPACE", teclado)

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


            for pacman in enemies_list:
                pacman.maze = maze
                pacman.get_next_closest_point()
                pacman.maze.level[pacman.nearest_point[1][0]][pacman.nearest_point[1][1]].get_flow_field()



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

        blinky_out = level_finished and blinky.matrix_coordinates == (15, 27) and blinky.vx > 0

        # Atualiza buffer de inputs
        blinky.buffer += dt
        blinky.shot_timer += dt
        if not pause and not level_start and not blinky_out:
            blinky.move1()
            blinky.x += blinky.vx * dt
            blinky.y += blinky.vy * dt
            blinky.update()

            for pacman in enemies_list:
                pacman.move1(blinky)
                pacman.x += pacman.vx * dt * time_ratio
                pacman.y += pacman.vy * dt * time_ratio
                pacman.update()

            if (teclado.key_pressed("SPACE") and blinky.facing != 'AFK' and (len(shots_list) < shots_list_max_len)):
                if(blinky.shot_timer > blinky.reload_time):
                    blinky.shot_timer = 0
                    shot = Shot("Assets\Sprites\VFX\\blue fireball_32x32_omni.png", blinky, 8)
                    shots_list.append(shot)

            for shot in shots_list:
                shot.x += shot.vx * dt
                shot.y += shot.vy * dt
                shot.check_collision_with_wall()

            for shot in shots_list:
                for enemy in enemies_list:
                    if (shot.collided(enemy) and not enemy.is_dead):
                        enemy.die()
                        shot.hit_enemy = True

            for shot in shots_list:
                if(shot.hit_enemy or shot.hit_wall):
                    shots_list.remove(shot)

            if(teclado.key_pressed("A") and len(traps_list) < 1):
                trap = Trap("Assets\Sprites\PickUps\\trap_20_108_196_98.png", blinky)
                traps_list.append(trap)

            if (teclado.key_pressed("X") and len(bombs_list) < 1):
                bomb = Bomb("Assets\Sprites\VFX\\bomb.png", maze, blinky)
                bombs_list.append(bomb)

            for bomb in bombs_list:
                bomb.timer += dt

            for bomb in bombs_list:
                if(bomb.timer > bomb.explode_time):
                    blasts_list = bomb.explode()

            for enemy in enemies_list:
                for blast in blasts_list:
                    if blast.collided(enemy):
                        enemy.die()

            for blast in blasts_list:
                if ((time() - blast.creation_instant) > blast.delta_time):
                    blasts_list.remove(blast)

            for bomb in bombs_list:
                if (bomb.exploded):
                    bombs_list.remove(bomb)

            for trap in traps_list:
                for enemy in enemies_list:
                    if (trap.collided(enemy) and not enemy.is_dead):
                        enemy.die()
                        trap.was_eaten = True

            for trap in traps_list:
                if (trap.was_eaten):
                    traps_list.remove(trap)

            for pacman in enemies_list:
                if pacman.is_dead:
                    enemies_list.remove(pacman)




            if not blinky.teleport_able and teclado.key_pressed("O"):
                blinky.teleport_able = True
                teleport_sprite = Sprite("Assets\Sprites\VFX\\teleport.png")
                teleport_sprite.set_position(blinky.x + blinky.width/2 - teleport_sprite.width/2, blinky.y + blinky.height/2 - teleport_sprite.height/2)
                teleport_sprite.set_sequence_time(0, 2, 100, True)
                teleport_sprite.draw()

            if blinky.teleport_able and teclado.key_pressed("I"):
                blinky.set_position(teleport_sprite.x - blinky.width/2 + teleport_sprite.width/2, 
                                    teleport_sprite.y - blinky.height/2 + teleport_sprite.height/2)
                blinky.teleport_able = False

            
            for enemy in enemies_list:
                if blinky.state == "vulnerable" and blinky.collided(enemy) and not blinky.is_dead:
                    blinky.is_dead = True



        # Displays and updates player credits at the end of the level.
        if len(enemies_list) == 0 and not level_finished:
            level_finished = True
            save.stage_no += 1
            previous_credits = save.credits
            credits_received = len(maze.list_of_points)
            save.credits += len(maze.list_of_points)
            credits_rollup = f"credits: {save.credits}"
        snip = font.render(credits_rollup, True, 'white')







        # FPS
        tempo += dt
        cont += 1
        if tempo >= 1:
            tempo = 0
            FPS = cont
            cont = 0
        fps_msg = f"{FPS} FPS"
        frames_per_second = font.render(fps_msg, True, 'white')





        janela.set_background_color((0, 0, 0))                                  # Fundo preto.












        janela.screen.blit(frames_per_second, (10, janela.height - 50))         # Draw no FPS.
        maze.draw()

        if level_start:
            fake_blinky.x += 25 * dt
            blinky.hide()
            if level_clock // 0.1 in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
                for pacman in enemies_list:
                    pacman.draw()
        else:
            if not blinky.is_dead:
                blinky.draw()

        # Blinky is hidden, Fake_Blinky walks out thought portal and screen fades to black.
        if blinky_out:
            blackout.play()
            fake_blinky.x += 25 * dt
            fake_blinky.unhide()
            blinky.hide()
            print(blackout.is_playing())
            if blackout.get_curr_frame() == 9:
                return["play", save]


        if not level_start and not level_finished:
            blinky.unhide()
            fake_blinky.hide()
            fake_blinky.set_position(873, 323)
            for pacman in enemies_list:
                pacman.draw()

        for shot in shots_list:
            shot.draw()
            shot.update()
        for trap in traps_list:
            trap.draw()
        for bomb in bombs_list:
            bomb.draw()
            bomb.update()

        for blast in blasts_list:
            blast.draw()

        if blinky.teleport_able:
            teleport_sprite.draw()
            teleport_sprite.update()







        janela.screen.blit(snip, (930, 630))                                    # Mostra Credits.
        janela.screen.blit(stage_render, (930, 600))
        fake_blinky.draw()
        fake_blinky.update()
        portal_esquerdo.update()
        portal_esquerdo.draw()
        portal_direito.update()
        portal_direito.draw()



        blackout.update()
        blackout.draw()








        janela.update()
