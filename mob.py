"""
##########
v. 0.6
"Bounce"
-0.5 sticking and left wall bugs fixed.
-moves based on vector (list of two values)
-chooses opposite direction and one of three congruent directions on collision
##########
"""

import pygame
from pygame.locals import *
from random import *


#Initialize pygame
pygame.init()

#Constant Definition:
    #Positions:
xpos = 300#starting position if camera skewed
ypos = 280
px=xpos#archaic variables for revision
py=ypos
speed = 3
mob_direction = [-1, 0]

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
mob_blue = (100,200,250)
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
        not_mob.append(self)
        self.color = cement

class Env(Rect):
    def __init__(self, *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)
        not_mob.append(self)
        self.color = dark_gray

class mob(Rect):
    def __init__(self, *args, **kwargs):
        super(mob, self).__init__(*args, **kwargs)
        self.color = mob_blue

class EndGoal(Rect):
    def __init__(self, *args, **kwargs):
        super(EndGoal, self).__init__(*args,**kwargs)
        not_mob.append(self)
        self.color = red
        
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
       
        self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(self.w+2*wall_thickness,wall_thickness)))
        self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        self.Walls.append(Wall((self.x-wall_thickness,self.y+self.h),(self.w+2*wall_thickness,wall_thickness)))
        self.Walls.append(Wall((self.x+self.w,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        for wall in self.Walls:
            wall.color = wall_color
        for floor in self.Floors:
            floor.color = floor_color
        
class Board(object):
    def __init__(self, rows, collumns, startX=0, startY=0, roomW = 500, roomH = 500, thick = 20):
        self.rows = rows
        self.collumns = collumns
        self.startX = startX
        self.startY = startY
        self.roomW = roomW
        self.roomH = roomH
        self.thick = thick
        self.goal = None
        self.level = 0
        self.generate()
        
    def generate(self):
        rooms = []
        row = []
        N,S,E,W = False,False,False,False
        room_layout = (N,S,E,W)
        for i in range(0,self.collumns):
            for j in range(0,self.rows):
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
                #Hallway Anomaly
                if self.collumns == 1:
                    N = True
                    S = True
                if self.rows == 1:
                    E = True
                    W = True
                #Sets the mandatory border walls
                if(i == 0):
                    W = False
                if(j == 0):
                    N = False
                if(i == self.collumns - 1):
                    S = True
                    E = False
                if(j == self.rows - 1):
                    E == True
                    S = False
                #Ends mandatory border walls
                #Sets the Dependent Walls
                if(i - 1 >= 0):
                    W = rooms[i-1][j].E
                if(j - 1 >= 0):
                    N = row[j-1].S
                #Ends the Dependent Walls
                #Ensures every room has an entrance
                if j != 0:
                    if (N == False and S == False and E == False and W == False):
                        E = True
                if i != self.collumns - 1:
                    if (N == False and S == False and E == False and W == False):
                        S = True
                #Theory: No room will be unaccessable with this code.
                room_layout = (N,S,E,W)
                row.append(Room(((self.startX+(self.thick+self.roomW)*i),(self.startY+(self.thick+self.roomH)*j)),(self.roomW,self.roomH),room_layout,floor_color = (randint(0,255),randint(0,255),randint(0,255)),wall_thickness = self.thick)) #Because, why not random colors?
            rooms.append(row)
            row = []
        #Would be nice to implement a gating mechanism which opens if the room is completed.
        #pick a room to set the endpoint in
        end_point = (randint(1,self.collumns)-1,randint(1,self.rows)-1)
        while end_point == (0,0) and collumns != 0 and rows != 0:
            end_point = (randint(1,self.collumns)-1,randint(1,self.rows)-1)
        self.goal = EndGoal((0,0),(40,40))
        print end_point
        self.goal.center = rooms[end_point[0]][end_point[1]].Floors[0].center
        #endpoint ends

    def wash_board(self):
        del walls[:]
        del not_mob[:]

    def remake(self, rows, collumns, startX=0, startY=0, roomW = 500, roomH = 500, thick = 20, level_up = 0):
        self.rows = rows
        self.collumns = collumns
        self.startX = startX
        self.startY = startY
        self.roomW = roomW
        self.roomH = roomH
        self.thick = thick
        self.goal = None
        self.generate()
        self.level += level_up

#End Class Declarations


clock = pygame.time.Clock()


window = pygame.display.set_mode([winX,winY])
camera = Rect((CameraX,CameraY),(winX,winY)) #Note!!! Currently camera doesn't effect anything after initializing the scene
pygame.display.set_caption("Moving Box")

pygame.display.flip()
walls = []
not_mob = [] #because of how movement works we could actually include mob, however it provides more clarity as to our method if we seperate them

#rectangles below -- NOTE!!!! Order is currently IMPORTANT, as they are drawn in order declared.
mob = mob((xpos - camera.x,ypos - camera.y), (40,40))
#floor = Env((0 - camera.x,0 - camera.y),(winX,winY))
#floor2 = Env((650 - camera.x, 0 - camera.y),(winX,winY))
#rect1 = Wall((100 - camera.x,300 - camera.y),(20,20))
#testRoom = Room((-700,0),(340,680),(True,False,False,False),light_green,blue)

#room generation:
rows = 2
collumns = 2
wall_count = (collumns - 1) * rows + collumns * (rows - 1) #number of internal walls -- Generally not needed?
board = Board(rows, collumns)

#centers camera at start
mob.center = camera.center#comment out to allow skewed camera

#adds to appropriate lists !!!could make a walls class and an environment class which does this in constructor <<<Class Made>>>
#walls.append(rect1)
#not_mob.append(rect1)
#not_mob.append(floor)
#not_mob.append(floor2)

#possibly create a velocity pair which is edited in the controller, which will consolidate velocity
#emplemented camera following with more robust movement detection preventing corner catching, etc.
#NOTE: haven't reemplemented border collision yet. Can do "Not Colliding With Floor" possibly
#Alternatively, make walls using rectangles included in a list of impassible objects <<<This method has been emplemented.
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
    
    ###########################################
    ###########################################
    ###########################################
    ###########################################
    if (mob_direction[0] < 0):
        mob_direction[0] = randint(1, 4)
    if(mob_direction[0] == 1 or mob_direction[1] == 1): #moving up
        if(moveRect(mob,0,-speed,*walls)):
            #print "Not Colliding!"
            moveRect(mob,0,+speed)
            camera.center = mob.center
            for obj in not_mob:
                moveRect(obj,0,speed)
        else:
            mob_direction[0] = 2
            mob_direction[1] = choice([2, 3, 4])
    if(mob_direction[0] == 2 or mob_direction[1] == 2): #moving down
        if(moveRect(mob,0,speed,*walls)):
            #print "Not Colliding!"
            moveRect(mob,0,-speed)
            camera.center = mob.center
            for obj in not_mob:
                moveRect(obj,0,-speed)
        else:
            mob_direction[0] = 1
            mob_direction[1] = choice([1, 3, 4])
    if(mob_direction[0] == 3 or mob_direction[1] == 3): #moving left
        if(moveRect(mob,-speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(mob,speed,0)
            camera.center = mob.center
            for obj in not_mob:
                moveRect(obj,speed,0)
        else:
            mob_direction[0] = 4
            mob_direction[1] = choice([1, 2, 4])
    if(mob_direction[0] == 4 or mob_direction[1] == 4): #moving right
        if(moveRect(mob,speed,0,*walls)):
            #print "Not Colliding!"
            moveRect(mob,-speed,0)
            camera.center = mob.center
            for obj in not_mob:
                moveRect(obj,-speed,0)
        else:
            mob_direction[0] = 3
            mob_direction[1] = choice([1, 2, 3])
    if mob.colliderect(board.goal):
        #print "next board"
        board.wash_board()
        print walls
        rows = 1
        collumns = randint(1,10)
        board.remake(rows,collumns,level_up = 1)
        mob.x = xpos
        mob.y = ypos
        camera.center = mob.center
        #Show levelup screen possibly with something like [space] to continue
        #clear board
        #increment level counter
        #move mob to start position
        #regenerate a board
#    roomBounds = getBounds(floor)
#   below is old border management
  

#Painting of scene:
    window.fill(bg_gray)
    for obj in not_mob:
        pygame.draw.rect(window, obj.color, obj)
        
    pygame.draw.rect(window, mob.color, mob)
    
#What's better, .update() or .flip()?
    pygame.display.update()

class myRect(pygame.rect):
    def __init__(self, *args, **kwargs):
        super(myRect, self).__init__(*args, **kwargs)
