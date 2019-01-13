import random

#particle effects
def particlemaker(xpos, ypos, xmom, ymom):
    # particle settings
    particle_lifespan = 45
    random_factor = 30 # higher number = less random
    max_particles = 6
    max_deviation = 2
    printerlist_add = []
    for i in range(random.randint(max_particles - max_deviation, max_particles)):
        printerlist_add += [xpos, ypos, xmom + ((random.randint(-20, 20))/random_factor), ymom + ((random.randint(-20, 20))/random_factor), 4, "N/A", particle_lifespan, True]      
    return printerlist_add

#physics handling
def doPhysics(object_list, width, height, max_speed, drag, step_drag):
    for i in range(int(len(object_list)/8)):
        #decaying objects
        if object_list[7 + (i * 8)]:
            object_list[6 + (i * 8)] -= 1
            
        # edges section
        if object_list[0 + (i * 8)] > width:
            object_list[0 + (i * 8)] -= width
        if  object_list[0 + (i * 8)] < 0:
            object_list[0 + (i * 8)] += width
        if object_list[1 + (i * 8)] > height:
            object_list[1 + (i * 8)] -= height
        if object_list[1 + (i * 8)] < 0:
            object_list[1 + (i * 8)] += height

        # positioner
        object_list[0 + (i * 8)] += object_list[2 + (i * 8)]
        object_list[1 + (i * 8)] -= object_list[3 + (i * 8)]

        #drag
        if object_list[4 +(i*8)] in drag:
            stepper = abs(object_list[2 +(i*8)]) + abs(object_list[3 +(i*8)])
            if stepper == 0:
                stepper = 1
            step_drag_x = abs(object_list[2 +(i*8)]) / stepper * step_drag
            step_drag_y = abs(object_list[3 +(i*8)]) / stepper * step_drag   
            if object_list[2 +(i*8)] > 0 and object_list[2 +(i*8)] > step_drag_x:
                object_list[2 +(i*8)] -= step_drag_x
            elif step_drag_x > object_list[2 +(i*8)] > 0:
                object_list[2 +(i*8)] = 0
            if object_list[2 +(i*8)] < 0 and object_list[2 +(i*8)] < step_drag_x:
                object_list[2 +(i*8)] += step_drag_x
            elif step_drag_x < object_list[2 +(i*8)] < 0:
                object_list[2 +(i*8)] = 0     
            if object_list[3 +(i*8)] > 0 and object_list[3 +(i*8)] > step_drag_y:
                object_list[3 +(i*8)] -= step_drag_y
            elif step_drag_y > object_list[3 +(i*8)] > 0:
                object_list[3 +(i*8)] = 0   
            if object_list[3 +(i*8)] < 0 and object_list[3 +(i*8)] < step_drag_y:
                object_list[3 +(i*8)] += step_drag_y
            elif step_drag_y < object_list[3 +(i*8)] < 0:
                object_list[3 +(i*8)] = 0

        #speed limit for ship
        if object_list[4+(i*8)] == 1 or object_list[4+(i*8)] == 5:
            if object_list[2 + (i*8)] > max_speed:
                object_list[2 + (i*8)] = max_speed
            if object_list[2 + (i*8)] < -1 * max_speed:
                object_list[2 + (i*8)] =  -1 * max_speed
            if object_list[3 + (i*8)] > max_speed:
                object_list[3 + (i*8)] = max_speed
            if object_list[3 + (i*8)] < -1 * max_speed:
                object_list[3 + (i*8)] = -1 * max_speed

    return object_list

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

#leveler
def leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, shield_lifespan):
    object_list = object_list[:8]
    for i in range(20):
        object_list += [random.randint(0,100)/100*width, random.randint(0,100)/100*height, 0, 0, 100, "NA", 1, False]
    countervar = 0
    while countervar < random.randint(max_asteroids - 2, max_asteroids):
        asteroid_speedset = asteroidspeedmaker(max_asteroid_spd)                    
        object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0], asteroid_speedset[1]]
        object_list_add += [d_sats[random.randint(0, len(d_sats)-1)], 3, 1, False] 
        xdiff = object_list[0] - object_list_add[0]
        ydiff = object_list[1] - object_list_add[1]
        distance = ((xdiff ** 2) + (ydiff ** 2)) ** 0.5
        countervar += 1
        object_list += object_list_add
    if object_list[4] == 1 or object_list[4] == 3:
        object_list[4] = 5
        object_list[5] = 3
        object_list[6] = shield_lifespan
        object_list[7] = True
    return object_list


#deaderizer -- perhaps amalgamated into doPhysics in the future, just outside its main for loop
def deaderizer(object_list):
    indexadj = 0
    while indexadj < len(object_list): 
        if object_list[6 + indexadj] <= 0:
            if object_list[4+indexadj] == 5:
                object_list[7+indexadj] = False
                object_list[6+indexadj] = 1
                object_list[4+indexadj] = 1
            else:
                object_list = object_list[:indexadj] + object_list[8 + indexadj:]
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
        
        





















            
    
