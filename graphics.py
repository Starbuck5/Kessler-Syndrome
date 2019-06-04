from pgx import pointsToRect
from game import Rotate
from pgx import rotatePixelArt
from pgx import scaleImage
from pgx import Texthelper
from pgx import loadImage
from pgx import spriteSheetBreaker

import pygame
import pgx

from pygame import gfxdraw
from pygame import Surface

#accepts a surface that supports palettes (gifs) and changes the color palette based on preference
#current and new colors are tuples of rgba (r, g, b, a)
def change_color(image, currentColor, newColor, toReturn = False):
    palette = image.get_palette()
    palette = list(palette)
    index = -1
    for i in range(255):
        if palette[i] == currentColor:
            index = i
            break
    if index == -1:
        raise Exception("no such currentColor found in image")
    palette[index] = newColor
    if toReturn:
        newImage = image.copy()
        newImage.set_palette(palette)
        return newImage
    image.set_palette(palette)

class Images:
    storage = {}
    bounding_rects = {}
    def add(name, image, **kwargs): #or (ID, dictionary of rotations)
        image = Images._processImage(image, **kwargs)
        Images.storage[name] = image
        Images.bounding_rects[name] = image.get_bounding_rect()

    def addRotate(ID, image, **kwargs): #takes an ID and a surface and adds the dictionary of its rotations to Images storage 
        image = Images._processImage(image, **kwargs)
        rotatedict = {}
        rectdict = {}
        for j in range(36):
            rotatedImage = rotatePixelArt(image, j*10)
            rotatedict[j*10] = rotatedImage
            rectdict[j*10] =  rotatedImage.get_bounding_rect()
        Images.storage[ID] = rotatedict
        Images.bounding_rects[ID] = rectdict

    def _processImage(image, **kwargs):
        if "colorkey" in kwargs:
            image.set_colorkey(kwargs["colorkey"])
        return image
    
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

    def getRect(name, *args):
        if not args:
            return Images.bounding_rects[name]
        var = args[0]
        var /= 10
        var = round(var)
        var *= 10
        var = int(var)
        var %= 360
        return Images.bounding_rects[name][var]

    #method used to get hitbox by looking at the image stored in Images class
    #when calling use later parameters, default parameters must be explicitly set
    #beFancy - True = use bounding rects of data ------ False = use image size alone
    def getHitbox(xpos, ypos, name, rotation, centered=True, beFancy=True, realRotation=False):
        if isinstance(rotation, str):
            image = Images.get(name)
        elif realRotation:
            image = rotatePixelArt(Images.get(name), rotation)
        else:
            image = Images.get(name, rotation)
        if beFancy:
            if isinstance(rotation, str):
                bound = Images.getRect(name)
            elif realRotation:
                image = rotatePixelArt(Images.get(name), rotation)
                bound = image.get_bounding_rect()
            else:
                bound = Images.getRect(name, rotation)
        else:
            bound = image.get_rect()
        if centered:
            return bound.move(xpos-0.5*image.get_width(), ypos-0.5*image.get_height())
        return bound.move(xpos, ypos)

    #inflates a centered hitbox outwards using a scalar
    def scaleHitbox(hitBox, scale):
        hitBox[0] -= hitBox[2]*0.5*scale
        hitBox[1] -= hitBox[3]*0.5*scale
        hitBox[2] *= scale
        hitBox[3] *= scale

#helps with caching of rotated asteroid images
def rotationCachingHelper(filepath, spritesheetWidth, spritesheetHeight, spritesheetRows, spritesheetColumns, idIntercept, scalar2):
    asteroids = loadImage(filepath)
    asteroids.set_colorkey((255,255,255))
    asteroids = spriteSheetBreaker(asteroids, spritesheetWidth, spritesheetHeight, 0, 0, spritesheetRows, spritesheetColumns)
    for i in range(len(asteroids)):
        asteroids[i] = scaleImage(asteroids[i], scalar2)
    for i in range(len(asteroids)):
        Images.addRotate(idIntercept + i, asteroids[i])

