from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.cinematic_classes import *
from EatThis.cinematics import *
from menu import *


def play_intro(screen_width, screen_height, save):
    #save.write_save_data(save)
    # font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 24)
    font = pygame.font.SysFont('arial', 24)
    msg1 = 'Somewhere in space, a ship carries imprisioned poor souls of conquered enemies.'
    msg2 = 'Literal ghosts of former selves and weakened they have no hope of escaping, unless..'
    msg3 = 'A miracle happens!'

    # snip = font.render('', True, 'white')
    counter = 0
    counter2 = 0
    counter3 = 0
    done = False
    done2 = False
    done3 = False
    tic = 0
    tic2 = 0
    tic3 = 0
    text_speed = 50

    janela = Window(screen_width, screen_height)
    janela.set_title("Intro")
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
    ship.vx = 120
    ship.ax = - (ship.vx ** 2) / (2 * ((janela.width / 2 - ship.width / 2) + ship.width))
    ship.set_position(- ship.width, janela.height / 2 - ship.height / 2)
    # ship.set_position(300, 300)
    ship.f = ship_func
    actor_list.append(ship)

    # Inicia meteoro
    meteor = Actor("Assets/Sprites/Intro/Meteor2.png", 2)
    meteor.set_position(0.8 * janela.width, -meteor.height)
    # meteor.set_position(100,100)
    meteor.set_sequence_time(0, 2, 100, True)
    meteor.play()
    actor_list.append(meteor)

    # Red Flash
    redflash = Sprite("Assets/Sprites/Intro/RedFlash.png")
    redflash.set_position(0, 0)

    # White Flash
    whiteflash = Sprite("Assets/Sprites/Intro/WhiteFlash.png")
    whiteflash.set_position(0, 0)

    # Music
    song = "Assets/Music/FTL - Lanius (Explore).ogg"
    bgm = Sound(song)
    print(f"\nPlaying: {song[13:len(song) - 4]} \n")
    bgm.set_volume(save.BGM_vol)
    bgm.play()

    t = 0.000001  # Evita divisão por 0 no cálculo da posição y da nave.
    on_intro = True

    explosion_sound = Sound("Assets/SFX/ShipExplosion.ogg")
    explosion_sound.set_volume(save.SFX_vol * save.Master_vol)
    play_once = False


    prison = Sprite("Assets/Sprites/Intro/Prison_2.png", 2)
    prison.set_position(0.5*(janela.width-prison.width), 0.5*(janela.height - prison.height))
    prison.set_curr_frame(0)
    prison.hide()

    # image_zoom_test = Actor('Assets/Sprites/WIPs/clock.png')
    # image_zoom_test.x = 50
    # image_zoom_test.y = 50

    one_hertz = False
    two_hertz = False
    freq_clock = 0
    freq_clock2 = 0
    intro_clock = 0
    ship.rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)

    while on_intro:

        dt = janela.delta_time()
        t += dt
        if dt > 0.1:
            dt = 0
        intro_clock += dt
        freq_clock += dt
        if freq_clock > 1:
            one_hertz = not one_hertz
            freq_clock = 0

        if freq_clock2 < 0.5:
            two_hertz = not two_hertz
            freq_clock2 = 0

        # Bloco de texto 1
        pygame.draw.rect(janela.screen, 'black', [0, 600, 1280, 720])
        if t - tic > 1 / text_speed and counter < len(msg1):
            tic = t
            counter += 1
        elif counter >= len(msg1) and not done:
            done = True
        surf_msg1 = font.render(msg1[0:counter], True, 'yellow')

        # Bloco de texto 2
        if intro_clock > 4 and t - tic2 > 1 / text_speed and counter2 < len(msg2):
            tic2 = t
            counter2 += 1
        elif counter2 >= len(msg2) and not done2:
            done2 = True
        surf_msg2 = font.render((msg2[0:counter2]), True, 'yellow')

        # Bloco de texto 3
        if intro_clock > 16 and t - tic3 > 1 / text_speed and counter3 < len(msg3):
            tic3 = t
            counter3 += 1
        elif counter3 >= len(msg3) and not done3:
            done3 = True
        surf_msg3 = font.render((msg3[0:counter3]), True, 'yellow')

        if intro_clock > 15:
            meteor.vx = -800
            meteor.vy = 800



        # Eventos
        update_actors(actor_list, dt, t, screen_width, screen_height)
        background.draw()
        stars.draw()
        # ship.draw()
        # ship.rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
        prison.draw()
        janela.screen.blit(ship.img, ship.rect)
        dust[0].draw()
        dust[1].draw()
        meteor.update()
        meteor.draw()

        # Texto
        if intro_clock < 29:
            janela.screen.blit(surf_msg1, (10, 580))
            janela.screen.blit(surf_msg2, (10, 620))
            janela.screen.blit(surf_msg3, (10, 660))
        # print(intro_clock)


        # zoom_speed = 1
        # image_zoom_test.change_size(zoom_speed)
        # alpha = 128
        # image_zoom_test.change_transparency(alpha)
        # image_zoom_test.rect = pygame.Rect(image_zoom_test.x, image_zoom_test.y, image_zoom_test.width, image_zoom_test.height)
        # janela.screen.blit(image_zoom_test.img, image_zoom_test.rect)
        #image_zoom_test.draw()

        if 0.5 * janela.height <= meteor.y < 0.6 * janela.height:
            redflash.draw()
            if not play_once:
                play_once = True
                explosion_sound.play()
        if 0.6 * janela.height <= meteor.y < 0.7 * janela.height:
            whiteflash.draw()
        if 0.7 * janela.height <= meteor.y < 0.8 * janela.height:
            redflash.draw()

        if intro_clock > 27:
            prison.unhide()

        if 29 < intro_clock < 31:
            if two_hertz:
                prison.set_curr_frame(0)
            else:
                prison.set_curr_frame(1)

        if 31 < intro_clock < 33:
            if one_hertz:
                prison.set_curr_frame(0)
            else:
                prison.set_curr_frame(1)
        if intro_clock > 33:
            prison.set_curr_frame(1)

        if intro_clock > 36:
            on_intro = False
            bgm.stop()
            return
        # Update
        janela.update()

        if input_teclado.key_pressed("ESC"):
            on_intro = False
            bgm.stop()
            return
