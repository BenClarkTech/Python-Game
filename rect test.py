import pygame
from pygame.locals import *
from random import *

"""
One half-mob added to first level. Enjoy
"""

#Initialize pygame
pygame.init()

#Constant Definition:
    #Positions:
xpos = 300#starting position if camera skewed
ypos = 280
px=xpos#archaic variables for revision
py=ypos
default_speed = 3
speed = default_speed
#mob_direction = [-1, 0]
CLOCK = 60

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
#End Constand Definition
#Begin Function Definition
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
#End Function Definition
#Begin Class Definition
class Wall(Rect):
    def __init__(self, (x,y) = (0,0), (w,h) = (0,0), rec = None, *args, **kwargs):
        if rec == None:
            super(Wall, self).__init__((x,y),(w,h),*args, **kwargs)
            walls.append(self)
            not_player.append(self)
            self.color = cement
        else:
            self.x = rec.x
            self.y = rec.y
            self.w = rec.w
            self.h = rec.h
            not_player.append(self)
            self.color = cement

    def remove(self):
        not_player.remove(self)
        walls.remove(self)


class Env(Rect):
    def __init__(self, (x, y) = (0,0), (w, h) = (0,0), rec = None, *args, **kwargs):
        if rec == None:
            super(Env, self).__init__((x,y),(w,h))
            not_player.append(self)
            self.color = dark_gray
        else:
            self.x = rec.x
            self.y = rec.y
            self.w = rec.w
            self.h = rec.h
            not_player.append(self)
            self.color = dark_gray
            
    def remove(self):
        not_player.remove(self)

class Player(Rect):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.color = player_blue

class mob(Rect):
    def __init__(self, *args, **kwargs):
        super(mob, self).__init__(*args, **kwargs)
        not_player.append(self)
        Mobs.append(self)
        self.direction = [-1, 0]
        self.color = black

    #def __call__(self, *args, **kwargs):
    #    return mob.__init__(self, *args, **kwargs)

    def remove(self):
        not_player.remove(self)
        walls.remove(self)

    def move(self):
        ##### mob movement ###
        if (mob.direction[0] < 0):
            mob.direction[0] = randint(1, 4)
            mob.direction[1] = randint(1, 4)
        if(mob.direction[0] == 1 or mob.direction[1] == 1): #moving up
            if(not moveRect(mob,0,-speed,*walls)):
                mob.direction[0] = 2
                mob.direction[1] = choice([2, 3, 4])
        if(mob.direction[0] == 2 or mob.direction[1] == 2): #moving down
            if(not moveRect(mob,0,speed,*walls)):
                mob.direction[0] = 1
                mob.direction[1] = choice([1, 3, 4])
        if(mob.direction[0] == 3 or mob.direction[1] == 3): #moving left
            if(not moveRect(mob,-speed,0,*walls)):
                mob.direction[0] = 4
                mob.direction[1] = choice([1, 2, 4])
        if(mob.direction[0] == 4 or mob.direction[1] == 4): #moving right
            if(not moveRect(mob,speed,0,*walls)):
                mob.direction[0] = 3
                mob.direction[1] = choice([1, 2, 3])

class EndGoal(Rect):
    def __init__(self, *args, **kwargs):
        super(EndGoal, self).__init__(*args,**kwargs)
        not_player.append(self)
        self.color = red

    def remove(self):
        not_player.remove(self)

#Event Class Blocks
"""
To add an event there are 4 components. First you must make a new event array. Simple, just declare it in the array block.
Second you must create a new event class. These are all pretty cookie cutter, just follow the models below and append to your appropriate array.
Third you must create a new event in the generation block. This is creating the hitbox and aligning it to the room center. Follow the existing examples.
Finally you must create the rule for those events. This is located in the main loop. Emplement by adding a for loop over your array to check collisions with Player.
"""
class SpeedS(Rect):
    def __init__(self, *args, **kwargs):
        super(SpeedS, self).__init__(*args,**kwargs)
        not_player.append(self)
        SmallSpeed.append(self)
        self.color = light_green

    def remove(self):
        not_player.remove(self)
        SmallSpeed.remove(self)

class SpeedB(Rect):
    def __init__(self, *args, **kwargs):
        super(SpeedB, self).__init__(*args,**kwargs)
        not_player.append(self)
        BigSpeed.append(self)
        self.color = purple

    def remove(self):
        not_player.remove(self)
        BigSpeed.remove(self)

#End Event Class Blocks
        
"""class SampleSprite(pygame.sprite.Sprite): #Example of sprites - this allows sprite groups <<<NOT BEING USED IN THIS PROJECT
    def __init__(self, color=light_green, x=-100, y=-100, player = None, *args, **kwargs):
        super(SampleSprite, self).__init__(*args, **kwargs)
        self.image = pygame.Surface([100,100])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.env = Env(rec = self.rect)
        self.env.color = color"""
        