#must be called after scaling is fully set up, not before
#starts image caching of rotated images
def init(d_asteroids, d_parts, d_sats, graphlist, scalar2, scalar3):
    #adding all asteroid images/rotations
    rotationCachingHelper("Assets\\images\\smallasteroids.gif", 40, 40, 1, 4, 70, scalar2)
    rotationCachingHelper("Assets\\images\\mediumasteroids.gif", 50, 50, 1, 4, 80, scalar2)
    rotationCachingHelper("Assets\\images\\largeasteroids.gif", 80, 80, 2, 4, 90, scalar2)
        
    #adding all satellites and parts images/rotations
    pixelStuff = d_parts + d_sats
    for i in range(len(pixelStuff)):
        surf = graphlist[pixelStuff[i] - 10]
        Images.addRotate(pixelStuff[i], surf)

    #adding images for info bars
    Images.add("fuelpic", scaleImage(loadImage("Assets\\images\\fuelcanister.tif"), 2))
    Images.add("armorpic", loadImage("Assets\\images\\armor.tif"))
    Images.add("shotpic", loadImage("Assets\\images\\missile.png"), colorkey=(255,255,255))

    #adding other icons
    Images.add("infinity", loadImage("Assets\\images\\infinity.tif"))

    #adding miscellaneous other object images
    Images.add(0, scaleImage(loadImage("Assets\\images\\zvezda.tif"), 2))
    Images.add(200, scaleImage(loadImage("Assets\\images\\fuelstation.tif"), 2))
    Images.addRotate(7, scaleImage(loadImage("Assets\\images\\alienMines.tif"), 2))
    Images.add(9, scaleImage(loadImage("Assets\\images\\ionBlast.tif"), .5))

    #aliens
    Images.addRotate(120, scaleImage(loadImage("Assets\\images\\aliendrone.gif"), 1.5), colorkey=(255,255,255))
    Images.addRotate(121, scaleImage(loadImage("Assets\\images\\spiker.gif"),2), colorkey=(255,255,255))
    Images.addRotate(122, loadImage("Assets\\images\\alienshot.gif"), colorkey=(255,255,255))
    #aliens - alien mines
    imageList = spriteSheetBreaker(loadImage("Assets\\images\\alienbomb.gif"), 19, 19, 0, 0, 1, 6)
    for i in range(len(imageList)):
        image = imageList[i]
        image.set_colorkey((255,255,255))
        image = scaleImage(image, 2)
        if i == 0:
            Images.addRotate(123, image) #reference image at 123 for hitboxes
        Images.addRotate(123 + (i+1)/100, image)
        
    #adding different types of stars
    base_star = loadImage("Assets\\images\\star.gif")
    base_star.set_colorkey((255,255,255))
    Images.add(100, base_star)    
    Images.add(101, change_color(base_star, (255,216,0,255), (255, 160, 0, 255), True))    
    Images.add(102, change_color(base_star, (255,216,0,255), (255, 130, 0, 255), True))
    base_star = scaleImage(base_star, 2)
    Images.add(103, base_star)
    Images.add(104, change_color(base_star, (255,216,0,255), (255, 160, 0, 255), True))    
    Images.add(105, change_color(base_star, (255,216,0,255), (255, 130, 0, 255), True))
    
    #adding ship, no rotation because it rotates in real time
    #loads up spritesheet and loads them all up under separate IDs
    imageList = spriteSheetBreaker(loadImage("Assets\\images\\ships.png"), 24, 60, 0, 0, 1, 4)
    for i in range(len(imageList)):
        imageList[i].set_colorkey((255,255,255))
    Images.add(1.1, imageList[0])
    Images.add(1.2, imageList[1])
    Images.add(1.3, imageList[2])
    Images.add(1.4, imageList[3])

    #adding downed fighters
    imageList = spriteSheetBreaker(loadImage("Assets\\images\\fighters.gif"), 42, 22, 0, 0, 2, 2)
    for i in range(len(imageList)):
        imageList[i].set_colorkey((255,255,255))
        imageList[i] = scaleImage(imageList[i], 1.1)
        Images.addRotate(130+i, imageList[i])

    #adding derelict ship, no rotation because it's always in the same orientation
    image = loadImage("Assets\\images\\derelict.gif")
    image.set_colorkey((255,255,255))
    change_color(image, (0,0,0,255), (25,25,25,255))
    Images.add(110, image)

    #adding president's ship
    Images.addRotate(666, loadImage("Assets\\images\\protoprez2.gif"), colorkey=(255,255,255))

#reorders the list so it will print in the correct order
background = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
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

SHIPSTATE = 1 #set in main, controls which of the durability stages of the ship prints (not always 1)

