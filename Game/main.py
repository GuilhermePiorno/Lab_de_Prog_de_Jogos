from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.Maze import *
from EatThis.Classes.Enemy import *
from EatThis.Classes.Player import *
from EatThis.a_star import *

def play_game(screen_width, screen_height, vol):
    print("Hotkeys:")
    print("        N - Gera mapa novo")
    print("        G - Liga/Desliga Grid")
    print("        M - Liga/Desliga Música")

    # Inicialização.
    janela = Window(screen_width, screen_height)
    janela.set_title("Eat This!")
    teclado = janela.get_keyboard()
    walltype = 'Curved_20'
    teste_debug_jogo = False
    grid_toggle = False
    BGM_Toggle = True
    pause = False
    bullet_time = False
    time_ratio = 1

    # Background Music.
    sorteio = random.random()
    if sorteio < 0.25:
        song = "music/Unreal Super Hero 3 by Kenet & Rez.mp3"
    elif sorteio < 0.5:
        song = "music/FLCTR4 (feat. Zabutom).mp3"
    elif sorteio < 0.75:
        song = "music/The Arcane Golem.mp3"
    else:
        song = "music/The Bat Matriarch.mp3"


    bgm = Sound(song)
    print(f"\nPlaying: {song[6:len(song) - 4]} \n")
    bgm.set_volume(5)
    bgm.set_repeat(True)
    bgm.play()

    # cria o objeto maze
    maze = Maze(walltype, janela)
    # cria o grafo a partir desse maze
    maze_graph = MazeGraph(maze.level)
    # maze_graph.create_graph()

    # Cria o sprite de Blinky e define o número de frames de sua animação.
    blinky = Player(janela, maze, "./Sprites/Blinky.png", 8)
    blinky.set_position(janela.width / 2 - maze.half_maze_width + (maze.wall.width * 1.5 - blinky.width / 2),
                        janela.height / 2 - maze.half_maze_height + (maze.wall.height * 1.5 - blinky.height / 2))
    blinky.set_sequence_time(0, 8, 100, True)
    blinky.set_sequence(0, 1, True)

    # Cria o sprite de Pacman e define o número de frames de sua animação.
    pacman = Enemy(janela, maze, "./Sprites/pacman_movimento_e_morte.png", 22)
    pacman.set_position(janela.width / 2 + maze.half_maze_width - (maze.wall.width * 1.5 + pacman.width / 2),
                        janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pacman.height / 2))
    pacman.set_sequence_time(0, 8, 100, True)
    pacman.set_sequence(0, 1, True)

    # --- Pacmans para teste, no futuro incializar pacmans em uma lista.
    pacman2 = Enemy(janela, maze, "./Sprites/pacman.png", 8)
    pacman2.set_position(janela.width / 2 - maze.half_maze_width / 2 - (maze.wall.width * 1.5 + pacman.width / 2),
                         janela.height / 2 + maze.half_maze_height - (maze.wall.height * 1.5 + pacman.height / 2))
    pacman2.set_sequence_time(0, 8, 100, True)
    pacman2.set_sequence(0, 1, True)

    pacman3 = Enemy(janela, maze, "./Sprites/pacman.png", 8)
    pacman3.set_position(janela.width / 2 + maze.half_maze_width / 2 - (maze.wall.width * 1.5 + pacman.width / 2),
                         janela.height / 2 - maze.half_maze_height + (maze.wall.height * 1.5 - pacman.height / 2))
    pacman3.set_sequence_time(0, 8, 100, True)
    pacman3.set_sequence(0, 1, True)
    # --- Fim da inicialização de Pacmans para teste


    # cria o caminho (no grafo) do pacman até o blinky
    # graph_path = a_star(maze_graph, pacman.get_matrix_coordinates(), blinky.get_matrix_coordinates())
    # graph_path.append(blinky.get_matrix_coordinates()) # gambiarra: deve dar pra fazer isso dentro da função
    # pacman_cmds = matrix_path(graph_path, pacman.get_matrix_coordinates())
    # pacman.cmdstr = pacman_cmds



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
        if not teclado.key_pressed("N") and not teclado.key_pressed("G") and not teclado.key_pressed("M") and not teclado.key_pressed("P") and not teclado.key_pressed("B"):
            teste_debug_jogo = False
        if teclado.key_pressed("N") and not teste_debug_jogo:
            maze = Maze(walltype, janela)

            # cria o grafo a partir desse maze
            # maze_graph = MazeGraph(maze.level)
            # maze_graph.create_graph()
            blinky.level = maze  # Atualiza o level do blinky
            pacman.level = maze  # Atualiza o level do pacman
            # pacman2.level = maze  # Atualiza o level do pacman2
            teste_debug_jogo = True

        if teclado.key_pressed("G") and not teste_debug_jogo:
            if grid_toggle:
                grid_toggle = False
                walltype = walltype.split("_")[0] + "_" + walltype.split("_")[1]
            else:
                grid_toggle = True
                walltype += '_Matrix'
            teste_debug_jogo = True
            maze.walltype = walltype  # Atualiza o walltype do maze
            maze.level = maze.fill_level()  # Atualiza o level do maze para incluir a walltype nova

        if teclado.key_pressed("M") and not teste_debug_jogo:
            if BGM_Toggle:
                BGM_Toggle = False
                bgm.pause()
            else:
                BGM_Toggle = True
                bgm.unpause()
            teste_debug_jogo = True

        if teclado.key_pressed("P") and not teste_debug_jogo:
            if pause:
                pause = False
            else:
                pause = True
            teste_debug_jogo = True

        if teclado.key_pressed("B") and not teste_debug_jogo:
            if bullet_time:
                bullet_time = False
                time_ratio = 1
            else:
                bullet_time = True
                time_ratio = 0.2
            teste_debug_jogo = True


        # cria o grafo a partir desse maze
        #maze_graph = MazeGraph(maze.level)
        #maze_graph.create_graph()
        blinky.maze = maze  # Atualiza o level do blinky
        pacman.maze = maze  # Atualiza o level do pacman
        pacman2.maze = maze  # Atualiza o level do pacman2
        pacman3.maze = maze  # Atualiza o level do pacman3


        # Atualiza buffer de inputs
        blinky.buffer += dt

        if not pause:
            blinky.move1()
            blinky.x += blinky.vx * dt
            blinky.y += blinky.vy * dt
            blinky.update()

            pacman.move1(blinky)
            pacman.x += pacman.vx * dt * time_ratio
            pacman.y += pacman.vy * dt * time_ratio
            pacman.update()

            pacman2.move1(blinky)
            pacman2.x += pacman2.vx * dt * time_ratio
            pacman2.y += pacman2.vy * dt * time_ratio
            pacman2.update()

            pacman3.move1(blinky)
            pacman3.x += pacman3.vx * dt * time_ratio
            pacman3.y += pacman3.vy * dt * time_ratio
            pacman3.update()



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
        pacman.draw()
        pacman2.draw()
        pacman3.draw()
        portal_esquerdo.draw()
        portal_esquerdo.update()
        portal_direito.draw()
        portal_direito.update()

        janela.update()

