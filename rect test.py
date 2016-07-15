import pygame
from pygame.locals import *
from random import *

"""This program generates two squares
One of them is moveable with the arrow keys.
You can change the color of the other using spacebar.
The moveable square will collide with the immobile one.
The moveable square will collide with the window walls.
"""

#Initialize pygame
pygame.init()

#Constant Definition:
    #Positions:
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
    #Colors:
red = (230,50,50)
purple = (128,0,128)
black = (0,0,0)
chocolate = (139,69,19)
cement = (205,197,191)
light_green = (113,198,113)
blue = (92,172,239)
dark_gray = (71,71,71)
player_blue = (100,200,250)
bg_gray = (19,19,19)
#For more colors see this resource: http://cloford.com/resources/colours/500col.htm or use paint
color = red



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
        self.color = cement

class Env(Rect):
    def __init__(self, *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)
        not_player.append(self)
        self.color = dark_gray

class Player(Rect):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.color = player_blue

class Room(object):
    """Class Room is a Highly Customizable Template class which can create various types of rooms. gap represents a fraction of the wall that is the door. Door is always centered."""
    def __init__(self, position=(0,0), size=(winX,winY),doors=(False,False,False,False),floor_color=dark_gray,wall_color=cement,wall_thickness = 20,gap = .32):
        chunk = (1-gap)/2 #size of a piece of the wall on a gap side
        (self.x,self.y) = position
        (self.w,self.h) = size
        (self.N,self.S,self.E,self.W) = doors
        self.floor_color = floor_color
        self.wall_color = wall_color
        self.Floors = []
        self.Floors.append(Env((self.x,self.y),(self.w,self.h)))
        self.Walls = []
        if self.N:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Walls.append(Wall((self.x+(chunk+gap)*self.w,self.y-wall_thickness),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Floors.append(Env((self.x+chunk*self.w - 1,self.y-wall_thickness),(self.w*gap + 1,wall_thickness)))
        else:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(self.w+2*wall_thickness,wall_thickness)))
        if self.W:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Walls.append(Wall((self.x-wall_thickness,self.y+(chunk+gap)*self.h),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Floors.append(Env((self.x-wall_thickness,self.y+chunk*self.h-1),(wall_thickness,self.h * gap + 1)))
        else:    
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        if self.S:
            self.Walls.append(Wall((self.x-wall_thickness,self.y+self.h),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Walls.append(Wall((self.x+(chunk+gap)*self.w,self.y+self.h),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Floors.append(Env((self.x+chunk*self.w,self.y+self.h),(self.w * gap,wall_thickness)))
        else:
            self.Walls.append(Wall((self.x-wall_thickness,self.y+self.h),(self.w+2*wall_thickness,wall_thickness)))
        if self.E:
            self.Walls.append(Wall((self.x+self.w,self.y-wall_thickness),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Walls.append(Wall((self.x+self.w,self.y+(chunk+gap)*self.h),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Floors.append(Env((self.x+self.w,self.y+chunk*self.h),(wall_thickness,self.h * gap)))
        else:    
            self.Walls.append(Wall((self.x+self.w,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        for wall in self.Walls:
            wall.color = wall_color
        for floor in self.Floors:
            floor.color = floor_color
        


clock = pygame.time.Clock()


window = pygame.display.set_mode([winX,winY])
camera = Rect((CameraX,CameraY),(winX,winY)) #Note!!! Currently camera doesn't effect anything after initializing the scene
pygame.display.set_caption("Moving Box")

pygame.display.flip()
walls = []
not_player = [] #because of how movement works we could actually include player, however it provides more clarity as to our method if we seperate them

#rectangles below -- NOTE!!!! Order is currently IMPORTANT, as they are drawn in order declared.
player = Player((xpos - camera.x,ypos - camera.y), (40,40))
#floor = Env((0 - camera.x,0 - camera.y),(winX,winY))
#floor2 = Env((650 - camera.x, 0 - camera.y),(winX,winY))
#rect1 = Wall((100 - camera.x,300 - camera.y),(20,20))
#testRoom = Room((-700,0),(340,680),(True,False,False,False),light_green,blue)

#room generation:
roomW = 500
roomH = 500
thick = 20
startX = 0
startY = 0
rows = randint(1,10)
collumns = randint(1,10)
wall_count = (collumns - 1) * rows + collumns * (rows - 1) #number of internal walls -- Generally not needed?
rooms = []
collumn = []
N,S,E,W = False,False,False,False
room_layout = (N,S,E,W)
for i in range(0,rows):
    for j in range(0,collumns):
        #Randomization
        seed = randint(0,2)
        if seed == 0:
            E = True
            S = True
        elif seed == 1:
            E = False
            S = True
        elif seed == 2: #anyway to make a W N room? <<<Interesting question
            E = True
            S = False
        #Sets the mandatory border walls
        if(i == 0):
            W = False
        if(j == 0):
            N = False
        if(i == rows - 1):
            E = False
        if(j == collumns - 1):
            S = False
        #Ends mandatory border walls
        #Sets the Dependent Walls
        if(i - 1 >= 0):
            W = rooms[i-1][j].E
        if(j - 1 >= 0):
            N = collumn[j-1].S
        #Ends the Dependent Walls
        #Ensures every room has an entrance
        if j == 0:
            if (N == False and S == False and E == False and W == False):
                E = True
        if i == rows - 1:
            if (N == False and S == False and E == False and W == False):
                S - True
        #Theory: No room will be unaccessable with this code.
        room_layout = (N,S,E,W)
        collumn.append(Room(((startX+(thick+roomW)*i),(startY+(thick+roomH)*j)),(roomW,roomH),room_layout,floor_color = (randint(0,255),randint(0,255),randint(0,255)),wall_thickness = thick)) #Because, why not random colors?
    rooms.append(collumn)
    collumn = []
#Would be nice to implement a gating mechanism which opens if the room is completed.


#centers camera at start
player.center = camera.center#comment out to allow skewed camera

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
        if(moveRect(player,0,-speed,*walls)):
            #print "Not Colliding!"
            moveRect(player,0,+speed)
            camera.center = player.center
            for obj in not_player:
                moveRect(obj,0,speed)
    if(pygame.key.get_pressed()[K_DOWN]):
        if(moveRect(player,0,speed,*walls)):
            #print "Not Colliding!"
            moveRect(player,0,-speed)
            camera.center = player.center
            for obj in not_player:
                moveRect(obj,0,-speed)
    if(pygame.key.get_pressed()[K_LEFT]):
        if(moveRect(player,-speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(player,speed,0)
            camera.center = player.center
            for obj in not_player:
                moveRect(obj,speed,0)
    if(pygame.key.get_pressed()[K_RIGHT]):
        if(moveRect(player,speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(player,-speed,0)
            camera.center = player.center
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

#Painting of scene:
    window.fill(bg_gray)
    for obj in not_player:
        pygame.draw.rect(window, obj.color, obj)
        
    pygame.draw.rect(window, player.color, player)

#What's better, .update() or .flip()?        
    pygame.display.update()

class myRect(pygame.rect):
    def __init__(self, *args, **kwargs):
        super(myRect, self).__init__(*args, **kwargs)


#If the player is colliding with a zone, outlined by rectangles
#Then the player should be effected by the bounds set by the particular rectangle
    #What if there is an "active room" concept, you pass the active room in as arguments for movement walls
#You should have open and closed boundaries. An array of 4 bools representing cardinal directions
#How would you open up zones to pass through? 
