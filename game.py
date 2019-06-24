import random
import math
import graphics
from pgx import loadImage
from pgx import spriteSheetBreaker
from pgx import scaleImage
from pgx import filehelper
import pgx

#stores a couple constants so they can be accessed without passing variables
class GameConstants():
    width = -1
    height = -1
    max_speed = -1
    drag = []
    step_drag = -1

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

    def rotate(self, pdt=1):
        self.pos += self.mom/7*pdt #the divided by moderates the speed of rotation
        if self.pos >= 360:
            self.pos -= 360
        if self.pos <= -360:
            self.pos += 360

    def rotateBy(self, value, pdt=1):
        self.pos += value * pdt

class AITools():
    #constants directly set by main
    missile_accel = -1
    missile_lifespan = -1
    
    #takes two object list indices and returns distance between them
    #object one is at index 0, two at index 1 (so not using true object list indices)
    def distanceBetween(object_list, index1, index2):
        xdiff = object_list[index1] - object_list[index2]
        ydiff = object_list[index1+1] - object_list[index2+1]
        return (xdiff**2 + ydiff**2)**0.5

    #releases a shot in the direction specified
    #currently starts from x,y - so usually the center of the entity
    #optional arg allows it to shoot entities of different types
    def shoot(xpos, ypos, object_list, self_loc, angle, shot_type=2, lifespan=-1):
        angle = -(angle-90)
        thrust_vector = (math.sin(math.radians(angle)), math.cos(math.radians(angle)))
        xmom = object_list[self_loc+2] + thrust_vector[0] * AITools.missile_accel
        ymom = object_list[self_loc+3] + thrust_vector[1] * AITools.missile_accel
        if lifespan < 0:
            lifespan = AITools.missile_lifespan
        if shot_type == 122: #alien shot
            angle = -angle + 90
            shot = [xpos, ypos, xmom, ymom, shot_type, RotationState(angle, 0), "NA", lifespan]
        else:
            shot = [xpos, ypos, xmom, ymom, shot_type, RotationState("NA", "NA"), "NA", lifespan]
        object_list += shot

    def releaseMine(object_list, self_loc, angle):
        xpos = object_list[self_loc]
        ypos = object_list[self_loc+1]
        angle = -(angle-90)
        thrust_vector = (math.sin(math.radians(angle)), math.cos(math.radians(angle)))
        xmom = object_list[self_loc+2] + thrust_vector[0] * AITools.missile_accel / 3
        ymom = object_list[self_loc+3] + thrust_vector[1] * AITools.missile_accel / 3
        object_list += [xpos, ypos, xmom, ymom, 123, RotationState(random.randint(0,360),
                        random.randint(-10,10)), AlienMineAI(), 1]

    def releaseDrone(object_list, self_loc, angle):
        xpos = object_list[self_loc]
        ypos = object_list[self_loc+1]
        angle = -(angle-90)
        thrust_vector = (math.sin(math.radians(angle)), math.cos(math.radians(angle)))
        xmom = object_list[self_loc+2] + thrust_vector[0] * AITools.missile_accel / 3
        ymom = object_list[self_loc+3] + thrust_vector[1] * AITools.missile_accel / 3
        object_list += [xpos, ypos, xmom, ymom, 120, RotationState(random.randint(0,360),
                        random.randint(-10,10)), DroneAI(), 1]

    #takes in the objectlist and two locations, uses the missile accel to find the angle for
    #the shooter to hit the target, taking into account both of their momentums
    def getInterceptAngle(object_list, self_loc, target_loc):
        shooter = object_list[self_loc:self_loc+8]
        target = object_list[target_loc:target_loc+8]
        coolTicker = 0
        colliding = False
        while not colliding:
            #doPhysics(shooter)
            #doPhysics(target)
            xdiff = target[0] + target[2]*coolTicker - shooter[0]
            ydiff = target[1] - target[3]*coolTicker - shooter[1]
            distance = (xdiff**2 + ydiff**2)**0.5
            if (xdiff**2 + ydiff**2)**0.5 < AITools.missile_accel * coolTicker:
                colliding = True
                if (shooter[1] - target[1]) > 0:
                    angle = math.degrees(math.acos(xdiff/distance))
                else:
                    angle = 360 - math.degrees(math.acos(xdiff/distance))
                return angle
    
            if coolTicker > 5000:
                break
            
            coolTicker += 1

    #combines the getInterceptAngle and shoot functions into one ~hopefully~ seamless package
    def shootAt(object_list, self_loc, target_loc, shot_type=2, lifespan=-1):
        xpos = object_list[self_loc]
        ypos = object_list[self_loc+1]
        angle = AITools.getInterceptAngle(object_list, self_loc, target_loc)
        shoot(xpos, ypos, object_list, self_loc, angle, shot_type, lifespan)