class Room(object):
    """Class Room is a Highly Customizable Template class which can create various types of rooms. gap represents a fraction of the wall that is the door. Door is always centered."""
    def __init__(self, position=(0,0), size=(winX,winY),doors=(False,False,False,False),floor_color=dark_gray,wall_color=cement,wall_thickness = 20,gap = .32,level = 0):
        chunk = (1-gap)/2 #size of a piece of the wall on a gap side
        self.chunk = chunk #optimization: replace chunk w/ self.chunk
        self.level = level
        self.level = (randint(0,2) + level) * randint(0,1)
        self.checked = False
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
        self.center = self.Floors[0].center

    def SetFloor(self,color):
        self.floor_color = color
        for floor in self.Floors:
            floor.color = color

    def SetWall(self,color):
        self.wall_color = color
        for wall in self.Walls:
            wall.color = color

    def remove(self):
        #print "remove called."
        for floor in self.Floors:
            floor.remove()
        for wall in self.Walls:
            wall.remove()

    def GetCover(self):
        covers = 3
        cover_model = randint(0,covers)
        if cover_model == 0:
            return
        elif cover_model == 1: #One Box Center
            self.Walls.append(Wall((self.x+self.w*.3,self.y+self.h*.3),(self.w*.4,self.h*.4)))
        elif cover_model == 2: #Three Box Center
            self.Walls.append(Wall((self.x + .1 * self.w, self.y + .1 * self.h),(.3*self.w,.3*self.h)))
            self.Walls.append(Wall((self.x + .6 * self.w, self.y + .1 * self.h),(.3*self.w,.3*self.h)))
            self.Walls.append(Wall((self.x + .35 * self.w, self.y + .6 * self.h),(.3*self.w,.3*self.h)))
        elif cover_model == 3: #Four corner boxes
            self.Walls.append(Wall((self.x,self.y),(self.w*self.chunk*.5,self.h*self.chunk*.5)))
            self.Walls.append(Wall((self.x,self.y),(self.w*self.chunk*.5,self.h*self.chunk*.5)))
            self.Walls[len(self.Walls)-1].topright = self.Floors[0].topright
            self.Walls.append(Wall((self.x,self.y),(self.w*self.chunk*.5,self.h*self.chunk*.5)))
            self.Walls[len(self.Walls)-1].bottomright = self.Floors[0].bottomright
            self.Walls.append(Wall((self.x,self.y),(self.w*self.chunk*.5,self.h*self.chunk*.5)))
            self.Walls[len(self.Walls)-1].bottomleft = self.Floors[0].bottomleft

    def GetMobs(self):
        decide = 1#randint(0, 1)
        if decide == 1:
            Mobs.append(mob((self.x+150,self.y+100), (40,40)))
            

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
        self.rooms = []
        self.mobs = []
        self.generate()
        
    def generate(self):
        self.collumns += self.level/2
        self.rows += self.level/2
        rooms = []
        row = []
        events = []
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
                    E = False
                    #if(j != self.rows - 1): #These caveats are optional.
                     #   S = True
                if(j == self.rows - 1):
                    S = False
                    #if(i != self.rows - 1): #(cont) They basically create an alley around the bottom right to navigate around.
                     #   E = True
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
                row.append(Room(((self.startX+(self.thick+self.roomW)*i),(self.startY+(self.thick+self.roomH)*j)),(self.roomW,self.roomH),room_layout,floor_color = (randint(0,255),randint(0,255),randint(0,255)),wall_thickness = self.thick,level = self.level)) #Because, why not random colors?
            """  #NEWCONECPT: Check passable if not remove the lock
            test = False
            if i != self.collumns - 1:
                for room in row:
                    if room.S == True:
                        test = True
            if test == False:
                print "Horizontal Lock Adjusted"
                rand = randint(0,len(row)-1)
                row[rand].S == True"""
            rooms.append(row)#not part of newconcept
            row = []#not part of newconcept
        """ test = False
        for y in range(0,self.collumns-1):
            for x in range(0,self.rows):
                room = rooms[x][y]
                if room.E == True:
                    test = True
            if test == False:
                print "Vertical Lock Adjusted"
                rand = randint(0,len(rooms) - 1)
                print rand
                rooms[rand][y].E = True
                rooms[rand-1][y].W = True\
        #END NEWCONCEPT"""
        #checker to get all passable terrain
        self.rooms = rooms
        self.checker(0,0);
        #Would be nice to implement a gating mechanism which opens if the room is completed.
        #pick a room to set the endpoint in
        end_point = (randint(1,self.collumns)-1,randint(1,self.rows)-1) #Endpoint is some random room on the board.
        while (end_point == (0,0) and collumns != 0 and rows != 0) or rooms[end_point[0]][end_point[1]].checked != True: 
            end_point = (randint(1,self.collumns)-1,randint(1,self.rows)-1)
        #creates the end point
        self.goal = EndGoal((0,0),(40,40))
        print end_point #debugging location of endpoint
        #aligns end point to middle of room
        self.goal.center = rooms[end_point[0]][end_point[1]].Floors[0].center
        #Sets levels to prevent unkindly spawns of cover
        rooms[end_point[0]][end_point[1]].level = 0
        rooms[0][0].level = 0
        #CoverGeneration is here
        for row in rooms:
            for room in row:
                if room.level > 0 and room.checked == True:
                    room.GetCover()
                    room.GetMobs()
                    
                    
        #EventGeneration goes here !!!Read instructions before adding event located near the event class block!!!
        for row in rooms:
            for room in row:
                if room.level == 0 and room.checked == True and room != rooms[end_point[0]][end_point[1]]:
                    if randint(0,9) == 9:
                        number_big = 1 #if you add a new big event increment this
                        choice = randint(1,number_big)
                        if choice == 1:
                            events.append(SpeedB((0,0),(100,100)))
                            events[len(events)-1].center = room.center
                        #addnew big events here as an elif
                    elif randint(0,4) == 4:
                        number_small = 1 #if you add a new small event increment this
                        choice = randint(1,number_small)
                        if choice == 1:
                            events.append(SpeedS((0,0),(50,50)))
                            events[len(events)-1].center = room.center
                        #addnew small events here as an elif
                            
        #Unaccessable room removal:
        for row in rooms:
            for room in row:
                if room.checked == False:
                    print "Removing room"
                    room.remove()
        self.rooms = rooms #saves rooms for later use - should make all rooms self.rooms for efficiency

    def wash_board(self):
        del walls[:]
        del not_player[:]
        del self.rooms[:]

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

    def checker(self,x,y):
        self.rooms[x][y].checked = True
        self.rooms[x][y].SetFloor(chocolate)
        #print str(x)+" "+str(y)
        if self.rooms[x][y].N:
            if self.rooms[x][y-1].checked == False:
                self.checker(x,y-1)
        if self.rooms[x][y].S:
            if self.rooms[x][y+1].checked == False:
                self.checker(x,y+1)
        if self.rooms[x][y].E:
            if self.rooms[x+1][y].checked == False:
                self.checker(x+1,y)
        if self.rooms[x][y].W:
            if self.rooms[x-1][y].checked == False:
                self.checker(x-1,y)

