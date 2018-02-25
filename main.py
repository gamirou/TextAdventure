"""
     : Empty
    1: Player
	C: Coin (you get 100pt)
	D: Door (you need a key)
	K: Key
	T: Treasure (you get 500pt)
	E: Exit, finished level
	A: Acropolis Treasure (1000pt)

Coordinates: u - going across, v - going down
"""
import csv

## FUNCTIONS

def findPos():
    for u in range(GRID_ROWS):
        for v in range(GRID_COLS):
             if grid[u][v] == '1':
                return {'x': v, 'y': u}
            

def printGrid(grid):
    str_grid = ''
    for u in range(GRID_ROWS):
        for v in range(GRID_COLS):
            str_grid += grid[u][v]

        str_grid += '\n'

    print(str_grid)

def updateGrid(new):
    ## CLEARS THE OLD MAP
    open('level'+ str(player.properties["currLevel"]) +'.txt', 'w').close()

    with open('level'+ str(player.properties["currLevel"]) +'.txt', 'a') as line:
        for i in range(GRID_ROWS):
            newLine = ''.join(new[i]) + '\n'
            line.write(newLine)

def updateStats(properties):
    global PLAYER_STATS
    
    ## UPDATING CSV FILE
    PLAYER_FILE = open('player_stats.csv', 'w')
    
    with PLAYER_FILE:
        writer = csv.DictWriter(PLAYER_FILE, fieldnames=PLAYER_STATS)    
        writer.writeheader()
        writer.writerow(properties)

def printInventory(player):
    print("""
Your inventory:
    Keys: {}
    Cash: {}
    Other Items :(coming soon)
""".format(player.properties['keys'], player.properties['score']))

    
## FUNCTIONS

## CLASSES

class Cell:

    def __init__(self, u, v, symbol):
        self.u = u
        self.v = v
        self.symbol = symbol

class Door(Cell):
    def __init__(self, u, v, index ,isOpen=False):
        super(Door, self).__init__(u, v, 'D')
        self.isOpen = isOpen
        self.index = index

class Player:

    def __init__(self):
        global PLAYER_STATS
        
        self.pos = None
        self.finished = False

        self.properties = {}

        ## ASSIGNING CSV FILE DATA TO PROPERTIES DICTIONARY
        with open('player_stats.csv', 'r') as line:
            reader = csv.reader(line)
            rowNum = 0
            
            for row in reader:
                if rowNum == 0:
                    PLAYER_STATS = list(row)
                else:
                    
                    colNum = 0 
                    for stat in row:
                        if not row[colNum]:
                            continue
                        self.properties[PLAYER_STATS[colNum]] = int(stat)
                        
                        colNum += 1

                rowNum += 1
        

    def move(self, movement):
        
        v = self.pos['x']
        u = self.pos['y']

        neighbour = self.getNeighbour(movement, u, v)

        if neighbour:
            if neighbour.symbol not in ('-', '+', '|'):
                if neighbour.symbol != 'D':
                    
                    if neighbour.symbol == 'C':
                        self.properties["score"] += 100
                        print("You got a coin! That means you are really close to the treasure! Go and find it!!")
                    elif neighbour.symbol == 'T':
                        self.properties["score"] += 500
                    elif neighbour.symbol == 'K':
                        self.properties["keys"] += 1
                        print("Woohoo!! You can finally open these ol' dungeon doors!!")
                    elif neighbour.symbol == 'E':
                        self.finished = True
                        print('Well done! You finished the level!')
                    elif neighbour.symbol == 'A':
                        self.properties["score"] += 1000
                        print("'OMG! You found the Acropolis Key. It doesn't unlock any modern door, but it is worth a lot! I will sell it' says 1")

                    grid[u][v] = ' '
                    grid[neighbour.u][neighbour.v] = '1'

                    cells[neighbour.u][neighbour.v].symbol = '1'
                    cells[u][v].symbol = ' '

                    updateGrid(grid)
                
                    self.pos = {'x': neighbour.v, 'y': neighbour.u}
                    self.properties["moves"] += 1
                    
                    updateStats(self.properties)
                    
                else: ## IF NEIGHBOUR == D
                    if neighbour.isOpen or self.properties["keys"] > 0:
                        if self.properties["keys"] > 0 and not neighbour.isOpen:
                            neighbour.isOpen = True
                            ALL_DOORS[int(self.properties['currLevel'])-1][neighbour.index] = True

                            open("doors.csv", "w").close()
                            
                            doorsFile = open("doors.csv", "w")
                            
                            with doorsFile:
                                writer = csv.writer(doorsFile)    
                                writer.writerows(ALL_DOORS)
                            
                                
                            self.properties["keys"] -= 1

                        grid[u][v] = ' '
                        grid[neighbour.u][neighbour.v] = '1'

                        cells[neighbour.u][neighbour.v].symbol = '1'
                        cells[u][v].symbol = ' '

                        updateGrid(grid)
                
                        self.pos = {'x': neighbour.v, 'y': neighbour.u}
                        self.properties["moves"] += 1
                    
                        updateStats(self.properties)

                    else:
                        print("Oops, you need a key, go and grab one!")
                


            else: ## IF NEIGHBOUR != W
                print("You hit a wall! You are not injured, but be careful next time!")

        else: ## IF NEIGHBOUR
            print("OOps, you hit the map's edges")
            
    def getNeighbour(self, movement, u, v):
        if movement == 'w':
            if u == 0:
                return None
            
            return cells[u-1][v]
                   
        elif movement == 'a':
            if v == 0:
                return None
            
            return cells[u][v-1]

        elif movement == 's':
            if u == GRID_ROWS - 1:
                return None
            
            return cells[u+1][v]
        
        else:
            if v == GRID_COLS - 1:
                return None
            
            return cells[u][v+1]