class DroneAI():
    def __init__(self):
        self.progression = 0
        self.shotCounter = 0
        self.direction = random.randint(0,1)
        self.speed = 2
        if self.direction == 0:
            self.direction = -1

    def attack(self, screen, object_list, self_loc):
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        droneShip[2] = math.cos(math.radians(droneShip[5].getRotation()))*self.speed
        droneShip[3] = math.sin(math.radians(droneShip[5].getRotation()))*self.speed
        newRotation = AITools.getInterceptAngle(object_list, self_loc, 0)
        rotationMom = newRotation - droneShip[5].getRotation()
        newRotationMom = rotationMom - 360
        if abs(newRotationMom) < abs(rotationMom):
            rotationMom = newRotationMom
        if rotationMom > 5:
            rotationMom = 5
        elif rotationMom < -5:
            rotationMom = -5
        if abs(rotationMom) == 5:
            droneShip[2] = droneShip[2]/2
            droneShip[3] = droneShip[3]/2
        droneShip[5].setMomentum(rotationMom)
        return droneShip

    def shooting(self, screen, object_list, self_loc, xpos, ypos):
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        newRotation = AITools.getInterceptAngle(object_list, self_loc, 0)
        droneShip[2] = 0
        droneShip[3] = 0
        droneShip[5].setMomentum(0)
        if self.shotCounter % 25 == 0:
            AITools.shoot(xpos, ypos, object_list, self_loc, object_list[self_loc+5].getRotation(), 122)
        self.shotCounter += 1
        return droneShip

    def enclose(self, screen, object_list, self_loc):
        distance = AITools.distanceBetween(object_list, 0, self_loc)
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        droneShip[2] = math.cos(math.radians(droneShip[5].getRotation()))*self.speed
        droneShip[3] = math.sin(math.radians(droneShip[5].getRotation()))*self.speed
        xMom = (humanShip[0] - droneShip[0])/distance
        if (droneShip[1] - humanShip[1]) > 0:
            newRotation = math.degrees(math.acos(xMom))
        else:
            newRotation = 360 - math.degrees(math.acos(xMom))
        newRotation += (45*self.direction)
        rotationMom = newRotation - droneShip[5].getRotation()
        newRotationMom = rotationMom - 360
        if abs(newRotationMom) < abs(rotationMom):
            rotationMom = newRotationMom
        if rotationMom > 5:
            rotationMom = 5
        elif rotationMom < -5:
            rotationMom = -5
        droneShip[5].setMomentum(rotationMom)
        return droneShip

    def releasingMine(self, screen, object_list, self_loc):
        distance = AITools.distanceBetween(object_list, 0, self_loc)
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        droneShip[2] = math.cos(math.radians(droneShip[5].getRotation()))*self.speed
        droneShip[3] = math.sin(math.radians(droneShip[5].getRotation()))*self.speed
        xMom = (humanShip[0] - droneShip[0])/distance
        if (droneShip[1] - humanShip[1]) > 0:
            newRotation = math.degrees(math.acos(xMom))
        else:
            newRotation = 360 - math.degrees(math.acos(xMom))
        angle = newRotation
        AITools.releaseMine(object_list, self_loc, angle)
        return droneShip

    def retreat(self, screen, object_list, self_loc):
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        droneShip[5].setMomentum(0)
        droneShip[2] = math.cos(math.radians(droneShip[5].getRotation()))*self.speed
        droneShip[3] = math.sin(math.radians(droneShip[5].getRotation()))*self.speed
        return droneShip

    def update(self, screen, object_list, self_loc):
        distance = AITools.distanceBetween(object_list, 0, self_loc)
        newRotation = AITools.getInterceptAngle(object_list, self_loc, 0)

        #pulling entities out of the list for ease of change
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        rotationDistance = abs(newRotation - droneShip[5].getRotation())
        
        if self.progression == 0:
            droneShip = self.attack(screen, object_list, self_loc)
            if distance <= 100:
                self.progression = 3
            elif distance <= 300 and (rotationDistance < 10 or 360 - rotationDistance < 10):
                self.progression = 1

        elif self.progression == 1:
            xpos = droneShip[0]
            ypos = droneShip[1]
            droneShip = self.shooting(screen, object_list, self_loc, xpos, ypos)
            if self.shotCounter == 100:
                self.shotCounter = 0
                self.progression = 2
            elif distance <= 100:
                self.progression = 3
            elif rotationDistance >= 20 and 360 - rotationDistance >= 20:
                self.progression = 0

        elif self.progression == 2:
            droneShip = self.enclose(screen, object_list, self_loc)
            if distance <= 150:
                droneShip[5].setMomentum(0)
                self.progression = 3
                self.direction = random.randint(0,1)
                if self.direction == 0:
                    self.direction = -1
            elif distance >= 400:
                self.progression = 0

        elif self.progression == 3:
            droneShip = self.releasingMine(screen, object_list, self_loc)
            self.progression = 4
                
        elif self.progression == 4:
            droneShip = self.retreat(screen, object_list, self_loc)
            if distance >= 400:
                self.progression = 0
                
        #zippings modified entity back into the list
        object_list[self_loc:self_loc+8] = droneShip

class ArmorManager():
    def __init__(self, totalarmor):
        self.armor = totalarmor
        self.totalarmor = totalarmor

    def applyDamage(self, amount):
        self.armor -= amount

    def getArmor(self):
        return self.armor

    def setArmor(self, amount):
        self.armor = amount

    def getTotalArmor(self):
        return self.totalarmor

    def setTotalArmor(self, amount):
        self.totalarmor = amount

#MulTiPle INheRiTAncE?!?! Suck it JAVA
class PrezAI(DroneAI, ArmorManager):
    def __init__(self):
        DroneAI.__init__(self)
        ArmorManager.__init__(self, 50)
        self.speed = 4
        self.RightLeft = 0

    def update(self, screen, object_list, self_loc):
        distance = AITools.distanceBetween(object_list, 0, self_loc)
        newRotation = AITools.getInterceptAngle(object_list, self_loc, 0)

        #pulling entities out of the list for ease of change
        droneShip = object_list[self_loc:self_loc+8]
        humanShip = object_list[0:8]
        rotationDistance = abs(newRotation - droneShip[5].getRotation())
        
        if self.progression == 0:
            droneShip = DroneAI.attack(self, screen, object_list, self_loc)
            if distance <= 100:
                self.progression = 3
            elif distance <= 300 and (rotationDistance < 10 or 360 - rotationDistance < 10):
                angle = droneShip[5].getRotation() + (90*self.direction)
                droneAICount = 0
                numExaminations = int(len(object_list)/8)
                for i in range(numExaminations):
                    if object_list[(i*8)+4] == 120:
                        droneAICount += 1
                if droneAICount <= 5:
                    AITools.releaseDrone(object_list, self_loc, angle)
                self.progression = 1

        elif self.progression == 1:
            xpos = droneShip[0]
            ypos = droneShip[1]
            angle = droneShip[5].getRotation()
            if self.RightLeft == 0:
                angle += 90
                self.RightLeft = 1
                xChange = math.cos(math.radians(angle))*45
                yChange = math.sin(math.radians(angle))*45
            elif self.RightLeft == 1:
                angle -= 90
                self.RightLeft = 2
                xChange = math.cos(math.radians(angle))*45
                yChange = math.sin(math.radians(angle))*45
            elif self.RightLeft == 2:
                self.RightLeft = 0
                xChange = 0
                yChange = 0
            xpos += xChange
            ypos += yChange
            droneShip = DroneAI.shooting(self, screen, object_list, self_loc, xpos, ypos)
            if self.shotCounter == 150:
                self.shotCounter = 0
                self.progression = 2
            elif distance <= 100:
                self.progression = 3
            elif rotationDistance >= 20 and 360 - rotationDistance >= 20:
                self.progression = 0

        elif self.progression == 2:
            droneShip = DroneAI.enclose(self, screen, object_list, self_loc)
            if distance <= 150:
                droneShip[5].setMomentum(0)
                self.progression = 3
                self.direction = random.randint(0,1)
                if self.direction == 0:
                    self.direction = -1
            elif distance >= 400:
                self.progression = 0

        elif self.progression == 3:
            droneShip = DroneAI.releasingMine(self, screen, object_list, self_loc)
            self.progression = 4
                
        elif self.progression == 4:
            droneShip = DroneAI.retreat(self, screen, object_list, self_loc)
            if distance >= 400:
                self.progression = 0

        object_list[self_loc:self_loc+8] = droneShip
        
        pgx.Texthelper.write(screen, [("center", 70), "President of the World", 2], color = (110,0, 30))
        pgx.draw.rect(screen, (200,0, 30), ["left.385", 100, 1150, 30])
        armorfraction = self.getArmor() / self.getTotalArmor()
        pgx.draw.rect(screen, (110,0, 30), ["left.385", 100, int(1150*armorfraction), 30])

        if self.getArmor() < 0:
            object_list[self_loc+7] = -1
            inp = object_list[self_loc:self_loc+4]
            for i in range(6):
                object_list += particlemaker(*inp)
        

