import random
import math
from pgx import loadImage
from pgx import spriteSheetBreaker
from pgx import scaleImage
from pgx import filehelper

class RotationState():
    def __init__(self, rotationPos, rotationMom):
        self.pos = rotationPos
        self.mom = rotationMom
        if not isinstance(rotationPos, str):
            self.rotating = True
        else:
            self.rotating = False

    def __str__(self):
        return "RotationStateObj: rot: " + str(self.pos) + " mom: " + str(self.mom)

    def getRotation(self):
        return self.pos

    def setRotation(self, value):
        self.pos = value

    def getMomentum(self):
        return self.mom

    def setMomentum(self, value):
        self.mom = value

    def getRotating(self):
        return self.rotating

    def rotate(self):
        self.pos += self.mom/7 #the divided by moderates the speed of rotation
        if self.pos >= 360:
            self.pos -= 360
        if self.pos <= -360:
            self.pos += 360

    def rotateBy(self, value):
        self.pos += value

class AITools():
    #takes two object list indices and returns distance between them
    #object one is at index 0, two at index 1 (so not using true object list indices)
    def distanceBetween(object_list, index1, index2):
        xdiff = object_list[index1] - object_list[index2]
        ydiff = object_list[index1+1] - object_list[index2+1]
        return (xdiff**2 + ydiff**2)**0.5

class DroneAI():
    def __init__(self):
        pass

    def update(self, object_list, self_loc):
        distance = AITools.distanceBetween(object_list, 0, self_loc)

        #pulling entities out of the list for ease of change
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]

        droneShip[2] = (humanShip[0] - droneShip[0])/distance
        droneShip[3] = (droneShip[1] - humanShip[1])/distance        
        if (droneShip[1] - humanShip[1]) > 0:
            newRotation = math.degrees(math.acos(droneShip[2]))
        else:
            newRotation = 360 - math.degrees(math.acos(droneShip[2]))
        rotationMom = newRotation - droneShip[5].getRotation()
        newRotationMom = rotationMom - 360
        if abs(newRotationMom) < abs(rotationMom):
            rotationMom = newRotationMom
        if rotationMom > 5:
            rotationMom = 5
        elif rotationMom < -5:
            rotationMom = -5
        droneShip[5].setMomentum(rotationMom)

        #zippings modified entity back into the list
        object_list[self_loc:self_loc+8] = droneShip
        
             
#particle effects
def particlemaker(xpos, ypos, xmom, ymom):
    # particle settings
    particle_lifespan = 45
    random_factor = 30 # higher number = less random
    max_particles = 6
    max_deviation = 2
    printerlist_add = []
    for i in range(random.randint(max_particles - max_deviation, max_particles)):
        printerlist_add += [xpos, ypos, xmom + ((random.randint(-20, 20))/random_factor), ymom +
                            ((random.randint(-20, 20))/random_factor), 4, RotationState(-1,-1), "NA", particle_lifespan]  
    return printerlist_add
    
#physics handling
def doPhysics(object_list, width, height, max_speed, drag, step_drag):
    for i in range(0, len(object_list), 8):
        #decaying objects
        if object_list[4 + i] in [2, 8, 5, 4, 9]: #stuff in list should have a decrement to their life force
            object_list[7 + i] -= 1

        #speed limit for ship
        if object_list[4+i] == 1 or object_list[4+i] == 5:
            if object_list[2 + i] > max_speed:
                object_list[2 + i] = max_speed
            if object_list[2 + i] < -1 * max_speed:
                object_list[2 + i] =  -1 * max_speed
            if object_list[3 + i] > max_speed:
                object_list[3 + i] = max_speed
            if object_list[3 + i] < -1 * max_speed:
                object_list[3 + i] = -1 * max_speed
            
        # positioner
        object_list[i] += object_list[2 + i]
        object_list[1 + i] -= object_list[3 + i]

        # edges section
        if object_list[i] > width:
            object_list[i] -= width
        if  object_list[i] < 0:
            object_list[i] += width
        if object_list[1 + i] > height:
            object_list[1 + i] -= height
        if object_list[1 + i] < 0:
            object_list[1 + i] += height

        #drag
        if object_list[4 +i] in drag:
            stepper = abs(object_list[2 +i]) + abs(object_list[3 +i])
            if stepper == 0:
                stepper = 1
            step_drag_x = abs(object_list[2 +i]) / stepper * step_drag
            step_drag_y = abs(object_list[3 +i]) / stepper * step_drag   
            if object_list[2 +i] > 0 and object_list[2 +i] > step_drag_x:
                object_list[2 +i] -= step_drag_x
            elif step_drag_x > object_list[2 +i] > 0:
                object_list[2 +i] = 0
            if object_list[2 +i] < 0 and object_list[2 +i] < step_drag_x:
                object_list[2 +i] += step_drag_x
            elif step_drag_x < object_list[2 +i] < 0:
                object_list[2 +i] = 0     
            if object_list[3 +i] > 0 and object_list[3 +i] > step_drag_y:
                object_list[3 +i] -= step_drag_y
            elif step_drag_y > object_list[3 +i] > 0:
                object_list[3 +i] = 0   
            if object_list[3 +i] < 0 and object_list[3 +i] < step_drag_y:
                object_list[3 +i] += step_drag_y
            elif step_drag_y < object_list[3 +i] < 0:
                object_list[3 +i] = 0

        #rotation
        #if not isinstance(object_list[5+i], str):
        #    object_list[5+i] += object_list[6+i]/7 #the divided by moderates the speed of rotation
        #    if object_list[5+i] >= 360:
        #        object_list[5+i] -= 360
        #    if object_list[5+i] <= -360:
        #        object_list[5+i] += 360

        #rotation - now with objects!
        if object_list[5+i].getRotating():
            object_list[5+i].rotate()
        
        
#helps out by setting entities to reasonable speeds
def asteroidspeedmaker(max_asteroid_spd):
    asteroid_speedset = []
    # if else statements institute a minimum horizontal and vertical speed (separately) of half the asteroid high speed
    if random.randint(0,1) == 1:
        asteroid_speedset.append(random.randint(int(max_asteroid_spd/2), max_asteroid_spd)/100)
    else:
        asteroid_speedset.append(random.randint(-1*max_asteroid_spd, int(-1*max_asteroid_spd/2))/100)
    if random.randint(0,1) == 1:
        asteroid_speedset.append(random.randint(int(max_asteroid_spd/2), max_asteroid_spd)/100)
    else:
        asteroid_speedset.append(random.randint(-1*max_asteroid_spd, int(-1*max_asteroid_spd/2))/100)
    return asteroid_speedset

#generates the stars for backgrounds
def generateStars(width, height):
    stars_list = []
    # number of occurerences refers to relative probability of it showing up
    possible_IDs = [100, 100, 100, 101, 101, 102, 102, 103, 104, 105]
    for i in range(24):
        ID = possible_IDs[random.randint(0, len(possible_IDs)-1)]
        stars_list += [random.randint(0,width), random.randint(0,height), 0, 0, ID, RotationState(-1,-1), "NA", 1]
    return stars_list

#leveler
def leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, d_parts, d_asteroids, sectornum):
    mineGeneration = [9, 10, 11, 12, 13, 14 ,15 ,16, 17, 18, 19]
    droneGeneration = [14, 15, 16, 17, 18, 19]
    if sectornum in droneGeneration:
        ASTEROID = 20
        SATS = 40
        PARTS = 0
        MINES = 20
        DRONES = 20
    elif sectornum in mineGeneration:
        ASTEROID = 25
        SATS = 40
        PARTS = 10
        MINES = 25
        DRONES = 0
    else:
        ASTEROID = 30
        SATS = 50
        PARTS = 20
        MINES = 0
        DRONES = 0
    object_list = object_list[:8]
    object_list += generateStars(width, height)
    countervar = 0
    while countervar < random.randint(max_asteroids - 2, max_asteroids):
        idChooser = random.randint(0, 100)
        if idChooser < MINES:
            idSelection = [7, 7]
        elif idChooser < ASTEROID + MINES:
            idSelection = d_asteroids
        elif idChooser < ASTEROID + MINES + SATS:
            idSelection = d_sats
        elif idChooser < ASTEROID + MINES + SATS + DRONES:
            idSelection = [120, 120]
        else:
            idSelection = d_parts
        asteroid_speedset = asteroidspeedmaker(max_asteroid_spd)
        if idSelection == [120, 120]: #drone creation
            object_list_add = [random.randint(0, width), random.randint(0, height), 0, 0,
                               idSelection[random.randint(0, len(idSelection)-1)], RotationState(random.randint(0,360), 0),
                               DroneAI(), 1]
        else:
            object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                               asteroid_speedset[1]]
            object_list_add += [idSelection[random.randint(0, len(idSelection)-1)], RotationState(random.randint(0,360),
                                random.randint(-10,10)),"NA", 1]                    
        countervar += 1
        object_list += object_list_add
    return object_list

#deaderizer -- perhaps amalgamated into doPhysics in the future, just outside its main for loop
def deaderizer(object_list):
    indexadj = 0
    while indexadj < len(object_list): 
        if object_list[7 + indexadj] <= 0:
            if object_list[4+indexadj] == 5:
                object_list[7+indexadj] = 1
                object_list[4+indexadj] = 1
            else:
                del object_list[indexadj:8+indexadj]
        else:
            indexadj += 8
    return object_list

sectorDestData = {1: [2, 5, 3, -1], 2: [-1, 4, 1, -1], 3: [1, -1, -1, -1], 4: [-1, -1, 5, 2], 5: [4, 6, -1, 1],
                  6: [8, -1, 7, 5], 7: [6, 9, -1, -1], 8: [12, 10, 6, -1], 9: [10, 14, -1, 7], 10: [-1, 11, 9, 8],
                  11: [13, 16, 17, 10], 12: [-1, 13, 8, -1], 13: [-1, -1, 11, 12], 14: [-1, 15, -1, 9], 15: [16, -1, -1, 14],
                  16: [-1, 18, 15, 11], 17: [11, -1, -1, -1], 18: [-1, -1, 19, 16], 19: [18, -1, -1, -1]}

def sectorDestinations(sectornum):
    #[left, up, right, down]
    if sectornum in sectorDestData:
        return sectorDestData[sectornum]
    else:
        return [1, 1, 1, 1] #in case you go into a sector that doesn't exist, it will redirect you to the home sector

#returns true if an infinite level that always regenerates
#else returns false to signal a level that doesn't get regenerated
def sectorGeneration(sectornum):
    infinite_sectors = [4, 12, 15]
    if sectornum in infinite_sectors:
        return True
    return False

def solarPanelDrops():
    drops = [0, 0, 0, 0]
    if random.randint(1,100) <= 80:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[0] += 1
        elif 61 <= percentHelper <= 90:
            drops[0] += 2
        else:
            drops[0] += 3
    if random.randint(1,100) <= 20:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[2] += 2
        elif 61 <= percentHelper <= 90:
            drops[2] += 3
        else:
            drops[2] += 6
    if random.randint(1,100) <= 10:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[3] += 3
        elif 61 <= percentHelper <= 90:
            drops[3] += 6
        else:
            drops[3] += 9
    return drops

def satelliteDrops():
    drops = [0, 0, 0, 0]
    if random.randint(1,100) <= 80:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[0] += 2
        elif 61 <= percentHelper <= 90:
            drops[0] += 4
        else:
            drops[0] += 6
    if random.randint(1,100) <= 40:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[1] += 2
        elif 61 <= percentHelper <= 90:
            drops[1] += 4
        else:
            drops[1] += 6
    if random.randint(1,100) <= 20:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[2] += 2
        elif 61 <= percentHelper <= 90:
            drops[2] += 4
        else:
            drops[2] += 6
    if random.randint(1,100) <= 70:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[3] += 5
        elif 61 <= percentHelper <= 90:
            drops[3] += 10
        else:
            drops[3] += 20
    return drops

