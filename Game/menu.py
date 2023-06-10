from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
import os

def open_menu(screen_width, screen_height, save):
    janela = Window(screen_width, screen_height)
    janela.set_title("Menu")
    background = Sprite("Assets/Sprites/Menu/Menu_Background_Empty.png")
    cursor = Sprite("Assets/Sprites/Characters/Blinky.png", 12)
    cursor.set_sequence_time(0, 2, 100, True)
    teclado = janela.get_keyboard()
    in_menu = True
    button_state = True
    last_input = "esc"
    selection_index = 0
    save_found = True if os.path.exists("./EatThis/savegame.txt") else False
    # print("Sava Data found!" if save_found else "No Save Data found..")

    # Sounds
    sfx_select = Sound('Assets/SFX/Select_0.wav')
    sfx_select.set_volume(save.SFX_vol * save.Master_vol)
    sfx_confirm = Sound('Assets/SFX/Confirm_0.wav')
    sfx_confirm.set_volume(save.SFX_vol * save.Master_vol)
    sfx_cancel = Sound('Assets/SFX/Cancel_0.wav')
    sfx_cancel.set_volume(save.SFX_vol * save.Master_vol)



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
        sfx_select.set_volume(save.SFX_vol * save.Master_vol)
        sfx_confirm.set_volume(save.SFX_vol * save.Master_vol)
        sfx_cancel.set_volume(save.SFX_vol * save.Master_vol)

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
                    return ["play", save]
                if menu_selection[selection_index] == "newgame":
                    print("New game selected.")
                    aux = [save.Master_vol, save.BGM_vol, save.SFX_vol]
                    save.reset_save_data() # resta o save
                    save.Master_vol = aux[0]
                    save.BGM_vol = aux[1]
                    save.SFX_vol = aux[2]
                    save.write_save_to_file() # escreve save em arquivo.
                    return ["play", save]
                elif menu_selection[selection_index] == "options":
                    print("Options selected.")
                    return ["options", save]
                elif menu_selection[selection_index] == "exit":
                    save.write_save_to_file()
                    return ["close", save]
        if not teclado.key_pressed(last_input) and not teclado.key_pressed("return"):
            button_state = False

        cursor_x_pos = janela.width / 2 - newgame.get_width() / 2 - cursor.width - 10
        if selection_index == 0:
            cursor.set_position(cursor_x_pos, 450)
            loadgame = font.render(message0, True, 'yellow')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 1:
            cursor.set_position(cursor_x_pos, 520)

            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'yellow')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 2:
            cursor.set_position(cursor_x_pos, 590)

            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'yellow')
            quit_game = font.render(message3, True, 'white')
        elif selection_index == 3:
            cursor.set_position(cursor_x_pos, 660)
            loadgame = font.render(message0, True, 'white')
            newgame = font.render(message1, True, 'white')
            options = font.render(message2, True, 'white')
            quit_game = font.render(message3, True, 'yellow')

        background.draw()

        janela.screen.blit(loadgame, (janela.width / 2 - newgame.get_width() / 2, 440))
        janela.screen.blit(newgame, (janela.width / 2 - newgame.get_width() / 2, 510))
        janela.screen.blit(options, (janela.width / 2 - newgame.get_width() / 2, 580))
        janela.screen.blit(quit_game, (janela.width / 2 - newgame.get_width() / 2, 650))
        cursor.draw()
        cursor.update()
        janela.update()