class SpikeAI():
    def __init__(self):
        self.timer = -random.randint(0,300)

    def update(self, screen, object_list, self_loc):
        self.timer += 1
        if self.timer >= 0:
            xpos = object_list[self_loc]
            ypos = object_list[self_loc+1]
            AITools.shoot(xpos, ypos, object_list, self_loc, object_list[self_loc+5].getRotation(), 122)
            AITools.shoot(xpos, ypos, object_list, self_loc, object_list[self_loc+5].getRotation()+90, 122)
            AITools.shoot(xpos, ypos, object_list, self_loc, object_list[self_loc+5].getRotation()+180, 122)
            AITools.shoot(xpos, ypos, object_list, self_loc, object_list[self_loc+5].getRotation()+270, 122)
            self.timer = -300


class AlienMineAI():
    numFrames = 6
    frameTick = 30 #number of ticks that constitute a new frame
    
    def __init__(self):
        self.time = 0
        self.frame = 1

    def update(self, screen, object_list, self_loc):
        self.time += 1
        if self.time >= AlienMineAI.frameTick:
            self.time = 0
            self.frame += 1
            if self.frame > AlienMineAI.numFrames:
                self.frame = 1

    def getFrame(self):
        return self.frame

    def getFrameNum(self):
        num = self.getFrame()
        return 123 + num/100

    #releases a bunch of spikes and destroys the entity
    def explode(self, object_list, self_loc):
        for i in range(15):
            xpos = object_list[self_loc]
            ypos = object_list[self_loc+1]
            AITools.shoot(xpos, ypos, object_list, self_loc, i*24, 122)
        object_list[self_loc + 7] = -1

class ShipExtras():
    def __init__(self):
        self.inventory = [0,0,0,0]

    def update(self, screen, object_list, object_loc):
        pass

    def getInventory(self):
        return self.inventory

    def setInventory(self, newInventory):
        self.inventory = newInventory

    def addInventory(self, newInventory):
        self.inventory = [a + b for a, b in zip(self.inventory, newInventory)]
             
#particle effects
def particlemaker(xpos, ypos, xmom, ymom):
    # particle settings
    lifespan_randomness = 300
    particle_lifespan = 600 # 45
    random_factor = 30 # higher number = less random
    max_particles = 6
    max_deviation = 2
    printerlist_add = []
    for i in range(random.randint(max_particles - max_deviation, max_particles)):
        printerlist_add += [xpos, ypos, xmom + ((random.randint(-20, 20))/random_factor), ymom +
                            ((random.randint(-20, 20))/random_factor), 4, RotationState(-1,-1), "NA", particle_lifespan + random.randint(-lifespan_randomness,lifespan_randomness)]  
    return printerlist_add

