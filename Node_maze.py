from Dice import Dice
import math
# dice_enc = dice encountered
class Node_maze:
    '''
    Class node represents a single location on the maze.
    '''
    __slots__ = 'val', 'row', 'col', 'dice', 'cost', 'parent', 'dice_enc', 'g_n_cost'

    def __init__(self, row, col):
        '''
        init function is used to assign the row and column values to the node. It also assigns default values to
        other variables.
        :param row: row number representing the node in maze
        :param col: column number representing the node in maze
        '''
        self.row = row
        self.col = col
        self.val = None
        self.cost = math.inf
        self.dice = Dice()
        self.parent = None
        self.dice_enc = []
        self.g_n_cost = 0

    def __eq__(self, other):
        if other == None:
            return 0
        return self.cost == other.cost and (self.row == other.row and self.col == other.col)

    def __le__(self, other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

    def __lt__(self, other):
        return self.cost < other.cost


