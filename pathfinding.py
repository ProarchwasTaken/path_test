from main import *
# Basic font
font = pygame.font.Font(None, 28)


# Out of Bounds Check
# Checks if the specified adjacent tile is out of bounds (outside the screen). Returns None if so.
def oobCheck(layout, x, y, offsetX, offsetY):
    # Checks if Y + offsetY would be greater than GRID_ROWS or lower than 0.
    if y + offsetY >= GRID_ROWS or y + offsetY < 0:
        return None
    # Checks if X + offsetX would be greater than GRID_COLS or lower than 0.
    if x + offsetX >= GRID_COLS or x + offsetX < 0:
        return None
    # If above statements are false.
    direction = layout[y + offsetY][x + offsetX]

    # Returns the direction, and the offset in a neat little list! :)
    return [direction, (offsetX, offsetY)]


# Used for checking what tiles are adjcent to a tile. Then returning the results
def getAdjacents(layout, objX, objY):
    adjacent = {
        # HINT: oobCheck(layout, X, Y, offsetX, offsetY)
        "right": oobCheck(layout, objX, objY, 1, 0),
        "down": oobCheck(layout, objX, objY, 0, 1),
        "left": oobCheck(layout, objX, objY, -1, 0),
        "up": oobCheck(layout, objX, objY, 0, -1)
    }
    return adjacent


