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



teclado = Window.get_keyboard()
facing = 'AFK'
# Game-loop
blinky.set_sequence(0, 1, True)

FPS = 0
tempo = 0
cont = 0
while True:
    # Leitura de Entradas

    # Mudança de animação de Blinky nas 4 direções cardinais.
    """
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
    """

    # Movimento do blinky, fazendo com que ele não possa se mover na diagonal
    if(teclado.key_pressed("UP") and not(teclado.key_pressed("DOWN") or teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT"))):
        blinky.set_sequence(6, 8, True)
        blinky.move_key_y(1)
    if(teclado.key_pressed("DOWN") and not(teclado.key_pressed("UP") or teclado.key_pressed("RIGHT") or teclado.key_pressed("LEFT"))):
        blinky.set_sequence(4, 6, True)
        blinky.move_key_y(1)
    if(teclado.key_pressed("RIGHT") and not(teclado.key_pressed("DOWN") or teclado.key_pressed("UP") or teclado.key_pressed("LEFT"))):
        blinky.set_sequence(0, 2, True)
        blinky.move_key_x(1)
    if(teclado.key_pressed("LEFT") and not(teclado.key_pressed("DOWN") or teclado.key_pressed("RIGHT") or teclado.key_pressed("UP"))):
        blinky.set_sequence(2, 4, True)
        blinky.move_key_x(1)

    """
    if facing == "U":
        blinky.set_sequence(6, 8, True)
    if facing == "D":
        blinky.set_sequence(4, 6, True)
    if facing == "L":
        blinky.set_sequence(2, 4, True)
    if facing == "R":
        blinky.set_sequence(0, 2, True)
    """
    


    # Movimento básico para teste de animação, descomente para habilitar.
    # blinky.move_key_x(1)
    # blinky.move_key_y(1)

    # FPS
    tempo += janela.delta_time()
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0



    # Inicialização de objetos
    janela.set_background_color((0, 0, 0))
    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))
    janela.draw_text("LEFT:" + str(teclado.key_pressed("LEFT")), 200, 200, size=25, color=(255,255,0))
    janela.draw_text("RIGHT:" + str(teclado.key_pressed("RIGHT")), 200, 225, size=25, color=(255,255,0))
    janela.draw_text("UP:" + str(teclado.key_pressed("UP")), 200, 250, size=25, color=(255,255,0))
    janela.draw_text("DOWN:" + str(teclado.key_pressed("DOWN")), 200, 275, size=25, color=(255,255,0))

    # Draw
    blinky.draw()
    blinky.update()
    janela.update()
