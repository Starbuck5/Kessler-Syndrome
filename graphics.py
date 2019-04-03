from pgx import pointsToRect
from game import Rotate
from pgx import rotatePixelArt
from game import Asteroid
from pgx import scaleImage
from pgx import Texthelper
from pgx import loadImage

import pygame
from pygame import gfxdraw
from pygame import Surface

class Images:
    storage = {}
    def add(name, image): #or (ID, dictionary of rotations) 
        Images.storage[name] = image
    def get(name, *args): #arg = rotation value
        if not args:
            return Images.storage[name]
        var = args[0]
        var /= 10
        var = round(var)
        var *= 10
        var = int(var)
        var %= 360
        return Images.storage[name][var]

#must be called after scaling is fully set up, not before
#starts image caching of rotated images, right now just asteroids
def init(d_asteroids, d_parts, d_sats, graphlist):
    for i in range(len(d_asteroids)):
        surf = Asteroid.getImage(d_asteroids[i])
        rotatedict = {}
        for j in range(36):
            rotatedict[j*10] = rotatePixelArt(surf, j*10)
        Images.add(d_asteroids[i], rotatedict)
    pixelStuff = d_parts + d_sats
    for i in range(len(pixelStuff)):
        surf = graphlist[pixelStuff[i] - 10]
        rotatedict = {}
        for j in range(36):
            rotatedict[j*10] = rotatePixelArt(surf, j*10)
        Images.add(pixelStuff[i], rotatedict)
    Images.add("fuelpic", scaleImage(loadImage("Assets\\images\\fuelcanister.tif"), 2))
    Images.add("armorpic", loadImage("Assets\\images\\armor.tif"))

#reorders the list so it will print in the correct order
background = [100]
ship = [1,5]
def reorderObjectList(object_list):
    newObject_list = []
    for i in range(3):
        for j in range(0, len(object_list), 8):
            object_number = object_list[j+4]
            if object_number in background and i == 0:
                newObject_list += object_list[j:j+8]
            elif object_number in ship and i == 1:
                newObject_list += object_list[j:j+8]
            elif object_number not in ship and object_number not in background and i == 2:
                newObject_list += object_list[j:j+8]
    return newObject_list

#the nuts and bolts of printing the things    
def crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar, specialpics, flame, ionBlast): 
    colliderect = ""
    if object_number == 100: #draws star
        screen.blit(specialpics[0], (xpos, ypos))
        
    if object_number == 0: #draws zvezda
        screen.blit(specialpics[1], (xpos, ypos))
            
    if object_number == 1 or object_number == 5: #draws main ship
        ship_pointlist = [[xpos, ypos-30*scalar3], [xpos+15*scalar3, ypos+10*scalar3], [xpos, ypos], [xpos-15*scalar3,
                            ypos+10*scalar3]]
        ship_pointlist = Rotate(xpos, ypos, ship_pointlist, rotation)
        pygame.gfxdraw.aapolygon(screen, ship_pointlist, (255,255,255))
        pygame.gfxdraw.filled_polygon(screen, ship_pointlist, (255,255,255))
        colliderect = pointsToRect(ship_pointlist)
        if flame == True:
            #flame_pointlist = [[50 + 6, 50 + 5], [50, 50 + 20], [50 - 6, 50 + 5]]
            flame_pointlist = [[xpos, ypos], [xpos+6*scalar3, ypos+5*scalar3],
                                [xpos, ypos+20*scalar3],
                                [xpos-6*scalar3, ypos+5*scalar3]]
            flame_pointlist = Rotate(xpos, ypos, flame_pointlist, rotation)
            pygame.gfxdraw.aapolygon(screen, flame_pointlist, (255,100,0))
            pygame.gfxdraw.filled_polygon(screen, flame_pointlist, (255,100,0))
        flame = False
        
    if object_number == 2 or object_number == 8: #draws missiles (id 8 are alien missiles)
        pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 2, 0)
        
    if object_number == 4: #draws explosion effects
        pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 1, 0)
                
    if object_number == 6: #draws alien
        alien_pointlist = [[xpos-25*scalar1, ypos], [xpos-18*scalar1, ypos], [xpos-10*scalar1, ypos+8*scalar1],
                           [xpos+10*scalar1, ypos+8*scalar1], [xpos+18*scalar1, ypos], [xpos+25*scalar1, ypos],
                           [xpos-18*scalar1, ypos], [xpos-10*scalar1, ypos], [xpos-7*scalar1, ypos-7*scalar1],
                           [xpos, ypos-10*scalar1], [xpos+7*scalar1, ypos-7*scalar1], [xpos+10*scalar1, ypos]]
        colliderect = pygame.draw.aalines(screen, (255,255,255), True, alien_pointlist, False)

    if object_number == 7: #draws alien mines
        image = rotatePixelArt(specialpics[2], rotation)
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = [int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height()), image.get_width(),
                       image.get_height()]

    if object_number == 9: #draws alien blasts
        scale = 1 + (.1 * (300 - decayLife))
        ionBlast = scaleImage(ionBlast, scale)
        screen.blit(ionBlast, (xpos, ypos))
        
    if 9 < object_number < 40: #draws satellites
        image = Images.get(object_number, rotation)
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = [int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height()), image.get_width(),
                       image.get_height()]
        
    if 69 < object_number < 100: #draws asteroids
        image = Images.get(object_number, rotation)
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = Asteroid.getHitbox(xpos, ypos, object_number)

    return colliderect

