
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
import time

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10624937, 'Adrian', 'Ash'), (10454012, 'Chiran', 'Walisundara'), (10496262, 'Don', 'Kaluarachchi') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# class tabooNode(search.Problem):
#     return 1


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
    frontier.append(Node(problem.initial[0]))
    explored = set() # initial empty set of explored states
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        # Python note: next line uses of a generator
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored
                        and child not in frontier)
    return explored


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

    print(warehouse.__str__())
    #"The warehouse object as a string is\n",
    #print("The object ware house is \n",warehouse)
    #print("The type of the object ware house is \n",type(warehouse))
    warehouseString = warehouse.__str__()
    columnsWarehouse = warehouse.ncols
    rowWarehouse = warehouse.nrows
    print("The rows of the warehouse is \n",rowWarehouse)
    print("The columns of the warehouse is \n",columnsWarehouse)
    
    twoDWarehouse = warehouseString.split("\n")
    print("The two dimensional warehouse is \n",twoDWarehouse)

    playerLocation = warehouse.worker
    wallLocations = warehouse.walls
    goalLocations = warehouse.targets
    
    goalLocations = [x[::-1] for x in goalLocations]
    playerLocation = playerLocation[::-1]
    wallLocations = [x[::-1] for x in wallLocations]



    for x in range(rowWarehouse):                
        twoDWarehouse[x] = twoDWarehouse[x].replace('$',' ')
        twoDWarehouse[x] = twoDWarehouse[x].replace('@',' ')  
        
        twoDWarehouse[x] = twoDWarehouse[x].replace('!',' ')
        twoDWarehouse[x] = twoDWarehouse[x].replace('*',' ')
        twoDWarehouse[x] = twoDWarehouse[x].replace('.',' ')                       
            
    print("The 2D warehouse is \n",twoDWarehouse)
    print("The player location is \n",playerLocation)
    returnString = "\n".join(twoDWarehouse)
    # for x in twoDWarehouse:
    #     twoDWarehouse.append
    print(returnString)
    #"The final warehouse when joined is\n"
    wh = SokobanPuzzle(warehouse=warehouse)
    
    #NOTE: TESTING
    # wh.actions(state=playerLocation)
    # #print(wh.initial)
    # print("Here")
    # #wh.result(state=playerLocation, action='U')
    # print(wh.result(state=playerLocation, action='U'))
    # print(wh.result(state=playerLocation, action='R'))
    
    explored = taboo_graph_search(problem = wh, frontier = FIFOQueue())

    tabooCells = []
    for openCell in explored:
        x = openCell[0]
        y = openCell[1]
        if (x,y) not in goalLocations:
            if (x+1, y) in wallLocations or (x-1, y) in wallLocations:
                if (x, y+1) in wallLocations or (x, y-1) in wallLocations:
                    tabooCells.append(openCell)
    
    print("This is explored cells", explored)
    print("This is taboo cells", tabooCells)

    combinationOfCorners = itertools.combinations(tabooCells, 2)
    sameLineCorners = []
    # get a list of all the corner combinations that are on the same column or row
    for x in combinationOfCorners:
        left = x[0]
        right = x[1]
        if left[0] == right[0]:
            #ensure the lowest number is positioned on the left for next section
            if left[1] < right[1]:
                sameLineCorners.append(x)
            else:
                sameLineCorners.append((right, left))
        if left[1] == right[1]:
            if left[0] < right[0]:
                sameLineCorners.append(x)
            else:
                sameLineCorners.append((right, left))

    inbetweenTabooCorners = []
    # get a list of all the corner combinations that have taboo cells between them
    for x in sameLineCorners:
        left = x[0]
        right = x[1]
        # on same row
        if left[0] == right[0]:
            boolean = 0
            row = left[0]
            #check all inbetween if they are a goal state or have atleast one wall adjacent 
            for col in range(left[1], right[1]):
                if (row,col) in goalLocations:
                    boolean = 1
                    break
                if (row+1, col) not in wallLocations and (row-1, col) not in wallLocations and (row, col+1) not in wallLocations and (row, col-1) not in wallLocations:
                    boolean = 1
                    break
            if boolean == 0:
                inbetweenTabooCorners.append(x)
        # on same column
        if left[1] == right[1]:
            boolean = 0
            col = left[1]
            for row in range(left[0], right[0]):
                if (row,col) in goalLocations:
                    boolean = 1
                    break
                if (row+1, col) not in wallLocations and (row-1, col) not in wallLocations and (row, col+1) not in wallLocations and (row, col-1) not in wallLocations:
                    boolean = 1
                    break
            if boolean == 0:
                inbetweenTabooCorners.append(x)

    for x in inbetweenTabooCorners:
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

    print("This is all taboo cells", tabooCells)
    for x in range(len(twoDWarehouse)):
        for y in range(len(twoDWarehouse[x])):
            if (x,y) in tabooCells:
                twoDWarehouse[x] = twoDWarehouse[x][:y] + "X" + twoDWarehouse[x][y+1:]
    
    # if [4,4] in goalLocations:
    #     print("WE ARE IN THE GOAL")
    # else:
    #     print("FAIL")

    returnString = "\n".join(twoDWarehouse)
    print(returnString)
    return returnString
    
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    """
    Need explaination

    h = (worker to box) + (box to goal) (how to do this is the most important question)

    @param warehouse: 
        with these

    @return
       and these
    """
    def __init__(self, warehouse):
        #used for taboo cells
        playerLocation = warehouse.worker
        boxLocations = warehouse.boxes
        wallLocations = warehouse.walls
        goalLocations = warehouse.targets
        t = playerLocation[::-1]
        a =  tuple([x[::-1] for x in boxLocations])

        self.weights = warehouse.weights
        self.initial = (t,)+a
        self.goalLocations = [x[::-1] for x in goalLocations]
        self.wallLocations = [x[::-1] for x in wallLocations]
        self.warehouse = warehouse

    def tabooCellFinder(self):
        warehouseString = taboo_cells(self.warehouse)
        twoDWarehouse = warehouseString.split("\n")
        tabooCellsWarehouse = []
        for x in twoDWarehouse:
            for y in twoDWarehouse[x]:
                if twoDWarehouse[x][y] == "X":
                    tabooCellsWarehouse.append((x,y))
        self.tabooCells = tabooCellsWarehouse
        self.tabooCells = tuple(self.tabooCell)

    def actions(self, state, taboo=1):
        # player position = intial state [~][~]
        # self ('##### ', '#.  ##', '#    #', '##   #', ' ##  #', '  ##.#', '   ###')
        if type(state[0]) == tuple:
            position_x = state[0][0]
            position_y = state[0][1]
        else:
            position_x = state[0]
            position_y = state[1]
        L = []  # list of legal actions
        

        # Up: If blank not on bottom row, swap it with tile below it
        if (position_x-1, position_y) not in self.wallLocations:
            if(position_x-1, position_y) in state[1:]:
                if(position_x-2, position_y) not in self.wallLocations and (position_x-2, position_y) not in state[1:]:
                    if taboo == 1:
                        if(position_x-2, position_y) not in self.tabooCells:
                            L.append("Up")
                    else:
                        L.append("Up")
            else:
                L.append("Up")
            

        # Down: if blank not on top row, swap it with tile above it
        if (position_x+1, position_y) not in self.wallLocations:
            if(position_x+1, position_y) in state[1:]:
                if(position_x+2, position_y) not in self.wallLocations and (position_x+2, position_y) not in state[1:]:
                    if taboo == 1:
                        if(position_x+2, position_y) not in self.tabooCells:
                            L.append("Down")
                    else:
                        L.append("Down")
            else:
                L.append("Down")

        # Left: If blank not on right column, swap it with tile to the right
        if (position_x, position_y-1) not in self.wallLocations:
            if(position_x, position_y-1) in state[1:]:
                if(position_x, position_y-2) not in self.wallLocations and (position_x, position_y-2) not in state[1:]:
                    if taboo == 1:
                        if(position_x, position_y-2) not in self.tabooCells:
                            L.append("Left")
                    else:
                        L.append("Left")
            else:
                L.append("Left")
            
        # Right: If blank not in left column, swap it with tile to the left
        if (position_x, position_y+1) not in self.wallLocations:
            if(position_x, position_y+1) in state[1:]:
                if(position_x, position_y+2) not in self.wallLocations and (position_x, position_y+2) not in state[1:]:
                    if taboo == 1:
                        if(position_x, position_y+2) not in self.tabooCells:
                            L.append("Right")
                    else:
                        L.append("Right")
            else:
                L.append("Right")

        #NOTE: TESTING
        # if(len(L) <= 0):
        #     print("fail")
        # print(L)
        return L

    def result(self, state, action):
        # index of the blank
        next_state = list(state)  # Note that  next_state = state   would simply create an alias
        if type(state[0]) == tuple:
            position_x = state[0][0]
            position_y = state[0][1]
        else:
            position_x = state[0]
            position_y = state[1]

        assert action in self.actions(state)  # defensive programming!
        
        # UP: if blank not on top row, swap it with tile above it
        if action == 'Up':
            if(position_x-1, position_y) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x-1, position_y):
                        next_state[x+1] = (position_x-2, position_y)
            
            player_location = (position_x-1, position_y)
            next_state[0] = player_location
        
        # DOWN: If blank not on bottom row, swap it with tile below it
        if action == 'Down':  
            if(position_x+1, position_y) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x+1, position_y):
                        next_state[x+1] = (position_x+2, position_y)

            player_location = (position_x+1, position_y)
            next_state[0] = player_location

        # LEFT: If blank not in left column, swap it with tile to the left
        if action == 'Left':
            if(position_x, position_y-1) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x, position_y-1):
                        next_state[x+1] = (position_x, position_y-2)

            player_location = (position_x, position_y-1)
            next_state[0] = player_location
        
        # RIGHT: If blank not on right column, swap it with tile to the right
        if action == 'Right':
            if(position_x, position_y+1) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x, position_y+1):
                        next_state[x+1] = (position_x, position_y+2)

            player_location = (position_x, position_y+1)
            next_state[0] = player_location

        return tuple(next_state)  # use tuple to make the state hashable

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        #set of target is equal to the set of
        currentBoxLocation = state[1:]
        return set(currentBoxLocation) == set(self.goalLocations)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def h(self):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        h = 1
        return h
    

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
    wh = SokobanPuzzle(warehouse=warehouse)


    state = wh.initial

    for x in action_seq:
        L = wh.actions(state=state, taboo = 0)
        if x in L:
            state = wh.result(state=state, action=x)
        else:
            return "Impossible"

    worker = state[0]
    worker = worker[::-1]
    boxes =  tuple([x[::-1] for x in state[1:]])
    warehouseFinish = warehouse.copy(worker=worker, boxes=boxes, weights = wh.weights)
    return warehouseFinish.__str__()


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

    wh = SokobanPuzzle(warehouse=warehouse)
    wh.actions(state=wh.initial)
    wh.tabooCellFinder()
    print(wh.tabooCells)
    #state = ((1,3),(4,4),(4,2))
    # result = search.astar_graph_search(problem = wh)
    # if result == None:
    #     return "Impossible", None
    
    # answer, cost = result.answer, result.cost

    #return answer, cost
    return 1, 1


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -