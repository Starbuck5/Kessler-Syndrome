import random
import math

#particle effects
def particlemaker(xpos, ypos, xmom, ymom):
    # particle settings
    particle_lifespan = 45
    random_factor = 30 # higher number = less random
    max_particles = 6
    max_deviation = 2
    printerlist_add = []
    for i in range(random.randint(max_particles - max_deviation, max_particles)):
        printerlist_add += [xpos, ypos, xmom + ((random.randint(-20, 20))/random_factor), ymom + ((random.randint(-20, 20))/random_factor), 4, "NA", "NA", particle_lifespan]      
    return printerlist_add

#physics handling
def doPhysics(object_list, width, height, max_speed, drag, step_drag):
    for i in range(0, len(object_list), 8):
        #decaying objects
        if object_list[4 + i] in [2, 8, 5, 4]: #stuff in list should have a decrement to their life force
            object_list[7 + i] -= 1
            
        # edges section
        if object_list[i] > width:
            object_list[i] -= width
        if  object_list[i] < 0:
            object_list[i] += width
        if object_list[1 + i] > height:
            object_list[1 + i] -= height
        if object_list[1 + i] < 0:
            object_list[1 + i] += height

        # positioner
        object_list[i] += object_list[2 + i]
        object_list[1 + i] -= object_list[3 + i]

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

        #rotation
        if not isinstance(object_list[5+i], str):
            object_list[5+i] += object_list[6+i]/7 #the divided by moderates the speed of rotation
            if object_list[5+i] >= 360:
                object_list[5+i] -= 360
            if object_list[5+i] <= -360:
                object_list[5+i] += 360                

#helps out by setting entities to reasonable speeds
def asteroidspeedmaker(max_asteroid_spd):
    asteroid_speedset = []
    if random.randint(0,1) == 1:# if else statements institute a minimum horizontal and vertical speed (separately) of half the asteroid high speed
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
    for i in range(20):
        stars_list += [random.randint(0,width), random.randint(0,height), 0, 0, 100, "NA", "NA", 1]
    return stars_list

#leveler
def leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, shield_lifespan):
    object_list = object_list[:8]
    object_list += generateStars(width, height)
    countervar = 0
    while countervar < random.randint(max_asteroids - 2, max_asteroids):
        asteroid_speedset = asteroidspeedmaker(max_asteroid_spd)                    
        object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0], asteroid_speedset[1]]
        object_list_add += [d_sats[random.randint(0, len(d_sats)-1)], random.randint(0,360), random.randint(-10,10), 1] 
        xdiff = object_list[0] - object_list_add[0]
        ydiff = object_list[1] - object_list_add[1]
        distance = ((xdiff ** 2) + (ydiff ** 2)) ** 0.5
        countervar += 1
        object_list += object_list_add
    if object_list[4] == 1 or object_list[4] == 3:
        object_list[4] = 5
        object_list[7] = shield_lifespan
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
        indexadj += 8
    return object_list

def sectorDestinations(sectornum):
    #[left, up, right, down]
    if sectornum == 1:
        return [2, 5, 3, -1]
    if sectornum == 5:
        return [4, 6, -1, 1]
    if sectornum == 2:
        return [-1, 4, 1, -1]
    if sectornum == 3:
        return [1, -1, -1, -1]
    if sectornum == 4:
        return [-1, -1, 5, 2]
    if sectornum == 6:
        return [8, -1, 7, 5]
    if sectornum == 7:
        return [6, 9, -1, -1]
    if sectornum == 8:
        return [12, 10, 6, -1]
    if sectornum == 9:
        return [10, 14, -1, 7]
    if sectornum == 10:
        return [-1, 11, 9, 8]
    if sectornum == 11:
        return [13, 16, 17, 10]
    if sectornum == 12:
        return [-1, 13, 8, -1]
    if sectornum == 13:
        return [-1, -1, 11, 12]
    if sectornum == 14:
        return [-1, 15, -1, 9]
    if sectornum == 15:
        return [16, -1, -1, 14]
    if sectornum == 16:
        return [-1, 18, 15, 11]
    if sectornum == 17:
        return [11, -1, -1, -1]
    if sectornum == 18:
        return [-1, -1, 19, 16]
    if sectornum == 19:
        return [18, -1, -1, -1]
    else:
        return [1, 1, 1, 1] #in case you go into a sector that doesn't exist, it will redirect you to the home sector

#returns true if an infinite level that always regenerates
#else returns false to signal a level that doesn't get regenerated
def sectorGeneration(sectornum):
    output = False
    infinite_sectors = [4, 12, 14]
    if sectornum in infinite_sectors:
        output = True
    return output

def satelliteDrops():
    drops = [0, 0, 0, 0]
    if random.randint(1,100) <= 80:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[0] += 1
        elif 61 <= percentHelper <= 90:
            drops[0] += 2
        else:
            drops[0] += 3
    if random.randint(1,100) <= 40:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[1] += 1
        elif 61 <= percentHelper <= 90:
            drops[1] += 2
        else:
            drops[1] += 3
    if random.randint(1,100) <= 20:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[2] += 1
        elif 61 <= percentHelper <= 90:
            drops[2] += 2
        else:
            drops[2] += 3
    if random.randint(1,100) <= 70:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[3] += 5
        elif 61 <= percentHelper <= 90:
            drops[3] += 10
        else:
            drops[3] += 20
    return drops

