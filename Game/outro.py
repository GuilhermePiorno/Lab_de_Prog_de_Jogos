from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *
import random

def cockpit_scene():
    janela = Window(1080, 720)
    teclado = janela.get_keyboard()

    cockpit = Sprite("Assets\Sprites\Outro\cockpit_1080_720(1)_sem_janela_3.png", 3)
    cockpit.set_sequence(0, 2, True)
    cockpit.set_total_duration(400)
    fundo = GameImage("Assets\Sprites\Intro\Asset_Sky_Extended.png")
    poeiras = [Sprite("Assets\Sprites\Intro\Asset_Dust_Extended.png", 1), Sprite("Assets\Sprites\Intro\Asset_Dust_Extended.png", 1)]
    poeiras[0].set_position(0, 0)
    poeiras[1].set_position(poeiras[0].width, 0)
    estrelas = [Sprite("Assets\Sprites\Intro\Asset_Stars_Extended.png", 1), Sprite("Assets\Sprites\Intro\Asset_Stars_Extended.png", 1)]
    estrelas[0].set_position(0, 0)
    estrelas[1].set_position(estrelas[0].width, 0)
    velocidade_poeira = 1000
    velocidade_estrelas = 10

    blinky = Sprite("Assets\Sprites\Outro\\blinky_cockpit.png", 2)
    blinky.set_sequence_time(0, 2, 100, True)
    blinky.set_position(-blinky.width, janela.height - blinky.height)

    while(True):

        dt = janela.delta_time()

        # movimenta o blinky
        if teclado.key_pressed("RIGHT"):
            blinky.x += 200 * dt
        if teclado.key_pressed("LEFT"):
            blinky.x -= 200 * dt

        # muda o conteúdo da tela da nave quando blinky chega perto dela
        if blinky.x + blinky.width >= janela.width/2:
            cockpit.set_sequence(2, 3)
            if(teclado.key_pressed("SPACE")):
                play_outro()

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
        
        fundo.draw()
        for poeira in poeiras:
            poeira.draw()
        for estrela in estrelas:
            estrela.draw()
        cockpit.draw()
        cockpit.update()
        blinky.draw()
        blinky.update()
        janela.update()

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
    vx_nave = 50
    vy_nave = 0
    velocidade_poeira = 1000
    velocidade_estrelas = 10
    sair = False

    pacman_dt = 3
    escolheu_pacman_dt = True
    pacman_timer_ejecao = 0

    som_pacman_morte = Sound("Assets\SFX\PacmanDeath.ogg")

    pacmans_ejetados = []

    while True:

        dt = janela.delta_time()
        if dt > 0.1:
            dt = 0
        
        # usado para adicionar aleatoriedade nos intervalos entre ejeções de pacmans
        if not escolheu_pacman_dt:
            pacman_dt = random.randint(2, 5)
            escolheu_pacman_dt = True

        pacman_timer_ejecao += dt
        
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

        nave.x += vx_nave * dt
        nave.y += vy_nave * dt
        # movimenta a nave até o meio da tela
        if nave.x + nave.width/2 < janela.width/2:
            if teclado.key_pressed("RIGHT"):
                vx_nave += 1
            if teclado.key_pressed("LEFT"):
                vx_nave -= 1
            if teclado.key_pressed("UP"):
                vy_nave -= 1
            if teclado.key_pressed("DOWN"):
                vy_nave += 1
        else:
            # após a nave chegar ao meio da tela, se espaço for pressionado a nave irá sair da tela pela extremidade direita
            if teclado.key_pressed("SPACE"):
                sair = True

        if sair:
            vx_nave += 5
            vy_nave = 0
            
        if nave.x > janela.width:
            janela.close()

        # ejeta um pacman de algum lugar da nave
        if pacman_timer_ejecao > pacman_dt:
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
            pacman_timer_ejecao = 0

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

cockpit_scene()
