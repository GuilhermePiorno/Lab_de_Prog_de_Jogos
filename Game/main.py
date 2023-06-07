from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.Maze import *
from EatThis.Classes.Enemy import *
from EatThis.Classes.Player import *
from EatThis.Classes.Shot import *
from EatThis.a_star import *
from EatThis.debug import *
from time import *


def play_game(screen_width, screen_height, vol):
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
    #shot_fireball = False
    moods = ["hungry", "afraid", "angry"]
    mood_ind = 0
    toggle_vulnerability = False
    time_ratio = 1
    shots_list = []
    enemies_list = []

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
    bgm.set_volume(vol)
    bgm.set_repeat(True)
    bgm.play()

    # cria o objeto maze
    maze = Maze(walltype, janela)

    # Cria o sprite de Blinky e define o número de frames de sua animação.
    blinky = Player(janela, maze, "Assets/Sprites/Characters/Blinky.png", 12)
    blinky.set_position(janela.width / 2 - maze.half_maze_width + (maze.wall.width * 1.5 - blinky.width / 2),
                        janela.height / 2 - maze.half_maze_height + (maze.wall.height * 1.5 - blinky.height / 2))
    blinky.set_sequence_time(0, 12, 100, True)
    blinky.set_sequence(0, 1, True)

    # Cria o sprite de Pacman e define o número de frames de sua animação.
    pacman = Enemy("pac1", janela, maze, "Assets/Sprites/Characters/pacman_movimento_e_morte.png", 22)
    pacman.set_position(janela.width / 2 + maze.half_maze_width - (maze.wall.width * 1.5 + pacman.width / 2),
                        janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pacman.height / 2))
    pacman.set_sequence_time(0, 8, 100, True)
    pacman.set_sequence(0, 1, True)
    enemies_list.append(pacman)

    pac2 = Enemy("pac2", janela, maze, "Assets/Sprites/Characters/pacman_movimento_e_morte.png", 22)
    pac2.set_position(janela.width / 2 - maze.half_maze_width + (maze.wall.width * 1.5 - pac2.width / 2),
                        janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pac2.height / 2))
    pac2.set_sequence_time(0, 8, 100, True)
    pac2.set_sequence(0, 1, True)
    enemies_list.append(pac2)

    pac3 = Enemy("pac3", janela, maze, "Assets/Sprites/Characters/pacman_movimento_e_morte.png", 22)
    pac3.set_position(janela.width / 2 + 0.5*maze.half_maze_width - (maze.wall.width * 1.5 + pacman.width / 2),
                        janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pac3.height / 2))
    pac3.set_sequence_time(0, 8, 100, True)
    pac3.set_sequence(0, 1, True)
    enemies_list.append(pac3)

    pac4 = Enemy("pac4", janela, maze, "Assets/Sprites/Characters/pacman_movimento_e_morte.png", 22)
    pac4.set_position(janela.width / 2 + -0.5*maze.half_maze_width - (maze.wall.width * 1.5 + pacman.width / 2),
                      janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pac4.height / 2))
    pac4.set_sequence_time(0, 8, 100, True)
    pac4.set_sequence(0, 1, True)
    enemies_list.append(pac4)

    # Portal_Esquerdo
    portal_esquerdo = Sprite("Assets/Sprites/Walls/" + walltype + "/Portal_L.png", 3)
    portal_esquerdo.set_sequence_time(0, 3, 100, True)
    portal_esquerdo.set_sequence(0, 3, True)
    portal_esquerdo.set_position(janela.width / 2 - maze.half_maze_width - maze.wall.width,
                                 janela.height / 2 - maze.half_maze_height + 13.5 * maze.wall.height - 1)


    # Portal_Direito
    portal_direito = Sprite("Assets/Sprites/Walls/" + walltype + "/Portal_D.png", 3)
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
            bgm.set_volume(vol * time_ratio)
            #print(pacman.distance_list)


        if grid_toggle:                                 #---DEBUG------> G
            wall_select += 1
            walltype = walltypes[wall_select % (len(walltypes))]
            maze.walltype = walltype  # Atualiza o walltype do maze
            maze.level = maze.fill_level()  # Atualiza o level do maze para incluir a walltype nova
            grid_toggle = False
            # trash below here
            pacman.get_next_closest_point()
            pacman.maze.level[pacman.nearest_point[1][0]][pacman.nearest_point[1][1]].get_flow_field()
            pac2.maze = maze  # Atualiza o level do pacman
            pac2.get_next_closest_point()
            pac2.maze.level[pac2.nearest_point[1][0]][pac2.nearest_point[1][1]].get_flow_field()
            pac3.maze = maze  # Atualiza o level do pacman
            pac3.get_next_closest_point()
            pac3.maze.level[pac3.nearest_point[1][0]][pac3.nearest_point[1][1]].get_flow_field()
            pac4.maze = maze  # Atualiza o level do pacman
            pac4.get_next_closest_point()
            pac4.maze.level[pac4.nearest_point[1][0]][pac4.nearest_point[1][1]].get_flow_field()


        if new_map:                                     #---DEBUG------> N
            maze = Maze(walltype, janela)
            blinky.maze = maze  # Atualiza o level do blinky
            pacman.maze = maze  # Atualiza o level do pacman
            pacman.get_next_closest_point()
            pacman.maze.level[pacman.nearest_point[1][0]][pacman.nearest_point[1][1]].get_flow_field()
            pac2.maze = maze  # Atualiza o level do pacman
            pac2.get_next_closest_point()
            pac2.maze.level[pac2.nearest_point[1][0]][pac2.nearest_point[1][1]].get_flow_field()
            pac3.maze = maze  # Atualiza o level do pacman
            pac3.get_next_closest_point()
            pac3.maze.level[pac3.nearest_point[1][0]][pac3.nearest_point[1][1]].get_flow_field()
            pac4.maze = maze  # Atualiza o level do pacman
            pac4.get_next_closest_point()
            pac4.maze.level[pac4.nearest_point[1][0]][pac4.nearest_point[1][1]].get_flow_field()
            new_map = False

        if toggle_mood:                                 # ---DEBUG------> T
            mood_ind = (mood_ind + 1) % 3
            pacman.state = moods[mood_ind]
            pac2.state = moods[mood_ind]
            pac3.state = moods[mood_ind]
            pac4.state = moods[mood_ind]
            toggle_mood = not toggle_mood
            print(f"Now I'm {moods[mood_ind]}!")


        if toggle_vulnerability:                        # ---DEBUG------> V
            blinky.change_state()
            print(f"Now I'm {blinky.state}!")
            toggle_vulnerability = not toggle_vulnerability

        # Atualiza caso algo tenha sido pressionado.
        just_pressed = check_keys(teclado, "B", "G", "M", "N", "P", "T", "V")
