from PPlay.window import *
from PPlay.sprite import *
from PPlay.keyboard import *

janela = Window(1280, 720)

# Cria o sprite de Blinky e define o número de frames de sua animação.
blinky = Sprite("./Sprites/Blinky.png", 8)


blinky.set_position(janela.width / 2 - blinky.width / 2, janela.height / 2 - blinky.height / 2)

# O intervalo de frames parece funcionar fechado/aberto -> [Frame_Inicial, Frame Final)
# ex: example.set_sequence_time(0, 1, _total_duration_, _loop_boolean_) mostra apenas o frame 0.
# Duração total da animação em ms, cada animação será mostrada por t/n onde n é o número de frames de animação.
blinky.set_sequence_time(0, 8, 100, True)



teclado = Keyboard()
facing = 'AFK'
# Game-loop
blinky.set_sequence(0, 1, True)
while True:
    # Leitura de Entradas


    if teclado.key_pressed("UP") and facing != 'U':
        facing = 'U'
        blinky.set_sequence(6, 8, True)
    if teclado.key_pressed("DOWN") and facing != 'D':
        facing = 'D'
        blinky.set_sequence(4, 6, True)
    if teclado.key_pressed("LEFT") and facing != 'L':
        facing = 'L'
        blinky.set_sequence(2, 4, True)
    if teclado.key_pressed("RIGHT") and facing != 'R':
        facing = 'R'
        blinky.set_sequence(0, 2, True)

    # Movimento básico para teste de animação, descomente para habilitar.
    # blinky.move_key_x(0.1)
    # blinky.move_key_y(0.1)

    # Inicialização de objetos
    janela.set_background_color((0, 0, 0))

    # Draw
    blinky.draw()
    blinky.update()
    janela.update()
