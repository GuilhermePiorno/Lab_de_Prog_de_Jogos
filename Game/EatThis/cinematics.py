from math import sin
import pygame

# Chama move_actor para cada item da lista e verifica se algum item é uma lista de atores.
def update_actors(actor_list, dt, time, width, height):
    for i in range(len(actor_list)):
        if type(actor_list[i]) == list:
            for j in range(len(actor_list[i])):
                move_actor(actor_list[i][j], dt, time, width, height)
        else:
            move_actor(actor_list[i], dt, time, width, height)

# Move o ator de acordo com sua função de movimento ou de acordo com a física.
def move_actor(actor, dt, time, width, height):
    if actor.f == "":  # Se não possuí função de movimento, usa física.
        actor.x += actor.vx * dt + (actor.ax * dt ** 2) / 2
        actor.y += actor.vy * dt + (actor.ay * dt ** 2) / 2
        actor.vx += actor.ax * dt
        actor.vy += actor.ax * dt
    else:
        actor.f(actor, dt, time, width, height)  # Chama função de movimento do ator.

# Utiliza *args para permitir que a função seja chamada com qualquer número de argumentos.
# já que nem toda função utiliza todos os argumentos.
def ship_func(*args):
    actor = args[0]
    dt = args[1]
    time = args[2]
    height = args[4]
    if 3 < time < 32:  # 3 segundos de delay para a nave aparecer
        if actor.vx > 0:
            actor.x += actor.vx * dt + (actor.ax * dt ** 2) / 2
            actor.vx += actor.ax * dt
            # actor.rect = actor.image.get_rect(center=(actor.x, actor.y))
            actor.rect = pygame.Rect(actor.x, actor.y, actor.width, actor.height)
        else:
            actor.change_size(3)
            actor.vx = 0
            actor.ax = 0
            alpha = 255
            if 30 < time < 32:
                alpha = 255*((-1*0.5*time)+16)
                if alpha < 0:
                    alpha = 0
            elif time >= 30:
                alpha = 0
            actor.change_transparency(alpha)

    amplitude = 500 / time
    actor.y = height / 2 - actor.height / 2 + amplitude * sin(time)


def dust_func(*args):
    actor = args[0]
    dt = args[1]
    actor.x += actor.vx * dt
    if actor.x < - actor.width:
        actor.x = actor.width






