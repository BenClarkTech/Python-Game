import pygame
import math
import time
import sys
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
default_speed = 4
speed = default_speed
default_bullet_speed = 15
default_shot_delay = 40.0
default_spread_angle = 0.1
#mob_direction = [-1, 0]
CLOCK = 60
timer = 0
spawn = (0,0)

CameraX = 0#camera start
CameraY = 0
cX = CameraX#archaic variables for revision
cY = CameraY

winX = 1200
winY = 900
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
orange = (255,140,0)
dark_orange = (139,69,0)
white = (255,255,255)
light_blue = (200,200,255)
blood_red = (70,7,7)
obsidian =  (6,6,6)
gold = (205, 173, 0)
light_yellow = (238, 238, 180)
dark_red = (127,0,0)

#For more colors see this resource: http://cloford.com/resources/colours/500col.htm or use paint
color = red

#
#Array Initialization
Mobs = []
bullets = []
walls = []
not_player = [] #because of how movement works we could actually include player, however it provides more clarity as to our method if we seperate them
SmallSpeed = []
BigSpeed = []
mob_gate = []
Fire = []
Buck = []
potential_end = []

#End Constand Definition
#Begin Function Definition


def fire_shot((x, y), (w, h), center_angle, speed, power, bounce, spread_count,
              spread_angle, owner, color=None):
    """Create one or more bullets with the given properties. Use this
    instead of the Bullet constructor.
    """
    # spread calculation expects that spread_count is at least 1
    if spread_count < 1:
        spread_count = 1

    # calculate the angles for all bullets in the spread
    bullet_angles = [center_angle
                     - ((spread_count - 1) * spread_angle / 2.0)
                     + (spread_angle * bullet_number)
                     for bullet_number in range(spread_count)]

    # create all bullets
    for angle in bullet_angles:
        Bullet((x, y), (w, h),
               speed * math.cos(angle), speed * math.sin(angle),
               power, bounce, owner, color)

def get_angle((origin_x, origin_y), (target_x, target_y)):
    """Return the angle of the vector from an origin position to a
    target position.
    """
    x_distance = target_x - origin_x
    y_distance = target_y - origin_y
    angle = math.atan2(y_distance, x_distance)
    return angle

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
    if type(rec) is Bullet:
        rec.realx += dx
        rec.realy += dy
        rec.x = int(round(rec.realx))
        rec.y = int(round(rec.realy))
    else:
        rec.x += dx
        rec.y += dy
    for arg in args:
        #print str(args[0])+str(rec) #object debugging
        if rec.colliderect(arg):
            #print "Collision Detected"
            if dx > 0:
                rec.right = arg.left
                if type(rec) is Bullet:
                    rec.realx = rec.x
                #print "left bump"
            if dx < 0:
                rec.left = arg.right
                if type(rec) is Bullet:
                    rec.realx = rec.x
                #print "right bump"
            if dy > 0:
                rec.bottom = arg.top
                if type(rec) is Bullet:
                    rec.realy = rec.y
                #print "top bump"
            if dy < 0:
                rec.top = arg.bottom
                if type(rec) is Bullet:
                    rec.realy = rec.y
                #print "bottom bump"
            #print "Colliding"
            #print "Transformed -> "+str(args[0])+str(rec) #object debugging
            return False
    #print "not Colliding"
    return True


def moveTrueRect(rec,dx,dy,*args):
    if dx != 0:
        ret = moveTrueRect_single_axis(rec,dx,0,*args)
        #print str(ret)+"({},{})".format(dx,dy)
        return ret
    if dy != 0:
        ret = moveTrueRect_single_axis(rec,0,dy,*args)
        #print str(ret)+"({},{})".format(dx,dy)
        return ret

def moveTrueRect_single_axis(rec,dx,dy,*args):
    rec.realx += dx
    rec.realy += dy
    rec.x = int(round(rec.realx))
    rec.y = int(round(rec.realy))
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

def terminate():
    pygame.quit()
    sys.exit()

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

class MobGate(Rect):
    def __init__(self, *args, **kwargs):
        super(MobGate,self).__init__(*args,**kwargs)
        not_player.append(self)
        mob_gate.append(self)
        self.color = gold

    def remove(self):
        not_player.remove(self)
        mob_gate.remove(self)

class Player(Rect):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.color = player_blue
        self.health = 3
        self.damage_cd = 0
        self.shot_timer = 0
        self.shot_spread = 1
        self.fire_rate = 1/default_shot_delay

class Mob(Rect):
    def __init__(self, (x, y) = (0,0), (w, h) = (0,0), speed_scale = 1,*args, **kwargs):
        super(Mob, self).__init__((x,y),(w,h),*args, **kwargs)
        not_player.append(self)
        Mobs.append(self)
        self.direction = [randint(1,4),0]
        self.color = dark_red
        self.speed = default_speed * .5 * speed_scale
        self.health = 5
        self.flash = 0
        
    #def __call__(self, *args, **kwargs):
    #    return mob.__init__(self, *args, **kwargs)

    def remove(self):
        not_player.remove(self)
        Mobs.remove(self)

    def move(self):
        ##### mob movement ###
        collideable = []
        for wall in walls:
            collideable.append(wall)
        for gate in mob_gate:
            collideable.append(gate)
        if(self.direction[0] == 1 or self.direction[1] == 1): #moving up
            if(not moveRect(self,0,-self.speed,*collideable)):
                self.direction[0] = 2
                self.direction[1] = choice([2, 3, 4])
        if(self.direction[0] == 2 or self.direction[1] == 2): #moving down
            if(not moveRect(self,0,self.speed,*collideable)):
                self.direction[0] = 1
                self.direction[1] = choice([1, 3, 4])
        if(self.direction[0] == 3 or self.direction[1] == 3): #moving left
            if(not moveRect(self,-self.speed,0,*collideable)):
                self.direction[0] = 4
                self.direction[1] = choice([1, 2, 4])
        if(self.direction[0] == 4 or self.direction[1] == 4): #moving right
            if(not moveRect(self,self.speed,0,*collideable)):
                self.direction[0] = 3
                self.direction[1] = choice([1, 2, 3])

    def takeDmg(self,dmg=1):
        print self.health
        self.health -= dmg
        print self.health
        self.flash = 5
        if(self.health <= 0):
            GetPowerup(self.x,self.y)
            self.remove()
            print "killed."

class MobBoss(Mob):
    def __init__(self,(x, y) = (0,0), (w, h) = (0,0), speed_scale = 1, level=0, *args, **kwargs):
        super(MobBoss, self).__init__((x,y),(w,h),speed_scale,*args,**kwargs)
        stage = level/5
        self.health = 100
        self.speed = default_speed * .5
        self.at_half_health = False
        self.at_quarter_health = False

    def takeDmg(self,dmg=1):
        global spawn
        self.health -= dmg
        self.flash = 20
        if(self.at_half_health == False and self.health <= 50):
            self.at_half_health = True
            self.w = self.w/2
            self.h = self.h/2
            newmob = MobBoss((self.x,self.y),(self.w,self.h))
            self.speed *= 2
            newmob.speed *= 2
            newmob.health = 50
            newmob.at_half_health = True
        if(self.at_quarter_health == False and self.health <= 25):
            self.at_quarter_health = True
            self.w = self.w/2
            self.h = self.h/2
            self.speed *= 1.5
            newmob2 = MobBoss((self.x,self.y),(self.w,self.h))
            newmob2.speed *= 3
            newmob2.health = 25
            newmob2.at_half_health = True
            newmob2.at_quarter_health = True
        if(self.health <= 0):
            spawn = (self.x,self.y)
            self.remove()

