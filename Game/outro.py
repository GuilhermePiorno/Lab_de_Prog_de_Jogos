from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *
import random

def play_outro():
    janela = Window(1280, 720)
    teclado = janela.get_keyboard()
    nave = Sprite("Assets\Sprites\Intro\SpaceShip_Scaled.png", 1)
    nave.set_position(-nave.width, janela.height/2)
    fundo = GameImage("Assets\Sprites\Intro\Asset_Sky_Extended.png")
    poeiras = [Sprite("Assets\Sprites\Intro\Asset_Dust_Extended.png", 1), Sprite("Assets\Sprites\Intro\Asset_Dust_Extended.png", 1)]
    poeiras[0].set_position(0, 0)
    poeiras[1].set_position(poeiras[0].width, 0)
    estrelas = [Sprite("Assets\Sprites\Intro\Asset_Stars_Extended.png", 1), Sprite("Assets\Sprites\Intro\Asset_Stars_Extended.png", 1)]
    estrelas[0].set_position(0, 0)
    estrelas[1].set_position(estrelas[0].width, 0)
    velocidade_nave = 500
    velocidade_poeira = 1000
    velocidade_estrelas = 10
    sair = False

    pacman_dt = 3
    escolheu_pacman_dt = True
    pacman_timer = 0

    som_pacman_morte = Sound("Assets\SFX\PacmanDeath.ogg")

    pacmans_ejetados = []

    while True:

        dt = janela.delta_time()

        if not escolheu_pacman_dt:
            pacman_dt = random.randint(2, 5)
            escolheu_pacman_dt = True
            
        pacman_timer += dt
        
        # movimenta as estrelas
        for estrela in estrelas:
            estrela.x -= velocidade_estrelas * dt
            if estrela.x < -estrela.width:
                estrela.x = estrela.width

        # movimenta a poeira
        for poeira in poeiras:
            poeira.x -= velocidade_poeira * dt
            if poeira.x < -poeira.width:
                poeira.x = poeira.width

        # movimenta a nave até o meio da tela
        if nave.x + nave.width/2 < janela.width/2:
            if teclado.key_pressed("RIGHT"):
                nave.x += velocidade_nave * dt
            if teclado.key_pressed("LEFT"):
                nave.x -= velocidade_nave * dt
            if teclado.key_pressed("UP"):
                nave.y -= velocidade_nave * dt
            if teclado.key_pressed("DOWN"):
                nave.y += velocidade_nave * dt
        else:
            if teclado.key_pressed("SPACE"):
                sair = True

        if sair:
            nave.x += 2 * velocidade_nave * dt
            
        if nave.x > janela.width:
            janela.close()

        # ejeta um pacman de algum lugar da nave
        if pacman_timer > pacman_dt:
            escolheu_pacman_dt = False
            pacman = Sprite("Assets\Sprites\Characters\pacman_movimento_e_morte.png", 22)
            x = random.randint(int(nave.x), int(nave.x + nave.width))
            y = random.randint(int(nave.y), int(nave.y + nave.height))
            pacman.set_position(x, y)
            pacman.set_sequence_time(0, 22, 100, False)
            vx = -random.randint(100, 500)
            vy = random.randint(-500, 500)
            pacmans_ejetados.append([pacman, vx, vy])
            som_pacman_morte.play()
            pacman_timer = 0

        # movimenta os pacmans ejetados
        for pacman in pacmans_ejetados:
            pacman[0].x += pacman[1] * dt
            pacman[0].y += pacman[2] * dt

        # remove os pacmans que estão fora da tela
        for pacman in pacmans_ejetados:
            if pacman[0].x < -pacman[0].width or pacman[0].y < -pacman[0].height or pacman[0].y > janela.height:
                pacmans_ejetados.remove(pacman)
        
        fundo.draw()
        for poeira in poeiras:
            poeira.draw()
        for estrela in estrelas:
            estrela.draw()
        nave.draw()
        for pacman in pacmans_ejetados:
            pacman[0].update()
            pacman[0].draw()
        janela.update()

play_outro()