from PPlay.window import *
from PPlay.sprite import *


# from main import *

def open_menu(screen_width, screen_height):
    janela = Window(screen_width, screen_height)
    background = Sprite("Sprites/Menu/Menu_Background.png")
    cursor = Sprite("Sprites/Blinky.png", 12)
    cursor.set_sequence_time(0, 2, 100, True)
    teclado = janela.get_keyboard()
    in_menu = True
    button_state = False
    last_input = "esc"
    menu_selection = ["start", "options", "exit"]
    selection_index = 0

    while in_menu:

        if not button_state:
            if teclado.key_pressed("down"):
                button_state = True
                last_input = "down"
                selection_index = (selection_index + 1) % len(menu_selection)
            if teclado.key_pressed("up"):
                button_state = True
                last_input = "up"
                selection_index = (selection_index - 1) % len(menu_selection)
            if teclado.key_pressed("return"):
                button_state = True
                last_input = "return"
                if menu_selection[selection_index] == "start":
                    print("New game selected")
                    return "play"
                elif menu_selection[selection_index] == "options":
                    print("Options selected")
                    return "options"
                elif menu_selection[selection_index] == "exit":
                    return "close"

        if not teclado.key_pressed(last_input):
            button_state = False

        if selection_index == 0:
            cursor.set_position(525, 510)
        elif selection_index == 1:
            cursor.set_position(525, 580)
        elif selection_index == 2:
            cursor.set_position(525, 650)

        background.draw()
        cursor.draw()
        cursor.update()
        janela.update()
