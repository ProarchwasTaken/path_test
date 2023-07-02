# =======GAME STATES==========
# 'standby' = Nothing is happening, you can place down walls and change the target position
# 'searching' = The Agent searchs the layout until it finds the Target
# 'pathing' = Generates a path starting from the target to the Agent
# 'moving' = The pathfinding agent traverses down the path generated until it reaches the target.

# The beginning state of the program.
GAME_STATE = 'standby'

# At first, I thought changing and checking the current game_state was as easy as just changing the value or using an
# if statment, but do to how importing from other python files works, it's not that simple, you could probably figure
# out why on Google. I did come up of a solution though, and it seems to work fine.


# When called, it returns the current game state. Allows other files to get info on what the current game state is.
def GET_GAMESTATE():
    return GAME_STATE


# Important function, when called, it will change the gamestate of the game, affecting lots of different things.
def CHANGE_GAMESTATE(newState):
    global GAME_STATE
    GAME_STATE = newState
    print(f"Switching gamestate to '{GAME_STATE}'")


# The size of the window
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
# Frames per second
FPS = 60
TARGET_FPS = 60
# The size of each tile.
TILE_SIZE = 40
# Calculates how many tiles can fit on the X and Y axis depending on the Window and Tile size
GRID_COLS = 15
GRID_ROWS = 15
# Color Dictionary
COLOR = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 128, 0)
}
