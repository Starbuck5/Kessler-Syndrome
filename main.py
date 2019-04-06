import math
import random
import pygame

from pgx import *
from level1 import *
from game import *
from UIscreens import *
import graphics
                                                
#backened for collinfo, returns hitboxes when given an index of the objectlist
def getHitbox(object_list, object_location, scalar3, graphlist):
    xpos = object_list[object_location*8]
    ypos = object_list[1+object_location*8]
    objectID = object_list[4+object_location*8]
    rotation = object_list[5+object_location*8]
    
    hitBox = [xpos, ypos, 0,0]
    if objectID == 1 or objectID == 5: #main ship
        hitBox = [xpos-15*scalar3, ypos-15*scalar3, 30*scalar3, 30*scalar3]
    elif objectID == 2 or objectID == 8: #shots
        hitBox = [xpos-2, ypos-2, 4, 4]
    elif objectID == 6: #aliens
        hitBox = [xpos, ypos, 60, 60]
    elif objectID == 0: #zvezda
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation, False)
    elif 9 < objectID < 40: #pixel things
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation)
    elif objectID == 7: #alien mines
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation)
    elif objectID == 9:
        scale = 1 + (.1 * (300 - object_list[object_location*8+7]))
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation, False, scale)
    elif 69 < objectID < 100: #asteroids
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation)
    return hitBox

#returns true if there is a collision between two objects, returns false otherwise
def collinfo(object_number1, object_number2, object_list, scalar3, graphlist, DEVMODE):
    intersection = False
    if object_number1 != object_number2: #exempts object intersecting itself
        #hitBox = [xpos, ypos, width, height]

        hitBox1 = getHitbox(object_list, object_number1, scalar3, graphlist)
        hitBox2 = getHitbox(object_list, object_number2, scalar3, graphlist)

        # shows all the hitboxes
        if DEVMODE:
            if hitBox1[2] != 0 and hitBox1[3] != 0:
                pygame.draw.rect(screen, (255,255,255), hitBox1, 3)
            if hitBox2[2] != 0 and hitBox1[3] != 0:
                pygame.draw.rect(screen, (255,255,255), hitBox2, 3)
        
        if hitBox1[2] != 0 and hitBox1[3] != 0 and hitBox2[2] != 0 and hitBox1[3] != 0:
            if pygame.Rect(hitBox1).colliderect(pygame.Rect(hitBox2)):
                intersection = True
    return intersection

#sound effects for collision        
def explosion_sounds():
    explosion_picker = random.randint(0,1)
    if explosion_picker == 0:
        SoundVault.play('explosion1')
    if explosion_picker == 1:
        SoundVault.play('explosion2')

#wrapper for saveObjects that determines how to save a level
def saveGame(sectornum, object_list, width, height):
    if sectorGeneration(sectornum):
        saveObjects(sectornum, [-1], width, height)
    else:
        saveObjects(sectornum, object_list[:], width, height)

#saves objectlist to file by breaking it into a maximum of 5 lines
def saveObjects(sectornum, save_list, width, height):
    for i in range(len(save_list)):
        if isinstance(save_list[i], float):
            save_list[i] = round(save_list[i], 1)
        if len(save_list) >= 8:
            # turning x and y coords into float percentages
            if i % 8 == 0:
                save_list[i] = round(save_list[i]/width, 3)
            if i % 8 == 1:
                save_list[i] = round(save_list[i]/height, 3)
                        
    if len(save_list) >= 1000:
        save_list = save_list[:1000]
        print("Error: overflow in Main/saveObjects")
    savelist = []
    listhelper = int(len(save_list)/200) #200 = entities per level
    for i in range(listhelper):
        savelist.append(save_list[:200])
        save_list = save_list[200:]
    savelist.append(save_list)    
    listhelper = 5- len(savelist)
    for i in range(listhelper):
        savelist.append([])    
    for i in range(5):
        filehelper.set(savelist[i], sectornum*5+i)

#extracts the list saveObjects saved to file
def getObjects(sectornum, width, height):
    object_list = []
    for i in range(5):
        object_list += filehelper.get(sectornum*5+i)
    if object_list != []:
        while object_list[-1] == '':
            object_list.pop()
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

