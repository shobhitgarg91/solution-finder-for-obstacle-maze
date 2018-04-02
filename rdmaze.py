import copy
import sys
import math
import queue
from Node_maze import Node_maze

#Global variables used in program
goal = None
start = None
flag1 = None
orig_maze = None
fringe_count = 0
visit_count = 0


def dice_moves(dice, next_dice, direction):
    '''
    dice_moves() is used to roll the dice over in one of the directions. It takes as input the current dice object,
    the dice object of neighbor, and assigns the neighbor's dice with an updated value depending on neighbor's position.
    A dice can be rolled in only one of the four directions. This function covers the cases for all those moves.
    Args:
        dice (Dice): current orientation of dice
        next_dice(Dice): new orientation of dice
        direction(String): direction of dice movement
    '''
    if direction == "right":
        next_dice.t, next_dice.d, next_dice.l, next_dice.r, next_dice.f, next_dice.b = dice.l, dice.r, dice.d, dice.t, dice.f, dice.b
    elif direction == "left":
        next_dice.t, next_dice.d, next_dice.l, next_dice.r, next_dice.f, next_dice.b = dice.r, dice.l, dice.t, dice.d, dice.f, dice.b
    elif direction == "back":
        next_dice.t, next_dice.d, next_dice.l, next_dice.r, next_dice.f, next_dice.b = dice.f, dice.b, dice.l, dice.r, dice.d, dice.t
    elif direction == "front":
        next_dice.t, next_dice.d, next_dice.l, next_dice.r, next_dice.f, next_dice.b = dice.b, dice.f, dice.l, dice.r, dice.t, dice.d


class ReadMaze:
    '''
    Class ReadMaze is used to Read the maze present in the file, that is provided as a command line argument.
    It reads the maze into a 2 D Node array and also assigns the global start and goal variables with the start
    and goal locations in the maze. It also contains the required functions to print the maze.
    Slots:
    mazeBoard: 2 D array of Nodes representing the maze
    filename: file name from which the maze is being read
    row_count: used to find out the number of rows in maze
    col_count: used to find out the number of columns in maze
    '''
    __slots__ = 'mazeBoard', 'filename', 'row_count', 'col_count'

    def __init__(self, filename):
        self.filename = filename
        self.mazeBoard = None
        self.row_count = None
        self.col_count = None
        self.read()

    def read(self):
        '''
        Used to read the file and create a maze.
        :return: None
        '''
        global start, goal, orig_maze
        print("Loading graph: " + self.filename)
        num_row = 1
        num_col = 0
        # open file to get number of rows and col in the maze
        inFile = open(self.filename)
        line = inFile.readline()

        for x in range(len(line)):
            if line[x] != " " and line[x] != "\n":
                num_col += 1  # number of columns in maze
        for _ in inFile:
            num_row += 1  # number of rows in maze
        if num_col == 0:
            print("invalid input")
            sys.exit()
        # create maze  array
        self.mazeBoard = [[Node_maze(j, i) for i in range(num_col)] for j in range(num_row)]
        self.row_count = num_row
        self.col_count = num_col
        # read file to read contents of maze
        inFile = open(self.filename)
        row = -1
        for line in inFile:
            row += 1
            col = 0
            for i in range(len(line)):
                if line[i] != " " and line[i] != "\n":
                    current_token = line[i]

                    # check if this is start location
                    if current_token == 'S':
                        start = self.mazeBoard[row][col]
                        start.parent = None

                    # check if this is goal location
                    if current_token == 'G':
                        goal = self.mazeBoard[row][col]


                    self.mazeBoard[row][col].val = line[i]
                    col += 1
        if start == None or goal == None:
            print("Error!!! Start/ Goal not found. ")
            sys.exit()
        orig_maze = copy.deepcopy(self.mazeBoard)


    def print_maze(self):
        '''
        function used to print the original maze
        :return: None
        '''
        x, y = len(self.mazeBoard), len(self.mazeBoard[0])
        for r in range(x):
            for c in range(y):
                print(self.mazeBoard[r][c].val, end=" ")
            print()

    def print_maze_soln(self, r_move, c_move):
        '''
        function used to print each move in the solution path
        :param r_move: row position of the move
        :param c_move: column position of the move
        :return: None
        '''
        x, y = len(self.mazeBoard), len(self.mazeBoard[0])
        for r in range(x):
            for c in range(y):
                if r == r_move and c == c_move:
                    print("X", end=" ")
                else:
                    print(self.mazeBoard[r][c].val, end=" ")
            print()

    def dims(self):
        '''
        function used to find the row and column size of the maze
        :return: row and column size of maze
        '''
        return self.row_count, self.col_count


