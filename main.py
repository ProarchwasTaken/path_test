from constants import *
import sys
import pygame
import time

"""====================================================================================================================
Pathfinding Algorithm written by: Tyler

I managed to write a pathfinding system without watching any direct coding tutorials on how to do it. All I've really 
done before codeing this, is watch a video on how pathfinding algorithms generally work and figured out the rest. It
wasn't easy though, this is probably the most lines of code I've written into a project so far.

I've also went about doing a different script structure than normal. Personally I think it looks better.

CONTROLS: 
- Click a tile to add/remove a wall.
- Right click to place/move the target tile
- Press the Space key and watch the magic happen!

The reason I went ahead to do this is because I figured that knowing how to do pathfinding is one of those things that 
are necessary to making most games. Along with animations, spritesheets, serialization, and the works. Hopefully I can
write a more efficient system in the future, so what do you think?

Thanks for checking this out!
====================================================================================================================="""


# Main program function
def Program():
    pygame.init()
    # General Imports
    from pathfinding import Agent, Target
    from grid import Grid

    # Window setup
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    viewport = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Game Clock setup
    Clock = pygame.time.Clock()
    prevTime = time.time()

    # Class Instances
    Grid.obj = Grid(0, 0, 1)

    Agent.obj = Agent(10, 10, prevTime)  # (Tile X, Tile Y, prevTime)

    # Main game loop
    while True:
        # Ticks the clock, making the program only run at a maximum set FPS
        Clock.tick(FPS)
        # FPS Counter
        pygame.display.set_caption(f"Pathfinding | FPS: {round(Clock.get_fps())}")
        # Gets the current time.
        curTime = time.time()
        # Gets deltatime value.
        deltaTime = curTime - prevTime
        # Resets prevTime to curTime
        prevTime = curTime

        # Clears the screen.
        viewport.fill(COLOR["white"])

        # Event interpreter which checks for program events and handles what to do when said events occur.
        # This function is starting to get a bit long, maybe I could have a seperate script for it...
        for event in pygame.event.get():
            # Allows the player to quit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Detect for any kind of mouse press.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # This would only run if the current game state is 'standby'
                if GET_GAMESTATE() == 'standby':
                    Grid.obj.mouseButtonDown(event.pos, event.button)
            # Checks for when a key is pressed
            if event.type == pygame.KEYDOWN:
                # DEBUG: Manually scans the layout and prints which tiles are adjacent to Agent.
                if event.key == pygame.K_e:
                    layout = Grid.obj.scanLayout()
                    for line in layout:
                        print(line)
                    Agent.obj.debug_adjacent(layout)

                # Triggers when the Space key is pressed and if the gamestate is at a specific value.
                if event.key == pygame.K_SPACE and GET_GAMESTATE() == 'standby':
                    # Tells the Agent to search for the Target. Not before checking if the Target exists at all.
                    if Agent.obj.startSearch(Grid.obj, curTime) is not False:
                        # Change the gamestate.
                        CHANGE_GAMESTATE("searching")

        # Updates class instances
        Grid.obj.draw(viewport)

        if Target.obj is not None:
            Target.obj.draw(viewport)

        Agent.obj.update(viewport, Grid.obj, curTime, deltaTime)

        # Updates screen to reflect changes
        screen.blit(viewport, (0, 0))
        pygame.display.flip()


# This is the main script! Run this first!
# Starting to realize the real importantance of this simple line of code. When I was new, I used to have problems with
# circular imports to the point where I was reluctant to try multi file projects for a while.
if __name__ == '__main__':
    Program()