#used by the map to actually draw out the sectors
def drawSector(location, number, currentsector):
    secsize = 80 #side length of the cubes
    if number != currentsector:
        pygame.draw.rect(screen, (255,255,255), (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
    if number == currentsector:
        pygame.draw.rect(screen, (255,15,25), (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
        Texthelper.write(screen, [(location[0]-35, location[1]-35), "U R Here", 1])
    Texthelper.write(screen, [(location[0]-len(str(number))*10, location[1]-15), str(number), 2])

           
def main():
    global screen
    file_settings = filehelper.get(0) #grabs settings from file

    #sets adjustable settings
    width = int(file_settings[0])
    height = int(file_settings[1])
    max_asteroids = 8
    drag = [1,5]

    #scaling
    scalarscalar = height / 1080
    scalar2 = 1.5 * scalarscalar # controls asteroid size
    scalar3 = 1.2 * scalarscalar # controls ship size
    sat_scalar = 1 * scalarscalar #controls satellite size
    alien_size = [1.2 * scalarscalar, 1.8 * scalarscalar]

    #graphical setup
    graphlist = [scaleImage(loadImage("Assets\\images\\sat1.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat2.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat3.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat4.tif"), sat_scalar),
                 "s", "d", "f", "h", "j", "k", "l", "a", "s", "e", "as", "4", "3", "2", "1", "x11",
                 loadImage("Assets\\images\\solarpanel.tif")]
    earthpic = loadImage("Assets\\images\\earth.tif")
    infinitypic = loadImage("Assets\\images\\infinity.tif")

    # settings
    max_speed = 4 * scalarscalar
    missile_lifespan = 130 * scalarscalar
    missile_accel = 7 * scalarscalar
    step_x = 0.08 * scalarscalar
    step_y = 0.08 * scalarscalar
    step_r = 2.3
    step_drag = 0.004 * scalarscalar
    max_asteroid_spd = 270 * scalarscalar
    color = (0, 0, 0) # for background
    shield_lifespan = 300
    DEVMODE = False

    # pygame setup
    pygame.init()
    pygame.display.set_caption("Kessler Syndrome")
    logo = loadImage("Assets\\images\\earth2.png")
    logo.set_colorkey((255,0,0))
    pygame.display.set_icon(logo)
    if width == 0 or height == 0:
        screen_sizes = pygame.display.list_modes()
        screen_sizes = screen_sizes[0]
        width = screen_sizes[0]
        height = screen_sizes[1]
    if file_settings[2]:
        screen = pygame.display.set_mode([width, height], pygame.NOFRAME | pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()

    #sound setup
    SoundVault("explosion1", "Assets\\sounds\\Bomb1.wav", volume=0.1)
    SoundVault("explosion2", "Assets\\sounds\\Bomb2.wav", volume=0.1)
    SoundVault("money", "Assets\\sounds\\clink.wav")
    SoundVault("death", "Assets\\sounds\\powerfailure.wav", volume=0.2)
    SoundVault("portal", "Assets\\sounds\\electric.wav", volume=0.15)
    SoundVault("shot", "Assets\\sounds\\shot.wav", volume=0.25)

    # variable setup
    playerinfo = filehelper.get(1)
    d_parts = [30]
    d_sats = [10, 11, 12, 13]
    d_asteroids = [70, 71, 72, 73, 80, 81, 82, 83, 90, 91, 92, 93]
    ship_id = [1, 5]
    status = "menuinit"
    flame = False
    sectornum = 1
    portalcoordsRevised = [[[0, height/2], [60, height/2-80], [60, height/2+80]],
                           [[width/2, 0], [width/2-80, 60],[width/2+80, 60]],
                           [[width, height/2], [width-60, height/2-80], [width-60, height/2+80]],
                           [[width/2, height], [width/2+80, height-60], [width/2-80, height-60]]]
    portalRects = []
    for i in range(len(portalcoordsRevised)):
        portalRects.append(pointsToRect(portalcoordsRevised[i]))
    lasttransit = 0
    timer_popupmenu = 0
    timer_shipdeath = 9500
    portal_toggle = False
    timer_portal_toggle = 0
    #locations for all sector icons on map screen, in order
    sector_map_coordinates = [(960, 990), (820, 970), (1110, 980), (810, 840), (970, 830), (965, 690), (1115, 680),
                              (830, 675), (1060, 525), (865, 535), (830, 400), (700, 630), (690, 455), (1095, 385),
                              (1055, 250), (840, 245), (965, 415), (870, 105), (1030, 90)]

    # class setup
    Asteroid(scalar2) #sets up Asteroid class to return lists of the appropriate scale
    Screenhelper(width,height)
    #texthelper setup for scaling
    Texthelper.scalar = scalarscalar
    Texthelper.width = width
    Texthelper.height = height
    #announcementbox setup
    AnnouncementBox.width = width
    AnnouncementBox.height = height

    #graphics setup
    graphics.init(d_asteroids, d_parts, d_sats, graphlist)
    
    
    running = True
    while running:
        clock.tick(100)
        collect_inputs() #syncs up event queue in pgx
        timer_popupmenu += 1
        timer_popupmenu = min(timer_popupmenu, 10000)
        timer_shipdeath += 1
        timer_shipdeath = min(timer_shipdeath, 10000)
        timer_portal_toggle += 1
        timer_portal_toggle = min(timer_portal_toggle, 10000)
     
        if status == "menuinit":
            pygame.mouse.set_visible(True)
            screen.fill(color)
            status = "menu" 

        if status == "menu": #if game is in menu
            # actual text
            Texthelper.write(screen, [(300, 540-200), "Kessler Syndrome", 7])
            
            # buttons
            text_input = [(410, 540-50), "[Play]", 3]
            if Texthelper.writeButton(screen, text_input):
                status = "gameinit"
            text_input = [(410, 550), "[Quit to desktop]", 3]
            if Texthelper.writeButton(screen, text_input): #if "quit to desktop" is clicked           
                pygame.quit() #stop the program
                raise SystemExit #close the program            
            screen.blit(earthpic, (1500,800))
            pygame.display.flip()
            
        if status == "pauseinit":
            filehelper.set([currentarmor, currentfuel, ammunition], 4)
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
            Font.set_scramble_paused(True) #pauses any scrambling going on
            drawPauseUI(screen, True)
            
            #saving objectlist, sector achievements data
            saveGame(sectornum, object_list[:], width, height)
            discovery = ""
            for i in range(len(discoverSector)):
                if discoverSector[i] == False:
                    discovery += "8"
                else:
                    discovery += "1"
            filehelper.setElement(discovery, 1, 2)
            
            status = "paused"

        if status == "paused":
            status = drawPauseUI(screen, False)
            inputvar = keyboard()
            if ("p" in inputvar or "escape" in inputvar) and timer_popupmenu > 25:
                status = "game"
                timer_popupmenu = 0
            if status != "paused":
                Font.set_scramble_paused(False) #resumes any scrambling going on
                pygame.mouse.set_visible(False)

        if status == "mapscreeninit":
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
           
            line_color = (255, 255, 255)

            for i in range(len(sector_map_coordinates)):
                drawSector(sector_map_coordinates[i], i + 1, sectornum)
                if sectorGeneration(i + 1): #draws infinity signs on map if regenerating sector
                    screen.blit(infinitypic, (sector_map_coordinates[i][0] - 10, sector_map_coordinates[i][1] + 15)) 
                #draws all links between sectors
                connections = sectorDestinations(i + 1)
                for j in range(4):
                    if connections[j] != -1:
                        if j == 0:
                            line_start = (sector_map_coordinates[i][0] - 40, sector_map_coordinates[i][1])
                            line_end = (sector_map_coordinates[connections[j] - 1][0] + 40,
                                        sector_map_coordinates[connections[j] - 1][1])
                        elif j == 1:
                            line_start = (sector_map_coordinates[i][0], sector_map_coordinates[i][1] - 40)
                            line_end = (sector_map_coordinates[connections[j] - 1][0],
                                        sector_map_coordinates[connections[j] - 1][1] + 40)
                        elif j == 2:
                            line_start = (sector_map_coordinates[i][0] + 40, sector_map_coordinates[i][1])
                            line_end = (sector_map_coordinates[connections[j] - 1][0] - 40,
                                        sector_map_coordinates[connections[j] - 1][1])
                        elif j == 3:
                            line_start = (sector_map_coordinates[i][0], sector_map_coordinates[i][1] + 40)
                            line_end = (sector_map_coordinates[connections[j] - 1][0],
                                        sector_map_coordinates[connections[j] - 1][1] - 40)
                        pygame.draw.aaline(screen, line_color, line_start, line_end)

            status = mapscreenUI(screen)            
            pygame.display.flip()
            status = "mapscreen"

        if status == "mapscreen":
            status = mapscreenUI(screen)
            inputvar = keyboard()
            if ("m" in inputvar or "escape" in inputvar) and timer_popupmenu > 25:
                status = "game"
                timer_popupmenu = 0

            if DEVMODE:
                if Texthelper.writeButton(screen, [(180, 600), "[teleport home]", 2.5]):
                    saveGame(sectornum, object_list, width, height)
                    sectornum = 1
                    lasttransit = 0
                    new_objects = getObjects(sectornum, width, height)
                    lastnumdebris = 0
                    if new_objects[0] == -1 and len(new_objects)<8:
                        object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height,
                            d_sats, d_parts, d_asteroids)
                    else:
                        object_list = object_list[:8] + new_objects[8:]
                    object_list[2] = 0  #kills momentum
                    object_list[3] = 0
                    status = "game"

                for i in range(len(sector_map_coordinates)):
                    if Texthelper.writeButton(screen, [(sector_map_coordinates[i][0] - len(str(i + 1)) * 10,
                                                        sector_map_coordinates[i][1] - 15), str(i + 1), 2]):
                        saveGame(sectornum, object_list, width, height)
                        sectornum = i + 1
                        lasttransit = 0
                        new_objects = getObjects(sectornum, width, height)
                        lastnumdebris = 0
                        if new_objects[0] == -1 and len(new_objects)<8:
                            object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height,
                                d_sats, d_parts, d_asteroids, sectornum)
                        else:
                            object_list = object_list[:8] + new_objects[8:]
                        object_list[2] = 0  #kills momentum
                        object_list[3] = 0
                        status = "game"

            if status == "game":
                pygame.mouse.set_visible(False)

            pygame.display.flip()

        if status == "exiting":
            pygame.quit()
            raise SystemExit

        if status == "homeinit":
            filehelper.set([currentarmor, currentfuel, ammunition], 4)
            fuelHelp = upgrades.get(ShipLv[1]+20)
            totalfuel = fuelHelp[4]
            armorHelp = upgrades.get(ShipLv[0])
            totalarmor = armorHelp[4]
            totalammunition = 0
            if ShipLv[2] == 0:
                totalammunition = 0
            else:
                ammunitionHelp = upgrades.get(ShipLv[2]+40)
                totalammunition = ammunitionHelp[4]
            screen.fill(color)
            homeInventory = filehelper.get(2)
            homeinitUI(screen, homeInventory)
            pygame.display.flip()
            ShipLv = filehelper.get(3)
            currentStats = filehelper.get(4)
            totalStats = (totalarmor, totalfuel, totalammunition)
            setupShop(ShipLv, shipInventory, homeInventory, currentStats, totalStats, color)
            status = "home"
            
        if status == "home":
            status = home(screen)
            if status != "home": #so when the code is exiting this part
                pygame.mouse.set_visible(False)
                totalarmor, totalfuel, totalammunition = shopStorage.totalStats
                currentarmor, currentfuel, ammunition = shopStorage.currentStats
                filehelper.set(shopStorage.currentStats, 4)
                filehelper.set(ShipLv, 3)
                filehelper.set(homeInventory, 2)
                if status == "game":
                    for i in range(0, len(object_list), 8):
                        object_number = object_list[i+4]
                        if object_number == 0:
                            dockPosition = dock(object_list[i], object_list[i+1], graphics.Images.get(0))
                            for i2 in range(0, len(object_list), 8):
                                if object_list[4 + i2] == 1:
                                    object_list[i2] = dockPosition[0]
                                    object_list[i2+1] = dockPosition[1]
                                    object_list[i2+2] = dockPosition[2]
                                    object_list[i2+3] = dockPosition[3]
                                    object_list[i2+5] = dockPosition[4]

        if status == "gameinit":       
            # changing variable setup
            object_list = getObjects(sectornum, width, height)
            previous_tick = 0
            previous_tick2 = 0
            scalar1 = 0
            lastnumdebris = 0
            pygame.mouse.set_visible(False)
            #inventory
            shipInventory = [0,0,0,0]

            #fuel and armor and ammunition
            upgrades = Filehelper("assets\\upgrades.txt")
            ShipLv = filehelper.get(3)
            fuelHelp = upgrades.get(ShipLv[1]+20)
            totalfuel = fuelHelp[4]
            currentfuel = filehelper.get(4)[1]
            armorHelp = upgrades.get(ShipLv[0])
            totalarmor = armorHelp[4]
            currentarmor = filehelper.get(4)[0]
            totalammunition = 0
            if ShipLv[2] == 0:
                totalammunition = 0
            else:
                ammunitionHelp = upgrades.get(ShipLv[2]+40)
                totalammunition = ammunitionHelp[4]
            ammunition = filehelper.get(4)[2]

            #initializes printouts of fuel and armor and ammo
            graphics.InfoBars.init(graphics.FlashyBox([1590, 990, 280, 70], 0.2, (255,0,0)),
                                   graphics.FlashyBox([1590, 920, 280, 70], 0.2, (255,0,0)))

            for i in range(0, len(object_list), 8):
                        object_number = object_list[i+4]
                        if object_number == 0:
                            dockPosition = dock(object_list[i], object_list[i+1], graphics.Images.get(0))
                            for i2 in range(0, len(object_list), 8):
                                if object_list[4 + i2] == 1:
                                    object_list[i2] = dockPosition[0]
                                    object_list[i2+1] = dockPosition[1]
                                    object_list[i2+2] = dockPosition[2]
                                    object_list[i2+3] = dockPosition[3]
                                    object_list[i2+5] = dockPosition[4]
            
            #game progression
            discoverSector = filehelper.get(1)[2]
            discoverSector = list(str(discoverSector))
            for i in range(len(discoverSector)):
                if discoverSector[i] == "8":
                    discoverSector[i] = False
                else:
                    discoverSector[i] = True
                
            if file_settings[3] == 0:
                level1(screen, width, height)
                file_settings[3] = 1
                filehelper.set(file_settings, 0)
                file_settings = filehelper.get(0)

            if file_settings[3] == 1:
                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Hey you, still alive out there? Then go pick up some space debris like a good prisoner")
                file_settings[3] = 2
                filehelper.set(file_settings, 0)
            
            status = "game"

        if status == "game":
            screen.fill(color)
            AnnouncementBox.play(screen)
            Font.timerhelper() #once a game loop update to a scramble timer
            
            # input handling
            inputvar = keyboard()
            ticks = pygame.time.get_ticks()
            if inputvar:
                if object_list[4] == 1:
                    thrust_vector = (math.cos(math.radians(object_list[5]-90)),
                                     math.sin(math.radians(object_list[5]+90)))
                    if "w" in inputvar or "uparrow" in inputvar:
                        object_list[2] += step_x * thrust_vector[0]
                        object_list[3] += step_y * thrust_vector[1]
                        flame = True
                    if "e" in inputvar or "rightarrow" in inputvar:
                        object_list[5] += step_r
                    if "q" in inputvar or "leftarrow" in inputvar:
                        object_list[5] -= step_r
                    if "space" in inputvar and (ticks - previous_tick) > 360 and ammunition > 0:
                        ammunition -= 1
                        SoundVault.play('shot')
                        xmom_miss = object_list[2] + (thrust_vector[0] * missile_accel)
                        ymom_miss = object_list[3] + (thrust_vector[1] * missile_accel)
                        front_pointlist = RotatePoint(object_list[0], object_list[1],
                                                      [object_list[0], object_list[1]-30*scalar3], object_list[5])
                        object_list_addition = [front_pointlist[0][0], front_pointlist[0][1], xmom_miss, ymom_miss, 2,
                                                "NA", "NA", missile_lifespan]
                        object_list += object_list_addition
                        previous_tick = ticks
                if "shift" in inputvar and "c" in inputvar and (ticks - previous_tick2) > 360:
                    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while color[0] + color[1] + color[2] > 150:
                        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    previous_tick2 = ticks
                if "m" in inputvar and timer_popupmenu > 25:
                    timer_popupmenu = 0
                    status = "mapscreeninit"
                if ("escape" in inputvar or "p" in inputvar or "windows" in inputvar) and len(inputvar) == 1:
                    if timer_popupmenu > 25:
                        timer_popupmenu = 0
                        status = "pauseinit"
                lasttransit += 1
                if "shift" in inputvar and "d" in inputvar and (ticks - previous_tick2) > 360:
                    DEVMODE = not DEVMODE #switches booleans
                    previous_tick2 = ticks
                if "shift" in inputvar and "f" in inputvar and (ticks - previous_tick2) > 360:
                    colorA = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while colorA[0] + colorA[1] + colorA[2] > 150:
                        colorA = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    Font.changeColor(colorA)
                    previous_tick2 = ticks
                if "t" in inputvar and timer_portal_toggle > 30:
                    portal_toggle = not portal_toggle
                    timer_portal_toggle = 0
            # input handling

            # collision detection                         
            for i in range(int(len(object_list)/8)):
                i2 = i + 1
                while i2 < int(len(object_list)/8):                   
                    if collinfo(i,i2,object_list, scalar3, graphlist, DEVMODE) == True:
                        printerlist_add = []
                        drops = [0,0,0,0] #why is this here?
                        if object_list[4 + (i * 8)] == 1 and object_list[4 + (i2 * 8)] in d_sats: #ship v satellite
                            xForce = abs(object_list[2+(i*8)] - object_list[2+(i2*8)]) 
                            yForce = abs(object_list[3+(i*8)] - object_list[3+(i2*8)])
                            force = (xForce + yForce)*2
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                             object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            drops = satelliteDrops()
                            if drops[3]: #if currency is dropped
                                SoundVault.play('money')
                            #merges the two lists by adding their like elements together
                            shipInventory = [a + b for a, b in zip(shipInventory, drops)]
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] in d_parts: #ship v debris
                           printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                            object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                           object_list[(i2*8)+7] = -1
                           drops = solarPanelDrops()
                           shipInventory = [a + b for a, b in zip(shipInventory, drops)]                            
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] == 0: #going to garage
                            Texthelper.writeBox(screen, [(800,500), "press enter", 1], color = (0,100,200))
                            if "enter" in inputvar:
                                status = "homeinit"
                        elif object_list[4 + (i * 8)] in ship_id and 69 < object_list[4 + (i2 * 8)] < 100: #ship v asteroid
                            xForce = abs(object_list[2+(i*8)] - object_list[2+(i2*8)]) 
                            yForce = abs(object_list[3+(i*8)] - object_list[3+(i2*8)])
                            force = (xForce + yForce)*2
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                             object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            if force < 5:
                                drops[0] = 1
                            else:
                                currentarmor = currentarmor - (int(force) - 5)
                                Font.scramble(100) #scrambles text for 100 ticks
                            explosion_sounds()
                        elif object_list[4 + (i2 * 8)] == 2 and 69 < object_list[4 + (i * 8)] < 100: #missile v asteroid
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                            explosion_sounds()
                        elif object_list[4 + (i2 * 8)] == 2 and object_list[4 + (i * 8)] in d_parts: #missile v debris
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                            explosion_sounds()
                        elif object_list[4 + (i2 * 8)] == 2 and object_list[4 + (i * 8)] in d_sats: #missile v sats
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                            explosion_sounds()
                        elif object_list[4 + (i2 * 8)] == 2 and object_list[4 + (i * 8)] == 7: #missile v mine
                            printerlist_add += [object_list[(i * 8)], object_list[1+(i * 8)], object_list[2+(i*8)],
                                                object_list[3+(i*8)], 9, "NA", "NA", 300]
                            object_list[(i*8)+7] = -1
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] == 7: #ship v mine
                            printerlist_add += [object_list[(i2 * 8)], object_list[1+(i2 * 8)], object_list[2+(i2*8)],
                                                object_list[3+(i2*8)], 9, "NA", "NA", 300]
                            object_list[(i2*8)+7] = -1
                            object_list[4] = 5
                            object_list[7] = 200
                            Font.scramble(200)
                            currentarmor -= 1
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] == 9: #ship v explosion
                            object_list[4] = 5
                            object_list[7] = 200
                            Font.scramble(200)
                            currentarmor -= 0.03
                        object_list += printerlist_add
                    i2 += 1            
            # collision detection

            #portals
            if portal_toggle: # ship collision with portal
                destinations = sectorDestinations(sectornum)
                for i in range(4):
                    if destinations[i] != -1:
                        pygame.gfxdraw.aapolygon(screen, portalcoordsRevised[i], (100,149,237))
                        pygame.gfxdraw.filled_polygon(screen, portalcoordsRevised[i], (100,149,237))
                        isValidTransfer = object_list[4] == 1 or object_list[4]==5 #if the first thing in object_list is allowed to transit
                        isValidTime = lasttransit > 100
                        isValidCollision = portalRects[i].collidepoint((object_list[0], object_list[1]))                        
                        if isValidTransfer and isValidTime and isValidCollision:
                            SoundVault.play('portal')
                            saveGame(sectornum, object_list, width, height)
                            sectornum = destinations[i]
                            lasttransit = 0
                            new_objects = getObjects(sectornum, width, height)
                            lastnumdebris = 0
                            if new_objects[0] == -1 and len(new_objects)<8:
                                object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height,
                                                      d_sats, d_parts, d_asteroids, sectornum)
                            else:
                                object_list = object_list[:8] + new_objects[8:]
                            #recordings needed
                            if sectornum == 4 and discoverSector[3] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Took you long enough to get here. Now clear this sector.")
                                discoverSector[3] = True
                            if sectornum == 6 and discoverSector[5] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "I see you finally decided to travel further. Better pray before you die.")
                                discoverSector[5] = True
                            if sectornum == 9 and discoverSector[8] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Congrats, you finally made it to the land of explosives. Have fun out there.")
                                discoverSector[8] = True
                            if sectornum == 12 and discoverSector[11] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Wow, you are so slow. Just clean this mess up before i get bored and launch rockets at you.")
                                discoverSector[11] = True
                            if sectornum == 17 and discoverSector[16] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "I see you found some more debris to clean up, make it quick.")
                                discoverSector[16] = True
                            if sectornum == 19 and discoverSector[18] == False:
                                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Take a look at this, this is the edge of your cleaning zone. Nothing more to do other than to keep cleaning for the rest of your life.")
                                discoverSector[18] = True

            # reward for killing a sector
            numdebris = 0
            for i in range(0, len(object_list), 8):
                if object_list[i+4] not in [0, 100, 1, 2, 8, 6, 4, 5]:
                    numdebris += 1
            if numdebris == 0 and lastnumdebris > 0:
                shipInventory[3] += 100 #adds 100 credits to ship inventory
                SoundVault.play('money')
                if not playerinfo[1]:
                    playerinfo[1] = True
                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                    pygame.mixer.Sound(file="Assets\\announcements\\reward2.wav"),                             
                                    "Nice job clearing your first sector, here's some cash. Don't get lazy now!")
                    filehelper.set(playerinfo, 1)

            lastnumdebris = numdebris

            # deaderizer
            object_list = deaderizer(object_list)
            
            # fuel consumption
            if flame == True:
                currentfuel -= 1

            #HACKZ
            if DEVMODE:
                currentfuel = totalfuel
                currentarmor = totalarmor
                ammunition = totalammunition
                
            #ship death
            if currentarmor <= 0 or currentfuel <= 0:
                saveGame(sectornum, object_list, width, height)
                object_list += particlemaker(object_list[0], object_list[1], object_list[2], object_list[3])
                object_list += particlemaker(object_list[0], object_list[1], object_list[2], object_list[3])
                SoundVault.play('death')
                object_list[7] = -10
                currentfuel = totalfuel
                currentarmor = totalarmor
                shipInventory = [0,0,0,0]
                lasttransit = 0
                timer_shipdeath = 0

            if timer_shipdeath == 200:
                sectornum = 1
                lastnumdebris = 0
                object_list = getObjects(sectornum, width, height)
                object_list[0] = width/2 - width*0.3
                object_list[1] = height/2 - height*0.2
                object_list[2] = 0
                object_list[3] = 0

            #physics!
            doPhysics(object_list, width, height, max_speed, drag, step_drag)

            # printer
            graphics.printer(screen, object_list, scalar1, scalar3, graphlist, scalarscalar, flame)
            graphics.InfoBars.draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition, totalammunition)
            ####inventory
            inventory_string = "metal:" + str(shipInventory[0]) + "   gas:" + str(shipInventory[1]) 
            inventory_string += "   circuits:" + str(shipInventory[2]) + "    currency:" + str(shipInventory[3])
            Texthelper.write(screen, [(0, 0), inventory_string,3])
            if DEVMODE:
                Texthelper.write(screen, [(1800, 20), str(round(clock.get_fps())),3]) 
            flame = False
            pygame.display.flip()
            # printer
       
        for event in AllEvents.TICKINPUT:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit


#checks if it needs to run setupper
if filehelper.get(0)[0] == "?":
    import setupper
    setupper.setup()
    
main()
