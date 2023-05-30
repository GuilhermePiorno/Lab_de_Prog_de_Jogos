from PPlay.window import *
from PPlay.sound import *
from EatThis.Classes.cinematic_classes import *
from math import sin


def ship_func(actor, dt, time):
    if time > 3:  # 3 segundos de delay para a nave aparecer
        if actor.vx > 0:
            actor.x += actor.vx * dt + (actor.ax * dt ** 2) / 2
            actor.vx += actor.ax * dt
        else:
            actor.vx = 0
            actor.ax = 0

    amplitude = 500 / time
    ship.y = janela.height / 2 - ship.height / 2 + amplitude * sin(time)


def dust_func(actor, dt, time):
    actor.x += actor.vx * dt
    if actor.x < - actor.width:
        actor.x = actor.width


def move_actor(actor, dt, time):
    if actor.f == "":
        actor.vx += actor.ax * dt
        actor.vy += actor.ax * dt
        actor.x += actor.vx * dt
        actor.y += actor.vy * dt
    else:
        actor.f(actor, dt, time)


def update_actors(actor_list, dt, time):
    for i in range(len(actor_list)):
        if type(actor_list[i]) == list:
            for j in range(len(actor_list[i])):
                move_actor(actor_list[i][j], dt, time)
        else:
            move_actor(actor_list[i], dt, time)


janela = Window(1280, 720)
janela.set_title("Game Start")

actor_list = []
# Spawn assets
background = Actor("Sprites/Intro/Asset_Sky_Extended.png")
background.vx = -2
actor_list.append(background)
stars = Actor("Sprites/Intro/Asset_Stars_Extended.png")
stars.vx = -4
actor_list.append(stars)

# Inicia poeira espacial/destritos voando rapidamente
dust = [Actor("Sprites/Intro/Asset_Dust_Extended.png"), Actor("Sprites/Intro/Asset_Dust_Extended.png")]
dust[0].f = dust_func
dust[1].f = dust_func
dust[0].x = 0
dust[0].vx = -1000
dust[1].x = dust[1].width
dust[1].vx = -1000
actor_list.append(dust)

# Inicia nave.
ship = Actor("Sprites/Intro/SpaceShip_Scaled.png")
ship.vx = 60
ship.ax = - (ship.vx ** 2) / (2 * ((janela.width / 2 - ship.width / 2) + ship.width))
ship.set_position(- ship.width, janela.height / 2 - ship.height / 2)
ship.f = ship_func
actor_list.append(ship)

song = "music/FTL - Lanius (Explore).mp3"

# Music
bgm = Sound(song)
print(f"\nPlaying: {song[6:len(song) - 4]} \n")
bgm.set_volume(50)
bgm.play()
time = 0.000001  # Evita divisão por 0 no cálculo da posição y da nave.
on_menu = True
tempo = 0
cont = 0
FPS = 0
while on_menu:
    dt = janela.delta_time()
    time += dt

    str1 = "looooooo-abcdefghijklkmlniopquertoqpoiueralkfdhzcv^oooooooooooooooooooooong"
    # str1 = "MUITO TEXTO"
    # str2 = "MUITO TEXTO"
    # str3 = "MUITO TEXTO"
    # str4 = "MUITO TEXTO"
    # str5 = "MUITO TEXTO"



    # FPS
    tempo += dt
    cont += 1
    if tempo >= 1:
        tempo = 0
        FPS = cont
        cont = 0

    update_actors(actor_list, dt, time)
    background.draw()
    stars.draw()
    ship.draw()
    dust[0].draw()
    dust[1].draw()
    janela.draw_text(str(FPS), 10, janela.height - 50, size=25, color=(255, 255, 0))
    janela.draw_text(str1, 10, 50, size=25, color=(255, 255, 0))
    # janela.draw_text(str2, 10, 100, size=25, color=(255, 255, 0))
    # janela.draw_text(str3, 10, 150, size=25, color=(255, 255, 0))
    # janela.draw_text(str4, 10, 200, size=25, color=(255, 255, 0))
    # janela.draw_text(str5, 10, 250, size=25, color=(255, 255, 0))
    janela.update()


