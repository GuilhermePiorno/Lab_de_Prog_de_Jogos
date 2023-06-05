from PPlay.window import *
from PPlay.sprite import *
from EatThis.game_save_data import *
from PPlay.sound import *
import os

UPGRADE_VELOCIDADE = 0      # [nível do upgrade]
UPGRADE_MEIA_VOLTA = 1      # [nível do upgrade]
UPGRADE_STATE_CHANGE = 2    # [liga/desliga, cooldown]
UPGRADE_TIRO = 3            # [liga/desliga]
BULLET_TIME = 4             # [liga/desliga, duration



def open_menu(screen_width, screen_height):

    janela = Window(screen_width, screen_height)
    background = Sprite("Assets/Sprites/Menu/Menu_Background_Empty.png")
    cursor = Sprite("Assets/Sprites/Characters/Blinky.png", 12)
    cursor.set_sequence_time(0, 2, 100, True)
    teclado = janela.get_keyboard()
    in_menu = True
    button_state = True
    last_input = "esc"
    selection_index = 0
    save_found = False
    sfx_select = Sound('Assets/SFX/Select_0.wav')
    sfx_select.set_volume(50)
    sfx_confirm = Sound('Assets/SFX/Confirm_0.wav')
    sfx_confirm.set_volume(50)
    sfx_cancel = Sound('Assets/SFX/Cancel_0.wav')
    sfx_cancel.set_volume(50)

    if os.path.exists("./EatThis/savegame.txt"):  # Caso não haja save..
        save_found = True

    print("Sava Data found!" if save_found else "No Save Data found..")


    menu_selection = ["continue", "newgame", "options", "exit"]


    font = pygame.font.Font('Assets/Fonts/ARCADE.TTF', 80)
    if save_found:
        message0 = 'CONTINUE'
    else:
        message0 = ''
    loadgame = font.render(message0, True, 'white')
    message1 = 'NEW GAME'
    newgame = font.render(message1, True, 'white')
    message2 = 'OPTIONS'
    options = font.render(message2, True, 'white')
    message3 = 'QUIT'
    quit_game = font.render(message3, True, 'white')

    select = selection_index
    selection_index = selection_index + 1 if not save_found else selection_index

    while in_menu:
        if not button_state:
            if teclado.key_pressed("down"):
                button_state = True
                last_input = "down"
                sfx_select.play()
                if save_found:
                    select = (select + 1) % len(menu_selection)
                    selection_index = select
                else:
                    select = (select + 1) % (len(menu_selection) - 1)
                    selection_index = select + 1

            if teclado.key_pressed("up"):
                button_state = True
                sfx_select.play()
                last_input = "up"
                if save_found:
                    select = (select - 1) % len(menu_selection)
                    selection_index = select
                else:
                    select = (select - 1) % (len(menu_selection) - 1)
                    selection_index = select + 1
            if teclado.key_pressed("return"):
                button_state = True
                sfx_confirm.play()
                last_input = "return"
                if menu_selection[selection_index] == "continue":
                    print("Load game selected.")
                    save_data = read_save_data()
                    return "play"
                if menu_selection[selection_index] == "newgame":
                    print("New game selected.")
                    reset_save_data()
                    save_data = read_save_data()
                    return "play"
                elif menu_selection[selection_index] == "options":
                    print("Options selected.")
                    return "options"
                elif menu_selection[selection_index] == "exit":
                    return "close"
        if not teclado.key_pressed(last_input) and not teclado.key_pressed("return"):
            button_state = False

        if selection_index == 0:
            cursor.set_position(janela.width/2 - newgame.get_width()/2 - cursor.width - 10, 450)
            loadgame = font.render(message0, True, 'yellow')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 1:
            cursor.set_position(janela.width/2 - newgame.get_width()/2 - cursor.width - 10, 520)

            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'yellow')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 2:
            cursor.set_position(janela.width/2 - newgame.get_width()/2 - cursor.width - 10, 590)

            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'yellow')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 3:
            cursor.set_position(janela.width / 2 - newgame.get_width() / 2 - cursor.width - 10, 660)
            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'yellow')

        background.draw()


        janela.screen.blit(loadgame, (janela.width / 2 - newgame.get_width() / 2, 440))
        janela.screen.blit(newgame, (janela.width/2 - newgame.get_width()/2, 510))
        janela.screen.blit(options, (janela.width / 2 - newgame.get_width() / 2, 580))
        janela.screen.blit(quit_game, (janela.width / 2 - newgame.get_width() / 2, 650))
        cursor.draw()
        cursor.update()
        janela.update()

