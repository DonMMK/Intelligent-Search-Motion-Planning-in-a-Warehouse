
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
from search import Problem, Node, FIFOQueue
import itertools

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10624937, 'Adrian', 'Ash'), (10454012, 'Chiran', 'Walisundara'), (10496262, 'Don', 'Kaluarachchi') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def taboo_graph_search(problem, frontier):
    """
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    If two paths reach a state, only use the first one. [Fig. 3.7]
    Return
        the node of the first goal state found
        or None is no goal state is found
    """
    assert isinstance(problem, Problem)
    frontier.append(Node(problem.initial))
    explored = set() # initial empty set of explored states
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        # Python note: next line uses of a generator
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored
                        and child not in frontier)
    return explored

class WarehouseTaboo(search.Problem):

    def __init__(self, warehouseString, initial):
        self.warehouseString = warehouseString
        self.initial = initial
        self.warehouseString = tuple(self.warehouseString)
        self.initial = tuple(self.initial)

    def actions(self, state):
        # player position = intial state [~][~]
        # self ('##### ', '#.  ##', '#    #', '##   #', ' ##  #', '  ##.#', '   ###')
        position_x = state[0]
        position_y = state[1]
        L = []  # list of legal actions
        # UP: if blank not on top row, swap it with tile above it
        if self.warehouseString[position_x+1][ position_y] != '#':
            L.append("D")

        # DOWN: If blank not on bottom row, swap it with tile below it
        if self.warehouseString[position_x-1][position_y] != '#':
            L.append("U")

        # LEFT: If blank not in left column, swap it with tile to the left
        if self.warehouseString[position_x][position_y-1] != '#':
            L.append("L")

        # RIGHT: If blank not on right column, swap it with tile to the right
        if self.warehouseString[position_x][position_y+1] != '#':
            L.append("R")

        #NOTE: TESTING
        # if(len(L) <= 0):
        #     print("fail")
        # print(L)

        return L

    def result(self, state, action):
        # index of the blank
        next_state = list(state)  # Note that  next_state = state   would simply create an alias
        position_x = state[0]
        position_y = state[1]
        #print(action)
        #print(self.actions(state))
        assert action in self.actions(state)  # defensive programming!
        # UP: if blank not on top row, swap it with tile above it
        
        if action == 'U':
            x_new = position_x-1
            next_state[0] = x_new
        # DOWN: If blank not on bottom row, swap it with tile below it
        if action == 'D':
            x_new = position_x+1
            next_state[0] = x_new
        # LEFT: If blank not in left column, swap it with tile to the left
        if action == 'L':
            y_new = position_y-1
            next_state[1] = y_new
        # RIGHT: If blank not on right column, swap it with tile to the right
        if action == 'R':
            y_new = position_y+1
            next_state[1] = y_new
        return tuple(next_state)  # use tuple to make the state hashable




def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"   
    print(warehouse.__str__())
    #"The warehouse object as a string is\n",
    #print("The object ware house is \n",warehouse)
    #print("The type of the object ware house is \n",type(warehouse))
    
    #raise NotImplementedError()
    WarehouseString = warehouse.__str__()
    ColumnsWarehouse = warehouse.ncols
    RowWarehouse = warehouse.nrows
    print("The rows of the warehouse is \n",RowWarehouse)
    print("The columns of the warehouse is \n",ColumnsWarehouse)
    
    TwoDWarehouse = WarehouseString.split("\n")
    print("The two dimensional warehouse is \n",TwoDWarehouse)

    for x in range(RowWarehouse):
        for y in range(ColumnsWarehouse):
            if TwoDWarehouse[x][y] == '@' or TwoDWarehouse[x][y] == '!':
                PlayerLocation = [x,y]
                
        TwoDWarehouse[x] = TwoDWarehouse[x].replace('$',' ')
        TwoDWarehouse[x] = TwoDWarehouse[x].replace('@',' ')  
        
        TwoDWarehouse[x] = TwoDWarehouse[x].replace('!','.')
        TwoDWarehouse[x] = TwoDWarehouse[x].replace('*','.')                  
            
    print("The 2D warehouse is \n",TwoDWarehouse)
    print("The player location is \n",PlayerLocation)
    finalString = "\n".join(TwoDWarehouse)
    # for x in TwoDWarehouse:
    #     TwoDWarehouse.append
    print(finalString)
    #"The final warehouse when joined is\n"
    wh = WarehouseTaboo(warehouseString=TwoDWarehouse, initial=PlayerLocation)
    
    #NOTE: TESTING
    # wh.actions(state=PlayerLocation)
    # #print(wh.initial)
    # print("Here")
    # #wh.result(state=PlayerLocation, action='U')
    # print(wh.result(state=PlayerLocation, action='U'))
    # print(wh.result(state=PlayerLocation, action='R'))
    explored = taboo_graph_search(problem = wh, frontier = FIFOQueue())
    tabooCells = []
    for openCell in explored:
        x = openCell[0]
        y = openCell[1]
        if TwoDWarehouse[x][y] != '.':
            if TwoDWarehouse[x+1][y] == '#' or TwoDWarehouse[x-1][y] == '#':
                if TwoDWarehouse[x][y+1] == '#' or TwoDWarehouse[x][y-1] == '#':
                    tabooCells.append(openCell)
    
    print("This is explored cells",explored)
    print("This is taboo cells",tabooCells)

    combinationTaboo = itertools.combinations(tabooCells, 2)
    checkInbetween = []
    for x in combinationTaboo:
        left = x[0]
        right = x[1]

        if left[0] == right[0]:
            if left[1] < right[1]:
                checkInbetween.append(x)
            else:
                checkInbetween.append((right, left))
        if left[1] == right[1]:
            if left[0] < right[0]:
                checkInbetween.append(x)
            else:
                checkInbetween.append((right, left))

    #print("This is the focus", checkInbetween)
    choosenCheckInbetween = []
    for x in checkInbetween:
        left = x[0]
        right = x[1]
        if left[0] == right[0]:
            boolean = 0
            row = left[0]
            for col in range(left[1], right[1]):
                #check if this is goal state
                #check if this has one wall
                if TwoDWarehouse[row][col] == '.':
                    boolean = 1
                    break
                if TwoDWarehouse[row+1][col] != "#" or TwoDWarehouse[row-1][col] != "#" or TwoDWarehouse[row][col+1] != "#" or TwoDWarehouse[row][col-1] != "#":
                    boolean = 1
                    break
            if boolean == 0:
                choosenCheckInbetween.append(x)

        if left[1] == right[1]:
            boolean = 0
            col = left[1]
            for row in range(left[1], right[1]):
                #check if this is goal state
                #check if this has one wall
                if TwoDWarehouse[row][col] == '.':
                    boolean = 1
                    break
                if TwoDWarehouse[row+1][col] != "#" or TwoDWarehouse[row-1][col] != "#" or TwoDWarehouse[row][col+1] != "#" or TwoDWarehouse[row][col-1] != "#":
                    boolean = 1
                    break
            if boolean == 0:
                choosenCheckInbetween.append(x)

    for x in choosenCheckInbetween:
        left = x[0]
        right = x[1]
        if left[0] == right[0]:
            row = left[0]
            for col in range(left[1]+1, right[1]):
                tabooCells.append((row,col))
        if left[1] == right[1]:
            col = left[1]
            for row in range(left[0]+1, right[0]):
                tabooCells.append((row,col))

    print("This is THE FOCUS", tabooCells)
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -