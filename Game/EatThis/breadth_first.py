# tutorial: https://www.youtube.com/watch?v=hettiSrJjM4 

import queue
from procedural_map import *


def foundTarget(maze, moves):
    i = pacman_x_index
    j = pacman_y_index

    k = blinky_x_index
    l = blinky_y_index

    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1

    if(i == k and j == l):
        print("Foundo: " + moves)
        return True
    
    return False


def valid(maze, moves):
    i = pacman_x_index
    j = pacman_y_index

    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1

        if not((2 <= i <= 30) and (2 <= j <= 27)):
            return False
        elif(maze[i][j] == 1):
            return False
        
    return True



createlevel()
maze = [[1]*30 for _ in range(33)]

with open('maze.txt', mode='r', encoding='utf-8') as fin:
    fin.readline() #pula a primeira linha vazia
    for i in range(31):
        linha = fin.readline()
        for j in range(28):
            if(linha[j] != "|"):
                maze[i+1][j+1] = 0

# posiciona por enquanto blinky e pacman nos extremos opostos do mapa. Posteriormente essas posições serão variáveis e serão importadas ou 
# de main.py ou dos objetos blinky e pacman
blinky_x_index = 2
blinky_y_index = 2
pacman_x_index = 2
pacman_y_index = 20

paths = queue.Queue()
paths.put("")
add = ""

while not foundTarget(maze, add):
    add = paths.get()
    for j in ["L", "R", "D", "U"]:
        put =  add + j
        if valid(maze, put):
            paths.put(put)
            print(put)
