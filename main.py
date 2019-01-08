import math
import random

import pygame
from pygame import gfxdraw
from pygame import Surface

from pgx import *
from level1 import *
from game import *
from UIscreens import *

#IDEA for resizing within savegames:
# store x and y coords as floats from 0.0 to 1.0
# maybe rounded to 4 decimal places


def printer2(ship_pointlist, object_list, color, scalar1, scalar3, graphlist, scalarscalar, specialpics):
    for i in range(int(len(object_list)/8)):
        xpos = object_list[(i * 8)]        
        ypos = object_list[1 + (i * 8)]
        object_number = object_list[4 + (i * 8)]
        
        if object_number == 100:
            screen.blit(specialpics[0], (xpos, ypos))
        if object_number == 0:
            screen.blit(specialpics[1], (xpos, ypos))
                
        if object_number == 1: #draws main ship
            pygame.gfxdraw.aapolygon(screen, ship_pointlist, (255,255,255))
            pygame.gfxdraw.filled_polygon(screen, ship_pointlist, (255,255,255))
        if object_number == 2 or object_number == 8: #draws missiles (id 8 are alien missiles)
            pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 2, 0)
        if object_number == 3: #draws reserve ships
            res_ship_pointlist = [[xpos, ypos-30*scalar3], [xpos+15*scalar3, ypos+10*scalar3], [xpos, ypos], [xpos-15*scalar3, ypos+10*scalar3]]
            pygame.gfxdraw.aapolygon(screen, res_ship_pointlist, (255,255,255))
            pygame.gfxdraw.filled_polygon(screen, res_ship_pointlist, (255,255,255))
        if object_number == 4: #draws explosion effects
            pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 1, 0)
        if object_number == 5: #draws shielded ship
            pygame.gfxdraw.aapolygon(screen, ship_pointlist, (100,100,100))
            pygame.gfxdraw.filled_polygon(screen, ship_pointlist, (100,100,100))
        if object_number == 6: #draws alien
            alien_pointlist = [[xpos-25*scalar1, ypos], [xpos-18*scalar1, ypos], [xpos-10*scalar1, ypos+8*scalar1], [xpos+10*scalar1, ypos+8*scalar1], [xpos+18*scalar1, ypos], [xpos+25*scalar1, ypos], [xpos-18*scalar1, ypos],
                            [xpos-10*scalar1, ypos], [xpos-7*scalar1, ypos-7*scalar1], [xpos, ypos-10*scalar1], [xpos+7*scalar1, ypos-7*scalar1], [xpos+10*scalar1, ypos]]
            pygame.draw.aalines(screen, (255,255,255), True, alien_pointlist, False)


        if 9 < object_number < 40:
            screen.blit(graphlist[object_number-10], (xpos, ypos))
        if 69 < object_number < 100:
            pygame.draw.aalines(screen, (255,255,255), True, Asteroid.getPoints(xpos, ypos, object_number), 4)
            


def portalcollision(object_list, portalcoords):
    if (portalcoords[0] < object_list[0] < portalcoords[0] + portalcoords[2] and portalcoords[1] < object_list[1] < portalcoords[1] + portalcoords[3]
        and (object_list[4] == 1 or object_list[4]==5)):
        return True
    else:
        return False

def explosion_sounds():
    explosion1 = pygame.mixer.Sound(handlePath("Assets\\Bomb1.wav"))
    explosion2 = pygame.mixer.Sound(handlePath("Assets\\Bomb2.wav"))
    explosion1.set_volume(0.05)
    explosion2.set_volume(0.05)
    explosion_picker = random.randint(0,1)
    if explosion_picker == 0:
        explosion1.play()
    if explosion_picker == 1:
        explosion2.play()

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
    return object_list

