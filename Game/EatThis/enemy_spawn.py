from random import randint
from random import random
from EatThis.Classes.Enemy import *
def getpositions(mat, num=1):
    lista = []
    for i in range(num):
        linha = randint(2, 30)
        coluna = randint(2, 27)
        while mat[linha][coluna] == 1 and (linha, coluna) not in lista:
            linha = randint(2, 30)
            coluna = randint(2, 27)
        lista.append((linha, coluna))
    return lista

def create_pacmans(janela, maze, numero_inimigos, save):
    """
    Creates a list of pacmans, each have a different position.
    :return:
    """
    enemies_list = []
    list_of_spawn_positions = getpositions(maze.pathing, numero_inimigos)
    enemy_type = "normal"
    for i in range(numero_inimigos):
        if i > 0:
            roll = random.random()
            if roll < 0.2:
                enemy_type = "angry"
            elif roll < 0.5:
                enemy_type = "tired"
            else:
                enemy_type = "normal"

        if enemy_type == "tired":
            pacman = Enemy(f"pac_{i}", janela, maze, save, "Assets/Sprites/Characters/pacman_tired.png", 22)
            pacman.base_speed *= 0.8
            pacman.base_fear_time *= 1.2
        elif enemy_type == "angry":
            pacman = Enemy(f"pac_{i}", janela, maze, save, "Assets/Sprites/Characters/pacman_angry.png", 22)
            pacman.base_speed *= 1.2
            pacman.base_fear_time *= 0.5
        else:
            pacman = Enemy(f"pac_{i}", janela, maze, save, "Assets/Sprites/Characters/pacman.png", 22)

        pacman.set_position(maze.get_spawn_coordinates(list_of_spawn_positions[i], pacman.width, pacman.height)[0],
                            maze.get_spawn_coordinates(list_of_spawn_positions[i], pacman.width, pacman.height)[1])
        pacman.set_sequence_time(0, 8, 100, True)
        pacman.set_sequence(0, 1, True)
        enemies_list.append(pacman)

    return enemies_list
