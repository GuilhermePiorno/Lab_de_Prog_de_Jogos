from PPlay.window import *
from PPlay.sprite import *

janela = Window(1280, 720)

# Cria o sprite de Blinky e define o número de frames de sua animação.
blinky = Sprite("./Sprites/Blinky.png", 2)
# Duração total da animação em ms, cada animação será mostrada por t/n onde n é o número de frames de animação.
blinky.set_total_duration(300)
blinky.set_position(janela.width/2 - blinky.width/2, janela.height/2 - blinky.height/2)
# Game-loop
while True:
    # Leitura de Entradas

    # Inicialização de objetos
    blinky.move_key_x(0.1)
    blinky.move_key_y(0.1)
    janela.set_background_color((0, 0, 0))

    # Draw
    blinky.draw()
    blinky.update()
    janela.update()