#the nuts and bolts of printing the things    
def crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar, flame, special): 
    colliderect = ""
    if 99 < object_number < 110: #draws stars
        image = Images.get(object_number)
        screen.blit(image, (xpos, ypos))
        
    elif object_number == 0: #draws zvezda
        image = Images.get(0)
        screen.blit(image, (xpos, ypos))
            
    elif object_number == 1 or object_number == 5: #draws main ship
        image = rotatePixelArt(Images.get(1+SHIPSTATE/10), -rotation.getRotation())
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = [int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height()), image.get_width(),
                       image.get_height()]
        if flame == True:
            #flame_pointlist = [[50 + 6, 50 + 5], [50, 50 + 20], [50 - 6, 50 + 5]]
            flame_pointlist = [[xpos, ypos], [xpos+6*scalar3, ypos+5*scalar3],
                                [xpos, ypos+20*scalar3],
                                [xpos-6*scalar3, ypos+5*scalar3]]
            flame_pointlist = Rotate(xpos, ypos, flame_pointlist, rotation.getRotation())
            pygame.gfxdraw.aapolygon(screen, flame_pointlist, (255,100,0))
            pygame.gfxdraw.filled_polygon(screen, flame_pointlist, (255,100,0))
        flame = False
        
    elif object_number == 2 or object_number == 8: #draws missiles (id 8 are alien missiles)
        pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 2, 0)
        
    elif object_number == 4: #draws explosion effects
        pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 1, 0)
                
    elif object_number == 9: #draws alien blasts
        scale = 1 + (.1 * (300 - decayLife))
        image = scaleImage(Images.get(9), scale)
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = Images.getHitbox(xpos, ypos, 9, rotation.getRotation())
        Images.scaleHitbox(colliderect, scale)  
            
    elif object_number == 110: #draws derelict ship
        image = Images.get(110)
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = Images.getHitbox(xpos, ypos, 110, rotation.getRotation())

    elif object_number == 123:
        image = Images.get(special.getFrameNum(), rotation.getRotation())
        screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
        colliderect = Images.getHitbox(xpos, ypos, 123, rotation.getRotation())

    else:
        try:
            image = Images.get(object_number, rotation.getRotation())
            screen.blit(image, (int(xpos-0.5*image.get_width()), int(ypos-0.5*image.get_height())))
            colliderect = Images.getHitbox(xpos, ypos, object_number, rotation.getRotation())
        except:
            pass
        
    return colliderect

#takes care of the printing logic
def printer(screen, object_list, scalar1, scalar3, graphlist, scalarscalar, flame):
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
        special = object_list[i+6]
        decayLife = object_list[i+7]
        
        colliderect = crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar,
                                  flame, special)
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
                
                crayprinter(screen, xpos, ypos, object_number, rotation, decayLife, scalar1, scalar3, graphlist, scalarscalar,
                            flame, special)

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
            pgx.draw.rect(screen, self.color, self.rect, 0)

#controls the fuel, armor, and ammunition readout in bottom right
class InfoBars:
    fuelalert = 1
    armoralert = 1
    def init(fuelalert, armoralert):
        InfoBars.fuelalert = fuelalert
        InfoBars.armoralert = armoralert

    #prints out the fuel and armor bars
    def draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition, totalammunition):
        fuelpic = Images.get("fuelpic")
        armorpic = Images.get("armorpic")
        shotpic = Images.get("shotpic")
        #fuel
        InfoBars.fuelalert.update(screen, currentfuel/totalfuel)
        screen.blit(fuelpic, (1600, 1000))
        pgx.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
        pgx.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])
        #Texthelper.write(screen, [(1665, 1005), str(currentfuel), 3])
        #armor
        InfoBars.armoralert.update(screen, currentarmor/totalarmor)
        screen.blit(armorpic, (1600, 930))
        pgx.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
        pgx.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])
        #Texthelper.write(screen, [(1665, 935), str(currentarmor), 3])
        #ammunition
        screen.blit(shotpic, (1600, 860))
        Texthelper.write(screen, [(1665, 865), str(ammunition) + "/" + str(totalammunition), 3])

#used by the map to actually draw out the sectors
def drawSector(screen, location, number, currentsector, cleared):
    secsize = 80 #side length of the cubes
    if number == currentsector:
        color = (70, 130, 180)
    elif cleared:
        color = (20, 160, 40)
    else:
        color = (180, 50, 50)
    
    pgx.draw.rect(screen, color, (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
    
    if number == currentsector:
        Texthelper.write(screen, [(location[0]-35, location[1]-35), "U R Here", 1], color=color)
    Texthelper.write(screen, [(location[0]-len(str(number))*10, location[1]-15), str(number), 2], color=color)

#used in UIscreens and the main game loop to display the inventory
def drawInventory(screen, shipInventory):
    Texthelper.write(screen, [(10,10), "metal:" + str(shipInventory[0]), 3], color = (120,120,120))
    Texthelper.write(screen, [(310,10), "gas:" + str(shipInventory[1]), 3], color = (185,20,20))
    Texthelper.write(screen, [(550,10), "circuits:" + str(shipInventory[2]), 3], color = (20,185,20))
    Texthelper.write(screen, [(935,10), "credits:" + str(shipInventory[3]), 3], color = (230,180,20))
    