# Master parent class. All child classes will inherit and go through the code of init. I did this to lower the amount
# of repeating code. Every developer hates that for some reason.
class Common:
    def __init__(self, tileX, tileY, pathID):
        self.rect = pygame.Rect(tileX * TILE_SIZE, tileY * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        # Saves the pathID for pathfinding.
        self.pathID = pathID
        # The text that will display the path ID of the child instance
        self.text = font.render(f"{self.pathID}", False, COLOR["white"], COLOR["black"])

        # Saves the tile position the instance started on.
        self.tileX = tileX
        self.tileY = tileY


# The Pathfinding agent who will pathfind their way to the next target.
# Man, and I thought making the grid script was complicated. I guess it makes sense.
class Agent(Common):
    obj = None

    # Runs on instance initilization.
    def __init__(self, tileX, tileY, prevTime):
        super().__init__(tileX, tileY, 0)

        # How much delay between each time the createPath function is called.
        self.searchDelay = 0.01
        # Becomes important when searching for the target is impossible.
        self.stall = 0
        # Time variable
        self.prevTime = prevTime

        # How fast the agent will move during the movement phase.
        self.speed = 5

        # List to hold all spread tiles for searching for the exit.
        self.pathList = list()
        # List of positions, generated during the pathing phase that the agent moves through
        self.route = list()

    # Runs once every frame
    def update(self, viewport, grid, curTime, deltaTime):

        # Runs a function depending on the game state.
        if GET_GAMESTATE() == 'searching':
            self.targetSearch(curTime, grid)
        elif GET_GAMESTATE() == 'pathing':
            self.routeCreation(grid)
        elif GET_GAMESTATE() == 'moving':
            self.movementPhase(deltaTime)

        # Draws everything associated with the Agent
        self.draw(viewport)

    # Searches for the target
    def targetSearch(self, curTime, grid):
        # Only runs after a specified amount of time has passed
        if curTime - self.prevTime >= self.searchDelay:
            # Gets the old length of the list to compare later.
            oldPathCount = len(self.pathList)
            for path in self.pathList:
                # Checks if path has found the target.
                if path.targetFound():
                    # Deletes the path that collided with target
                    self.pathList.remove(path)

                    # Deletes any extra path tiles
                    self.pathCleanup()

                    # Generates and prints the layout.
                    layout = grid.scanLayout()
                    for line in layout:
                        print(line)

                    # Change the game state to the pathing phase.
                    CHANGE_GAMESTATE("pathing")
                    print(f"Path Count: {len(self.pathList)}")
                    break
                # Runs if the path tile is active
                elif path.active is True:

                    # Scan the layout
                    layout = grid.scanLayout()
                    # Get the adjacent tile information
                    adjacent = getAdjacents(layout, path.tileX, path.tileY)

                    # Create more path tiles based of said info
                    self.createPathTile(path.tileX, path.tileY, adjacent, path.pathID)

                    # Make the path tile unactive
                    path.active = False

                    # Resets the stall counter.
                    self.stall = 0

                    # Ends the loop
                    break

            # If the length of the new path list is the same as the old one, then increase stall by one.
            if len(self.pathList) == oldPathCount:
                self.stall += 1

            # Ends the search prematurely if stall is over 5
            if self.stall > 5:
                # Deletes all path tiles.
                self.pathList.clear()
                # Display error message
                print("[SEARCH FAILED] The target was impossible to get to!")
                # Change the gamestate back to standby.
                CHANGE_GAMESTATE("standby")
            # Resets the timer
            self.prevTime = curTime

    # Deletes any extra path tiles
    def pathCleanup(self):
        for path in self.pathList:
            if path.agentCollide():
                self.pathList.remove(path)
            if path.selfCollide():
                self.pathList.remove(path)

    # Sets up the route to the target
    # Probably the most complicated part of this program.
    # There's a lot of complicated things I write in this script
    def routeCreation(self, grid):
        # Gets selection rect
        selection = Target.selectionRect

        # Gets the tile position of selection
        tileX = int(selection.x / TILE_SIZE)
        tileY = int(selection.y / TILE_SIZE)

        # Gets the layout of the level.
        layout = grid.scanLayout()

        # Gets tiles adjacent to selection
        adjacent = getAdjacents(layout, tileX, tileY)

        # Declare list for get the index of adjacent path tiles
        adjPaths = list()

        # For each direction in adjacent
        for direction in adjacent:
            # Shortens the path for convenience
            dirInfo = adjacent[direction]
            # If the contents of dirInfo is not None
            if dirInfo is not None:
                # The tile found in that direction
                tile = dirInfo[0]

                # If tile is the agent tile
                if tile == 2:
                    print("The route has been completed!")
                    # Pauses the program for two seconds
                    time.sleep(2)

                    # Deletes all path tiles
                    self.pathList.clear()
                    # Reverse the order of every position in route.
                    self.route.reverse()

                    # Change the game state and end the function
                    CHANGE_GAMESTATE("moving")
                    return

                # If the tile is a path tile
                elif tile == 3:
                    # The offset to get that direction.
                    offsetX, offsetY = dirInfo[1]
                    # Gets the adjacent tile's position.
                    adjPos = (tileX + offsetX) * TILE_SIZE, (tileY + offsetY) * TILE_SIZE

                    # Every path checks if the following conditions are true
                    for path in self.pathList:
                        # Checks if the adjPos is inside path
                        if path.rect.collidepoint(adjPos):
                            # Appends data about the path to adjPaths
                            adjPaths.append(
                                {
                                    "pathID": path.pathID,
                                    "index": self.pathList.index(path),
                                    "pos": path.rect.topleft
                                }
                            )

        # This next part involves finding the adjacent tile with the lowest path id and setting up the other values
        # associated with it. For some reason I can't use min() with dictionaries so this is the solution I came up
        # with. It's probably terrible.

        # List of adjacent path IDs
        idList = list()
        # List of adjacent path indexs
        indexList = list()
        # List of avalible adjacent path positions
        posList = list()

        # Each dictionary in adjPaths
        for item in adjPaths:
            # Add each key is appended to their own seperate lists
            # Since each key is added at the same time, hopefully they will have the same indexes, so it will be easy to
            # get them when needed.
            idList.append(item["pathID"])
            indexList.append(item["index"])
            posList.append(item["pos"])

        # Gets the index of the lowest path id. Hopefully, this will allow the program to get the other keys that are
        # associated with the id.
        lowPathIndex = idList.index(min(idList))

        # Finally, using lowPathIndex, puts the right values right back into a dictionary that is the key to making
        # this work. Man, this took a bit to figure out :(
        tileData = {
            "pathID": idList[lowPathIndex],
            "index": indexList[lowPathIndex],
            "pos": posList[lowPathIndex]
        }

        print(f"Current Path Data: {tileData}")

        # Now that the program has the information needed. Here's the easy/fun part!

        # Adds the position to the route.
        self.route.append(tileData["pos"])

        # Shortens the path to the next tile.
        nextTile = self.pathList[tileData["index"]]

        # Change the color of the next tile.
        nextTile.color = COLOR["orange"]

        # Move the selection to the next tile's position
        Target.selectionRect.topleft = tileData["pos"]

    # TODO: Make it so the agent moves along a route.
    def movementPhase(self, deltatime):
        # If the route list is empty.
        if len(self.route) == 0:
            print("The agent has made it to their destination!")
            # Updates the agent's tile position
            self.tileX = int(self.rect.x / TILE_SIZE)
            self.tileY = int(self.rect.y / TILE_SIZE)

            # Change the gamestate and ends the function.
            CHANGE_GAMESTATE("standby")
            return

        # Gets the first position in the route.
        nextPos = self.route[0]

        # Checks if the agent's position is equal to nextPos
        if self.rect.topleft == nextPos:
            # Remove nextPos from the route
            self.route.remove(nextPos)
        else:
            # Splits the agent's position and nextPos into seperate variables
            x, y = self.rect.topleft
            nx, ny = nextPos

            if x < nx:  # If nextPos is to the right of Agent
                # Move Right
                self.movement(1, 0, deltatime)
            elif x > nx: # If nextPos is to the left of Agent
                # Move left
                self.movement(-1, 0, deltatime)
            elif y < ny: # If nextPos is below Agent
                # Move Down
                self.movement(0, 1, deltatime)
            elif y > ny: # If nextPos is above Agent
                # Move Up
                self.movement(0, -1, deltatime)

    # When called, moves the agent in a certain direction depending on the offset.
    def movement(self, offsetX, offsetY, dt):
        # The offset has to range from 1 to 0 to -1. With 0 not moving the agent at all
        self.rect.x += (self.speed * offsetX)
        self.rect.y += (self.speed * offsetY)

    # When called, begins the search for the target instance.
    def startSearch(self, grid, curTime):
        # Checks if a Target even exists in the first place, return False if not.
        if Target.obj is None:
            print("There is no target tile!")
            return False
        # Checks if Target is inside the agent.
        elif self.rect.colliderect(Target.obj.rect):
            print("The agent is already inside the target! Try moving it.")
            return False

        # Deletes all path tiles before proceeding
        self.pathList.clear()

        # First it asked the grid to generate a layout.
        layout = grid.scanLayout()
        # Then uses the layout to get what tiles are adjacent to him.
        adjacent = getAdjacents(layout, self.tileX, self.tileY)

        self.createPathTile(self.tileX, self.tileY, adjacent, self.pathID)
        self.prevTime = curTime

    # This functions creates path tiles on avalible adjacent tiles
    def createPathTile(self, tileX, tileY, adjacent, oldPathID):
        # For each direction in adjacent
        for direction in adjacent:
            # Shortens the path to the directions items for convenience.
            dirInfo = adjacent[direction]
            # Checks if the contents of dirInfo is not None
            if dirInfo is not None:
                # Gets the tile found from that direction.
                tile = dirInfo[0]
                # Gets the offset used to find the tile.
                offsetX, offsetY = dirInfo[1]

                # Checks if the tile is an empty tile or the target tile
                if tile == 0 or tile == 9:
                    # Creates a path tower at a chosen position + the offset and Path ID
                    self.pathList.append(Agent.Path(tileX + offsetX, tileY + offsetY, oldPathID + 1))

    # Debug function which prints out tiles adjcent to Agent
    def debug_adjacent(self, layout):
        adjacent = getAdjacents(layout, self.tileX, self.tileY)

        for direction in adjacent:
            print(f"{direction}: {adjacent[direction]}")

    # Draws the instance and all path tiles
    def draw(self, viewport):
        # Draw the path tiles
        for path in self.pathList:
            pygame.draw.rect(viewport, path.color, path.rect)
            viewport.blit(path.text, path.rect)

        # Then draw the agent
        pygame.draw.rect(viewport, COLOR["blue"], self.rect)
        viewport.blit(self.text, self.rect)

    # Path child class, this will be helpful in searching the Target and making a path to it.
    class Path(Common):
        def __init__(self, tileX, tileY, pathID):
            super().__init__(tileX, tileY, pathID)
            # Basic tile data
            self.color = COLOR["yellow"]

            # Determine whether the Path should create more Path instances
            self.active = True

            # Appends itself to agent's spread list
            Agent.obj.pathList.append(self)

        # Returns true if path tile has collided with Target object
        def targetFound(self):
            if self.rect.colliderect(Target.obj):
                return True

        # Returns true if path tile is inside another path tile
        def selfCollide(self):
            if self.rect.collideobjects(Agent.obj.pathList):
                return True

        # Returns the if path tile is inside the agent
        def agentCollide(self):
            if self.rect.colliderect(Agent.obj):
                return True


# Target child class, used as a finish line for the agent.
class Target:
    obj = None
    # Stores a copy of Target's Rect for later
    selectionRect = None

    # Runs on instance initilization.
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        # Clears and adds the Target's position to the Agent's route.
        # This will be important later.
        Agent.obj.route.clear()
        Agent.obj.route.append(self.rect.topleft)

        # Copy the instance's rect to a class variable
        Target.selectionRect = pygame.Rect.copy(self.rect)

    # Draws the instance
    def draw(self, viewport):
        pygame.draw.rect(viewport, COLOR["red"], self.rect)
