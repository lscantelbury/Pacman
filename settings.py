from pygame.math import Vector2 as vec

# screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)


# font settings
START_TEXT_SIZE = 50
START_FONT = 'verdana'

# player settings
# PLAYER_START_POS = vec(2, 2)

# mob settings

LEFT_BOUNDARY = (31.0, 315.0)
RIGHT_BOUNDARY = (581.0, 315.0)
