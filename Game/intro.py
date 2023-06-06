from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.cinematic_classes import *
from EatThis.cinematics import *
from menu import *


def play_intro(screen_width, screen_height):
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    message = 'Check out this long ass message! The quick brown fox jumps over the lazy dog.'
    # snip = font.render('', True, 'white')
    counter = 0
    done = False
    tic = 0
    text_speed = 50

    janela = Window(screen_width, screen_height)
    janela.set_title("Game Start")
    input_teclado = janela.get_keyboard()

    # ============================Incialização de atores em uma lista "actor_list"============================
    actor_list = []
    # Spawn assets
    background = Actor("Assets/Sprites/Intro/Asset_Sky_Extended.png")
    background.vx = -2
    actor_list.append(background)
    stars = Actor("Assets/Sprites/Intro/Asset_Stars_Extended.png")
    stars.vx = -4
    actor_list.append(stars)

    # Inicia poeira espacial/destritos voando rapidamente
    dust = [Actor("Assets/Sprites/Intro/Asset_Dust_Extended.png"), Actor(
        "Assets/Sprites/Intro/Asset_Dust_Extended.png")]
    dust[0].f = dust_func
    dust[1].f = dust_func
    dust[0].x = 0
    dust[0].vx = -1000
    dust[1].x = dust[1].width
    dust[1].vx = -1000
    actor_list.append(dust)

    # Inicia nave.
    ship = Actor("Assets/Sprites/Intro/SpaceShip_Scaled.png")
    ship.vx = 60
    ship.ax = - (ship.vx ** 2) / (2 * ((janela.width / 2 - ship.width / 2) + ship.width))
    ship.set_position(- ship.width, janela.height / 2 - ship.height / 2)
    ship.f = ship_func
    actor_list.append(ship)

    # Music
    song = "Assets/Music/FTL - Lanius (Explore).mp3"
    bgm = Sound(song)
    print(f"\nPlaying: {song[13:len(song) - 4]} \n")
    bgm.set_volume(50)
    bgm.play()

    t = 0.000001  # Evita divisão por 0 no cálculo da posição y da nave.
    on_intro = True

    while on_intro:
        dt = janela.delta_time()
        t += dt
        if dt > 0.1:
            dt = 0

        pygame.draw.rect(janela.screen, 'black', [0, 600, 1280, 720])
        if t - tic > 1 / text_speed and counter < len(message):
            tic = t
            counter += 1
        elif counter >= len(message) and not done:
            done = True
        snip = font.render(message[0:counter], True, 'white')

        # Eventos
        update_actors(actor_list, dt, t, screen_width, screen_height)
        background.draw()
        stars.draw()
        ship.draw()
        dust[0].draw()
        dust[1].draw()

        # Texto
        janela.screen.blit(snip, (10, 610))
        janela.screen.blit(snip, (10, 650))
        janela.screen.blit(snip, (10, 690))

        # Update
        janela.update()

        if input_teclado.key_pressed("ESC"):
            on_intro = False
            bgm.stop()
            return