#physics wrapper
#dt is measured in
def doPhysics(object_list, pdt):
    specedPhysics(object_list, GameConstants.width, GameConstants.height, GameConstants.max_speed, GameConstants.drag,
                  GameConstants.step_drag, pdt)

#physics handling
def specedPhysics(object_list, width, height, max_speed, drag, step_drag, pdt):   
    for i in range(0, len(object_list), 8):
        #decaying objects
        if object_list[4 + i] in [2, 8, 5, 4, 9, 122]: #stuff in list should have a decrement to their life force
            object_list[7 + i] -= int(1*pdt)

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
        object_list[i] += object_list[2 + i]*pdt
        object_list[1 + i] -= object_list[3 + i]*pdt

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
            step_drag_x = abs(object_list[2 +i]) / stepper * step_drag * pdt
            step_drag_y = abs(object_list[3 +i]) / stepper * step_drag * pdt 
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

        #rotation - now with objects!
        if object_list[5+i].getRotating():
            object_list[5+i].rotate(pdt)
        
        
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
    for i in range(random.randint(45, 55)):
        ID = possible_IDs[random.randint(0, len(possible_IDs)-1)]
        stars_list += [random.randint(0,width), random.randint(0,height), 0, 0, ID, RotationState("NA","NA"), "NA", 1]
    return stars_list

#leveler
def leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, d_parts, d_asteroids, d_fighters, sectornum):
    mineGeneration = [9, 10, 11, 12, 13, 14 ,15 ,16, 17, 18, 19]
    droneGeneration = [14, 15, 16, 17, 18, 19]
    supplyGeneration = [12, 13, 14, 15, 16, 17, 18, 19]
    fighterGeneration = [11, 12, 13, 14, 15, 16, 17, 18, 19]
    additionalEntities = 0 #allows different sectors to generate greater numbers of entities than the base
    if sectornum in droneGeneration:
        ASTEROID = 15
        SATS = 40
        PARTS = 15
        MINES = 15
        DRONES = 15
        additionalEntities = 4
    elif sectornum in mineGeneration:
        ASTEROID = 20
        SATS = 45
        PARTS = 15
        MINES = 20
        DRONES = 0
        additionalEntities = 2
    else:
        ASTEROID = 30
        SATS = 50
        PARTS = 20
        MINES = 0
        DRONES = 0
    object_list = object_list[:8]
    object_list += generateStars(width, height) #adding in a star field
    repetitions = random.randint(max_asteroids - 2, max_asteroids) + additionalEntities
    for i in range(repetitions):
        #choosing the ID
        idChooser = random.randint(0, 100)
        if idChooser < MINES:
            idSelection = [121, 121, 7, 7, 7, 7, 123, 123]
        elif idChooser < ASTEROID + MINES:
            idSelection = d_asteroids
        elif idChooser < ASTEROID + MINES + SATS:
            idSelection = d_sats[:]
            if sectornum in fighterGeneration:
                idSelection += d_fighters
        elif idChooser < ASTEROID + MINES + SATS + DRONES:
            idSelection = [120, 120]
        else:
            idSelection = d_parts[:]
            if sectornum not in supplyGeneration:
                idSelection.remove(31) #takes out ID 31, which is the supply drop
        ID = idSelection[random.randint(0, len(idSelection)-1)]

        #creating the entity        
        asteroid_speedset = asteroidspeedmaker(max_asteroid_spd) #getting reasonable speed
        if ID == 120: #special for drone creation
            object_list_add = [random.randint(0, width), random.randint(0, height), 0, 0,
                               ID, RotationState(random.randint(0,360), 0),
                               DroneAI(), 1]
        elif ID == 121: #special for spike shooter creation
            object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                               asteroid_speedset[1], ID, RotationState(random.randint(0,360),random.randint(-10,10)),
                               SpikeAI(), 1]
        elif 130 <= ID < 140: #special for fighters
            object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                               asteroid_speedset[1], ID, RotationState(random.randint(0,360),random.randint(-3,3)),
                               "NA", 1]
        elif ID == 123: #special for alien animated bombs
            object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                               asteroid_speedset[1], ID, RotationState(random.randint(0,360),random.randint(-10,10)),
                               AlienMineAI(), 1]
        else:
            object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                               asteroid_speedset[1], ID, RotationState(random.randint(0,360),random.randint(-10,10)),
                               "NA", 1]                    
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

