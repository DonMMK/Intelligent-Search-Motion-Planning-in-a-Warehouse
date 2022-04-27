
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
    wh = SokobanPuzzle(warehouse=warehouse, emptyWarehouseFlag=1)
    #NOTE: TESTING
    # wh.actions(state=playerLocation)
    # #print(wh.initial)
    # print("Here")
    # #wh.result(state=playerLocation, action='U')
    # print(wh.result(state=playerLocation, action='U'))
    # print(wh.result(state=playerLocation, action='R'))
    
    explored = taboo_graph_search(problem = wh, frontier = FIFOQueue())

    tabooCells = []
    print(explored)
    for openCell in explored:
        x = openCell[0][0]
        y = openCell[0][1]
        if (x,y) not in goalLocations:
            if (x+1, y) in wallLocations or (x-1, y) in wallLocations:
                if (x, y+1) in wallLocations or (x, y-1) in wallLocations:
                    tabooCells.append(openCell[0])
    
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
                if (row,col) in goalLocations or (row, col) in wallLocations:
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
                if (row,col) in goalLocations or (row, col) in wallLocations:
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
    def __init__(self, warehouse, emptyWarehouseFlag = 0, tabooFlag = 0):
        #used for taboo cells
        playerLocation = warehouse.worker
        boxLocations = warehouse.boxes
        wallLocations = warehouse.walls
        goalLocations = warehouse.targets
        
        t = playerLocation[::-1]
        if emptyWarehouseFlag == 0:
            a =  tuple([x[::-1] for x in boxLocations])
            self.initial = (t,)+a
        else:
            self.initial = (t,)

        self.weights = warehouse.weights
        self.goalLocations = [x[::-1] for x in goalLocations]
        self.wallLocations = [x[::-1] for x in wallLocations]
        self.warehouse = warehouse
        self.tabooFlag = tabooFlag

    def tabooCellFinder(self):
        warehouseString = taboo_cells(self.warehouse)
        twoDWarehouse = warehouseString.split("\n")
        tabooCellsWarehouse = []
        for x in range(len(twoDWarehouse)):
            for y in range(len(twoDWarehouse[x])):
                if twoDWarehouse[x][y] == "X":
                    tabooCellsWarehouse.append((x,y))
        self.tabooCells = tabooCellsWarehouse
        self.tabooCells = tuple(self.tabooCells)

    def actions(self, state):
        # player position = intial state [~][~]
        # self ('##### ', '#.  ##', '#    #', '##   #', ' ##  #', '  ##.#', '   ###')
        position_x = state[0][0]
        position_y = state[0][1]
        L = []  # list of legal actions
        

        # Up: Write something
        if (position_x-1, position_y) not in self.wallLocations:
            if(position_x-1, position_y) in state[1:]:
                if(position_x-2, position_y) not in self.wallLocations and (position_x-2, position_y) not in state[1:]:
                    if self.tabooFlag != 1:
                        if(position_x-2, position_y) not in self.tabooCells:
                            L.append("Up")
                    else:
                        L.append("Up")
            else:
                L.append("Up")
            

        # Down: Write something
        if (position_x+1, position_y) not in self.wallLocations:
            if(position_x+1, position_y) in state[1:]:
                if(position_x+2, position_y) not in self.wallLocations and (position_x+2, position_y) not in state[1:]:
                    if self.tabooFlag != 1:
                        if(position_x+2, position_y) not in self.tabooCells:
                            L.append("Down")
                    else:
                        L.append("Down")
            else:
                L.append("Down")

        # Left: Write something
        if (position_x, position_y-1) not in self.wallLocations:
            if(position_x, position_y-1) in state[1:]:
                if(position_x, position_y-2) not in self.wallLocations and (position_x, position_y-2) not in state[1:]:
                    if self.tabooFlag != 1:
                        if(position_x, position_y-2) not in self.tabooCells:
                            L.append("Left")
                    else:
                        L.append("Left")
            else:
                L.append("Left")
            
        # Right: Write something
        if (position_x, position_y+1) not in self.wallLocations:
            if(position_x, position_y+1) in state[1:]:
                if(position_x, position_y+2) not in self.wallLocations and (position_x, position_y+2) not in state[1:]:
                    if self.tabooFlag != 1:
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
        position_x = state[0][0]
        position_y = state[0][1]
        assert action in self.actions(state)  # defensive programming!
        
        # UP: Write something
        if action == 'Up':
            if(position_x-1, position_y) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x-1, position_y):
                        next_state[x+1] = (position_x-2, position_y)
            
            player_location = (position_x-1, position_y)
            next_state[0] = player_location
        
        # DOWN: Write something
        if action == 'Down':  
            if(position_x+1, position_y) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x+1, position_y):
                        next_state[x+1] = (position_x+2, position_y)

            player_location = (position_x+1, position_y)
            next_state[0] = player_location

        # LEFT: Write something
        if action == 'Left':
            if(position_x, position_y-1) in state[1:]:
                for x in range(len(state[1:])):
                    if next_state[x+1] == (position_x, position_y-1):
                        next_state[x+1] = (position_x, position_y-2)

            player_location = (position_x, position_y-1)
            next_state[0] = player_location
        
        # RIGHT: Write something
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
        cost = 0
        for x in range(len(state1[1:])):
            if state1[x+1] != state2[x+1]:
                cost = self.weights[x]
        return c + 1 + cost

    def h(self, n):
        '''
        Heuristic for goal state of the form range(k,-1,1) where k is a positive integer. 
        h(n) = 1 + the index of the largest pancake that is still out of place
        '''
        #NOTE: TEST AND FIX UP - most certainly wrong at the moment

        playerLocation = n.state[0]
        boxLocation = n.state[1:]
        goalLocation = self.goalLocations
        minWorkerToBox = 999999
        minBoxToGoal = 999999
        for x in boxLocation:
            workerDistance = abs(playerLocation[0] - x[0]) + abs(playerLocation[1] - x[1])
            minWorkerToBox = min(workerDistance, minWorkerToBox)
            for y in range(len(goalLocation)):
                boxDistance = abs(x[0] - goalLocation[y][0]) + abs(x[1] - goalLocation[y][1])
                boxDistance = boxDistance * self.weights[y]
                minBoxToGoal = min(boxDistance, minBoxToGoal)

        return minWorkerToBox + minBoxToGoal
    

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
    wh = SokobanPuzzle(warehouse=warehouse, tabooFlag=1)
    state = wh.initial

    for x in action_seq:
        L = wh.actions(state=state)
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
    wh.tabooCellFinder()
    #print(wh.tabooCells)
    
    #NOTE: Works - Test Action is Correct
    #wh.actions(state=wh.initial)
    #print(wh.actions(state=wh.initial))
    
    #NOTE: Works - Check all Taboo Cells were found
    #wh.tabooCellFinder()
    #print(wh.tabooCells)
    
    #NOTE: Works - Check Goal test is working
    #stateTest = ((4,1), (4, 2), (4, 4))
    #print(wh.goalLocations)
    #print(wh.initial[1:])
    #print(stateTest[1:])
    #print(wh.goal_test(stateTest))

    #NOTE: Test Action works with path cost
    
    #Right
    # state1 = wh.initial
    # actions = wh.actions(state=wh.initial)
    # print(actions)
    # print("Our weights, correlate directly with our boxes")
    # print(wh.weights)

    # print("Moving right, note the first values changes right")
    # action = "Right"
    # state2 = wh.result(state = state1, action=action)
    # print(state1)
    # print(state2)
    # cost = wh.path_cost(c=0, state1=state1, action=action, state2=state2)
    # print("Cost:")
    # print(cost)

    # print("Moving right again")
    # state1 = state2
    # action = "Right"
    # state2 = wh.result(state = state1, action=action)
    # print(state1)
    # print(state2)
    # cost = wh.path_cost(c=cost, state1=state1, action=action, state2=state2)
    # print("Cost:")
    # print(cost)

    # print("Moving down, next to the second box")
    # state1 = state2
    # action = "Down"
    # state2 = wh.result(state = state1, action=action)
    # print(state1)
    # print(state2)
    # cost = wh.path_cost(c=cost, state1=state1, action=action, state2=state2)
    # print("Cost:")
    # print(cost)

    # print("Moving left and pushing the box, the cost is 1+ weight of box (which is 6)")
    # print(wh.actions(state=state2))
    # state1 = state2
    # action = "Left"
    # state2 = wh.result(state = state1, action=action)
    # print(state1)
    # print(state2)
    # cost = wh.path_cost(c=cost, state1=state1, action=action, state2=state2)
    # print("Cost:")
    # print(cost)

    print(wh.actions(state=wh.initial))

    result = search.astar_graph_search(problem = wh)
    if result == None:
        return "Impossible", None
    
    path = result.path()
    actionsTaken = []
    for node in path[1:]:
        actionsTaken.append(node.action)
    print("This is the path: ")
    print(actionsTaken)

    print("This is state")
    print(result.state)
    print(wh.goalLocations)

    answer, cost = actionsTaken, result.path_cost
    
    return answer, cost


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -