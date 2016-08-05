import pygame
import math
import time
import sys
from pygame.locals import *
from random import choice, randint

#Initialize pygame
pygame.init()

#Constant Definition:
    #Positions:
START_X = 300#starting position if camera skewed
START_Y = 280
DEFAULT_SPEED = 4
DEFAULT_HP = 3
DEFAULT_BULLET_SPEED = 15
DEFAULT_SHOT_DELAY = 40.0
DEFAULT_SPREAD_ANGLE = 0.1
FPS = 60
spawn = (0, 0)

#camera start
CAMERA_X = 0
CAMERA_Y = 0

WIN_X = 1200
WIN_Y = 900
    #Colors:
RED = (230, 50, 50)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
CHOCOLATE = (139, 69, 19)
CEMENT = (205, 197, 191)
LIGHT_GREEN = (113, 198, 113)
BLUE = (92, 172, 239)
DARK_GRAY = (71, 71, 71)
PLAYER_BLUE = (100, 200, 250)
BG_GRAY = (19, 19, 19)
ORANGE = (255, 140, 0)
DARK_ORANGE = (139, 69, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (200, 200, 255)
BLOOD_RED = (70, 7, 7)
OBSIDIAN = (6, 6, 6)
GOLD = (205, 173, 0)
LIGHT_YELLOW = (238, 238, 180)
DARK_RED = (127, 0, 0)
MOB_BOSS_COLOR = (130, 10, 10)
MOB1_COLOR = (190, 0, 10)
MOB2_COLOR = (130, 0, 30)
MOB3_COLOR = (128, 0, 50)
MOB4_COLOR = (127, 0, 70)
MOB5_COLOR = (127, 0, 110)
# For more colors see this resource:
# http://cloford.com/resources/colours/500col.htm or use paint

#images:
FLAG_I = pygame.image.load("Flag.png")
SMALL_I = pygame.image.load("SmallS.png")
LARGE_I = pygame.image.load("LargeS.png")
BUCK_I = pygame.image.load("BuckShot.png")
RATE_I = pygame.image.load("FireRate.png")
HP_I = pygame.image.load("HP.png")

#font initialization:
TITLE_FONT = pygame.font.Font(None, 288)
SUBTITLE_FONT = pygame.font.Font(None, 220)
HEADER_FONT = pygame.font.Font(None, 134)
SUBHEAD_FONT = pygame.font.Font(None, 72)
SUBHEAD2_FONT = pygame.font.Font(None, 58)
BODY_FONT = pygame.font.Font(None, 36)

#Array Initialization
mobs = []
bullets = []
walls = []
not_player = []
small_speed = []
big_speed = []
mob_gate = []
fire = []
health_block = []
buck = []
potential_end = []

clock = pygame.time.Clock()

window = pygame.display.set_mode([WIN_X, WIN_Y])
camera = Rect((CAMERA_X, CAMERA_Y), (WIN_X, WIN_Y))

#End Constand Definition
#Begin Function Definition


def fire_shot((x, y), (w, h), center_angle, speed, power, bounce,
              spread_count, spread_angle, owner, color_=None):
    """Create one or more bullets with the given properties.  Use this
    instead of the Bullet constructor.
    """
    # Spread calculation expects that spread_count is at least 1.
    if spread_count < 1:
        spread_count = 1

    # Calculate the angles for all bullets in the spread.
    bullet_angles = [center_angle
                     - ((spread_count - 1) * spread_angle / 2.0)
                     + (spread_angle * bullet_number)
                     for bullet_number in range(spread_count)]

    # Create all bullets.
    for angle in bullet_angles:
        Bullet((x, y), (w, h),
               speed * math.cos(angle), speed * math.sin(angle),
               power, bounce, owner, color_)

def get_angle((origin_x, origin_y), (target_x, target_y)):
    """Return the angle of the vector from an origin position to a
    target position.
    """
    x_distance = target_x - origin_x
    y_distance = target_y - origin_y
    angle = math.atan2(y_distance, x_distance)
    return angle

def move_rect(rec, x_distance, y_distance, *args):
    if x_distance != 0:
        ret = move_rect_single_axis(rec, x_distance, 0, *args)
        return ret
    if y_distance != 0:
        ret = move_rect_single_axis(rec, 0, y_distance, *args)
        return ret

def move_rect_single_axis(rec, x_distance, y_distance, *args):
    if type(rec) is Bullet:
        rec.real_x += x_distance
        rec.real_y += y_distance
        rec.x = int(round(rec.real_x))
        rec.y = int(round(rec.real_y))
    else:
        rec.x += x_distance
        rec.y += y_distance
    for arg in args:
        if rec.colliderect(arg):
            # Collision detected
            if x_distance > 0:
                # Left bump
                rec.right = arg.left
                if type(rec) is Bullet:
                    rec.real_x = rec.x
            if x_distance < 0:
                # Right bump
                rec.left = arg.right
                if type(rec) is Bullet:
                    rec.real_x = rec.x
            if y_distance > 0:
                # Top bump
                rec.bottom = arg.top
                if type(rec) is Bullet:
                    rec.real_y = rec.y
            if y_distance < 0:
                # Bottom bump
                rec.top = arg.bottom
                if type(rec) is Bullet:
                    rec.real_y = rec.y
            return False
    return True

def terminate():
    pygame.quit()
    sys.exit()

#End Function Definition
#Begin Class Definition

class Wall(Rect):
    def __init__(self, (x, y)=(0, 0), (w, h)=(0, 0), rec=None, *args, **kwargs):
        if rec == None:
            Rect.__init__(self, (x, y), (w, h), *args, **kwargs)
            walls.append(self)
            not_player.append(self)
            self.color = CEMENT
        else:
            self.x = rec.x
            self.y = rec.y
            self.w = rec.w
            self.h = rec.h
            not_player.append(self)
            self.color = CEMENT

    def remove(self):
        not_player.remove(self)
        walls.remove(self)

class Env(Rect):
    def __init__(self, (x, y)=(0, 0), (w, h)=(0, 0), rec=None, *args, **kwargs):
        if rec == None:
            Rect.__init__(self, (x, y), (w, h), *args, **kwargs)
            not_player.append(self)
            self.color = DARK_GRAY
        else:
            self.x = rec.x
            self.y = rec.y
            self.w = rec.w
            self.h = rec.h
            not_player.append(self)
            self.color = DARK_GRAY

    def remove(self):
        not_player.remove(self)

class MobGate(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        mob_gate.append(self)
        self.color = GOLD

    def remove(self):
        not_player.remove(self)
        mob_gate.remove(self)

class Player(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        self.color = PLAYER_BLUE
        self.health = DEFAULT_HP
        self.hpboost = 0
        self.damage_cd = 0
        self.shot_timer = 0
        self.shot_spread = 1
        self.fire_rate = 1/DEFAULT_SHOT_DELAY

class Mob(Rect):
    def __init__(self, mob_type=1, (x, y)=(0, 0), (w, h)=(0, 0), speed_scale=1,
                 *args, **kwargs):
        Rect.__init__(self, (x, y), (w, h), *args, **kwargs)
        not_player.append(self)
        mobs.append(self)
        self.type = mob_type
        self.direction = [randint(1, 4), 0]
        self.speed = DEFAULT_SPEED * .5 * speed_scale
        self.health = 5
        self.flash = 0
        self.shot_timer = randint(0, 15)
        self.shot_spread = 1
        self.fire_rate = 1/DEFAULT_SHOT_DELAY
        self.fire_angle = randint(0, 359)* 1.0
        if mob_type == 0: # Boss type
            self.real_color = MOB_BOSS_COLOR
        if mob_type == 1:
            self.real_color = MOB1_COLOR
        if mob_type == 2:
            self.real_color = MOB2_COLOR
        if mob_type == 3:
            self.real_color = MOB3_COLOR
        self.color = self.real_color

    def remove(self):
        not_player.remove(self)
        mobs.remove(self)

    def move(self):
        collideable = []
        for wall in walls:
            collideable.append(wall)
        for gate in mob_gate:
            collideable.append(gate)
        if self.direction[0] == 1 or self.direction[1] == 1: # Moving up
            if not move_rect(self, 0, -self.speed, *collideable):
                self.direction[0] = 2
                self.direction[1] = choice([2, 3, 4])
        if self.direction[0] == 2 or self.direction[1] == 2: # Moving down
            if not move_rect(self, 0, self.speed, *collideable):
                self.direction[0] = 1
                self.direction[1] = choice([1, 3, 4])
        if self.direction[0] == 3 or self.direction[1] == 3: # Moving left
            if not move_rect(self, -self.speed, 0, *collideable):
                self.direction[0] = 4
                self.direction[1] = choice([1, 2, 4])
        if self.direction[0] == 4 or self.direction[1] == 4: # Moving right
            if not move_rect(self, self.speed, 0, *collideable):
                self.direction[0] = 3
                self.direction[1] = choice([1, 2, 3])

    def take_damage(self, dmg=1):
        print self.health
        self.health -= dmg
        print self.health
        self.flash = 5
        if self.health <= 0:
            get_powerup(self.x, self.y)
            self.remove()
            print "killed."

class MobBoss(Mob):
    def __init__(self, (x, y)=(0, 0), (w, h)=(0, 0), speed_scale=1,
                 *args, **kwargs):
        Mob.__init__(self, 0, (x, y), (w, h), speed_scale, *args, **kwargs)
        self.health = 100
        self.boss_timer = 0.0
        self.speed = DEFAULT_SPEED * .5
        self.at_half_health = False
        self.at_quarter_health = False

    def take_damage(self, dmg=1):
        global spawn
        self.health -= dmg
        self.flash = 5
        if self.at_half_health == False and self.health <= 50:
            self.at_half_health = True
            self.w = self.w/2
            self.h = self.h/2
            newmob = MobBoss((self.x, self.y), (self.w, self.h))
            self.speed *= 2
            newmob.speed *= 2
            newmob.health = 50
            newmob.at_half_health = True
        if self.at_quarter_health == False and self.health <= 25:
            self.at_quarter_health = True
            self.w = self.w/2
            self.h = self.h/2
            self.speed *= 1.5
            newmob2 = MobBoss((self.x, self.y), (self.w, self.h))
            newmob2.speed *= 3
            newmob2.health = 25
            newmob2.at_half_health = True
            newmob2.at_quarter_health = True
        if self.health <= 0:
            spawn = (self.x, self.y)
            self.remove()

class Bullet(Rect):
    def __init__(self, (x, y)=(0, 0), (w, h)=(0, 0), x_speed=0, y_speed=15,
                 power=1, bounce=0, owner="player", color_=None,
                 *args, **kwargs):
        Rect.__init__(self, (x, y), (w, h), *args, **kwargs)

        not_player.append(self)
        bullets.append(self)

        self.real_x = self.x
        self.real_y = self.y
        self.x_speed = x_speed
        self.y_speed = y_speed
        if power < 1:
            self.power = 1
        else:
            self.power = power
        self.bounce = bounce # Number of times bullet can bounce off walls.
        self.owner = owner # Could be things like "player", "mob", "trap".
        if color_ == None:
            if owner == "player":
                self.color = BLUE
            else:
                self.color = ORANGE
        else:
            self.color = color_

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
        # Horizontal movement
        if self.x_speed != 0 and not move_rect(self, self.x_speed, 0,
                                               *collideable):
            if self.bounce == 0:
                self.remove()
            else:
                self.x_speed *= -1
                if self.bounce > 0:
                    self.bounce -= 1
        # Vertical movement
        if self.y_speed != 0 and not move_rect(self, 0, self.y_speed,
                                               *collideable):
            if self.bounce == 0:
                self.remove()
            else:
                self.y_speed *= -1
                if self.bounce > 0:
                    self.bounce -= 1

class EndGoal(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        self.color = WHITE

    def remove(self):
        not_player.remove(self)

#Event Class Blocks
# To add an event there are 4 components.
#
# First you must make a new event array. Simple, just declare it in the
# array block.
#
# Second you must create a new event class. These are all pretty cookie-
# cutter, just follow the models below and append to your appropriate
# array.
#
# Third you must create a new event in the generation block. This is
# creating the hitbox and aligning it to the room center. Follow the
# existing examples.
#
# Finally you must create the rule for those events. This is located in
# the main loop. Emplement by adding a for loop over your array to check
# collisions with Player.

class SpeedS(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        small_speed.append(self)
        self.color = LIGHT_GREEN

    def remove(self):
        not_player.remove(self)
        small_speed.remove(self)

class SpeedB(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        big_speed.append(self)
        self.color = PURPLE

    def remove(self):
        not_player.remove(self)
        big_speed.remove(self)

#End Event Class Blocks

#Power Up Blocks
def get_powerup(x, y):
    num_ups = 3
    powerup_choice = randint(1, num_ups)
    if powerup_choice == 1:
        BuckShotUP((x, y), (40, 40))
    if powerup_choice == 2:
        FireRateUP((x, y), (40, 40))
    if powerup_choice == 3:
        Hp((x, y), (40, 40))

class BuckShotUP(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        buck.append(self)
        self.color = ORANGE

    def remove(self):
        not_player.remove(self)
        buck.remove(self)

class FireRateUP(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        fire.append(self)
        self.color = LIGHT_YELLOW

    def remove(self):
        not_player.remove(self)
        fire.remove(self)

class Hp(Rect):
    def __init__(self, *args, **kwargs):
        Rect.__init__(self, *args, **kwargs)
        not_player.append(self)
        health_block.append(self)
        self.color = WHITE

    def remove(self):
        not_player.remove(self)
        health_block.remove(self)

#End Power Up Blocks

class Room(object):
    """Class Room is a Highly Customizable Template class which can
    create various types of rooms. gap represents a fraction of the wall
    that is the door. Door is always centered.
    """
    def __init__(self, position=(0, 0), size=(WIN_X, WIN_Y),
                 doors=(False, False, False, False), floor_color=DARK_GRAY,
                 wall_color=CEMENT, wall_thickness=20, gap=.32, level=0):
        chunk = (1-gap)/2 # Size of a piece of the wall on a gap side
        self.chunk = chunk
        self.level = level
        if randint(0, 3) == 0:
            s = 0
        else:
            s = 1
        self.level = (randint(0, 2) + level) * s
        self.checked = False
        (self.x, self.y) = position
        (self.w, self.h) = size
        (self.north, self.south, self.east, self.west) = doors
        self.floor_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.wall_color = wall_color
        self.Floors = []
        self.Floors.append(Env((self.x, self.y), (self.w, self.h)))
        self.walls = []
        self.mobs = []
        if self.north:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y-wall_thickness),
                (self.w * chunk+wall_thickness, wall_thickness)))
            self.walls.append(Wall(
                (self.x+(chunk+gap)*self.w, self.y-wall_thickness),
                (self.w * chunk+wall_thickness, wall_thickness)))
            self.Floors.append(MobGate(
                (self.x+chunk*self.w - 1, self.y-wall_thickness),
                (self.w*gap + 1, wall_thickness)))
        else:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y-wall_thickness),
                (self.w+2*wall_thickness, wall_thickness)))
        if self.west:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y-wall_thickness),
                (wall_thickness, self.h * chunk+wall_thickness)))
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y+(chunk+gap)*self.h),
                (wall_thickness, self.h * chunk+wall_thickness)))
            self.Floors.append(MobGate(
                (self.x-wall_thickness, self.y+chunk*self.h-1),
                (wall_thickness, self.h * gap + 1)))
        else:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y-wall_thickness),
                (wall_thickness, self.h+2*wall_thickness)))
        if self.south:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y+self.h),
                (self.w * chunk+wall_thickness, wall_thickness)))
            self.walls.append(Wall(
                (self.x+(chunk+gap)*self.w, self.y+self.h),
                (self.w * chunk+wall_thickness, wall_thickness)))
            self.Floors.append(MobGate(
                (self.x+chunk*self.w, self.y+self.h),
                (self.w * gap, wall_thickness)))
        else:
            self.walls.append(Wall(
                (self.x-wall_thickness, self.y+self.h),
                (self.w+2*wall_thickness, wall_thickness)))
        if self.east:
            self.walls.append(Wall(
                (self.x+self.w, self.y-wall_thickness),
                (wall_thickness, self.h * chunk+wall_thickness)))
            self.walls.append(Wall(
                (self.x+self.w, self.y+(chunk+gap)*self.h),
                (wall_thickness, self.h * chunk+wall_thickness)))
            self.Floors.append(MobGate(
                (self.x+self.w, self.y+chunk*self.h),
                (wall_thickness, self.h * gap)))
        else:
            self.walls.append(Wall(
                (self.x+self.w, self.y-wall_thickness),
                (wall_thickness, self.h+2*wall_thickness)))
        for wall in self.walls:
            wall.color = wall_color
        for floor in self.Floors:
            if type(floor) != MobGate:
                floor.color = floor_color
        self.center = self.Floors[0].center

    def set_floor(self, floor_color):
        self.floor_color = floor_color
        for floor in self.Floors:
            if type(floor) != MobGate:
                floor.color = floor_color

    def set_wall(self, wall_color):
        self.wall_color = wall_color
        for wall in self.walls:
            wall.color = wall_color

    def remove(self):
        for floor in self.Floors:
            floor.remove()
        for wall in self.walls:
            wall.remove()

    def get_cover(self):
        covers = 5
        cover_model = randint(0, covers)
        if cover_model == 0:
            return
        elif cover_model == 1: # One box off-center
            randx = choice([.1, .6])
            randy = choice([.1, .6])
            self.walls.append(Wall(
                (self.x+self.w*randx, self.y+self.h*randy),
                (self.w*.3, self.h*.3)))
        elif cover_model == 2: # Three box center
            self.walls.append(Wall(
                (self.x + .1 * self.w, self.y + .1 * self.h),
                (.3*self.w, .3*self.h)))
            self.walls.append(Wall(
                (self.x + .6 * self.w, self.y + .1 * self.h),
                (.3*self.w, .3*self.h)))
            self.walls.append(Wall(
                (self.x + .35 * self.w, self.y + .6 * self.h),
                (.3*self.w, .3*self.h)))
        elif cover_model == 3: # Four corner boxes
            self.walls.append(Wall(
                (self.x, self.y),
                (self.w*self.chunk*.5, self.h*self.chunk*.5)))
            self.walls.append(Wall(
                (self.x, self.y),
                (self.w*self.chunk*.5, self.h*self.chunk*.5)))
            self.walls[len(self.walls)-1].topright = self.Floors[0].topright
            self.walls.append(Wall(
                (self.x, self.y),
                (self.w*self.chunk*.5, self.h*self.chunk*.5)))
            self.walls[len(self.walls)-1].bottomright \
                = self.Floors[0].bottomright
            self.walls.append(Wall(
                (self.x, self.y),
                (self.w*self.chunk*.5, self.h*self.chunk*.5)))
            self.walls[len(self.walls)-1].bottomleft = self.Floors[0].bottomleft
        elif cover_model == 4: # 4 bar room
            self.walls.append(Wall(
                (self.x+self.w*.3, self.y+self.h*.35),
                (self.w*.7, self.h*.03)))
            self.walls.append(Wall(
                (self.x+self.w*.0, self.y+self.h*.15),
                (self.w*.7, self.h*.03)))
            self.walls.append(Wall(
                (self.x+self.w*.0, self.y+self.h*.65),
                (self.w*.7, self.h*.03)))
            self.walls.append(Wall(
                (self.x+self.w*.3, self.y+self.h*.85),
                (self.w*.7, self.h*.03)))
        elif cover_model == 5: # Two bars, two side boxes
            self.walls.append(Wall(
                (self.x+self.w*.25, self.y+self.h*.24),
                (self.w*.5, self.h*.05)))
            self.walls.append(Wall(
                (self.x+self.w*.2, self.y+self.h*.45),
                (self.w*.1, self.h*.1)))
            self.walls.append(Wall(
                (self.x+self.w*.7, self.y+self.h*.45),
                (self.w*.1, self.h*.1)))
            self.walls.append(Wall(
                (self.x+self.w*.25, self.y+self.h*.74),
                (self.w*.5, self.h*.05)))

    def get_boss_cover(self):
        covers = 4
        cover_model = randint(1, covers)
        cover_model = 2
        if cover_model == 0:
            return
        elif cover_model == 1: # One box center
            self.walls.append(Wall(
                (self.x+self.w*.4, self.y+self.h*.4),
                (self.w*.2, self.h*.2)))
        elif cover_model == 2: # Half room
            self.walls.append(Wall(
                (self.x+self.w*.49, self.y + self.h*.35),
                (self.w*.02, self.h*.3)))
            SpeedS((self.x+self.w/4-30, self.y+self.h/2-30), (60, 60))
            SpeedB((self.x+3*self.w/4-50, self.y+self.h/2-50), (100, 100))
        elif cover_model == 3: # Four corner boxes
            self.walls.append(Wall((self.x, self.y), (100, 100)))
            self.walls.append(Wall((self.x, self.y), (100, 100)))
            self.walls[len(self.walls)-1].topright = self.Floors[0].topright
            self.walls.append(Wall((self.x, self.y), (100, 100)))
            self.walls[len(self.walls)-1].bottomright \
                = self.Floors[0].bottomright
            self.walls.append(Wall((self.x, self.y), (100, 100)))
            self.walls[len(self.walls)-1].bottomleft = self.Floors[0].bottomleft
        elif cover_model == 4: # Cross room
            self.walls.append(Wall(
                (self.x+self.w*.49, self.y + self.h*.35),
                (self.w*.02, self.h*.3)))
            self.walls.append(Wall(
                (self.x+self.w*.35, self.y + self.h*.49),
                (self.w*.3, self.h*.02)))

    def get_mobs(self):
        num_mobs = 3
        if self.level < 3:
            mob_type = (randint(0, self.level)+1)
        else:
            mob_type = randint(1, num_mobs)
        ran = randint(0, 15)
        self.mobs.append(Mob(mob_type, (self.x+227, self.y+227),
                             (30 + ran, 30 + ran), 1 + self.level/5))

    def get_boss(self, level):
        self.mobs.append(MobBoss((0, 0), (200, 200)))
        self.mobs[0].midright = self.Floors[0].midright


class Board(object):
    def __init__(self, rows, collumns, start_x=0, start_y=0,
                 room_w=500, room_h=500, thick=20):
        self.rows = rows
        self.collumns = collumns
        self.start_x = start_x
        self.start_y = start_y
        self.room_w = room_w
        self.room_h = room_h
        self.thick = thick
        self.goal = None
        self.level = 0
        self.rooms = []
        self.generate()

    def generate(self):
        global potential_end
        print "Generating new board"
        if self.level != 0 and self.level%5 == 4:
            self.generate_boss()
            return
        self.collumns += self.level/2
        self.rows += self.level/2
        rooms = []
        row = []
        events = []
        north, south, east, west = False, False, False, False
        room_layout = (north, south, east, west)
        print "Making rooms"
        for i in range(0, self.collumns):
            for j in range(0, self.rows):
                # Randomization
                seed = randint(0, 2)
                if seed == 0:
                    east = True
                    south = True
                elif seed == 1:
                    east = False
                    south = True
                elif seed == 2:
                    east = True
                    south = False
                # Hallway anomaly
                if self.collumns == 1:
                    north = True
                    south = True
                if self.rows == 1:
                    east = True
                    west = True
                # Sets the mandatory border walls
                if i == 0:
                    west = False
                if j == 0:
                    north = False
                if i == self.collumns - 1:
                    east = False
                    # The following commented-out caveats are optional.
                    # They basically create an alley around the
                    # bottom-right to navigate around.

                    # if(j != self.rows - 1):
                    #     south = True
                if j == self.rows - 1:
                    south = False
                    # if(i != self.rows - 1):
                    #     east = True

                # Sets the dependent walls
                if i - 1 >= 0:
                    west = rooms[i-1][j].east
                if j - 1 >= 0:
                    north = row[j-1].south

                # Ensures every room has an entrance
                if j != 0:
                    if north == False and south == False and east == False \
                            and west == False:
                        east = True
                if i != self.collumns - 1:
                    if north == False and south == False and east == False \
                            and west == False:
                        south = True
                # Theory: No room will be unaccessable with this code.
                room_layout = (north, south, east, west)
                row.append(Room(
                    ((self.start_x+(self.thick+self.room_w)*i),
                     (self.start_y+(self.thick+self.room_h)*j)),
                    (self.room_w, self.room_h), room_layout,
                    floor_color=(60, 60, 60), wall_thickness=self.thick,
                    level=self.level))

            rooms.append(row)
            row = []
        print "Checking rooms"
        # Checker to get all passable terrain
        self.rooms = rooms
        potential_end = []
        if self.checker(0, 0) != 0:
            return
        # Pick a room to set the endpoint in
        end_point = choice(potential_end)
        # Creates the end point
        self.goal = EndGoal((0, 0), (40, 40))
        print end_point # Debugging location of endpoint
        # Aligns end point to middle of room
        self.goal.center = rooms[end_point[0]][end_point[1]].Floors[0].center
        # Sets levels to prevent unkindly spawns of cover
        rooms[end_point[0]][end_point[1]].level = 0
        rooms[0][0].level = 0
        # Cover generation is here
        for row in rooms:
            for room in row:
                if room.level > 0 and room.checked == True:
                    room.get_cover()
                    print "Mob got."
                    room.get_mobs()

        print "Generating Events."
        # Event generation goes here ***Read instructions before adding
        # an event located near the event class block***
        for row in rooms:
            for room in row:
                if room.level == 0 and room.checked == True \
                        and room != rooms[end_point[0]][end_point[1]]:
                    if randint(0, 9) == 9:
                        # If you add a new big event, increment number_big
                        number_big = 1
                        x = randint(1, number_big)
                        if x == 1:
                            events.append(SpeedB((0, 0), (100, 100)))
                            events[len(events)-1].center = room.center
                        # Add new big events here as elif blocks
                    elif randint(4, 4) == 4:
                        # If you add a new small event, increment number_small
                        number_small = 1
                        x = randint(1, number_small)
                        if x == 1:
                            events.append(SpeedS((0, 0), (50, 50)))
                            events[len(events)-1].center = room.center
                        # Add new small events here as elif blocks
        print "Removing rooms"
        # Unaccessable room removal:
        for row in rooms:
            for room in row:
                if room.checked == False:
                    room.remove()
        self.rooms = rooms
        print "Generation complete"

    def wash_board(self):
        del fire[:]
        del buck[:]
        del small_speed[:]
        del big_speed[:]
        del walls[:]
        del not_player[:]
        del self.rooms[:]
        del mobs[:]
        del bullets[:]
        del mob_gate[:]

    def remake(self, rows, collumns, start_x=0, start_y=0,
               room_w=500, room_h=500, thick=20, level_up=0):
        self.rows = rows
        self.collumns = collumns
        self.start_x = start_x
        self.start_y = start_y
        self.room_w = room_w
        self.room_h = room_h
        self.thick = thick
        self.goal = None
        self.generate()
        self.level += level_up

    def checker(self, x, y, flag=False):
        self.rooms[x][y].checked = True
        flag2 = True
        if self.rooms[x][y].north:
            flag = True
            print "N" + str(x) + str(y)
            if self.rooms[x][y-1].checked == False:
                flag2 = False
                self.checker(x, y-1, True)
        if self.rooms[x][y].south:
            flag = True
            print "S" + str(x) + str(y)
            if self.rooms[x][y+1].checked == False:
                flag2 = False
                self.checker(x, y+1, True)
        if self.rooms[x][y].east:
            flag = True
            print "E" + str(x) + str(y)
            if self.rooms[x+1][y].checked == False:
                flag2 = False
                self.checker(x+1, y, True)
        if self.rooms[x][y].west:
            flag = True
            print "W" + str(x) + str(y)
            if self.rooms[x-1][y].checked == False:
                flag2 = False
                self.checker(x-1, y, True)
        if not flag:
            self.wash_board()
            rows = randint(1, 4)
            collumns = randint(1, 4)
            self.remake(rows, collumns, level_up=0)
            return -1
        if flag2:
            potential_end.append((x, y))
        return 0

    def generate_boss(self):
        self.rooms = []
        row = []
        row.append(Room(
            (self.start_x, self.start_y), (self.room_w*1.5, self.room_h*1),
            (False, False, False, False), floor_color=BLOOD_RED,
            wall_color=OBSIDIAN, wall_thickness=self.thick*3, level=0))
        self.rooms.append(row)
        self.rooms[0][0].get_boss_cover()
        self.rooms[0][0].get_boss(self.level)
#End Class Definition

def game_loop():
    # Array initialization
    speed = DEFAULT_SPEED
    timer = 0
    # Rectangles below -- NOTE!!!! Order is currently IMPORTANT, as they
    # are drawn in order declared.
    player = Player((START_X, START_Y), (40, 40))
    # Room generation:
    rows = randint(1, 4)
    collumns = randint(1, 4)
    board = Board(rows, collumns)
    # Centers camera at start
    camera.center = player.center # Comment out to allow skewed camera
    count = 0


    while True:
        clock.tick(FPS)
        if player.damage_cd != 0:
            count += 1
            player.damage_cd -= 1
            if count % 10 == 0:
                if player.color == PLAYER_BLUE:
                    player.color = LIGHT_BLUE
                else:
                    player.color = PLAYER_BLUE
        else:
            player.color = PLAYER_BLUE
        if timer != 0:
            timer -= 1
        else:
            speed = DEFAULT_SPEED
        if player.shot_timer > 0:
            player.shot_timer -= 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_j:
                    for mob in mobs:
                        mob.take_damage(1)
                if event.key == K_p:
                    while True:
                        text = SUBHEAD_FONT.render("Game Paused (p)", 1,
                                                   (255, 140, 0))
                        textpos = text.get_rect()
                        textpos.center = camera.center
                        textpos.y -= 40
                        window.blit(text, textpos)
                        text = SUBHEAD2_FONT.render("Press Q to quit", 1,
                                                    (255, 140, 0))
                        textpos = text.get_rect()
                        textpos.center = camera.center
                        textpos.y += 40
                        window.blit(text, textpos)
                        pygame.display.update()
                        event = pygame.event.wait()
                        if event.type == QUIT:
                            terminate()
                        elif event.type == KEYDOWN:
                            if event.key == K_p:
                                break
                            if event.key == K_q:
                                terminate()

        # Player movement
        if pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]:
            if move_rect(player, 0, -speed, *walls):
                camera.center = player.center
        if pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]:
            if move_rect(player, 0, speed, *walls):
                camera.center = player.center
        if pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]:
            if move_rect(player, -speed, 0, *walls):
                camera.center = player.center
        if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
            if move_rect(player, speed, 0, *walls):
                camera.center = player.center

        # Player aiming and firing
        if True in pygame.mouse.get_pressed() and player.shot_timer <= 0:
            player.shot_timer = 1/player.fire_rate
            mouse_angle = get_angle(player.center, pygame.mouse.get_pos())
            fire_shot((player.centerx - 5, player.centery - 5), (10, 10),
                      mouse_angle, DEFAULT_BULLET_SPEED, 1, 0,
                      player.shot_spread, DEFAULT_SPREAD_ANGLE, "player")

        # Goal generation
        if board.goal == None:
            if len(mobs) == 0:
                board.goal = EndGoal(spawn, (40, 40))
        if board.goal != None:
            if player.colliderect(board.goal):
                # Create next board
                board.wash_board()
                rows = randint(1, 3)
                collumns = randint(1, 3)
                board.remake(rows, collumns, level_up=1)
                player.x = START_X
                player.y = START_Y
                camera.center = player.center

                ##### mob movement && damage && such###
        for mob in mobs:
            if mob.flash != 0:
                mob.color = (128, 40, 40)
                mob.flash -= 1
            else:
                mob.color = mob.real_color

            if mob.type == 1 or mob.type == 3:
                mob.move()
            if player.colliderect(mob) and player.damage_cd == 0:
                player.health -= 1
                player.color = LIGHT_BLUE
                player.damage_cd = 1 * 60
            if mob.type == 2:
                mob.fire_angle += .05
                if mob.fire_angle >= 2 * math.pi:
                    mob.fire_angle = 0
                fire_shot((mob.centerx - 5, mob.centery - 5), (10, 10),
                          mob.fire_angle, DEFAULT_BULLET_SPEED, 1, 0,
                          mob.shot_spread, DEFAULT_SPREAD_ANGLE, "mob")
            if mob.type == 3:
                if mob.shot_timer > 0:
                    mob.shot_timer -= .1
                mob.fire_angle = get_angle((mob.centerx, mob.centery),
                                           (player.centerx, player.centery))
                if mob.shot_timer <= 0:
                    mob.shot_timer = 10
                    fire_shot((mob.centerx- 5, mob.centery - 5), (10, 10),
                              mob.fire_angle, DEFAULT_BULLET_SPEED-6, 1, 2,
                              mob.shot_spread, DEFAULT_SPREAD_ANGLE, "mob")

            if mob.type == 0: # Boss type
                mob.color = mob.real_color
                mob.move()
                mob.boss_timer += .5
                if mob.boss_timer >= 10000000:
                    mob.boss_timer = 0

                if mob.boss_timer %300 == 0: # Ring of death
                    mob.color = (50, 90, 30)
                    for i in range(0, 360, 20):
                        fire_shot((mob.centerx - 5, mob.centery - 5), (10, 10),
                          i, DEFAULT_BULLET_SPEED-12, 1, 0, mob.shot_spread,
                          DEFAULT_SPREAD_ANGLE, "mob")

                if mob.boss_timer %100 == 0: # Bouncing shot
                    mob.color = (80, 00, 90)
                    mob.fire_angle = get_angle((mob.centerx, mob.centery),
                                               (player.centerx, player.centery))
                    fire_shot((mob.centerx- 5, mob.centery - 5), (10, 10),
                              mob.fire_angle, DEFAULT_BULLET_SPEED-10, 1, 5,
                              mob.shot_spread, DEFAULT_SPREAD_ANGLE, "mob")

        # Bullet movement and damage
        for bullet in bullets:
            bullet.move()
            # Damage for bullets not owned by the player
            if bullet.owner != "player":
                if player.colliderect(bullet) and player.damage_cd == 0:
                    player.health -= 1
                    player.color = LIGHT_BLUE
                    player.damage_cd = 1 * 60
                    bullet.remove()
            # Damage for bullets owned by the player
            else:
                for mob in mobs:
                    if mob.colliderect(bullet):
                        mob.take_damage(bullet.power)
                        bullet.remove()
                        break

        # Event executions go here ***Read instructions before adding
        # an event located near the event class block***
        for event in big_speed:
            if player.colliderect(event):
                speed = DEFAULT_SPEED+2
                timer = 2 * FPS
        for event in small_speed:
            if player.colliderect(event):
                speed = DEFAULT_SPEED+1
                timer = 1 * FPS

        # PowerUp executions go here
        for powerup in buck:
            if player.colliderect(powerup):
                player.shot_spread += 1
                powerup.remove()
        for powerup in fire:
            if player.colliderect(powerup):
                player.fire_rate += .25/DEFAULT_SHOT_DELAY
                powerup.remove()
        for powerup in health_block:
            if player.colliderect(powerup):
                player.hpboost += 1
                player.health = player.hpboost + DEFAULT_HP
                powerup.remove()

        # Painting of scene:
        window.fill(BG_GRAY)
        for obj in not_player:
            obj.x -= camera.x
            obj.y -= camera.y
            if type(obj) is Bullet:
                obj.real_x -= camera.x
                obj.real_y -= camera.y
            if obj.colliderect(camera):
                pygame.draw.rect(window, obj.color, obj)
        for event in big_speed:
            model = Rect((0, 0), (40, 40))
            model.center = event.center
            window.blit(LARGE_I, (model.x, model.y))
        for event in small_speed:
            model = Rect((0, 0), (40, 40))
            model.center = event.center
            window.blit(SMALL_I, (model.x, model.y))
        for powerup in buck:
            model = Rect((0, 0), (40, 40))
            model.center = powerup.center
            window.blit(BUCK_I, (model.x, model.y))
        for powerup in fire:
            model = Rect((0, 0), (40, 40))
            model.center = powerup.center
            window.blit(RATE_I, (model.x, model.y))
        for powerup in health_block:
            model = Rect((0, 0), (40, 40))
            model.center = powerup.center
            window.blit(HP_I, (model.x, model.y))
        if board.goal != None:
            window.blit(FLAG_I, (board.goal.x, board.goal.y))
        player.x -= camera.x
        player.y -= camera.y
        camera.center = player.center
        pygame.draw.rect(window, player.color, player)


        # Paint text:
        text = SUBHEAD_FONT.render(str(board.level), 1, CEMENT)
        textpos = text.get_rect()
        textpos.topright = camera.topright
        window.blit(text, textpos)
        text = SUBHEAD_FONT.render(str(player.health), 1, RED)
        textpos = text.get_rect()
        textpos.topleft = camera.topleft
        window.blit(text, textpos)

        # Scene reversion
        for obj in not_player:
            obj.x += camera.x
            obj.y += camera.y
            if type(obj) is Bullet:
                obj.real_x += camera.x
                obj.real_y += camera.y
        player.x += camera.x
        player.y += camera.y
        pygame.display.flip()

        if player.health == 0:
            board.wash_board()
            break