def drawSector(location, number):
    secsize = 80 #side length of the cubes
    pygame.draw.rect(screen, (255,255,255), (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
    if len(str(number)) == 1:
        Texthelper.write(screen, [(location[0]-10, location[1]-15), str(number), 2])
    else:
        Texthelper.write(screen, [(location[0]-20, location[1]-15), str(number), 2])
        
#just for generating backgrounds for manually built levels
def generateStars(width, height):
    object_list = []
    for i in range(20):
        object_list += [random.randint(0,100)/100*width, random.randint(0,100)/100*height, 0, 0, 100, "NA", 1, False]
    print(object_list)
    
def main():
    global screen
    file_settings = filehelper.get(0) #grabs settings from file

    #sets adjustable settings
    width = int(file_settings[0])
    height = int(file_settings[1])
    max_asteroids = 8
    drag = [1,5]

    #graphical setup
    graphlist = [loadImage("Assets\\sat1.tif"), loadImage("Assets\\sat2.tif"), loadImage("Assets\\sat3.tif"),
                 loadImage("Assets\\sat4.tif"), "s", "d", "f", "h", "j", "k", "l", "a", "s", "e", "as", "4", "3", "2", "1", #random elements to pad indices
                 loadImage("Assets\\solarpanel.tif")]
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)
    armorpic = loadImage("Assets\\armor.tif")
    earthpic = loadImage("Assets\\earth.tif")
    specialpics = [loadImage("Assets\\star.tif"), scaleImage(loadImage("Assets\\zvezda.tif"), 2)]
    infinitypic = loadImage("Assets\\infinity.tif")

    #scaling
    scalarscalar = height / 1080
    scalar2 = 1.5 * scalarscalar # controls asteroid size
    scalar3 = 1.2 * scalarscalar # controls ship size
    alien_size = [1.2 * scalarscalar, 1.8 * scalarscalar]

    #texthelper setup for scaling
    Texthelper.scalar = scalarscalar
    Texthelper.width = width
    Texthelper.height = height

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
    extratime_setter = 25
    FPSDISPLAY = True

    # pygame setup
    pygame.init()
    pygame.display.set_caption("Kessler Syndrome")
    logo = loadImage("Assets\\earth2.png")
    pygame.display.set_icon(logo)
    if width == 0 or height == 0:
        screen_sizes = pygame.display.list_modes()
        screen_sizes = screen_sizes[0]
        width = screen_sizes[0]
        height = screen_sizes[1]
    if file_settings[2] == "true":
        screen = pygame.display.set_mode([width, height], pygame.NOFRAME | pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([width, height])
        
    # variable setup
    d_parts = [30]
    d_sats = [10, 11, 12, 13, 71, 72, 73, 91]
    status = "menuinit"
    lower_rotation_constant = math.degrees(math.asin(10 / 325 ** 0.5))
    flame_rotation_constant = math.degrees(math.atan(6 / 5))
    flame = False
    menu_music_fadeout_OG = 1200
    menu_music_fadeout = menu_music_fadeout_OG
    clock = pygame.time.Clock()
    sectornum = 1
    portalcoords = [(0, height/2-75, 25, 150), (width/2-75, 0, 150, 25), (width-25, height/2-75, 25, 150), (width/2-75, height-25, 150, 25)]
    lasttransit = 0
    
    running = True
    while running:
        clock.tick(100)
     
        if status == "menuinit":
            # sound
            pygame.mixer.init()
            menu_music = pygame.mixer.Sound(handlePath("Assets\\AsteroidsTitle.wav"))
            menu_music.play(-1)
            menu_music.set_volume(0.4)
            menu_music_fadeout = menu_music_fadeout_OG

            pygame.mouse.set_visible(True)
            screen.fill(color)
            status = "menu" 

        if status == "menu": #if game is in menu
            # actual text
            text_input = [(300, 540-200), "Kessler Syndrome", 7]
            Texthelper.write(screen, text_input)
            
            # buttons
            text_input = [(410, 540-50), "[Play]", 3]
            if Texthelper.writeButton(screen, text_input):
                status = "gameinit"
                menu_music.fadeout(menu_music_fadeout)
            text_input = [(410, 550), "[Quit to desktop]", 3]
            if Texthelper.writeButton(screen, text_input): #if "quit to desktop" is clicked           
                pygame.quit() #stop the program
                raise SystemExit #close the program            
            screen.blit(earthpic, (1500,800))
            pygame.display.flip()
            
        if status == "pauseinit":
            pygame.mouse.set_visible(True)
            pauseinitUI(screen)
            saveObjects(sectornum, object_list[:], width, height)
            status = "paused"

        if status == "paused":
            status = pauseUI(screen)

        if status == "gameoverinit":            
            pygame.mouse.set_visible(True)
            gameoverinitUI(screen)
            status = "gameover"

        if status == "gameover":
            status = gameoverUI(screen)

        if status == "mapscreen":
            pygame.mouse.set_visible(True)
            #consider automating connection drawing by using a map drawing method that would look at sectordesinations
            drawSector((960, 990), 1)
            pygame.draw.aaline(screen, (255,255,255), (960-40, 990), (820+40, 970))
            drawSector((820, 970), 2)
            screen.blit(infinitypic, (800,855)) #x-10, y+15
            pygame.draw.aaline(screen, (255,255,255), (820, 970-40), (810, 840+40))
            drawSector((810, 840), 4)
            pygame.draw.aaline(screen, (255,255,255), (960, 990-40), (970, 830+40))
            pygame.draw.aaline(screen, (255,255,255), (810+40, 840), (970-40, 830))
            drawSector((970, 830), 5)
            pygame.draw.aaline(screen, (255,255,255), (960+40, 990), (1110-40, 980))
            drawSector((1110, 980), 3)
            pygame.draw.aaline(screen, (255,255,255), (970, 830-40), (965, 690+40))
            drawSector((965, 690), 6)
            pygame.draw.aaline(screen, (255,255,255), (965+40, 690), (1115-40, 680))
            drawSector((1115, 680), 7)
            pygame.draw.aaline(screen, (255,255,255), (965-40, 690), (830+40, 675))
            drawSector((830, 675), 8)
            pygame.draw.aaline(screen, (255,255,255), (830, 675-40), (865, 535+40))
            drawSector((865, 535), 10)
            pygame.draw.aaline(screen, (255,255,255), (1115, 680-40), (1060, 525+40))
            pygame.draw.aaline(screen, (255,255,255), (865+40, 535), (1060-40, 525))
            drawSector((1060, 525), 9)
            pygame.draw.aaline(screen, (255,255,255), (1060, 525-40), (1095, 385+40))         
            drawSector((1095, 385), 14)
            screen.blit(infinitypic, (1085,400)) #x-10, y+15
            drawSector((700, 630), 12)
            screen.blit(infinitypic, (690,645)) #x-10, y+15
            pygame.draw.aaline(screen, (255,255,255), (830-40, 675), (700+40, 630))
            pygame.draw.aaline(screen, (255,255,255), (865, 535-40), (830, 400+40))
            drawSector((830, 400), 11)
            pygame.draw.aaline(screen, (255,255,255), (700,630-40), (690,455+40))
            pygame.draw.aaline(screen, (255,255,255), (690+40, 455), (830-40, 400))
            drawSector((690, 455), 13)
            pygame.draw.aaline(screen, (255,255,255), (830+40, 400), (965-40, 415))
            drawSector((965, 415), 17)
            pygame.draw.aaline(screen, (255,255,255), (1095, 385-40), (1055, 250+40))
            drawSector((1055, 250), 15)
            pygame.draw.aaline(screen, (255,255,255), (840+40,245), (1055-40,250))
            pygame.draw.aaline(screen, (255,255,255), (830,400-40), (840,245+40))
            drawSector((840, 245), 16)
            pygame.draw.aaline(screen, (255,255,255), (840,245-40), (870,105+40))
            drawSector((870, 105), 18)
            pygame.draw.aaline(screen, (255,255,255), (870+40,105), (1030-40,90))
            drawSector((1030, 90), 19)
            status = mapscreenUI(screen) #<-- placeholder for static text or buttons relating to status that will eventually be on the map screen
            pygame.display.flip()

        if status == "exiting":
            pygame.quit()
            raise SystemExit

        if status == "garageinit":
            #ship lv [armor, fuel]
            ShipLv = filehelper.get(3)
            homeInventory = filehelper.get(2)
            garageinitUI(screen, ShipLv, homeInventory)
            status = "garage"

        if status == "garage":
            ShipLv = filehelper.get(3)
            homeInventory = filehelper.get(2)
            garageHelp = GarageUI(screen, ShipLv, homeInventory)
            status = garageHelp[0]
            ShipLv = garageHelp[1]
            homeInventory = garageHelp[2]
            filehelper.set(ShipLv,3)
            filehelper.set(homeInventory,2)
            if status == "game":
                shipInventory = [0,0,0,0]
                object_list[2] = 0
                object_list[3] = 0
                object_list[4] = 5
                object_list[6] = 500
                object_list[7] = True

        if status == "gameinit":       
            # changing variable setup
            object_list = getObjects(sectornum, width, height)
            rotation = 90
            serialnumber = 2
            extratime = extratime_setter
            extratime_trigger = False
            previous_tick = 0
            previous_tick2 = 0
            scalar1 = 0
            Asteroid(scalar2) #sets up Asteroid class to return lists of the appropriate scale

            # sound
            beat_timer = 250
            max_beat_timer = beat_timer
            beat1 = pygame.mixer.Sound(handlePath("Assets\\Beat1loud.wav"))
            beat1.set_volume(0.9)
            beat2 = pygame.mixer.Sound(handlePath("Assets\\Beat2loud.wav"))
            beat2.set_volume(0.9)
            missilesound = pygame.mixer.Sound(handlePath("Assets\\missilesound.wav"))
            missilesound.set_volume(0.35)
            enginesound = pygame.mixer.Sound(handlePath("Assets\\enginesoundloud.wav"))
            enginesound.set_volume(0.2)
            timer1 = 0

            pygame.mouse.set_visible(False)

            #fuel and armor
            ShipLv = filehelper.get(3)
            totalfuel = 1000 + ((ShipLv[1] - 1) * 50)
            currentfuel = totalfuel

            #inventory
            homeInventory = filehelper.get(2)
            shipInventory = [0,0,0,0]

            if file_settings[3] == 0:
                level1(screen, width, height)
                file_settings[3] = 1
                filehelper.set(file_settings, 0)
                file_settings = filehelper.get(0)

            status = "game"

        if status == "game":
            screen.fill(color)

            # sound
            if menu_music_fadeout >= 0:
                menu_music_fadeout -= 10
            if menu_music_fadeout < 0:
                if beat_timer == max_beat_timer:
                    beat2.stop()
                    beat1.play()
                beat_timer -= 1
                if beat_timer == int(max_beat_timer/2):
                    beat1.stop()
                    beat2.play()
                if beat_timer <= 0:
                    beat_timer = max_beat_timer    
            # sound
            
            # input handling
            inputvar = keyboard()
            thrust_vector = (math.cos(math.radians(rotation)), math.sin(math.radians(rotation)))
            ticks = pygame.time.get_ticks()
            if inputvar:
                if object_list[4] == 1 or object_list[4] == 5:
                    if "w" in inputvar or "uparrow" in inputvar:
                        object_list[2] += step_x * thrust_vector[0]
                        object_list[3] += step_y * thrust_vector[1]
                        flame = True
                    if "e" in inputvar or "rightarrow" in inputvar:
                        rotation -= step_r
                    if "q" in inputvar or "leftarrow" in inputvar:
                        rotation += step_r
                    if "space" in inputvar and (ticks - previous_tick) > 360:
                        xmom_miss = object_list[2] + (thrust_vector[0] * missile_accel)
                        ymom_miss = object_list[3] + (thrust_vector[1] * missile_accel)
                        object_list_addition = [object_list[0]+top_xrot*scalar3, object_list[1]-top_yrot*scalar3, xmom_miss, ymom_miss, 2, serialnumber, missile_lifespan, True]
                        object_list += object_list_addition
                        serialnumber += 1
                        previous_tick = ticks
                        missilesound.stop()
                        missilesound.play()
                if "shift" in inputvar and "c" in inputvar and (ticks - previous_tick2) > 360:
                    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while color[0] + color[1] + color[2] > 150:
                        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    previous_tick2 = ticks
                if "m" in inputvar:
                    status = "mapscreen"
                if "escape" in inputvar or "p" in inputvar or "windows" in inputvar and len(inputvar) == 1:
                    status = "pauseinit"
                lasttransit += 1
                if "a" in inputvar and "d" in inputvar:
                    destinations = sectorDestinations(sectornum)
                    for i in range(4):
                        if destinations[i] != -1:
                            pygame.draw.rect(screen, (120,22,78), portalcoords[i])
                            if portalcollision(object_list, portalcoords[i]) and lasttransit > 150:
                                if sectorGeneration(sectornum):
                                    saveObjects(sectornum, [-1], width, height)
                                else:
                                    saveObjects(sectornum, object_list[:], width, height)
                                sectornum = destinations[i]
                                lasttransit = 0
                                new_objects = getObjects(sectornum, width, height)
                                if new_objects[0] == "-1":
                                    object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, shield_lifespan)
                                else:
                                    object_list = object_list[:8] + new_objects[8:]
                            
            # input handling


            # rotation section
            top_xrot = 30 * math.cos(math.radians(rotation))
            top_yrot = 30 * math.sin(math.radians(rotation))
            right_yrot = 325 ** (1/2.0) * math.cos(math.radians(rotation - lower_rotation_constant))
            right_xrot = 325 ** (1/2.0) * math.sin(math.radians(rotation - lower_rotation_constant))
            left_yrot = 325 ** (1/2.0) * math.cos(math.radians(rotation + 180 + lower_rotation_constant))
            left_xrot = 325 ** (1/2.0) * math.sin(math.radians(rotation + 180 + lower_rotation_constant))
            if flame:
                bottomflame_xrot = 20 * math.cos(math.radians(rotation))
                bottomflame_yrot = 20 * math.sin(math.radians(rotation))
                rightflame_xrot = 61 ** (1/2.0) * math.sin(math.radians(rotation - flame_rotation_constant))
                rightflame_yrot = 61 ** (1/2.0) * math.cos(math.radians(rotation - flame_rotation_constant))
                leftflame_xrot = 61 ** (1/2.0) * math.sin(math.radians(rotation + 180 + flame_rotation_constant))
                leftflame_yrot = 61 ** (1/2.0) * math.cos(math.radians(rotation + 180 + flame_rotation_constant))
            # rotation section

            # collision detection
            def collinfo(object_number1, object_number2):
                intersection = False
                if object_number1 != object_number2: #exempts object intersecting itself
                    #hitBox = [xpos, ypos, width, height] xpos and ypos is orgin
                    hitBox1 = [object_list[(object_number1 * 8)], object_list[1 + (object_number1 * 8)], 0,0]
                    hitBox2 = [object_list[(object_number2 * 8)], object_list[1 + (object_number2 * 8)], 0,0]
                    
                    if object_list[4 + (object_number1 * 8)] == 1: #main ship
                        hitBox1 = [object_list[(object_number1 * 8)]-15*scalar3, object_list[1 + (object_number1 * 8)]-15*scalar3, 30*scalar3, 30*scalar3]
                    elif object_list[4 + (object_number1 * 8)] == 2 or object_list[4 + (object_number1 * 8)] == 8: #shots
                        hitBox1 = [object_list[(object_number1 * 8)], object_list[1 + (object_number1 * 8)], 5, 5]
                    elif object_list[4 + (object_number1 * 8)] == 6: #aliens
                        hitBox1 = [object_list[(object_number1 * 8)], object_list[1 + (object_number1 * 8)], 60, 60]
                    elif object_list[4 + (object_number1 * 8)] == 0: #zvezda
                        hitBox1 = [object_list[(object_number1 * 8)], object_list[1+(object_number1*8)],specialpics[1].get_size()[0], specialpics[1].get_size()[1]]
                    elif 9 < object_list[4 + (object_number1 * 8)] < 40: #pixel things
                        object_type = object_list[4+object_number1*8]
                        hixBox1 = [object_list[(object_number1 * 8)], object_list[1+(object_number1*8)], graphlist[object_type-10].get_size()[0], 
                                   graphlist[object_type-10].get_size()[1]]
                    if object_list[4 + (object_number2 * 8)] == 1: #main ship
                        hitBox2 = [object_list[(object_number1 * 8)]-15*scalar3, object_list[1 + (object_number1 * 8)]-15*scalar3, 30*scalar3, 30*scalar3]
                    elif object_list[4 + (object_number2 * 8)] == 2 or object_list[4 + (object_number2 * 8)] == 8: #shots
                        hitBox2 = [object_list[(object_number2 * 8)], object_list[1 + (object_number2 * 8)], 5, 5]
                    elif object_list[4 + (object_number2 * 8)] == 6: #aliens
                        hitBox2 = [object_list[(object_number2 * 8)], object_list[2 + (object_number2 * 8)], 60, 60]
                    elif object_list[4 + (object_number2 * 8)] == 0: #zvezda
                        hitBox2 = [object_list[(object_number2 * 8)], object_list[1+(object_number2*8)], specialpics[1].get_size()[0], specialpics[1].get_size()[1]]
                    elif 9 < object_list[4 + (object_number2 * 8)] < 40: #pixel things
                        object_type = object_list[4+object_number2*8]
                        hitBox2 = [object_list[(object_number2 * 8)], object_list[1+(object_number2*8)], graphlist[object_type-10].get_size()[0],
                                   graphlist[object_type-10].get_size()[1]]                        

                    # shows all the hitboxes
                    if hitBox1[2] != 0 and hitBox1[3] != 0:
                        pygame.draw.rect(screen, (255,255,255), hitBox1, 3)
                    if hitBox2[2] != 0 and hitBox1[3] != 0:
                        pygame.draw.rect(screen, (255,255,255), hitBox2, 3)
                    
                    if hitBox1[2] != 0 and hitBox1[3] != 0 and hitBox2[2] != 0 and hitBox1[3] != 0:
                        if pygame.Rect(hitBox1).colliderect(pygame.Rect(hitBox2)):
                            intersection = True
                return intersection
                         
            for i in range(int(len(object_list)/8)):
                for i2 in range(int(len(object_list)/8)):                   
                    if collinfo(i,i2) == True:
                        printerlist_add = []
                        if object_list[4 + (i * 8)] == 1 and object_list[4 + (i2 * 8)] in d_sats:
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)], object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+6] = -1
                            shipInventory[object_list[4+i2*8]-10] += 1
                        elif object_list[4 + (i * 8)] == 1 and object_list[4 + (i2 * 8)] == 0:
                            status = "garageinit"
                            homeInventory[0] = homeInventory[0] + shipInventory[0]
                            homeInventory[1] = homeInventory[1] + shipInventory[1]
                            homeInventory[2] = homeInventory[2] + shipInventory[2]
                            homeInventory[3] = homeInventory[3] + shipInventory[3]
                            filehelper.set(homeInventory, 2)
                            currentfuel = 1000 + ((ShipLv[1] - 1) * 50)
                        object_list += printerlist_add
            # collision detection

            #inventory
            Texthelper.write(screen, [(0, 0), "sat1:" + str(shipInventory[0]) + "     sat2:" + str(shipInventory[1]) + "     sat3:" + str(shipInventory[2]) + "     sat4:" + str(shipInventory[3]), 3])

            # deaderizer
            object_list = deaderizer(object_list)
            
            # fuel
            if flame == True:
                currentfuel -= 1
            if currentfuel < 0:
                object_list[6] = -10
                if object_list[12] == 3:
                    object_list[12] = 5
                    object_list[14] = shield_lifespan
                    object_list[15] = True
                    rotation = 90
                    object_list[8] = width/2
                    object_list[9] = height/2
                else:
                    extratime_trigger = True
                currentfuel = totalfuel

            #physics!
            object_list = doPhysics(object_list, width, height, max_speed, drag, step_drag)
            
            # printer and flame and score            
            if object_list[4] == 1 or object_list[4] == 5:
                ship_pointlist = [[object_list[0]+top_xrot*scalar3, object_list[1]-top_yrot*scalar3], [object_list[0]+right_xrot*scalar3, object_list[1]+right_yrot*scalar3], [object_list[0], object_list[1]],
                                  [object_list[0]+left_xrot*scalar3, object_list[1]+left_yrot*scalar3]]
            else:
                ship_pointlist = [[0,0],[0,0]]
            printer2(ship_pointlist, object_list, color, scalar1, scalar3, graphlist, scalarscalar, specialpics)
            if flame == True and (object_list[4] == 1 or object_list[4] == 5):
                flame_pointlist = [[object_list[0], object_list[1]], [object_list[0]+rightflame_xrot*scalar3, object_list[1]+rightflame_yrot*scalar3], [object_list[0]-bottomflame_xrot*scalar3, object_list[1]+bottomflame_yrot*scalar3],
                                   [object_list[0]+leftflame_xrot*scalar3, object_list[1]+leftflame_yrot*scalar3]]
                pygame.gfxdraw.aapolygon(screen, flame_pointlist, (255,100,0))
                pygame.gfxdraw.filled_polygon(screen, flame_pointlist, (255,100,0))
            if flame == True and timer1 == 0:
                enginesound.stop()
                enginesound.play()
            if flame == True and timer1 < 21:
                timer1 += 1
            if flame == True and timer1 == 21:
                timer1 = 0
            if flame == False:
                enginesound.fadeout(10)
            flame = False
            
            screen.blit(fuelpic, (1600, 1000))
            pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
            pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])
            #Texthelper.write(screen, [(1700, 1000), str(currentfuel), 3])
            if FPSDISPLAY:
                Texthelper.write(screen, [(1800, 20), str(round(clock.get_fps())),3])
            pygame.display.flip()
            # printer and flame and score

            # helpers
            if extratime_trigger == True: #lets particle effects dissipate after gameover
                extratime -= 1
                if extratime < 0:
                    status = "gameoverinit"
            previous_inputvar = inputvar #helps with distinct keyclicks
            # helpers
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit


#checks if it needs to run setupper
if filehelper.get(0)[0] == "?":
    from setupper import *
    
main()
