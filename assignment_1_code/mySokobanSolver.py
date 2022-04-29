
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
from search import Problem, Node, FIFOQueue
import itertools
import sys


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    @param: 
        N/A

    @return:
       A list of the 3 members of our team:
        - Adrian Ash: n10624937
        - Chiran Walisundara: n10454012
        - Don Kaluarachchi: n10496262 

    '''
    return [ (10624937, 'Adrian', 'Ash'), (10454012, 'Chiran', 'Walisundara'), 
            (10496262, 'Don', 'Kaluarachchi') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_graph_search(problem, frontier):
    """
    A modified graph search method that search through the successors 
    of a problem adding the state (grid locations) of each node to an explored variable.

    Used by taking a SokobanPuzzle (problem subclass) object
    and an empty queue object.

    Returns all the grid locations that are within the walls of the
    SokobanPuzzles warehouse object.
    
    @params: 
        problem - a problem (or subclass) object
        frontier - a queue object (whether it be FIFOQueue or LIFOQueue)

    @return:
       explored - a set of all the visited states
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
    A method used to discover all the taboo cells located within a warehouse object.
    Will return a string representation of all the taboo locations and wall locations
    marked as "#" for walls and "X" for taboo cells.

    A "taboo cell" is by definition:
        - a cell inside a warehouse such that whenever a box get pushed on such 
        - a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo. Additionally we will ignore all the existing boxes, 
    only consider the walls and the target cells. 
    
    With the above definition we can determine the rules are define a taboo cells as:
        Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
        Rule 2: all the cells between two corners along a wall are taboo if none of 
                these cells is a target.

    @params: 
        warehouse - a Warehouse object with the worker inside the warehouse

    @return:
        returnString - A string representing the warehouse with only the wall cells marked with 
                      a '#' and all the discovered taboo cells marked with a 'X'.  
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
    An instance contains information about the walls, the targets, the box weights,
    various helper flags and the initial box locations and worker location.

    This class is a subclass of the Problem class from the search file and overwrites multiple
    functions that require unique implementations for solving the Sokoban Puzzle.

    This object is compatible with multiple search algorithms that are also present in the search file
    and which will be used to find potential solutions to a given warehouse.      
    '''
    def __init__(self, warehouse, emptyWarehouseFlag = 0, tabooFlag = 0):
        '''  
        Using the Warehouse object passed into this constructor various important information is extracted
        and set of SokobanPuzzle object variables. 
        
        Additionally two seperate flags are set that modify the behaviour of the objects, 
        with emptyWarehouseFlag used by taboo_cells() and tabooFlag used by check_elem_action_seq()

        This is also were the initial state is set. Will take the form of a tuple of tuples. The first
        tuple being the location of the worker. All following tuples will represent the locations of the boxes.
        This is our the state will be represent for the rest of the functions aswell.
            An Example: ((4,6),(2,3),(1,2))
                - Here the worker is located at row 4 column 6
                - The boxes are located at rows 2 and 1 and columns 3 and 2 respectively
                - NOTE: the rows and columns are flipped from the original warehouse object so as
                        to match our initial taboo_cells() design. No significant reason but our own
                        continuity 

        @params: 
            warehouse - a valid Warehouse object

            emptyWarehouseFlag - a flag used for setting the initial state without box locations
                                    - Used by taboo_cells() which does not make use of box locations

            tabooFlag - a flag used by actions() to define if the taboo cells should be checked
                        when searching are legal actions to take
                                    - Used by check_elem_action_seq() which does not need to check taboo cells for
                                    legal moves 
        '''
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
        '''  
        A method used by solve_weighted_sokoban() to extract the taboo cell locations from
        the warehouse and set them as SokobanPuzzle variables. 
        
        This function will make use of the taboo_cells() function to return of string of a warehouse
        with the taboo cells defined.
        
        The tabooCells that are set will take the form of a tuple of tuples depicting all the taboo cells
        grid locations.
            An Example: ((1, 3), (2, 7), (5, 9))
                - Here the taboo cells are located at rows 1, 2 and 5 and columns 3,7 and 9 respectively
        '''
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
        '''  
        Uses the state variable provided, which is a tuple of tuples in the same format as the 
        initial variable set in __init__ with the first tuple defining the worker location and the following
        tuples defining the box locations.

        Given this state variable it calculates all the possible moves that the agent can perform. The behaviour of this
        function is also modified based on if the emptyWarehouseFlag and tabooFlag were set in the constructor (__init__):
            
            emptyWarehouseFlag = 1 - means that state will only contain the worker location and will only search based on if the
                                 worker will hit a wall "#" or not
            tabooFlag = 1 - will ignore if the worker move will push a box into a taboo cell or not
        
        Without the flags the function will check:
            1) will a workers movement result in hitting the wall
            2) will a workers movement result in hitting a box
                if so
                2.a) will the box movement result in hitting the wall or another box
                2.b) will the box movement in the box entering a tabooCells or not
        
        Depending on which above conditions are met different actions are added to L which results
        in this function finally returning all possible moves the agent (worker) can make from there current location

        @param: 
            state - a tuple of tuples defining the worker and box locations 
                    defined the same as the __init__ function sets initial variable
        @return:
            L - a list of legal actions that can be taken given the current state
        '''
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
        #print(L)
        return L

    def result(self, state, action):
        '''  
        Uses the state and action variable provided this function will move the workers location and if the
        action results in the worker pushing a box then the location of said box will also be moved.

        It will define these changes as the next_state and will return a tuple of next_state

        @params: 
            state - a tuple of tuples defining the worker and box locations 
            action - an single action from the list returned from the actions() function
                        For Example: if actions() returns ['Up', 'Right']
                                     then the action passed maybe 'Up' or 'Right' 
        @return:
            tuple(next_state) - a tuple representation of the next state
                                    NOTE: the same format as all states. A tuple of tuples with the
                                    first tuple denoting the worker location and the remaining tuples
                                    denoting the boxes locations
        '''
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
        '''  
        Uses the state provided return true of all the locations of the boxes are on the goalLocations

        For Example -
                   currentBoxLocations = ((4,6), (2,3))
                   goalLocations = ((4,6), (2,3))
                   Will return true

                   Whereas

                   currentBoxLocations = ((4,5), (2,3))
                   goalLocations = ((4,6), (2,3))
                   Will return false
        
        NOTE: that since we are using set representations of both currentBoxLocations and goalLocations
              the order of the locations will not matter

              For Example -
                   currentBoxLocations = ((4,6), (2,3))
                   goalLocations = ((2,3), (4,6))
                   Will still return true
        @param: 
            state - a tuple of tuples defining the worker and box locations
        @return:
            result - a boolean value (true or false) denoting if the goal condition has been met
                     Defined by all currentBoxLocation being position on all the goalLocations
        '''
        #set of target is equal to the set of
        currentBoxLocations = state[1:]
        result = set(currentBoxLocations) == set(self.goalLocations)
        return result

    def path_cost(self, c, state1, action, state2):
        '''  
        Uses the state1 and state2 we determine if a box location, stored in all the tuples of the state but the first,
        has changed between the states and if it has then add the weight of the box to the result variable.

        The result will be a combination of the cost of the previous actions up till state2 (c) + the default cost of an
        action (1) + the cost of moving a box (if there is one)

        @params:
            c - the cost of the solution path up to state1
            state1 - a tuple of tuples defining the worker and box locations before the action
            action - the action taken from state1 to get to state2 
                        NOTE: not used for our solution
            state2 - a tuple of tuples defining the worker and box locations after the action

        @return:
            result - the cost of the solution path up to state2 coming from state1
                     given the action
        '''
        cost = 0
        for x in range(len(state1[1:])):
            if state1[x+1] != state2[x+1]:
                cost = self.weights[x]
        result = c + 1 + cost
        return result

    def h(self, n):
        '''  
        Uses the state1 and state2 we determine if a box location, stored in all the tuples of the state but the first,
        has changed between the states and if it has then add the weight of the box to the result variable.

        The result will be a combination of the cost of the previous actions up till state2 (c) + the default cost of an
        action (1) + the cost of moving a box (if there is one)

        @param:
            n - a node object (contains the current state)

        @return:
            completeToGoal - the cost of the solution path up to state2 coming from state1
                     given the action
        '''
        playerLocation = n.state[0]
        boxLocation = n.state[1:]
        goalLocation = self.goalLocations
        
        #talk about how the exponental issue with more boxes
        #NOTE: Solution 1 (main solution)
        #sys.maxsize
        minWorkerToBox = sys.maxsize
        minBoxToGoal = sys.maxsize
        completeToGoal = 0
        for x in boxLocation:
            if x not in goalLocation:
                workerDistance = abs(playerLocation[0] - x[0]) + abs(playerLocation[1] - x[1]) - 1
                minWorkerToBox = min(workerDistance, minWorkerToBox)
                for y in range(len(goalLocation)):
                    boxDistance = abs(x[0] - goalLocation[y][0]) + abs(x[1] - goalLocation[y][1])
                    #boxDistance = boxDistance * self.weights[y]
                    minBoxToGoal = min(boxDistance, minBoxToGoal)
                completeToGoal = max(completeToGoal, minBoxToGoal + minWorkerToBox)

        #NOTE: Solution 2 (need to fix)
        # minWorkerToBox = sys.maxsize
        # minBoxToGoal = sys.maxsize
        # combineMinBoxToGoal = 0
        # completeToGoal = 0
        # for x in boxLocation:
        #     if x not in goalLocation:
        #         workerDistance = abs(playerLocation[0] - x[0]) + abs(playerLocation[1] - x[1]) - 1
        #         minWorkerToBox = min(workerDistance, minWorkerToBox)
        #         for y in range(len(goalLocation)):
        #             boxDistance = abs(x[0] - goalLocation[y][0]) + abs(x[1] - goalLocation[y][1])
        #             #boxDistance = boxDistance * self.weights[y]
        #             minBoxToGoal = min(boxDistance, minBoxToGoal)
        #         combineMinBoxToGoal = combineMinBoxToGoal + minBoxToGoal
        # #print(combineMinBoxToGoal)
        # completeToGoal = combineMinBoxToGoal + minWorkerToBox

        #NOTE: Solution 3 (old solution)
        # maxWorkerToBox = 0
        # maxBoxToGoal = 0
        # completeToGoal = 0
        # for x in boxLocation:
        #     if x not in goalLocation:
        #         workerDistance = abs(playerLocation[0] - x[0]) + abs(playerLocation[1] - x[1]) - 1
        #         maxWorkerToBox = max(workerDistance, maxWorkerToBox)
        #         for y in range(len(goalLocation)):
        #             boxDistance = abs(x[0] - goalLocation[y][0]) + abs(x[1] - goalLocation[y][1])
        #             #boxDistance = boxDistance * self.weights[y]
        #             maxBoxToGoal = min(boxDistance, maxBoxToGoal)
        #             completeToGoal = max(completeToGoal, maxBoxToGoal + maxWorkerToBox)
        #print(completeToGoal)
        return completeToGoal
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    This does not nessarily mean solving the puzzle or pushing a box into a taboo cell.

    This is purely if the set of actions can be performed legally. The illegal moves are:
        - If the worker tries to move into a wall
        - If the worker tries to push a box into another box
        - If the workers tries to push a box into a wall

    Will return the state if all actions are successful and will return "Impossible" if an action
    is an illegal move

    @params: 
        warehouse - a valid Warehouse object
        action_seq - a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return:
        result - The string 'Impossible', if one of the action was not valid.
                    - For example, if the agent tries to push two boxes at the same time,
                                    or push a box into a wall.
                Otherwise, if all actions were successful, return                 
                    A string representing the state of the puzzle after applying
                    the sequence of actions.
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
    result = warehouseFinish.__str__()
    return result


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse. It will use the A Star Graph Search algorithm
    to search our problem space for a solution that fits our goal state (which is defined by all
    boxes on a goal/target location).

    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param:
        warehouse - a valid Warehouse object

    @returns:
        If puzzle cannot be solved
            answer - a string of "Impossible
            cost - None

        If a solution was found 
            answer - A list of actions that solves the puzzle
                For example: ['Left', 'Down', Down','Right', 'Up', 'Down']
            cost - The total cost of actions taken to get the solution
                For example: 26

    '''

    wh = SokobanPuzzle(warehouse=warehouse)
    wh.tabooCellFinder()
    # print("Taboo Cells")
    # print(wh.tabooCells)
    
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