def solarPanelDrops(shipLv):
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
    if shipLv[3] > 0: #scavenging module
        drops = [round(drop*1.5) for drop in drops]
    return drops

def satelliteDrops(shipLv):
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
    if shipLv[3] > 0: #scavenging module
        drops = [round(drop*1.5) for drop in drops]
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

def updateShipGraphics(currentarmor, totalarmor, timer_shipdeath, deathtimer):
    armorPercent = currentarmor / totalarmor * 100
    if timer_shipdeath < deathtimer:
        graphics.SHIPSTATE = 5
    elif armorPercent <= 30:
        graphics.SHIPSTATE = 4
    elif armorPercent <= 60:
        graphics.SHIPSTATE = 3
    elif armorPercent <= 90:
        graphics.SHIPSTATE = 2
    else:
        graphics.SHIPSTATE = 1    

#wrapper for saveObjects that determines how to save a level
#if ship_id is changed, this function needs to be changed as well
def saveGame(sectornum, object_list, width, height):
    if sectorGeneration(sectornum) and object_list[4] not in [1, 5]:
        saveObjects(sectornum, [-1], width, height)
    else:
        saveObjects(sectornum, object_list[:], width, height)

def _processListForSave(save_list, width, height):
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
    _processListForSave(save_list, width, height)
    
    resave_list = filehelper.loadObj(6)
    resave_list[sectornum-1] = save_list

    filehelper.saveObj(resave_list, 6)

def _processListFromSave(object_list, width, height):
    # turning x and y float percentages back into coords
    if len(object_list) >= 8:
        for i in range(len(object_list)):
            if i % 8 == 0:
                object_list[i] = round(object_list[i]*width)     
            if i % 8 == 1:
                object_list[i] = round(object_list[i]*height)

#extracts the list saveObjects saved to file
def getObjects(sectornum, width, height):
    object_list = filehelper.loadObj(6)[sectornum-1]

    if object_list == [-1]:
        object_list = ["PLEASE GENERATE"]
    if len(object_list) > 1:
        if sectorGeneration(sectornum) and object_list[4] not in [1,5]:
           object_list = ["PLEASE GENERATE"] 
                    
    if object_list != ["PLEASE GENERATE"]:
        _processListFromSave(object_list, width, height)
        for i in range(int(len(object_list)/8)):
            if object_list[4+i*8] == 2 or object_list[4+i*8] == 8:
                object_list[7+i*8] = -10 #gets rid of shots and alien shots when entering a sector
    return object_list

#deletes everyinstance of toDelete type in the delSector - only changes the file doesn't change anything in play
def deleteObject(toDelete, delSector, width, height):
    object_list = getObjects(delSector, width, height)
    deletedex = ""
    for i in range(0, len(object_list), 8):
        if object_list[i+4] == toDelete:
            deletedex = i
    if deletedex != "":
        del object_list[deletedex:deletedex+8]
    saveGame(delSector, object_list, width, height)

#mini program to replace the star fields of pre-generated sectors when star generation is changed
def _changeStars(sectornum):
    d_stars = [100, 101, 102, 103, 104, 105]
    newstars = generateStars(1920,1080)
    sector1 = getObjects(sectornum, 1920, 1080)
    for i in range(0, len(sector1), 8):
        if sector1[i+4] in d_stars:
            sector1[i+7] = -1
    sector1 = deaderizer(sector1)
    sector1 += newstars
    saveObjects(sectornum, sector1, 1920, 1080)

def _discretionaryactivity():
    print("working on corrections...")
    obj = getObjects(1, 1920, 1080)
    obj = obj[8:]
    saveObjects(1, obj, 1920, 1080)