def heuristic(next, dist_type, old_g_n):
    '''
    function used to calculate the Evaluation function f(n). It takes as parameter the name of the heuristic function
    that should be used to calculate the heuristic cost. It returns the total cost, i.e. f(n), where f(n) = g(n) + h(n).
    g(n) = cost to reach node n from start node
    h(n) = cost to reach goal node G from node n
    :param next: node from where the distance to goal is to be calculated.
    :param dist_type: type of heuristic to be used
    :return: total cost f(n)
    '''
    global goal, start
    g_n = old_g_n + 1
    next.g_n_cost = g_n
    h_n = heuristic_calculator(next, goal, dist_type)
    f_n = g_n + h_n
    return f_n


def heuristic_calculator(current, next, dist_type):
    '''
    used to calculate the goal between two nodes based on the given heuristic type
    :param current: first node
    :param next:    other node
    :param dist_type: type of heuristic to be used
    :return: heuristic cost
    '''

    if current.val == "G":
        return 0.0
    elif current.col == next.col:
        dist = abs(next.row - current.row)
    elif current.row == next.row:
        dist = abs(next.col - current.col)
    else:
        if dist_type == 'manhattan':
            dist = float(abs(next.row - current.row) + abs(next.col - current.col))
        # Euclidean
        elif dist_type == 'euclidean':
            val1 = next.row - current.row
            val2 = next.col - current.col
            dist = float(math.sqrt(math.pow(val1, 2) + math.pow(val2, 2)))
        # l3norm
        elif dist_type == 'l3norm':
            val1 = abs(next.row - current.row)
            val2 = abs(next.col - current.col)
            dist = float((math.pow(val1, 3) + math.pow(val2, 3))**(1/3))

    return dist


def A_star(maze , dist_type):
    '''
    function used to compute the solution path using A star algorithm.
    :param maze: maze object
    :param dist_type: type of heuristic to be used
    :return: None
    '''
    print("Heuristic Function: ", dist_type)
    global start, goal, fringe_count, visit_count, orig_maze
    maze.mazeBoard = copy.deepcopy(orig_maze)
    start = maze.mazeBoard[start.row][start.col]
    goal = maze.mazeBoard[goal.row][goal.col]
    visited = []
    fringe_list = []
    fringe = queue.PriorityQueue()
    fringe.put(start)
    fringe_list.append(start)
    fringe_count += 1
    gameWon = False

    while not fringe.empty():
        current = fringe.get()
        #managining dice_encountered
        fringe_list.remove(current)
        current.dice_enc.append([current.dice.t, current.dice.f])

        if current.dice.t != 6:
            if current.val == goal.val and current.dice.t == 1:
                print("Solution Found\n")
                goal = current
                gameWon = True
                break
            else:
                visited.append(current)
                visit_count += 1
                nbr_list = find_nbr(current, maze , dist_type, fringe_list)
                for i in range(len(nbr_list)):
                    present = -1
                    for j in range(len(visited)):
                        if (nbr_list[i].row == visited[j].row and nbr_list[i].col == visited[j].col):
                            present = j
                            break
                    if present == -1:
                        nbr_list[i].parent = current
                        fringe.put(nbr_list[i])
                        fringe_list.append(nbr_list[i])
                        fringe_count += 1
                    else:
                        if not visited[j].dice_enc.__contains__([nbr_list[i].dice.t, nbr_list[i].dice.f]):
                            nbr_list[i].parent = current
                            fringe.put(nbr_list[i])
                            fringe_list.append(nbr_list[i])
                            fringe_count += 1

    soln = []
    goal1 = goal
    #handling the solution path
    if gameWon:
        print("The path followed is: ")
        while goal1:
            soln.append(goal1)
            goal1 = goal1.parent
        soln_len = len(soln)

        #printing the solution path
        while len(soln)>0:
            node1 = soln.pop()
            maze.print_maze_soln(node1.row, node1.col)
            print(node1.dice)
            print()
        print("Total number of moves in Solution: ", soln_len)
    else:
        # if game not won
        print("No Solution Found")
    print("Total number of nodes put on the frontier queue: ", fringe_count)
    print("Total number of nodes visited: ", visit_count)
    print()

