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
        ret = moveRect_single_axis(rec,dx,0,*args)
        #print str(ret)+"({},{})".format(dx,dy)
        return ret
    if dy != 0:
        ret = moveRect_single_axis(rec,0,dy,*args)
        #print str(ret)+"({},{})".format(dx,dy)
        return ret

def moveRect_single_axis(rec,dx,dy,*args):
    rec.x += dx
    rec.y += dy
    for arg in args:
        #print str(args[0])+str(rec) #object debugging
        if rec.colliderect(arg):
            #print "Collision Detected"
            if dx > 0:
                rec.right = arg.left
                #print "left bump"
            if dx < 0:
                rec.left = arg.right
                #print "right bump"
            if dy > 0:
                rec.bottom = arg.top
                #print "top bump"
            if dy < 0:
                rec.top = arg.bottom
                #print "bottom bump"
            #print "Colliding"
            #print "Transformed -> "+str(args[0])+str(rec) #object debugging
            return False
    #print "not Colliding"
    return True

class Wall(Rect):
    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        walls.append(self)
        not_player.append(self)

class Env(Rect):
    def __init__(self, *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)
        not_player.append(self)
    
pygame.init()

clock = pygame.time.Clock()

xpos = 300#starting position if camera skewed
ypos = 280
px=xpos#archaic variables for revision
py=ypos
speed = 3

CameraX = 0#camera start
CameraY = 0
cX = CameraX#archaic variables for revision
cY = CameraY

winX = 640
winY = 600

window = pygame.display.set_mode([winX,winY])
camera = Rect((CameraX,CameraY),(winX,winY)) #Note!!! Currently camera doesn't effect anything after initializing the scene
pygame.display.set_caption("Moving Box")

pygame.display.flip()
red = (230,50,50)
purple = (128,0,128)
black = (0,0,0)

color = red
walls = []
not_player = [] #because of how movement works we could actually include player, however it provides more clarity as to our method if we seperate them

#rectangles below
rect1 = Wall((100 - camera.x,300 - camera.y),(20,20))
rect2 = Rect((xpos - camera.x,ypos - camera.y), (40,40))
floor = Env((0 - camera.x,0 - camera.y),(winX,winY))
floor2 = Env((650 - camera.x, 0 - camera.y),(winX,winY))

#centers camera at start
rect2.center = camera.center#comment out to allow skewed camera

#adds to appropriate lists !!!could make a walls class and an environment class which does this in constructor <<<Class Made>>>
#walls.append(rect1)
#not_player.append(rect1)
#not_player.append(floor)
#not_player.append(floor2)

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
#emplemented camera following with more robust movement detection preventing corner catching, etc.
#NOTE: haven't reemplemented border collision yet. Can do "Not Colliding With Floor" possibly
#Alternatively, make walls using rectangles included in a list of impassible objects
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
        if(moveRect(rect2,0,-speed,*walls)):
            #print "Not Colliding!"
            moveRect(rect2,0,+speed)
            camera.center = rect2.center
            for obj in not_player:
                moveRect(obj,0,speed)
    if(pygame.key.get_pressed()[K_DOWN]):
        if(moveRect(rect2,0,speed,*walls)):
            #print "Not Colliding!"
            moveRect(rect2,0,-speed)
            camera.center = rect2.center
            for obj in not_player:
                moveRect(obj,0,-speed)
    if(pygame.key.get_pressed()[K_LEFT]):
        if(moveRect(rect2,-speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(rect2,speed,0)
            camera.center = rect2.center
            for obj in not_player:
                moveRect(obj,speed,0)
    if(pygame.key.get_pressed()[K_RIGHT]):
        if(moveRect(rect2,speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(rect2,-speed,0)
            camera.center = rect2.center
            for obj in not_player:
                moveRect(obj,-speed,0)
#    roomBounds = getBounds(floor)
#   below is old border management
    """if xpos < 0:
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
        CameraY = cY"""
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