#takes care of the printing logic
def printer(screen, object_list, scalar1, scalar3, graphlist, scalarscalar, specialpics, flame, ionBlast):
    object_list = reorderObjectList(object_list)
    #needed for testing which direction things are off the screen
    width, height = screen.get_size()
    left = pygame.Rect(-1,0,1,height)
    right = pygame.Rect(width,0,1,height)    
    up = pygame.Rect(0,-1,width,1)
    down = pygame.Rect(0,height,width,1)
    
    for i in range(0, len(object_list), 8):
        xpos = object_list[i]       
        ypos = object_list[i+1]
        object_number = object_list[i+4] #object type
        rotation = object_list[i+5] #rotation position
        decayLife = object_list[i+7]

        colliderect = crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar,
                                  specialpics, flame, ionBlast)
        if colliderect:
            if not screen.get_rect().contains(colliderect):
                if left.colliderect(colliderect):
                    xpos += width
                elif right.colliderect(colliderect):
                    xpos -= width

                if up.colliderect(colliderect):
                    ypos += height
                elif down.colliderect(colliderect):
                    ypos -= height
                
                crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar, specialpics,
                            flame, ionBlast)

#flashing alerts for low fuel and armor
class FlashyBox:
    def __init__(self, rect, threshold, color):
        self.rect = rect
        self.threshold = threshold
        self.color = color
        self.timer = -1
        self.displaying = False

    def update(self, screen, current):
        if current < self.threshold:
            self.timer += 1
        elif current > self.threshold:
            self.timer = -1
            self.displaying = False

        if self.timer != -1: #flips displaying when timer reaches 50
            if self.timer == 50:
                self.displaying = not self.displaying
                self.timer = 0

        if self.displaying: #draws the rectangle
            pygame.draw.rect(screen, self.color, self.rect, 0)

#controls the fuel, armor, and ammunition readout in bottom right
class InfoBars:
    fuelalert = 1
    armoralert = 1
    def init(fuelalert, armoralert):
        InfoBars.fuelalert = fuelalert
        InfoBars.armoralert = armoralert

    #prints out the fuel and armor bars
    def draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition):
        fuelpic = Images.get("fuelpic")
        armorpic = Images.get("armorpic")
        #fuel
        InfoBars.fuelalert.update(screen, currentfuel/totalfuel)
        screen.blit(fuelpic, (1600, 1000))
        pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
        pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])
        #armor
        InfoBars.armoralert.update(screen, currentarmor/totalarmor)
        screen.blit(armorpic, (1600, 930))
        pygame.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
        pygame.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])
        #ammunition
        Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])