class Bullet(Rect):
    def __init__(self, (x, y)=(0, 0), (w, h)=(0, 0), x_speed=0, y_speed=15,
                 power=1, bounce=0, owner="player", color=None,
                 *args, **kwargs):
        super(Bullet, self).__init__((x, y), (w, h), *args, **kwargs)
        
        not_player.append(self)
        bullets.append(self)
        
        self.realx = self.x
        self.realy = self.y
        self.x_speed = x_speed
        self.y_speed = y_speed
        if power < 1:
            self.power = 1
        else:
            self.power = power
        self.bounce = bounce # number of times bullet can bounce off walls
        self.owner = owner # could be things like "player", "mob", "trap"
        if color == None:
            if owner == "player":
                self.color = blue
            else:
                self.color = orange
        else:
            self.color = color

    def remove(self):
        if self in not_player:
            not_player.remove(self)
        if self in bullets:
            bullets.remove(self)

    def move(self):
        collideable = []
        for wall in walls:
            collideable.append(wall)
        for gate in mob_gate:
            collideable.append(gate)
        # horizontal movement
        if self.x_speed != 0 and not moveRect(self, self.x_speed, 0, *collideable):
            if self.bounce == 0:
                self.remove()
            else:
                self.x_speed *= -1
                if self.bounce > 0:
                    self.bounce -= 1
        # vertical movement
        if self.y_speed != 0 and not moveRect(self, 0, self.y_speed, *collideable):
            if self.bounce == 0:
                self.remove()
            else:
                self.y_speed *= -1
                if self.bounce > 0:
                    self.bounce -= 1

class EndGoal(Rect):
    def __init__(self, *args, **kwargs):
        super(EndGoal, self).__init__(*args,**kwargs)
        not_player.append(self)
        self.color = white

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

#Power Up Blocks
def GetPowerup(x,y):
    numUPs = 2
    z = randint(1,numUPs)
    if z == 1:
        powerup = BuckShotUP((x,y),(40,40))
    if z == 2:
        powerup = FireRateUP((x,y),(40,40))

class BuckShotUP(Rect):
    def __init__(self, *args, **kwargs):
        super(BuckShotUP,self).__init__(*args,**kwargs)
        not_player.append(self)
        Buck.append(self)
        self.color = orange

    def remove(self):
        not_player.remove(self)
        Buck.remove(self)

class FireRateUP(Rect):
    def __init__(self, *args, **kwargs):
        super(FireRateUP,self).__init__(*args,**kwargs)
        not_player.append(self)
        Fire.append(self)
        self.color = light_yellow

    def remove(self):
        not_player.remove(self)
        Fire.remove(self)