def Chk_Nbr(current,maze,next_nbr,dist_type,direction,fringe_list,nbr):
    '''
    Used to find the possible neighbors and their costs.
    :param current: current node position
    :param maze: maze object
    :param next_nbr: the neighbor to be determined
    :param dist_type: type of heuristic to be used
    :param direction: direction of movement to reach the neighbor
    :param fringe_list: list containing fringe elements
    :param nbr: list containing the possible neighbors
    :return: None
    '''
    nbr_copy = copy.deepcopy(next_nbr)
    nbr_copy.dice_enc = next_nbr.dice_enc
    cost = heuristic(nbr_copy, dist_type, current.g_n_cost)
    nbr_copy.cost = cost
    dice_moves(current.dice, nbr_copy.dice, direction)

    if nbr_copy.dice.t != 6:
        if nbr_copy not in fringe_list:
            if direction == 'left':
                maze.mazeBoard[current.row][current.col - 1] = nbr_copy
                nbr.append(nbr_copy)
            elif direction == 'right':
                maze.mazeBoard[current.row][current.col + 1] = nbr_copy
                nbr.append(nbr_copy)
            elif direction == 'front':
                maze.mazeBoard[current.row + 1][current.col] = nbr_copy
                nbr.append(nbr_copy)
            elif direction == 'back':
                maze.mazeBoard[current.row - 1][current.col] = nbr_copy
                nbr.append(nbr_copy)
        else:
            index = fringe_list.index(nbr_copy)
            if fringe_list[index].dice != nbr_copy.dice:
                nbr.append(nbr_copy)



def find_nbr(current, maze, dist_type, fringe_list):
    '''
    used to determine the valid neighbors of a node
    :param current: the current node
    :param maze: maze object
    :param dist_type: type of heuristic to be used
    :param fringe_list: list containing fringe elements
    :return: list containing the possible neighbors
    '''
    nbr = []
    r, c = maze.dims()
    # front move
    if current.row + 1 < r and maze.mazeBoard[current.row + 1][current.col].val != '*':
        next_nbr = maze.mazeBoard[current.row + 1][current.col]
        Chk_Nbr(current,maze,next_nbr,dist_type,'front',fringe_list,nbr)
    # back move
    if current.row - 1 >= 0 and maze.mazeBoard[current.row - 1][current.col].val != '*':
        next_nbr = maze.mazeBoard[current.row - 1][current.col]
        Chk_Nbr(current,maze,next_nbr,dist_type,'back',fringe_list,nbr)
    # right move
    if current.col + 1 < c and maze.mazeBoard[current.row][current.col + 1].val != '*':
        next_nbr = maze.mazeBoard[current.row][current.col + 1]
        Chk_Nbr(current,maze,next_nbr,dist_type,'right',fringe_list,nbr)
    # left move
    if current.col - 1 >= 0 and maze.mazeBoard[current.row][current.col - 1].val != '*':
        next_nbr = maze.mazeBoard[current.row][current.col - 1]
        Chk_Nbr(current,maze,next_nbr,dist_type,'left',fringe_list,nbr)
    return nbr


def main():
    '''
    used to run the program
    :return: None
    '''
    if len(sys.argv) != 2:
        print('Usage: python rdmaze.py File_name')
        return
    else:
        maze = ReadMaze(sys.argv[1])
        maze.print_maze()
        A_star(maze, "manhattan")
        A_star(maze, "euclidean")
        A_star(maze, "l3norm")
main()