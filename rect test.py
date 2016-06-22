import pygame
from pygame.locals import *

"""This program generates two squares
One of them is moveable with the arrow keys.
You can change the color of the other using spacebar.
The moveable square will collide with the immobile one.
The moveable square will collide with the window walls.
"""

pygame.init()

xpos = 360
ypos = 300
px=xpos
py=ypos
speed = .3


window = pygame.display.set_mode([640,600])

pygame.display.set_caption("Moving Box")

red = (230,50,50)
purple = (128,0,128)
black = (0,0,0)

color = red

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                if color == purple:
                    color = red
                else:
                    color = purple
        
    if(pygame.key.get_pressed()[K_UP]):
        py = ypos
        ypos = ypos - speed
    if(pygame.key.get_pressed()[K_DOWN]):
        py = ypos
        ypos = ypos + speed
    if(pygame.key.get_pressed()[K_LEFT]):
        px = xpos
        xpos = xpos - speed
    if(pygame.key.get_pressed()[K_RIGHT]):
        px = xpos
        xpos = xpos + speed
    if xpos < 0:
        xpos = 0
    if ypos < 0:
        ypos = 0
    if xpos > 600:
        xpos = 600
    if ypos > 560:
        ypos = 560
    window.fill((40,50,180))
    rect1 = pygame.draw.rect(window, color, Rect((100,300),(20,20)))
    rect2 = pygame.draw.rect(window, (100,200,250), Rect((xpos,ypos), (40,40)))
    if rect1.colliderect(rect2):
        xpos = px
        ypos = py
        
    pygame.display.update()
