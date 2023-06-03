from intro import *
from menu import *
from main import *
from options import *

screen_width = 1280
screen_height = 720
janela = Window(screen_width, screen_height)
janela.set_title("Splash")
input_teclado = janela.get_keyboard()
vol = 10

play_intro(screen_width, screen_height)
next_step = ""
while next_step != "close":
    next_step = open_menu(screen_width, screen_height)

    if next_step == "play":
        play_game(screen_width, screen_height, vol)
    elif next_step == "options":
        vol = open_options(screen_width, screen_height)

print("Game closed by launcher.")
janela.close()