## CLASSES

## OPENS THE MAP
grid = []
cells = []
doors = []

GRID_ROWS = 0
GRID_COLS = 0

ALL_DOORS = []
PLAYER_STATS = []

LEVELS = {
   'level': [],
   'score': [],
   'highsc': [],
   'stars': [],
   'city': [],
   'location': [],
   'transport': [],
   'story': [],
}

player = Player()
CURR_LEVEL = {
    'level': player.properties['currLevel'],
}

## Storing all levels so I won't have to keep doing it
with open('levels.csv', 'r') as line:
    reader = csv.reader(line)
    x_index = 0
    y_index = 0
    for row in reader:
        if x_index == 0:
            lvl_header = row
        else:
            for val in row:
                LEVELS[lvl_header[y_index]].append(val)
                if x_index == int(CURR_LEVEL['level']):
                    CURR_LEVEL[lvl_header[y_index]] = val
                    
                y_index += 1

            y_index = 0

        x_index += 1

## SETUP

if player.properties['moves'] == 0:
    print("""
    Hello and Welcome to my first ever Maze Adventure Game!
    In this game, the mighty and adventurous '1' will have to go through a series of mazes throughout the world
    in his trip around the world. With your help, 1 will stop in 10 cities across the world, London, Athens, Giza, Dubai,
    New Delhi, Hiroshima, Los Angeles, New York, Reykjavik and Dublin. You will need to guide him across the famous
    places he goes so he can complete his ultimate quest, to go around the world.

    Instructions:
    You will see across the map different symbols. +, - and | represent the map's walls and borders. C and T represent money
    and you will need them to buy the transport methods needed to go to the next level. K and D are the keys and doors. It seems
    that each of these keys can open any door. That's really handy. You can keep the keys from the previous levels to use
    in the current level. Great! The E is the exit of the maze. You will need some keys to get out of the the maze. It will be tricky,
    but 1 agreed to leave to you all the remaining money for your help. Do you wish to embark on this tremendous journey? Sure you do!
    """)
else:
    print("Welcome back mate! Let's get back in the adventure!")


print("""Level {2}
Location: {0} - {1}

{3}
""".format(CURR_LEVEL['city'], CURR_LEVEL['location'], CURR_LEVEL['level'], CURR_LEVEL['story']))

def updateLevelMap():
    global grid
    global cells
    global doors
    global player
    global GRID_ROWS
    global GRID_COLS

    mapFile = open('level' + str(player.properties['currLevel']) +'.txt', 'r')
    rows = mapFile.readlines()
    GRID_ROWS = len(rows)
    GRID_COLS = len(rows[0]) - 1

    doorIndex = 0
    for u in range(GRID_ROWS):
        grid.append([])
        cells.append([])
        for v in range(GRID_COLS):
            grid[u].append(rows[u][v])

            if rows[u][v] == 'D':
                cell = Door(u, v, doorIndex)
            else:
                cell = Cell(u, v, rows[u][v])

            if isinstance(cell, Door):
                doors.append(cell)
                doorIndex += 1
            
            cells[u].append(cell)

    player.pos = findPos()
    mapFile.close()


## MAIN PROGRAM
updateLevelMap()

## Storing all doors so I won't have to keep doing it
with open('doors.csv', 'r') as line:
    reader = csv.reader(line)
    y_index = 0
    x_index = 0
    for row in reader:
        ALL_DOORS.append([])
        for val in row:
            if val == 'FALSE':
                doorVal = False
            else:
                doorVal = True

            if y_index == int(CURR_LEVEL['level']) - 1:
                doors[x_index].isOpen = doorVal
                
            ALL_DOORS[y_index].append(doorVal)
            
            x_index += 1

        
        y_index += 1
        x_index = 0

while True:
    printGrid(grid)
    printInventory(player)
    movement = input("Enter W for up, A for left, S for down, D for right!").lower()
    
    if movement in ('w', 'a', 's', 'd'):
        player.move(movement)

        u = player.pos['y']
        v = player.pos['x']
        for door in doors:
            if (door.u != u or door.v != v) and door.isOpen and door.symbol != 'D':
                cells[door.u][door.v].symbol = 'D'
                grid[door.u][door.v] = 'D'

        if player.finished:
            printGrid(grid)
            if CURR_LEVEL != 10:
                player.properties['currLevel'] += 1
            else:
                ## GAME FINISHED
                break

            player.properties['score'] -= int(CURR_LEVEL['transport'])
            player.finished = False
            
            print("WOW, well done, you finished level" + CURR_LEVEL['level'])

            for key in CURR_LEVEL:
                CURR_LEVEL[key] = LEVELS[key][player.properties['currLevel'] - 1]

            print("""Level {2}
            Location: {0} - {1}

            {3}
            """.format(CURR_LEVEL['city'], CURR_LEVEL['location'], CURR_LEVEL['level'], CURR_LEVEL['story']))

            for i in range(len(ALL_STATS[player.properties['currLevel']-1])):
                doors[i].isOpen = ALL_STATS[player.properties['currLevel']-1][i]

            updateLevelMap()

    elif movement == 'quit':
        print("1 can't wait for you to come back! :)")
        break
    else:
        print("Enter a valid input like W,A,S,D or quit")


