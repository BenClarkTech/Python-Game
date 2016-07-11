import pygame
from pygame.locals import *

"""This program generates two squares
One of them is moveable with the arrow keys.
You can change the color of the other using spacebar.
The moveable square will collide with the immobile one.
The moveable square will collide with the window walls.
"""

def getBounds(rec):
    """Takes in a rectangle and returns a list of the various bounds.
    [0] is x left bound, [1] is x right bound, [2] is y top bound
    [3] is y bottom bound. ***not sure if useful with moving cam."""
    return {rec.x,rec.x+rec.width,rec.y,rec.y+rec.height}

def moveRect(rec,dx,dy,*args):
    if dx != 0:
        moveRect_single_axis(rec,dx,0,args)
    if dy != 0:
        moveRect_single_axis(rec,0,dy,args)

def moveRect_single_axis(rec,dx,dy,*args):
    rec.x += dx
    rec.y += dy

    for arg in args[0]:
        if rec.colliderect(arg):
            if dx > 0:
                rec.right = arg.left
            if dx < 0:
                rec.left = arg.right
            if dy > 0:
                rec.bottom = arg.top
            if dy < 0:
                rec.top = arg.bottom
            return False

    return True


pygame.init()

clock = pygame.time.Clock()

xpos = 360
ypos = 300
px=xpos
py=ypos
speed = 3

CameraX = 0
CameraY = 0
cX = CameraX
cY = CameraY

#camera = pygame.rect.Rect(0,0,640,600)

window = pygame.display.set_mode([640,600])

pygame.display.set_caption("Moving Box")

pygame.display.flip()
red = (230,50,50)
purple = (128,0,128)
black = (0,0,0)

color = red

#rectangles below
rect1 = pygame.rect.Rect((100 - CameraX,300 - CameraY),(20,20))
rect2 = pygame.rect.Rect((xpos - CameraX,ypos - CameraY), (40,40))
floor = Rect((0 - CameraX,0 - CameraY),(640,600))
floor2 = Rect((650 - CameraX, 0 - CameraY),(640,600))

#saved code from initial movement structure
    
"""    if(pygame.key.get_pressed()[K_UP]):
        py = ypos
        ypos = ypos - speed
        cY = CameraY
        CameraY = CameraY - speed
    if(pygame.key.get_pressed()[K_DOWN]):
        py = ypos
        ypos = ypos + speed
        cY = CameraY
        CameraY = CameraY + speed
    if(pygame.key.get_pressed()[K_LEFT]):
        px = xpos
        xpos = xpos - speed
        cX = CameraX
        CameraX = CameraX - speed
    if(pygame.key.get_pressed()[K_RIGHT]):
        px = xpos
        xpos = xpos + speed
        cX = CameraX
        CameraX = CameraX + speed"""

#saved code from initial collision detecter


"""    if rect1.colliderect(rect2): #emplement this as a for loop for the future
        xpos = px
        ypos = py
        CameraX = cX
        CameraY = cY
        rect1.x = 100-CameraX
        rect1.y = 300-CameraY
        rect2.x = xpos - CameraX
        rect2.y = ypos - CameraY
        floor.x = 0-CameraX
        floor.y = 0-CameraY """
    
#possibly create a velocity pair which is edited in teh controller, which will consolidate velocity
#Current issue: it doesn't move the camera anymore. The emplementation commented out does move camera
#NOTE: haven't reemplemented border collision yet. Can do "Not Colliding With Floor" possibly
while True:
    clock.tick(60)
    
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
        if(moveRect(rect2,0,-speed,rect1)):
           moveRect(floor1,0,-speed)#a loop would go here
           moveRect(floor2,0,-speed)
           CameraY = CameraY - speed
    if(pygame.key.get_pressed()[K_DOWN]):
        if(moveRect(rect2,0,speed,rect1)):
           moveRect(floor1,0,speed)#a loop would go here
           moveRect(floor2,0,speed)
           CameraY = CameraY + speed
    if(pygame.key.get_pressed()[K_LEFT]):
        if(moveRect(rect2,-speed,0,rect1)):
           moveRect(floor1,-speed,0)#a loop would go here
           moveRect(floor2,-speed,0)
           CameraX = CameraX - speed
    if(pygame.key.get_pressed()[K_RIGHT]):
        if(moveRect(rect2,speed,0,rect1)):
           moveRect(floor1,speed,0)#a loop would go here
           moveRect(floor2,speed,0)
           CameraX = CameraX + speed
#    roomBounds = getBounds(floor)
    if xpos < 0:
        xpos = px
        CameraX = cX
 #       print "Hit Left."
    if ypos < 0:
        ypos = py
        CameraY = cY
 #       print "Hit Top."
    if xpos > 600:
        xpos = px
        CameraX = cX
 #       print "Hit Right."
    if ypos > 560:
        ypos = py
        CameraY = cY
 #       print "Hit Bottom."
 #   camera.x = CameraX
 #   camera.y = CameraY
    window.fill((40,50,180))
    pygame.draw.rect(window, (200,200,200), floor)
    pygame.draw.rect(window, (200,200,200), floor2)
    
    pygame.draw.rect(window, color, rect1)
    pygame.draw.rect(window, (100,200,250), rect2)
    

    
        
    pygame.display.update()

class myRect(pygame.rect):
    def __init__(self, *args, **kwargs):
        super(myRect, self).__init__(*args, **kwargs)


#If the player is colliding with a zone, outlined by rectangles
#Then the player should be effected by the bounds set by the particular rectangle
    #What if there is an "active room" concept, you pass the active room in as arguments for movement walls
#You should have open and closed boundaries. An array of 4 bools representing cardinal directions
#How would you open up zones to pass through? 
