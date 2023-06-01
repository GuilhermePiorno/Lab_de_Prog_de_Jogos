from PPlay.window import *


def open_options(screen_width, screen_height):
    janela = Window(1280, 720)
    teclado = janela.get_keyboard()
    ingame = True
    while ingame:
        if teclado.key_pressed("ESC"):
            return 100

        janela.set_background_color((100, 100, 100))
        janela.update()
