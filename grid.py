from main import *
from pathfinding import Agent, Target

# The more I go on, I keep finding better ways of doing certain things. Before, I just create multiple instance of
# tiles, instead, I just have to make a list of multiple rects and I think it works much better.

# Well nevermind then... recently I've gone back to using class instances. The reason for this because I could properly
# use if statments to check which tile it actually is. Also, I think this will improve code readability for me and
# others later on.


# The Base grid class.
# Resposible for rendering the grid and generating the layout for the path finding agent.
class Grid:
    obj = None

    # Runs on instance initilization.
    def __init__(self, offX, offY, spacing):
        # Declares list of to store all tile rects and wall instances.
        self.tilelist = []
        # Stores all tile positions
        self.tileRects = []
        # The offset position of the grid.
        self.offset = (offX, offY)
        # The amount of pixels between each tile.
        self.spacing = spacing

        # Prepare a list of tiles based of col and row index
        for row_index in range(GRID_ROWS):
            for col_index in range(GRID_COLS):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                # With said information, adds the rect to the list.
                self.tilelist.append(Tile(x, y, TILE_SIZE - spacing))
                self.tileRects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

        # The most primal form of the layout, will soon to used later
        self.rawList = []
        # Holds the full layout with the correct listing.
        self.layout = list()

    # When called it will check for mouse inputs and save the position the mouse was at when pressed
    def mouseButtonDown(self, pos, key):
        # Swap tile
        if key == 1:  # Left Mouse Button
            # For each tile of the instance, check if the mouse position is inside any given rect.
            for tile in self.tilelist:
                if tile.rect.collidepoint(pos):
                    # Swaps the tile
                    self.swapTile(tile)
        if key == 3:  # Right Mouse Button
            # For each tile, check of the mouse position is inside any of them.
            for tile in self.tilelist:
                if tile.rect.collidepoint(pos):
                    # Create/Change the position of Target at the position of tile.
                    Target.obj = Target(tile.rect.x, tile.rect.y)

    # Swap tile function, this still works whether if it's a tile or a wall.
    # This function also ensures that the new tile will retain the list index the old tile used to have thanks to
    # insert()
    def swapTile(self, tile):
        print(f"Removed tile ID: {self.tilelist.index(tile)}")
        # Retrieves some information about the tile
        targetedIndex = self.tilelist.index(tile)
        oldRectX = tile.rect.x
        oldrectY = tile.rect.y

        # Deletes the rect
        self.tilelist.remove(tile)

        # A class check which determines what happens next.
        if tile.__class__ == Tile:
            # Creates a regular tile at the old rect's position and with its old index.
            self.tilelist.insert(targetedIndex, Wall(oldRectX, oldrectY, TILE_SIZE))
        elif tile.__class__ == Wall:
            # Creates a wall tile at the old rect's position and with its old index.
            self.tilelist.insert(targetedIndex, Tile(oldRectX, oldrectY, TILE_SIZE - self.spacing))

    # Will called, it will return a layout of the map in the form of a nested list.
    def scanLayout(self):
        # Clears the list to prevent unexpected layout duplication
        self.rawList.clear()
        self.layout.clear()
        # For every tile in the grid, it will check to see of it collides with the windowRect
        for tile in self.tilelist:
            # Appends a certain number to the raw list depending on the class of the tile.
            if tile.__class__ == Tile:
                self.rawList.append(0)
            if tile.__class__ == Wall:
                self.rawList.append(1)

        # Converts the long list into a clean, nested list. Thus saving the structual layout of the level
        for i in range(0, len(self.rawList), GRID_ROWS):
            self.layout.append(self.rawList[i:i + GRID_COLS])

        # Gets the agent's center position
        agentCenter = Agent.obj.rect.center
        # Sets targetCenter to None
        targetCenter = None
        # Checks if a Target exists.
        if Target.obj is not None:
            targetCenter = Target.obj.rect.center

        # Each tile checks to see if the agent's center position is inside their rect.
        for tile in self.tilelist:
            # Checks if the tile detects Agent.
            if tile.rect.collidepoint(agentCenter):
                self.tileIntegration(tile, 2)
            # Checks if the tile detects a path tile
            elif tile.rect.collideobjects(Agent.obj.pathList):
                self.tileIntegration(tile, 3)
            # Check if the tile detects Target
            elif targetCenter is not None:
                if tile.rect.collidepoint(targetCenter):
                    self.tileIntegration(tile, 9)

        # Returns the layout to the thing that called it.
        # Empty Tiles = 0, Walls = 1, Agent = 2, Path Tile = 3, Target = 9
        return self.layout

    # Function for replacing values in self.layout
    # Funny How I realize a better way of doing this, days after I wrote it
    def tileIntegration(self, tile, newID):
        # Splits the tile's position into two seperate variables
        objX, objY = tile.rect.topleft

        # Divides each value by the tilesizes to get true tile positions
        objTileX = int(objX / TILE_SIZE)
        objTileY = int(objY / TILE_SIZE)

        # Sets a specific nested list value using the two position variable to new ID
        self.layout[objTileY][objTileX] = newID

    # Draws every tile on the screen
    def draw(self, viewport):
        # Draws each rect in the list
        for tile in self.tilelist:
            # Checks if the class of the tile and will act accordingly
            if tile.__class__ == Tile:
                pygame.draw.rect(viewport, COLOR["black"], tile)
            elif tile.__class__ == Wall:
                pygame.draw.rect(viewport, COLOR["grey"], tile)


# Tile Sub-Class
class Tile:
    def __init__(self, x, y, tilesize):
        self.rect = pygame.Rect(x, y, tilesize, tilesize)


# Wall Sub-Class
class Wall:
    def __init__(self, x, y, tilesize):
        self.rect = pygame.Rect(x, y, tilesize, tilesize)

