from intro import *
from menu import *
from main import *
from options import *
from EatThis.Classes.save_systems import *

screen_width = 1280
screen_height = 720
janela = Window(screen_width, screen_height)
janela.set_title("Splash")
input_teclado = janela.get_keyboard()

save = SaveFile("./EatThis/savegame.txt")
save.read_save_from_file()
# plays intro..
play_intro(screen_width, screen_height, save)
next_step = ["menu", save]


while next_step[0] != "close":
    if next_step[0] == "menu":
        next_step = open_menu(screen_width, screen_height, save)
    if next_step[0] == "play":
        play_game(screen_width, screen_height, save)
    if next_step[0] == "options":
        next_step = open_options(screen_width, screen_height, save)
print("Game closed by launcher.")
janela.close()


# TODO: fazer spawn do player pelo portal esquerdo, fazer spawn de "reinforcements" do portal mais distante, fazer spawn da "cadeia".
# TODO: fazer contagem de dinheiro e armazenamento no save.