def makeAsteroidList(scalar2): #generates a list of offsets for all of the separate asteroid designs
    asteroidlist = [[[17*scalar2, 1*scalar2], [12*scalar2, 8*scalar2], [-2*scalar2, 17*scalar2],
                     [-8*scalar2, 11*scalar2], [-16*scalar2, 3*scalar2], [-14*scalar2, -7*scalar2],
                     [-4*scalar2, -17*scalar2], [10*scalar2, -10*scalar2]],
                    [[16*scalar2, -3*scalar2], [12*scalar2, 10*scalar2], [-2*scalar2, 17*scalar2],
                     [-10*scalar2, 14*scalar2], [-19*scalar2, -2*scalar2], [-8*scalar2, -13*scalar2],
                     [2*scalar2, -16*scalar2], [8*scalar2, -12*scalar2]],
                    [[16*scalar2, 3*scalar2], [7*scalar2, 13*scalar2], [-8*scalar2, 14*scalar2],
                     [-18*scalar2, 4*scalar2], [-11*scalar2, -11*scalar2], [-3*scalar2, -16*scalar2],
                     [11*scalar2, -9*scalar2]],
                    [[18*scalar2, 0], [10*scalar2, -10*scalar2], [0*scalar2, -17*scalar2],
                     [-13*scalar2, -12*scalar2], [-20*scalar2, 0], [-11*scalar2, 11*scalar2],
                     [0*scalar2, 13*scalar2], [14*scalar2, 12*scalar2]],
                    "4", "5", "6", "7", "8", "9",
                    [[26*scalar2, -3*scalar2], [20*scalar2, 10*scalar2], [4*scalar2, 21*scalar2],
                     [-8*scalar2, 9*scalar2], [-8*scalar2, 10*scalar2], [-18*scalar2, 14*scalar2],
                     [-26*scalar2, 10*scalar2], [-25*scalar2, -1*scalar2], [-9*scalar2, -18*scalar2],
                     [10*scalar2, -12*scalar2], [19*scalar2, -16*scalar2]],
                    [[24*scalar2, 2*scalar2], [11*scalar2, 9*scalar2], [4*scalar2, 24*scalar2],
                     [-9*scalar2, 19*scalar2], [-22*scalar2, 5*scalar2], [-13*scalar2, -20*scalar2],
                     [3*scalar2, -24*scalar2], [18*scalar2, -13*scalar2]],
                    [[23*scalar2, -1*scalar2], [16*scalar2, 19*scalar2], [-4*scalar2, 26*scalar2],
                     [-13*scalar2, 13*scalar2], [-26*scalar2, 3*scalar2], [-17*scalar2, -20*scalar2],
                     [-4*scalar2, -23*scalar2], [16*scalar2, -14*scalar2]],
                    [[27*scalar2, 0], [15*scalar2, -15*scalar2], [0*scalar2, -25*scalar2],
                     [-21*scalar2, -15*scalar2], [-22*scalar2, 0],
                     [-19*scalar2, 15*scalar2], [0*scalar2, 24*scalar2], [21*scalar2, 17*scalar2]],
                    "14", "15", "16", "17", "18", "19",
                    [[33*scalar2, -4*scalar2], [27*scalar2, 23*scalar2], [-6*scalar2, 30*scalar2],
                     [-18*scalar2, 24*scalar2], [-32*scalar2, 5*scalar2], [-25*scalar2, -18*scalar2],
                     [6*scalar2, -30*scalar2], [20*scalar2, -22*scalar2]],
                    [[20*scalar2, 0], [24*scalar2, 24*scalar2], [-8*scalar2, 32*scalar2], [-23*scalar2, 18*scalar2],
                     [-33*scalar2, 5*scalar2], [-26*scalar2, -28*scalar2], [3*scalar2, -33*scalar2],
                     [27*scalar2, -22*scalar2]],
                    [[30*scalar2, 0], [26*scalar2, -22*scalar2], [3*scalar2, -33*scalar2],
                     [-22*scalar2, -22*scalar2], [-38*scalar2, 0], [-27*scalar2, 22*scalar2],
                     [3*scalar2, 34*scalar2], [30*scalar2, 23*scalar2]],
                    [[39*scalar2, 0], [29*scalar2, -22*scalar2], [0, -35*scalar2], [-28*scalar2, -20*scalar2],
                     [-37*scalar2, 0], [-24*scalar2, 23*scalar2], [0, 35*scalar2], [19*scalar2, 22*scalar2]],
                    "24", "25", "26", "27", "28", "29"]
    return asteroidlist

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
    currentPosition = 0
    for i in range(len(points)):
        revisedPoints += RotatePoint(xpos, ypos, points[i], rotationPosition)
    return revisedPoints

def dock(xpos, ypos, image):
    width = image.get_size()[0]
    height = image.get_size()[1]
    newXpos = xpos+(width/2)
    newYpos = ypos+height+10
    rotation = 90
    xmom = 0
    ymom = 0
    return (newXpos, newYpos, xmom, ymom, rotation)
      
class Asteroid():
    asteroidlist = "not yet a thing"
    scalar2 = -1
    def __init__ (self, scalar2):
        Asteroid.asteroidlist = makeAsteroidList(scalar2)
        Asteroid.scalar2 = scalar2

    def getPoints(xpos, ypos, objectID):
        offsetList = Asteroid.asteroidlist[objectID-70][:]
        pointList = []
        for i in range(len(offsetList)):
            pointList.append([xpos + offsetList[i][0], ypos + offsetList[i][1]])
        return pointList

    def getHitbox(xpos, ypos, objectID): # in rect format
        if 69 < objectID < 80:
            hitrange = 15
        if 79 < objectID < 90:
            hitrange = 20
        if 89 < objectID < 100:
            hitrange = 25
        return [xpos-hitrange*Asteroid.scalar2, ypos-hitrange*Asteroid.scalar2, hitrange*2*Asteroid.scalar2, hitrange*2*Asteroid.scalar2]
        