#End Class Definition


clock = pygame.time.Clock()

window = pygame.display.set_mode([winX,winY])
camera = Rect((CameraX,CameraY),(winX,winY)) #Note!!! Currently camera doesn't effect anything after initializing the scene*****not true anymore technically?
pygame.display.set_caption("Moving Box")

pygame.display.flip()

timer = 0

Mobs = []
                                          
#Array Initialization
walls = []
not_player = [] #because of how movement works we could actually include player, however it provides more clarity as to our method if we seperate them
SmallSpeed = []
BigSpeed = []

#rectangles below -- NOTE!!!! Order is currently IMPORTANT, as they are drawn in order declared.
player = Player((xpos - camera.x,ypos - camera.y), (40,40))
#room generation:
rows = randint(1,10)
collumns = randint(1,10)

rows = 2
collumns = 2
board = Board(rows, collumns)
#mobs:
mob = mob((300,11), (40,40))
#centers camera at start
player.center = camera.center#comment out to allow skewed camera

#text initialization:
body = pygame.font.Font(None, 36)
subhead = pygame.font.Font(None, 72)
header = pygame.font.Font(None, 144)
subtitle = pygame.font.Font(None, 220)
title = pygame.font.Font(None, 288)

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
    
#possibly create a velocity pair which is edited in the controller, which will consolidate velocity
#emplemented camera following with more robust movement detection preventing corner catching, etc.
#NOTE: haven't reemplemented border collision yet. Can do "Not Colliding With Floor" possibly
#Alternatively, make walls using rectangles included in a list of impassible objects <<<This method has been emplemented.
while True:
    clock.tick(CLOCK)
    if timer != 0:
        timer -= 1
    else:
        speed = default_speed
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
    if player.colliderect(board.goal):
        #print "next board"
        board.wash_board()
        #print walls
        rows = randint(1,4)
        collumns = randint(1,4)
        board.remake(rows,collumns,level_up = 1)
        player.x = xpos
        player.y = ypos
        camera.center = player.center
        #Show levelup screen possibly with something like [space] to continue
        #clear board
        #increment level counter
        #move player to start position
        #regenerate a board

        ##### mob movement ###
    for mob in Mobs:
            mob.move()
        
    for event in BigSpeed: #Event Executions go here !!!Read instructions before adding event located near the event class block!!!
        if player.colliderect(event):
                speed = default_speed+3
                timer = 10 * CLOCK
    for event in SmallSpeed:
        if player.colliderect(event):
                speed = default_speed+1
                timer = 10 * CLOCK
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

#Paint Text:
    for row in board.rooms:#This loop paints all the room levels
        for room in row:
            if room.checked:
                text = body.render(str(room.level), 1, (10,10,10))
                textpos = text.get_rect()
                textpos.center = room.Floors[0].center
                window.blit(text,textpos)
    text = subhead.render(str(board.level), 1, cement)
    textpos = text.get_rect()
    textpos.topright = camera.topright
    window.blit(text,textpos)
    
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