# <============================================================ DEBUG AREA END

        if teclado.key_pressed("SPACE"):
            if(blinky.shot_timer > blinky.reload_time):
                blinky.shot_timer = 0
                shot = Shot("Assets\Sprites\VFX\\fireball_teste.png", blinky, frames=8)
                shots_list.append(shot)
        
        for shot in shots_list:
            if((shot.x > (janela.width/2 + maze.half_maze_width)) or shot.x < (janela.width/2 - maze.half_maze_width)):
                shots_list.remove(shot)
            if((shot.y > (janela.height/2 + maze.half_maze_height)) or (shot.y < janela.height/2 - maze.half_maze_height)):
                shots_list.remove(shot)

        # Atualiza buffer de inputs
        blinky.buffer += dt
        blinky.shot_timer += dt
        if not pause:
            blinky.move1()
            blinky.x += blinky.vx * dt
            blinky.y += blinky.vy * dt
            blinky.update()


            pacman.move1(blinky)
            pacman.x += pacman.vx * dt * time_ratio
            pacman.y += pacman.vy * dt * time_ratio
            pacman.update()


            pac2.move1(blinky)
            pac2.x += pac2.vx * dt * time_ratio
            pac2.y += pac2.vy * dt * time_ratio
            pac2.update()

            pac3.move1(blinky)
            pac3.x += pac3.vx * dt * time_ratio
            pac3.y += pac3.vy * dt * time_ratio
            pac3.update()

            pac4.move1(blinky)
            pac4.x += pac4.vx * dt * time_ratio
            pac4.y += pac4.vy * dt * time_ratio
            pac4.update()

            for shot in shots_list:
                shot.x += shot.vx * dt
                shot.y += shot.vy * dt

            for shot in shots_list:
                for enemy in enemies_list:
                    if shot.collided_perfect(enemy):
                        enemy.die()
                        shot.hit_enemy = True

            for shot in shots_list:
                if(shot.hit_enemy):
                    shots_list.remove(shot)
            
            for enemy in enemies_list:
                if(enemy.is_dead and (time() - enemy.death_instant) > 3): # esperando o tempo da animação de morte do pacman para então remover ele da lista
                    enemies_list.remove(enemy)




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
        #pacman.draw()
        #pac2.draw()
        #pac3.draw()
        #pac4.draw()
        for enemy in enemies_list:
            enemy.draw()
        for shot in shots_list:
            shot.draw()
            #shot.update()
        portal_esquerdo.draw()
        portal_esquerdo.update()
        portal_direito.draw()
        portal_direito.update()
        janela.update()