#End Power Up Blocks
        
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
        self.floor_color = (randint(0,255),randint(0,255),randint(0,255))#floor_color
        self.wall_color = wall_color
        self.Floors = []
        self.Floors.append(Env((self.x,self.y),(self.w,self.h)))
        self.Walls = []
        self.Mobs = []
        if self.N:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Walls.append(Wall((self.x+(chunk+gap)*self.w,self.y-wall_thickness),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Floors.append(MobGate((self.x+chunk*self.w - 1,self.y-wall_thickness),(self.w*gap + 1,wall_thickness)))
        else:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(self.w+2*wall_thickness,wall_thickness)))
        if self.W:
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Walls.append(Wall((self.x-wall_thickness,self.y+(chunk+gap)*self.h),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Floors.append(MobGate((self.x-wall_thickness,self.y+chunk*self.h-1),(wall_thickness,self.h * gap + 1)))
        else:    
            self.Walls.append(Wall((self.x-wall_thickness,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        if self.S:
            self.Walls.append(Wall((self.x-wall_thickness,self.y+self.h),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Walls.append(Wall((self.x+(chunk+gap)*self.w,self.y+self.h),(self.w * chunk+wall_thickness,wall_thickness)))
            self.Floors.append(MobGate((self.x+chunk*self.w,self.y+self.h),(self.w * gap,wall_thickness)))
        else:
            self.Walls.append(Wall((self.x-wall_thickness,self.y+self.h),(self.w+2*wall_thickness,wall_thickness)))
        if self.E:
            self.Walls.append(Wall((self.x+self.w,self.y-wall_thickness),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Walls.append(Wall((self.x+self.w,self.y+(chunk+gap)*self.h),(wall_thickness,self.h * chunk+wall_thickness)))
            self.Floors.append(MobGate((self.x+self.w,self.y+chunk*self.h),(wall_thickness,self.h * gap)))
        else:    
            self.Walls.append(Wall((self.x+self.w,self.y-wall_thickness),(wall_thickness,self.h+2*wall_thickness)))
        for wall in self.Walls:
            wall.color = wall_color
        for floor in self.Floors:
            if type(floor) != MobGate:
                floor.color = floor_color
        self.center = self.Floors[0].center

    def SetFloor(self,color):
        self.floor_color = color
        for floor in self.Floors:
            if type(floor) != MobGate:
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

    def GetBossCover(self):
        covers = 4
        cover_model = randint(1,covers)
        cover_model = 2
        if cover_model == 0:
            return
        elif cover_model == 1: #One Box Center
            self.Walls.append(Wall((self.x+self.w*.4,self.y+self.h*.4),(self.w*.2,self.h*.2)))
        elif cover_model == 2: #HalfRoom
            self.Walls.append(Wall((self.x+self.w*.49,self.y + self.h*.35),(self.w*.02,self.h*.3)))
            event = SpeedS((self.x+self.w/4-30,self.y+self.h/2-30),(60,60))
            event = SpeedB((self.x+3*self.w/4-50,self.y+self.h/2-50),(100,100))
        elif cover_model == 3: #Four corner boxes
            self.Walls.append(Wall((self.x,self.y),(100,100)))
            self.Walls.append(Wall((self.x,self.y),(100,100)))
            self.Walls[len(self.Walls)-1].topright = self.Floors[0].topright
            self.Walls.append(Wall((self.x,self.y),(100,100)))
            self.Walls[len(self.Walls)-1].bottomright = self.Floors[0].bottomright
            self.Walls.append(Wall((self.x,self.y),(100,100)))
            self.Walls[len(self.Walls)-1].bottomleft = self.Floors[0].bottomleft
        elif cover_model == 4: #CrossRoom
            self.Walls.append(Wall((self.x+self.w*.49,self.y + self.h*.35),(self.w*.02,self.h*.3)))
            self.Walls.append(Wall((self.x+self.w*.35,self.y + self.h*.49),(self.w*.3,self.h*.02)))
    

    def GetMobs(self):
        decide = 1#randint(0, 1)
        if decide == 1:
            ran = randint(0,15)
            self.Mobs.append(Mob((self.x+150,self.y+100), (30 + ran,30 + ran), 1 + self.level/5))

    def GetBoss(self,level):
        self.Mobs.append(MobBoss((0,0),(200,200)))
        self.Mobs[0].midright = self.Floors[0].midright
            

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
        #self.mobs = []
        self.generate()
        
    def generate(self):
        global potential_end
        print "Generating new board"
        if(self.level != 0 and self.level%5 == 4):
            self.generateBoss()
            return
        self.collumns += self.level/2
        self.rows += self.level/2
        rooms = []
        row = []
        events = []
        N,S,E,W = False,False,False,False
        room_layout = (N,S,E,W)
        print "Making rooms"
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
                row.append(Room(((self.startX+(self.thick+self.roomW)*i),(self.startY+(self.thick+self.roomH)*j)),(self.roomW,self.roomH),room_layout,floor_color = (60,60,60),wall_thickness = self.thick,level = self.level)) #Because, why not random colors?

            rooms.append(row)#not part of newconcept
            row = []#not part of newconcept
        print "Checking rooms"
        #checker to get all passable terrain
        self.rooms = rooms
        potential_end = []
        if self.checker(0,0) != 0:
            return
        #Would be nice to implement a gating mechanism which opens if the room is completed.
        #pick a room to set the endpoint in
        end_point = choice(potential_end) #Endpoint is some random room on the board.
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
                    print "Mob got."
                    room.GetMobs()
                    
        print "Generating Events."
        #EventGeneration goes here !!!Read instructions before adding event located near the event class block!!!
        for row in rooms:
            for room in row:
                if room.level == 0 and room.checked == True and room != rooms[end_point[0]][end_point[1]]:
                    if randint(0,9) == 9:
                        number_big = 1 #if you add a new big event increment this
                        x = randint(1,number_big)
                        if x == 1:
                            events.append(SpeedB((0,0),(100,100)))
                            events[len(events)-1].center = room.center
                        #addnew big events here as an elif
                    elif randint(4,4) == 4:
                        number_small = 1 #if you add a new small event increment this
                        x = randint(1,number_small)
                        if x == 1:
                            events.append(SpeedS((0,0),(50,50)))
                            events[len(events)-1].center = room.center
                        #addnew small events here as an elif
        print "Removing rooms"
        #Unaccessable room removal:
        for row in rooms:
            for room in row:
                if room.checked == False:
                    room.remove()
        self.rooms = rooms #saves rooms for later use - should make all rooms self.rooms for efficiency
        print "Generation complete"

    def wash_board(self):
        del Fire[:]
        del Buck[:]
        del SmallSpeed[:]
        del BigSpeed[:]
        del walls[:]
        del not_player[:]
        del self.rooms[:]
        del Mobs[:]
        del bullets[:]
        del mob_gate[:]

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

    def checker(self,x,y,flag = False):
        self.rooms[x][y].checked = True
        flag2 = True
        #self.rooms[x][y].SetFloor(chocolate)
        #print str(x)+" "+str(y)
        if self.rooms[x][y].N:
            flag = True
            print "N" + str(x) + str(y)
            if self.rooms[x][y-1].checked == False:
                flag2 = False
                self.checker(x,y-1,True)
        if self.rooms[x][y].S:
            flag = True
            print "S" + str(x) + str(y)
            if self.rooms[x][y+1].checked == False:
                flag2 = False
                self.checker(x,y+1,True)
        if self.rooms[x][y].E:
            flag = True
            print "E" + str(x) + str(y)
            if self.rooms[x+1][y].checked == False:
                flag2 = False
                self.checker(x+1,y,True)
        if self.rooms[x][y].W:
            flag = True
            print "W" + str(x) + str(y)
            if self.rooms[x-1][y].checked == False:
                flag2 = False
                self.checker(x-1,y,True)
        if not flag:
            self.wash_board()
            rows = randint(1,4)
            collumns = randint(1,4)
            self.remake(rows,collumns,level_up = 0)
            return -1
        if flag2:
            potential_end.append((x,y))
        return 0

    def generateBoss(self):
        self.rooms = []
        row = []
        row.append(Room((self.startX,self.startY),(self.roomW*1.5,self.roomH*1),(False,False,False,False),floor_color = blood_red, wall_color = obsidian, wall_thickness = self.thick*3, level = 0))
        self.rooms.append(row)
        self.rooms[0][0].GetBossCover()
        self.rooms[0][0].GetBoss(self.level)
#End Class Definition


clock = pygame.time.Clock()

window = pygame.display.set_mode([winX,winY])
camera = Rect((CameraX,CameraY),(winX,winY)) #Note!!! Currently camera doesn't effect anythind

#text initialization:
body = pygame.font.Font(None, 36)
subhead2 = pygame.font.Font(None, 58)
subhead = pygame.font.Font(None, 72)
header = pygame.font.Font(None, 134)
subtitle = pygame.font.Font(None, 220)
title = pygame.font.Font(None, 288)


def game_loop():                                          
    #Array Initialization
    speed = default_speed
    """Mobs = []
    walls = []
    not_player = [] #because of how movement works we could actually include player, however it provides more clarity as to our method if we seperate them
    SmallSpeed = []
    BigSpeed = []"""
    timer = 0
    #rectangles below -- NOTE!!!! Order is currently IMPORTANT, as they are drawn in order declared.
    player = Player((xpos,ypos), (40,40))
    #room generation:
    rows = randint(1,10)
    collumns = randint(1,10)
    
    rows = 2
    collumns = 2
    board = Board(rows, collumns)
    #mobs:
    #mob = mob((300,11), (40,40))
    #centers camera at start
    camera.center = player.center#comment out to allow skewed camera
    count = 0


    while True:
        clock.tick(CLOCK)
        #print speed
        if player.damage_cd != 0:
            count += 1
            player.damage_cd -= 1
            if count % 10 == 0:
                if player.color == player_blue:
                    player.color = light_blue
                else:
                    player.color = player_blue
        else:
            player.color = player_blue
        if timer != 0:
            timer -= 1
        else:
            speed = default_speed
        if player.shot_timer > 0:
            player.shot_timer -= 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_j:
                        for mob in Mobs:
                            mob.takeDmg(1)
                if event.key == K_p:
                    while(True):
                        text = subhead.render("Game Paused (p)", 1, (255,140,0))
                        textpos = text.get_rect()
                        textpos.center = camera.center
                        textpos.y -= 40
                        window.blit(text,textpos)
                        text = subhead2.render("Press Q to quit", 1, (255,140,0))
                        textpos = text.get_rect()
                        textpos.center = camera.center
                        textpos.y += 40
                        window.blit(text,textpos)
                        pygame.display.update()
                        event = pygame.event.wait()
                        if event.type == QUIT:
                            terminate()
                        elif event.type == KEYDOWN:
                            if event.key == K_p:
                                break
                            if event.key == K_q:
                                terminate()

        ### player movement ###
        if(pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]):
            if(moveRect(player,0,-speed,*walls)):
                #print "Not Colliding!"
                #moveRect(player,0,+speed)
                camera.center = player.center
                """for obj in not_player:
                    moveRect(obj,0,speed)"""
        if(pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]):
            if(moveRect(player,0,speed,*walls)):
                #print "Not Colliding!"
                #moveRect(player,0,-speed)
                camera.center = player.center
                """for obj in not_player:
                    moveRect(obj,0,-speed)"""
        if(pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]):
            if(moveRect(player,-speed,0,*walls)):
                #print "Not Colliding!"
                #moveRect(player,speed,0)
                camera.center = player.center
                """for obj in not_player:
                    moveRect(obj,speed,0)"""
        if(pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]):
            if(moveRect(player,speed,0,*walls)):
                #print "Not Colliding!"
                #moveRect(player,-speed,0)
                camera.center = player.center
                """for obj in not_player:
                    moveRect(obj,-speed,0)"""

        ### player aiming and firing ###
        if True in pygame.mouse.get_pressed() and player.shot_timer <= 0:
            player.shot_timer = 1/player.fire_rate
            mouse_angle = get_angle(player.center, pygame.mouse.get_pos())
            fire_shot((player.centerx - 5, player.centery - 5), (10, 10),
                      mouse_angle, default_bullet_speed, 1, 0, player.shot_spread,
                      default_spread_angle, "player")

        ### goal generation ###
        if board.goal == None:
            if len(Mobs) == 0:
                board.goal = EndGoal(spawn,(40,40))
        if board.goal != None:
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

                ##### mob movement && damage###
        for mob in Mobs:
                if(mob.flash != 0):
                    mob.color = (128,40,40)
                    mob.flash -= 1
                else:
                    mob.color = dark_red
                mob.move()
                if player.colliderect(mob) and player.damage_cd == 0:
                    player.health -= 1
                    player.color = light_blue
                    player.damage_cd = 1 * 60
        # bullet movement and damage (currently only checks for "player" owner)
        for bullet in bullets:
            bullet.move()
            # damage for bullets not owned by the player
            if bullet.owner != "player":
                if player.colliderect(bullet) and player.damage_cd == 0:
                    player.health -= 1
                    player.color = light_blue
                    player.damage_cd = 1 * 60
                    bullet.remove()
            # damage for bullets owned by the player
            else:
                for mob in Mobs:
                    if mob.colliderect(bullet):
                        mob.takeDmg(bullet.power)
                        bullet.remove()
                        break

        for event in BigSpeed: #Event Executions go here !!!Read instructions before adding event located near the event class block!!!
            if player.colliderect(event):
                    #print "You should get BIGSPEED"
                    speed = default_speed+2
                    timer = 2 * CLOCK
        for event in SmallSpeed:
            if player.colliderect(event):
                    #print "You should get tinehsped"
                    speed = default_speed+1
                    timer = 1 * CLOCK
                    
        for powerup in Buck: #PowerUp Executions go here
            if player.colliderect(powerup):
                player.shot_spread += 1
                powerup.remove()
        for powerup in Fire:
            if player.colliderect(powerup):
                player.fire_rate += .5/default_shot_delay
                powerup.remove()
                
    #Painting of scene:
        window.fill(bg_gray)
        for obj in not_player:
            obj.x -= camera.x
            obj.y -= camera.y
            if type(obj) is Bullet:
                obj.realx -= camera.x
                obj.realy -= camera.y
            pygame.draw.rect(window, obj.color, obj)


        player.x -= camera.x
        player.y -= camera.y
        camera.center = player.center
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
        text = subhead.render(str(player.health), 1, red)
        textpos = text.get_rect()
        textpos.topleft = camera.topleft
        window.blit(text,textpos)

        #scene reversion
        for obj in not_player:
            obj.x += camera.x
            obj.y += camera.y
            if type(obj) is Bullet:
                obj.realx += camera.x
                obj.realy += camera.y
        player.x += camera.x
        player.y += camera.y
        #What's better, .update() or .flip()?
        pygame.display.flip()

        if player.health == 0:
            board.wash_board()
            break
    
if __name__ == "__main__":
    pygame.init()
    title = pygame.image.load("TitleScreen.png")
    menu_value = 0
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w or event.key == K_UP:
                    if(menu_value > 0):
                        menu_value -= 1
                if event.key == K_s or event.key == K_DOWN:
                    if(menu_value < 1):
                        menu_value += 1
                if event.key == K_RETURN:
                    if(menu_value == 1):
                        terminate()
                    if(menu_value == 0):
                        flag = False
        c0 = cement
        c1 = cement
        if(menu_value == 0):
            c0 = player_blue
        if(menu_value == 1):
            c1 = player_blue
        window.blit(title, (0,0))
        text = subhead.render("Play Game", 1, c0)
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y += 20
        window.blit(text,textpos)
        text = subhead.render("Quit", 1, c1)
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y += 130
        window.blit(text,textpos)
        pygame.display.update()
    while True:
        game_loop()
        text = header.render(" You have died!", 1, purple)
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y = textpos.y - 100
        window.blit(text,textpos)
        text = subhead.render("Press R to try again.", 1, (255,140,0))
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y = textpos.y + 50
        window.blit(text,textpos)
        pygame.display.update()

        pygame.event.clear()
        while(True):
            event = pygame.event.wait()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and event.key == K_r:
                break


#If the player is colliding with a zone, outlined by rectangles
#Then the player should be effected by the bounds set by the particular rectangle
    #What if there is an "active room" concept, you pass the active room in as arguments for movement walls
#You should have open and closed boundaries. An array of 4 bools representing cardinal directions
#How would you open up zones to pass through? 