def main():
    pygame.init()
    title = pygame.image.load("TitleScreen.png")
    menu_value = 0
    flag = True
    while flag:
        play_color = CEMENT
        quit_color = CEMENT
        if menu_value == 1:
            play_color = PLAYER_BLUE
        if menu_value == 2:
            quit_color = PLAYER_BLUE
        window.blit(title, (0, 0))
        play_text = SUBHEAD_FONT.render("Play Game", 1, play_color)
        play_rect = play_text.get_rect()
        play_rect.center = camera.center
        play_rect.y += 20
        window.blit(play_text, play_rect)
        quit_text = SUBHEAD_FONT.render("Quit", 1, quit_color)
        quit_rect = quit_text.get_rect()
        quit_rect.center = camera.center
        quit_rect.y += 130
        window.blit(quit_text, quit_rect)
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == QUIT:
            terminate()
        elif event.type == MOUSEMOTION:
            if play_rect.collidepoint(event.pos):
                menu_value = 1
            elif quit_rect.collidepoint(event.pos):
                menu_value = 2
            else:
                menu_value = 0
        elif event.type == MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                flag = False
            elif quit_rect.collidepoint(event.pos):
                terminate()
    while True:
        game_loop()
        text = HEADER_FONT.render(" You have died!", 1, PURPLE)
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y = textpos.y - 100
        window.blit(text, textpos)
        text = SUBHEAD_FONT.render("Press R to try again.", 1, (255, 140, 0))
        textpos = text.get_rect()
        textpos.center = camera.center
        textpos.y = textpos.y + 50
        window.blit(text, textpos)
        pygame.display.update()

        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN and event.key == K_r:
                break

if __name__ == "__main__":
    main()