def RotatePoint(xpos, ypos, point, rotation):
    point[1] -= ypos
    point[0] -= xpos
    revisedPoint = []
    if point[0] or point[1]:
        if point[1] > 0 and point[0] == 0:
            currentPosition = 90
        elif point[1] < 0 and point[0] == 0:
            currentPosition = 270
        elif point[0] > 0:
            currentPosition = math.degrees(math.atan(point[1]/point[0]))
        elif point[0] <= 0:
            currentPosition = math.degrees(math.atan(point[1]/point[0])) + 180
        realPosition = currentPosition + rotation
        distance = (abs(point[0])**2 + abs(point[1])**2)**0.5
        xPoint = math.cos(math.radians(realPosition)) * distance + xpos
        yPoint = math.sin(math.radians(realPosition)) * distance + ypos
        revisedPoint.append([xPoint, yPoint])
    else:
        #if the point being rotated around is in the list
        point[1] += ypos
        point[0] += xpos
        revisedPoint.append([point[0], point[1]])
    return revisedPoint

def Rotate(xpos, ypos, points, rotationPosition):
    revisedPoints = []
    for i in range(len(points)):
        revisedPoints += RotatePoint(xpos, ypos, points[i], rotationPosition)
    return revisedPoints

def dock(xpos, ypos, image):
    width = image.get_size()[0]
    height = image.get_size()[1]
    newXpos = xpos+(width/2)+10
    newYpos = ypos+height+10
    rotation = RotationState(180, 0)
    xmom = 0
    ymom = -0.5
    return (newXpos, newYpos, xmom, ymom, rotation)

#wrapper for saveObjects that determines how to save a level
def saveGame(sectornum, object_list, width, height):
    if sectorGeneration(sectornum):
        saveObjects(sectornum, [-1], width, height)
    else:
        saveObjects(sectornum, object_list[:], width, height)

def processListForSave(save_list, width, height):
    for i in range(len(save_list)):
        if isinstance(save_list[i], float):
            save_list[i] = round(save_list[i], 1)
        if len(save_list) >= 8:
            # turning x and y coords into float percentages
            if i % 8 == 0:
                save_list[i] = round(save_list[i]/width, 3)
            if i % 8 == 1:
                save_list[i] = round(save_list[i]/height, 3)
    

#saves objectlist to file by breaking it into a maximum of 5 lines
def saveObjects(sectornum, save_list, width, height):
    processListForSave(save_list, width, height)
    
    resave_list = filehelper.loadObj(5)
    resave_list[sectornum-1] = save_list

    filehelper.saveObj(resave_list, 5)

#extracts the list saveObjects saved to file
def getObjects(sectornum, width, height, **kwargs):
    if 'old' in kwargs:
        if kwargs['old']:
            object_list = []
            for i in range(5):
                object_list += filehelper.get(sectornum*5+i)
            if object_list != []:
                while object_list[-1] == '':
                    object_list.pop()
        else:
            object_list = filehelper.loadObj(5)[sectornum-1]
    else:
        object_list = filehelper.loadObj(5)[sectornum-1]
            
    # turning x and y float percentages back into coords
    if len(object_list) >= 8:
        for i in range(len(object_list)):
            if i % 8 == 0:
                object_list[i] = round(object_list[i]*width)     
            if i % 8 == 1:
                object_list[i] = round(object_list[i]*height)
    for i in range(int(len(object_list)/8)):
        if object_list[4+i*8] == 2 or object_list[4+i*8] == 8:
            object_list[6+i*8] = -10 #gets rid of shots and alien shots when entering a sector
    return object_list

#deletes everyinstance of toDelete type in the delSector - only changes the file doesn't change anything in play
def deleteObject(toDelete, delSector, width, height):
    object_list = getObjects(delSector, width, height)
    for i in range(0, len(object_list), 8):
        if object_list[i+4] == toDelete:
            del object_list[i:i+8]
    saveGame(delSector, object_list, width, height)

##pgx.filehelper = pgx.Filehelper("Assets\\saves\\defaultgamedata.txt")
##for sectornum in range(1,19):
##    resave = getObjects(sectornum, 1920, 1080)
##    if len(resave) > 1:
##        for i in range(0, len(resave), 8):
##            resave[i+5] = RotationState(resave[i+5], resave[i+6])
##            resave[i+6] = "NA"
##        print(resave)
##        saveGame(sectornum, resave, 1920, 1080)
##print("finished")


