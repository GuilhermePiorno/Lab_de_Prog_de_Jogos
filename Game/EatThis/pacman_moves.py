# tutorial: https://www.youtube.com/watch?v=hettiSrJjM4 

import queue

def foundTarget(moves, pacman_matrix_position, blinky_matrix_position):
    i = pacman_matrix_position[0]
    j = pacman_matrix_position[1]

    k = blinky_matrix_position[0]
    l = blinky_matrix_position[1]

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
        print("Found: " + moves)
        return True
    
    return False


def valid(maze, moves, pacman_matrix_position):
    i = pacman_matrix_position[0]
    j = pacman_matrix_position[1]

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
        elif(maze[i][j] != 0):
            return False
        
    return True


def pacman_move_list(maze, pacman_matrix_position, blinky_matrix_position):
    
    paths = queue.Queue()
    paths.put("")
    add = ""

    while not foundTarget(add, pacman_matrix_position, blinky_matrix_position):
        add = paths.get()
        for j in ["L", "R", "D", "U"]:
            put =  add + j
            if valid(maze, put, pacman_matrix_position):
                if len(put) < 3:
                    paths.put(put)
                else:
                    if((put[-1] == "L" and put[-2] != "R") or (put[-1] == "R" and put[-2] != "L") or 
                       (put[-1] == "U" and put[-2] != "D") or (put[-1] == "D" and put[-2] != "U")):
                        paths.put(put)
    
        if(len(put) == 2):
            return put
