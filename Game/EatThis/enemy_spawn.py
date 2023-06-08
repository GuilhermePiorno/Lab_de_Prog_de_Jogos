from random import randint
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
    for i in range(numero_inimigos):
        pacman = Enemy(f"pac_{i}", janela, maze, save, "Assets/Sprites/Characters/pacman_movimento_e_morte.png", 22)
        pacman.set_position(maze.get_spawn_coordinates(list_of_spawn_positions[i], pacman.width, pacman.height)[0],
                            maze.get_spawn_coordinates(list_of_spawn_positions[i], pacman.width, pacman.height)[1])
        pacman.set_sequence_time(0, 8, 100, True)
        pacman.set_sequence(0, 1, True)
        enemies_list.append(pacman)
    return enemies_list
