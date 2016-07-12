"""This program creates a menu screen that the user can interact with.
Move up and down with the arrow keys or 'w' and 's'. Select the current
option with the spacebar or the enter key.
(Currently, only the 'Quit' option works.)
"""
import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (80, 40, 0)

BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_BG_COLOR = BROWN
OUTLINE_COLOR = RED

FONT_SIZE = 20

SELECTION_COUNT = 3

OUTLINE_MAX_ALPHA = 255
OUTLINE_MIN_ALPHA = 63
OUTLINE_FADE_SPEED = 5


def main():
    """Create and maintain a menu screen.
    :returns: None
    :raises: None
    """
    global DISPLAY_SURF, START_SURF, START_RECT, OPTIONS_SURF, OPTIONS_RECT
    global QUIT_SURF, QUIT_RECT, BASIC_FONT

    menuSelection = 0
    outlineAlpha = OUTLINE_MAX_ALPHA
    outlineFading = True
    
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame: The Game")
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)

    """visual representations of the menu options"""
    START_SURF, START_RECT = makeText("Start Game", TEXT_COLOR, TEXT_BG_COLOR,
                                      int(WINDOW_WIDTH / 2),
                                      int(WINDOW_HEIGHT * 0.4))
    OPTIONS_SURF, OPTIONS_RECT = makeText("Options", TEXT_COLOR, TEXT_BG_COLOR,
                                          int(WINDOW_WIDTH / 2),
                                          int(WINDOW_HEIGHT * 0.5))
    QUIT_SURF, QUIT_RECT = makeText("Quit", TEXT_COLOR, TEXT_BG_COLOR,
                                    int(WINDOW_WIDTH / 2),
                                    int(WINDOW_HEIGHT * 0.6))

    """main game loop"""
    while True:
        drawMenu()

        """event handling"""
        for event in pygame.event.get():
            if (event.type == QUIT
              or (event.type == KEYUP and event.key == K_ESCAPE)):
                terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    menuSelection = (menuSelection - 1) % SELECTION_COUNT
                elif event.key in (K_DOWN, K_s):
                    menuSelection = (menuSelection + 1) % SELECTION_COUNT
                elif event.key in (K_SPACE, K_RETURN):
                    if menuSelection == 0:
                        pass # TODO: Start Game functionality
                    elif menuSelection == 1:
                        pass # TODO: Options functionality
                    elif menuSelection == 2:
                        terminate()

        """modify the outline's alpha value"""
        if outlineFading == True:
            outlineAlpha -= OUTLINE_FADE_SPEED
            if outlineAlpha <= OUTLINE_MIN_ALPHA:
                outlineAlpha = OUTLINE_MIN_ALPHA
                outlineFading = False
        elif outlineFading == False:
            outlineAlpha += OUTLINE_FADE_SPEED
            if outlineAlpha >= OUTLINE_MAX_ALPHA:
                outlineAlpha = OUTLINE_MAX_ALPHA
                outlineFading = True

        """draw the outline around the correct menu option"""
        if menuSelection == 0:
            selectionRect = START_RECT
        elif menuSelection == 1:
            selectionRect = OPTIONS_RECT
        elif menuSelection == 2:
            selectionRect = QUIT_RECT
        drawOutline(selectionRect, outlineAlpha)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    """Exit the program.
    :returns: None
    :raises: None
    """
    pygame.quit()
    sys.exit()


def makeText(text, color, bgColor, centerX, centerY):
    """Create the Surface and Rect objects for some text.
    :param text: The character string to render.
    :type text: String
    :param color: The color of the text.
    :type color: Color
    :param bgColor: The color of the background behind the text.
    :type bgColor: Color
    :param centerX: The x position of the center of the text.
    :type centerX: Integer
    :param centerY: The y position of the center of the text.
    :type centerY: Integer
    :returns: Tuple containing the Surface and Rect objects
    :raises: None
    """
    textSurf = BASIC_FONT.render(text, True, color, bgColor)
    textRect = textSurf.get_rect()
    textRect.center = (centerX, centerY)
    return (textSurf, textRect)


def drawMenu():
    """Draw the menu background and menu options.
    :returns: None
    :raises: None
    """
    DISPLAY_SURF.fill(BG_COLOR)
    DISPLAY_SURF.blit(START_SURF, START_RECT)
    DISPLAY_SURF.blit(OPTIONS_SURF, OPTIONS_RECT)
    DISPLAY_SURF.blit(QUIT_SURF, QUIT_RECT)


def drawOutline(selectionRect, outlineAlpha):
    """Draw an outline around the given menu option.
    :param selectionRect: The Rect object of the selected menu option.
    :type selectionRect: Rect
    :param outlineAlpha: The alpha value of the outline.
    :type outlineAlpha: Integer
    :returns: None
    :raises: None
    """
    alphaSurf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(alphaSurf, OUTLINE_COLOR + (outlineAlpha,),
                     (selectionRect.left - 2, selectionRect.top - 2,
                      selectionRect.width + 4, selectionRect.height + 4),
                     3)
    DISPLAY_SURF.blit(alphaSurf, (0, 0))


if __name__ == "__main__":
    main()
