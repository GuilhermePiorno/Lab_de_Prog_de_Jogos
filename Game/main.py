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
    tp_button = False

    # Variáveis que impactam dificuldade.
    powerups_no = 2
    numero_inimigos = save.stage_no

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
    fake_blinky_pos = maze.get_spawn_coordinates((15, 1), fake_blinky.width, fake_blinky.height)
    fake_blinky.set_position(fake_blinky_pos[0] - 50, fake_blinky_pos[1])
    fake_blinky.set_sequence_time(0, 12, 100, True)
    fake_blinky.set_sequence(0, 2, True)

    # Cria o sprite de Blinky e define o número de frames de sua animação.
    blinky = Player(janela, maze, save, "Assets/Sprites/Characters/Blinky.png", 12)
    player_start_pos = maze.get_spawn_coordinates((15, 1), blinky.width, blinky.height)
    blinky.set_position(player_start_pos[0], player_start_pos[1])
    blinky.set_sequence_time(0, 12, 100, True)
    blinky.set_sequence(0, 1, True)

    # transfer information from save into blinky.
    # blinky.has_shoes = save.has_shoes

    # Fade-to-Black sprite
    blackout = Sprite("Assets/Sprites/VFX/Fade_To_Black.png", 10)
    blackout.set_position(0, 0)
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

    cheat_guide_1 = Sprite("Assets/Sprites/CheatStuff/123.png")
    cheat_guide_1.set_position(0, 50)

    cheat_guide_2 = Sprite("Assets/Sprites/CheatStuff/4.png")
    cheat_guide_2.set_position(150, 50)

    cheat_guide_3 = Sprite("Assets/Sprites/CheatStuff/567.png")
    cheat_guide_3.set_position(0, 200)

    cheat_guide_4 = Sprite("Assets/Sprites/CheatStuff/890.png")
    cheat_guide_4.set_position(0, 400)

    # Inicia variáveis para o FPS.
    FPS = 0
    tempo = 0
    cont = 0
    x_state = False

    cheat_toggle_aux = False
    cheat_toggle = False
    cheat_sequence = ["U", "U", "D", "D", "L", "R", "L", "R"]
    input_sequence = []
    state_1 = False
    state_2 = False
    state_3 = False
    state_4 = False
    state_5 = False
    state_6 = False
    state_7 = False
    state_8 = False
    state_9 = False
    state_0 = False

    # Game-loop
    notagain = False
    while True:
        # Leitura de Entradas
        dt = janela.delta_time()
        blinky.dt = dt

        # Se algum carregamento gerar um dt muito grande, considerar dt=0 para evitar movimentos "pulados".
        if dt > 0.1:
            dt = 0
        debug_timer += dt
        level_clock += dt

        if level_start and level_clock >= 2:
            level_start = False

        # UPGRADE ICONS
        upgrade_draw_list = []

        if save.speed_upgrade > 0:
            speed_increase_icon = Sprite("Assets/Sprites/UI Icons/speed_up.png")
            speed_increase_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            speed_increase_level = Sprite("Assets/Sprites/UI Icons/amount_box_black_and_white_borders.png", 10)
            speed_increase_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            speed_increase_level.set_curr_frame(save.speed_upgrade)
            upgrade_draw_list.append(speed_increase_icon)
            upgrade_draw_list.append(speed_increase_level)

        if save.has_shoes:
            boots = Sprite("Assets/Sprites/UI Icons/boots_box.png")
            boots.set_position(370 + len(upgrade_draw_list) * 22, 670)
            upgrade_draw_list.append(boots)
            upgrade_draw_list.append(boots)

        if 1 < save.grip_factor < 99:
            grip_icon = Sprite("Assets/Sprites/UI Icons/boots_spiked_box.png")
            grip_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon = Sprite("Assets/Sprites/UI Icons/amount_box_up.png", 10)
            grip_level_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon.set_curr_frame((save.grip_factor - 1) // 0.5)
            upgrade_draw_list.append(grip_icon)
            upgrade_draw_list.append(grip_level_icon)
        elif save.grip_factor == 100:
            grip_icon = Sprite("Assets/Sprites/UI Icons/golden_boots_spiked_box.png")
            grip_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon = Sprite("Assets/Sprites/UI Icons/amount_box_max.png", 2)
            grip_level_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            grip_level_icon.set_curr_frame(1)
            upgrade_draw_list.append(grip_icon)
            upgrade_draw_list.append(grip_level_icon)

        if save.has_bomb_ability:
            # bomb enable icon
            bomb_box = Sprite("Assets/Sprites/UI Icons/bomb_box.png")
            bomb_box.set_position(370 + len(upgrade_draw_list) * 22, 670)
            # bomb max quantity
            bomb_amount = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            bomb_amount.set_position(370 + len(upgrade_draw_list) * 22, 670)
            bomb_amount.set_curr_frame(save.max_bombs)
            upgrade_draw_list.append(bomb_box)
            upgrade_draw_list.append(bomb_amount)
            b_range = Sprite("Assets/Sprites/UI Icons/bomb_upgrade_box.png")
            b_range.set_position(370 + len(upgrade_draw_list) * 22, 670)
            b_range_level = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            b_range_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            b_range_level.set_curr_frame(save.bomb_range_upgrade + 1)
            upgrade_draw_list.append(b_range)
            upgrade_draw_list.append(b_range_level)

        if save.has_fireball_ability:
            fireball_icon = Sprite("Assets/Sprites/UI Icons/fireball_box.png")
            fireball_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_ammo = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            fireball_ammo.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_ammo.set_curr_frame(save.fireball_ammo)
            upgrade_draw_list.append(fireball_icon)
            upgrade_draw_list.append(fireball_ammo)

        if save.fireball_mult_spd > 1:
            fireball_spd_icon = Sprite("Assets/Sprites/UI Icons/fireball_speed_box.png")
            fireball_spd_icon.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_spd_level = Sprite("Assets/Sprites/UI Icons/amount_box.png", 10)
            fireball_spd_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            fireball_spd_level.set_curr_frame((save.fireball_mult_spd - 1) // 0.1)
            upgrade_draw_list.append(fireball_spd_icon)
            upgrade_draw_list.append(fireball_spd_level)

        if save.vuln_res != 0:
            vulnerability_res = Sprite("Assets/Sprites/UI Icons/vulnerability_res2.png")
            vulnerability_res.set_position(370 + len(upgrade_draw_list) * 22, 670)
            resistance_level = Sprite("Assets/Sprites/UI Icons/amount_box_down.png", 10)
            resistance_level.set_position(370 + len(upgrade_draw_list) * 22, 670)
            resistance_level.set_curr_frame(save.vuln_res * 10)
            upgrade_draw_list.append(vulnerability_res)
            upgrade_draw_list.append(resistance_level)

        # <============================================================ DEBUG AREA START
        # cheat enable/diable
        if cheat_sequence == input_sequence:
            cheat_toggle = True

        # input detection for sequence
        if teclado.key_pressed("UP") and not cheat_toggle_aux:
            cheat_toggle_aux = True
            if len(input_sequence) >= 8:
                del input_sequence[0]
            input_sequence.append("U")
        # input detection for sequence
        if teclado.key_pressed("DOWN") and not cheat_toggle_aux:
            cheat_toggle_aux = True
            if len(input_sequence) >= 8:
                del input_sequence[0]
            input_sequence.append("D")
        # input detection for sequence
        if teclado.key_pressed("LEFT") and not cheat_toggle_aux:
            cheat_toggle_aux = True
            if len(input_sequence) >= 8:
                del input_sequence[0]
            input_sequence.append("L")
        # input detection for sequence
        if teclado.key_pressed("RIGHT") and not cheat_toggle_aux:
            cheat_toggle_aux = True
            if len(input_sequence) >= 8:
                del input_sequence[0]
            input_sequence.append("R")
        # input detection for sequence
        if not teclado.key_pressed("UP") and not teclado.key_pressed("DOWN") and not teclado.key_pressed(
                "LEFT") and not teclado.key_pressed("RIGHT"):
            cheat_toggle_aux = False

        if cheat_toggle:
            # toggle bomb ability
            if teclado.key_pressed("1") and not state_1:
                state_1 = True
                save.has_bomb_ability = not save.has_bomb_ability
                if save.has_bomb_ability:
                    print("Bombs unlocked!")
                else:
                    print("Bombs disabled! :(")
            if not teclado.key_pressed("1"):
                state_1 = False

            # increase maximum bombs +
            if teclado.key_pressed("2") and not state_2:
                state_2 = True
                save.max_bombs += 1
                if save.max_bombs > 9:
                    save.max_bombs = 1
                print(f"Your max bombs: {save.max_bombs}")
            if not teclado.key_pressed("2"):
                state_2 = False

            # increase bomb range
            if teclado.key_pressed("3") and not state_3:
                state_3 = True
                save.bomb_range_upgrade += 1
                if save.bomb_range_upgrade > 9:
                    save.bomb_range_upgrade = 0
                print(f"Your bomb range was upgraded to: {save.bomb_range_upgrade + 1}")
            if not teclado.key_pressed("3"):
                state_3 = False

            # Move speed.
            if teclado.key_pressed("4") and not state_4:
                state_4 = True
                save.speed_upgrade += 1
                blinky.base_speed = 100 + 10 * save.speed_upgrade
                print(f"Blinky's new speed: {blinky.base_speed}")
            if not teclado.key_pressed("4"):
                state_4 = False

            # Has fireball
            if teclado.key_pressed("5") and not state_5:
                state_5 = True
                save.has_fireball_ability = not save.has_fireball_ability
                if save.has_fireball_ability:
                    print("Fireball unlocked!")
                else:
                    print("Fireball disabled! :(")

            if not teclado.key_pressed("5"):
                state_5 = False

            # Fireball ammo.
            if teclado.key_pressed("6") and not state_6:
                state_6 = True
                save.fireball_ammo += 1
                print(f"Current fireball ammmo: {save.fireball_ammo}")
            if not teclado.key_pressed("6"):
                state_6 = False

            # Fireball sppeed.
            if teclado.key_pressed("7") and not state_7:
                save.fireball_mult_spd += 0.1
                print(f"Fireballs are {int(save.fireball_mult_spd * 100)}%")
                state_7 = True
            if not teclado.key_pressed("7"):
                state_7 = False

            # Vulnerability resistance.
            if teclado.key_pressed("8") and not state_8:
                save.vuln_res += 0.1
                if save.vuln_res > 1:
                    save.vuln_res = 0
                print(f"Vulnerability Resistance: {int(save.vuln_res * 100)}%")
                state_8 = True
            if not teclado.key_pressed("8"):
                state_8 = False

            # Boots.
            if teclado.key_pressed("9") and not state_9:
                save.has_shoes = not save.has_shoes
                blinky.has_shoes = save.has_shoes
                state_9 = True
                if save.has_shoes:
                    print(f"Shoes ON!")
                else:
                    print(f"Shoes OFF.")
            if not teclado.key_pressed("9"):
                state_9 = False

            # Boots grip.
            if teclado.key_pressed("0") and not state_0:
                if save.grip_factor < 5.5:
                    save.grip_factor += 0.5
                else:
                    save.grip_factor = 100
                blinky.grip_factor = save.grip_factor
                blinky.shoe_grip = blinky.base_speed * blinky.grip_factor
                print(f"Grip factor: {save.grip_factor}")
                state_0 = True
            if not teclado.key_pressed("0"):
                state_0 = False

        # Se nada tiver sido pressionado, checa inputs.
        if not just_pressed:
            bullet_time = var_toggle(bullet_time, "B", teclado)
            bgm_toggle = var_toggle(bgm_toggle, "M", teclado)
            pause = var_toggle(pause, "P", teclado)
            grid_toggle = var_toggle(grid_toggle, "G", teclado)
            new_map = var_toggle(new_map, "N", teclado)
            toggle_mood = var_toggle(toggle_mood, "T", teclado)
            toggle_vulnerability = var_toggle(toggle_vulnerability, "V", teclado)
            # shot_fireball = var_toggle(shot_fireball, "SPACE", teclado)

        # Notação pythonica de atribuição simples com if.
        # variável = valor_se_sim if condicao else valor_se_nao.
        bgm.unpause() if bgm_toggle else bgm.pause()  # ---DEBUG------> M

        change_state = time_ratio
        time_ratio = 0.2 if bullet_time else 1  # ---DEBUG------> B
        if change_state != time_ratio:
            # 0.2//1 = 0 ou 1//1 = 1, ou seja, alterna entre som de SlowMotionIn ou SlowMotionOut.
            slowmo[int(time_ratio // 1)].play()
            bgm.set_volume(save.BGM_vol * save.Master_vol * time_ratio)
            # print(pacman.distance_list)

        if grid_toggle:  # ---DEBUG------> G
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

        if new_map:  # ---DEBUG------> N
            maze = Maze(walltype, janela, powerups_no)
            blinky.maze = maze  # Atualiza o level do blinky

            for i in range(numero_inimigos):
                enemies_list[i].maze = maze
                enemies_list[i].get_next_closest_point()
                enemies_list[i].maze.level[enemies_list[i].nearest_point[1][0]][
                    enemies_list[i].nearest_point[1][1]].get_flow_field()

            new_map = False

        if toggle_mood:  # ---DEBUG------> T
            pass

        if toggle_vulnerability:  # ---DEBUG------> V
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
            # TODO: quando colado numa parede é possivel atirar para fora da fase e o jogo crasha (sem resolvido com verificação de velocidade, testar mais)
            # TODO: Blinky crasha ao jogo se atirar em direção do portal direito.
            # if teclado.key_pressed("SPACE") and save.has_fireball_ability and blinky.facing != 'AFK' and (len(shots_list) < shots_list_max_len):
            if teclado.key_pressed(
                    "SPACE") and save.has_fireball_ability and blinky.facing != 'AFK' and save.fireball_ammo > 0 and (
                    blinky.vx != 0 or blinky.vy != 0):
                if blinky.shot_timer > blinky.reload_time:
                    blinky.shot_timer = 0
                    shot = Shot("Assets/Sprites/VFX/blue_fireball_32x32_omni.png", blinky, 8)
                    shots_list.append(shot)
                    save.fireball_ammo -= 1

            for shot in shots_list:
                shot.x += shot.vx * save.fireball_mult_spd * dt
                shot.y += shot.vy * save.fireball_mult_spd * dt
                shot.check_collision_with_wall()
                shot.check_inside_maze_boundary()

            for shot in shots_list:
                for enemy in enemies_list:
                    if shot.collided(enemy) and not enemy.is_dead:
                        enemy.die()
                        shot.hit_enemy = True

            for shot in shots_list:
                if shot.hit_enemy or shot.hit_wall or shot.out_of_bounds:
                    shots_list.remove(shot)

            if teclado.key_pressed("A") and len(traps_list) < 1 and save.has_poison_pill:
                trap = Trap("Assets/Sprites/PickUps/trap_20_108_196_98.png", blinky)
                traps_list.append(trap)

            if teclado.key_pressed("X") and save.has_bomb_ability and not x_state and len(bombs_list) < save.max_bombs:
                x_state = True
                bomb = Bomb("Assets/Sprites/VFX/Bomb_Animated.png", maze, blinky, save.bomb_range_upgrade)
                bomb.set_sequence_time(0, 4, 1000, True)
                bombs_list.append(bomb)
            if not teclado.key_pressed("X"):
                x_state = False

            for bomb in bombs_list:
                bomb.timer += dt

            for bomb in bombs_list:
                if bomb.timer > bomb.explode_time:
                    blasts_list = bomb.explode()

            for enemy in enemies_list:
                for blast in blasts_list:
                    if blast.collided(enemy):
                        enemy.die()

            for blast in blasts_list:
                if blinky.collided(blast):
                    blinky.is_dead = True

            for blast in blasts_list:
                if blinky.collided(blast):
                    blinky.is_dead = True

            for blast in blasts_list:
                if (time() - blast.creation_instant) > blast.delta_time:
                    blasts_list.remove(blast)

            for bomb in bombs_list:
                if bomb.exploded:
                    bombs_list.remove(bomb)

            for trap in traps_list:
                for enemy in enemies_list:
                    if trap.collided(enemy) and not enemy.is_dead:
                        enemy.die()
                        trap.was_eaten = True

            for trap in traps_list:
                if trap.was_eaten:
                    traps_list.remove(trap)

            for pacman in enemies_list:
                if pacman.is_dead:
                    enemies_list.remove(pacman)

            if not teclado.key_pressed("T"):
                tp_button = False

            if not tp_button and teclado.key_pressed("T") and save.has_teleport:
                tp_button = True
                if not blinky.teleport_able:
                    teleport_sprite = Sprite("Assets\Sprites\Characters\Blinky_transparente.png")
                    teleport_sprite.set_position(blinky.x, blinky.y)
                    teleport_sprite.draw()
                else:
                    blinky.set_position(teleport_sprite.x - blinky.width / 2 + teleport_sprite.width / 2,
                                        teleport_sprite.y - blinky.height / 2 + teleport_sprite.height / 2)
                blinky.teleport_able = not blinky.teleport_able

            for enemy in enemies_list:
                if (blinky.state == "vulnerable" or blinky.state == "transition") and (
                        blinky.get_matrix_coordinates() == enemy.get_matrix_coordinates()) and not blinky.is_dead:
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

        janela.set_background_color((0, 0, 0))  # Fundo preto.

        janela.screen.blit(frames_per_second, (10, janela.height - 50))  # Draw no FPS.
        maze.draw()

        # walks fake blink into the maze and makes enemies blink.
        if level_start:
            fake_blinky.x += 25 * dt
            blinky.hide()
            if level_clock // 0.1 in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
                for pacman in enemies_list:
                    pacman.draw()
        else:
            blinky.draw()

        # Blinky is hidden, Fake_Blinky walks out thought portal and screen fades to black.
        if blinky_out:
            blackout.play()
            fake_blinky.x += 25 * dt
            fake_blinky.unhide()
            blinky.hide()
            if blackout.get_curr_frame() == 9:
                if save.stage_no % 2 == 0:
                    bgm.pause()
                    return ["shop", save]
                return ["play", save]

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
            blast.update()

        if blinky.teleport_able:
            teleport_sprite.draw()

        for item in upgrade_draw_list:
            item.draw()

        janela.screen.blit(snip, (930, 630))  # Mostra Credits.
        janela.screen.blit(stage_render, (930, 600))
        fake_blinky.draw()
        fake_blinky.update()
        portal_esquerdo.update()
        portal_esquerdo.draw()
        portal_direito.update()
        portal_direito.draw()
        if cheat_toggle:
            cheat_guide_1.draw()
            cheat_guide_2.draw()
            cheat_guide_3.draw()
            cheat_guide_4.draw()

        blackout.update()
        blackout.draw()

        janela.update()

        # morte do blinky
        if blinky.is_dead or (len(maze.list_of_points) == 0):
            save.stage_no = 1
            save.credits = 0
            bgm.stop()
            bgm.pause()
            blinky.hide()
            dead_blinky = Sprite("Assets/Sprites/Characters/blinky_morto.png", 1)
            dead_blinky.x = blinky.x
            dead_blinky.y = blinky.y
            blinky_death_sound = Sound("Assets/SFX/BlinkyDeath.mp3")
            blinky_death_sound.set_volume(save.SFX_vol * save.Master_vol)
            blinky_death_sound.play()
            # blinky.state = "vulnerable"
            # blinky.update_sequence()
            while dead_blinky.y > 0:
                janela.set_background_color((0, 0, 0))
                janela.screen.blit(frames_per_second, (10, janela.height - 50))  # Draw no FPS.
                maze.draw()
                for enemy in enemies_list:
                    enemy.draw()
                for blast in blasts_list:
                    blast.draw()
                    blast.update()
                janela.screen.blit(snip, (930, 630))  # Mostra Credits.
                janela.screen.blit(stage_render, (930, 600))
                portal_esquerdo.update()
                portal_esquerdo.draw()
                portal_direito.update()
                portal_direito.draw()
                dead_blinky.y -= 1
                dead_blinky.draw()
                # blinky.update()
                janela.update()
            return ["menu", save]
