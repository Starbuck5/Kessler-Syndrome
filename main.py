import math
import random
import pygame

from pgx import *
import pgx
from level1 import *
from game import *
import game
from UIscreens import *
import graphics
import Collisions
from Collisions import explosion_sounds

upgrades = Filehelper("assets\\data\\upgrades.txt")
                                                
def main():
    file_settings = filehelper.get(0) #grabs settings from file

    #sets adjustable settings
    width = int(file_settings[0])
    height = int(file_settings[1])
    max_asteroids = 8
    if file_settings[5]:
        GameConstants.drag = [1,5]

    #scaling
    scalarscalar = height / 1080
    scalar2 = 1.5 * scalarscalar # controls asteroid size
    scalar3 = 1.2 * scalarscalar # controls ship size
    sat_scalar = 1.2 * scalarscalar #controls satellite size
    alien_size = [1.2 * scalarscalar, 1.8 * scalarscalar]

    #graphical setup
    temp_image = loadImage("Assets\\images\\supplies.gif")
    temp_image.set_colorkey((255,255,255))
    graphlist = [scaleImage(loadImage("Assets\\images\\sat1.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat2.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat3.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat4.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat5.tif"), 0.9*sat_scalar),
                 "d", "f", "h", "j", "k", "l", "a", "s", "e", "as", "4", "3", "2", "1", "x11",
                 loadImage("Assets\\images\\solarpanel.tif"), temp_image,
                 scaleImage(loadImage("Assets\\images\\sat3w.tif"), sat_scalar),
                 scaleImage(loadImage("Assets\\images\\sat4w.tif"), sat_scalar)]
    earthpic = loadImage("Assets\\images\\earth.tif")

    # settings
    GameConstants.max_speed = 4 * scalarscalar
    missile_lifespan = 130 * scalarscalar
    missile_accel = 7 * scalarscalar
    AITools.missile_accel = missile_accel
    AITools.missile_lifespan = missile_lifespan
    step_x = 0.08 * scalarscalar
    step_y = 0.08 * scalarscalar
    step_r = 2.3
    GameConstants.step_drag = 0.004 * scalarscalar
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
    SoundVault("explosion1", "Assets\\sounds\\Bomb1.ogg", volume=0.1)
    SoundVault("explosion2", "Assets\\sounds\\Bomb2.ogg", volume=0.1)
    SoundVault("money", "Assets\\sounds\\clink.ogg")
    SoundVault("death", "Assets\\sounds\\powerfailure.ogg", volume=0.2)
    SoundVault("portal", "Assets\\sounds\\electric.ogg", volume=0.15)
    SoundVault("shot", "Assets\\sounds\\shot.ogg", volume=0.25)

    # variable setup
    playerinfo = filehelper.get(1)
    cheats_settings = filehelper.get(5)
    d_parts = [30, 31, 32, 33]
    d_sats = [10, 11, 12, 13, 14]
    d_asteroids = [70, 71, 72, 73, 80, 81, 82, 83, 90, 91, 92, 93, 94, 95, 96, 97]
    d_aliens = [120, 121, 122, 123]
    d_stars = [100, 101, 102, 103, 104, 105]
    d_fighters = [130, 131, 132, 133]
    #list of things to be eliminated before officially clearing a sector ->
    d_debris = d_parts + d_sats + d_asteroids + d_aliens + d_fighters + [7]
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
    sector_map_coordinates = {1: (960, 990), 2: (820, 970), 3: (1110, 980), 4: (810, 840), 5: (970, 830), 6: (965, 690), 7: (1115, 680),
                              8: (830, 675), 9: (1060, 525), 10: (865, 535), 11: (830, 400), 12: (700, 630), 13: (690, 455), 14: (1095, 385),
                              15: (1055, 250), 16: (840, 245), 17: (965, 415), 18: (870, 105), 19: (1030, 90)}
    optionsScreenshot = "" #saves a screenshot of the game so the pause menu looks correct after exitting options

    # class setup
    Screenhelper(width,height)
    Texthelper.scalar = scalarscalar
    Texthelper.width = width
    Texthelper.height = height
    GameConstants.width = width
    GameConstants.height = height
    AnnouncementBox.width = width
    AnnouncementBox.height = height

    #graphics setup
    graphics.init(d_asteroids, d_parts, d_sats, graphlist, scalar2, scalar3, scalarscalar)
    
    
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
            if Texthelper.writeButtonBox(screen, [(410, 490), "Play", 3]):
                status = "gameinit"
            if Texthelper.writeButtonBox(screen, [(410, 550), "Arcade Mode [Beta]", 3]):
                status = "arcadeinit"
            if Texthelper.writeButtonBox(screen, [(410, 610), "Options", 3]):
                status = "optionsinit"
                OptionsInput.backStatus = "menuinit"
            if Texthelper.writeButtonBox(screen, [(410, 670), "Quit to desktop", 3]): #if "quit to desktop" is clicked           
                status = "exiting"         

            screen.blit(earthpic, (1500,800))
            pygame.display.flip()
            
        if status == "pauseinit":
            optionsScreenshot = screen.copy()
            filehelper.set([currentarmor, currentfuel, ammunition], 4)
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
            Font.set_scramble_paused(True) #pauses any scrambling going on
            drawPauseUI(screen, "pauseinit", True)
            
            #saving objectlist, sector achievements data
            saveGame(sectornum, object_list, width, height)
            discovery = list("8" * len(sector_map_coordinates))
            for i in discoverSector.keys():
                if discoverSector[i]:
                    discovery[i - 1] = "1"
            filehelper.setElement("".join(discovery), 1, 2)
            cleared = list(cleared) 
            for i in range(1, 20):
                if clearedSector[i]:
                    cleared[i - 1] = "1"
            filehelper.setElement("".join(cleared), 1, 1)
            status = "paused"

        if status == "paused":
            status = drawPauseUI(screen, "pauseinit", False)
            inputvar = keyboard()
            if ("p" in inputvar or "escape" in inputvar) and timer_popupmenu > 25:
                status = "game"
                timer_popupmenu = 0
            if status != "paused":
                Font.set_scramble_paused(False) #resumes any scrambling going on
                pygame.mouse.set_visible(False)
            if status == "menuinit":
                Font.endScramble()

        if status == "optionsinit":
            optionsUIinit(screen, file_settings)
            status = "options"

        if status == "options":
            screen.fill(color)
            status = optionsUI(screen, file_settings) 

            inputvar = keyboard()
            if "escape" in inputvar:
                status = "pauseinit"

            if status != "options":
                if status == "pauseinit":
                    screen.blit(optionsScreenshot, (0, 0))
                timer_popupmenu = 0
                filehelper.set(file_settings, 0)
                if (not file_settings[4]):
                    DEVMODE = False #if you disable cheats devmode is turned off

            pygame.display.flip()

        if status == "cheatsmenu":
            screen.fill(color)
            status = cheatsMenuUI(screen, cheats_settings)

            if status != "cheatsmenu":
                timer_popupmenu = 0
                filehelper.set(cheats_settings, 5)

        if status == "mapscreeninit":
            pygame.mouse.set_visible(True)
            Font.set_scramble_paused(True) #pauses any scrambling going on
            Screenhelper.greyOut(screen)
            mapscreenUI(screen, sector_map_coordinates, discoverSector, sectornum, DEVMODE, cheats_settings, clearedSector)      

            pygame.display.flip()
            status = "mapscreen"

        if status == "mapscreen":
            status = mapscreenUI(screen, sector_map_coordinates, discoverSector, sectornum, DEVMODE, cheats_settings, clearedSector)
            inputvar = keyboard()

            if ("m" in inputvar or "escape" in inputvar) and timer_popupmenu > 25:
                status = "game"
                timer_popupmenu = 0

            if DEVMODE and cheats_settings[3]:
                Texthelper.write(screen, [(250, 200), "Click on a sector", 2.5], color = (125, 15, 198))
                Texthelper.write(screen, [(250, 250), "to teleport", 2.5], color = (125, 15, 198))
                for i in sector_map_coordinates.keys():
                    if discoverSector[i] or cheats_settings[4]:
                        if Texthelper.writeButton(screen, [(sector_map_coordinates[i][0] - len(str(i)) * 10,
                                                            sector_map_coordinates[i][1] - 15), str(i), 2]):
                            saveGame(sectornum, object_list[8:], width, height)
                            sectornum = i
                            lasttransit = 0
                            new_objects = getObjects(sectornum, width, height)
                            if new_objects == ["PLEASE GENERATE"]:
                                object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height,
                                                      d_sats, d_parts, d_asteroids, d_fighters, sectornum)
                            else:
                                object_list = object_list[:8] + new_objects
                            object_list[2] = 0  #kills momentum
                            object_list[3] = 0
                            status = "game"
                            
            if status != "mapscreen":
                pygame.mouse.set_visible(False)
                Font.set_scramble_paused(False) #resumes any scrambling going on

            pygame.display.flip()

        if status == "exiting":
            ## sector object list visualizer ##
            #for i in range(1, 20):
            #    print("SECTOR", i)
            #    print(getObjects(i, 1920, 1080))
            #    print("\n")
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
            totalStats = [totalarmor, totalfuel, totalammunition]
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

            start_sector = -1
            for i in range(1, 19):
                if len(getObjects(i, width, height)) > 1:
                    if getObjects(i, width, height)[4] in ship_id:
                        start_sector = i
                        break

            if start_sector > 0:
                object_list = getObjects(start_sector, width, height)
                sectornum = start_sector
            else:
                print("we lost the ship, recreating now boss")
                object_list = [width*0.5, height*0.3, 0, 0, 1, RotationState(90,0), "NA", 1] + getObjects(1, width, height)
                sectornum = 1
                                
            previous_tick = 0
            previous_tick2 = 0
            pygame.mouse.set_visible(False)
            #inventory
            shipInventory = [0,0,0,0]

            #fuel and armor and ammunition
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
            discovery = str(filehelper.get(1)[2])
            discoverSector = {}
            for i in sector_map_coordinates.keys():
                if discovery[i - 1] == "8":
                    discoverSector[i] = False
                else:
                    discoverSector[i] = True
                    
            cleared = str(filehelper.get(1)[1])
            clearedSector = {}
            for i in range(1, 20):
                if cleared[i - 1] == "8":
                    clearedSector[i] = False
                else:
                    clearedSector[i] = True
                    
            if file_settings[3] == 0:
                level1(screen, width, height)
                file_settings[3] = 1
                filehelper.set(file_settings, 0)
                file_settings = filehelper.get(0)

            if file_settings[3] == 1:
                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                loadSound("Assets\\announcements\\1r.ogg"),
                                "You're still alive? Well then go pick up some space debris like a good prisoner!")
                file_settings[3] = 2
                filehelper.set(file_settings, 0)
            
            status = "game"

        if status == "game" or status == "arcade":            
            # input handling
            inputvar = keyboard()
            ticks = pygame.time.get_ticks()
            if inputvar:
                if object_list[4] == 1:
                    thrust_vector = (math.cos(math.radians(object_list[5].getRotation()-90)),
                                     math.sin(math.radians(object_list[5].getRotation()+90)))
                    if "w" in inputvar or "uparrow" in inputvar:
                        object_list[2] += step_x * thrust_vector[0]
                        object_list[3] += step_y * thrust_vector[1]
                        flame = True
                    if "e" in inputvar or "rightarrow" in inputvar:
                        object_list[5].rotateBy(step_r)
                    if "q" in inputvar or "leftarrow" in inputvar:
                        object_list[5].rotateBy(-step_r)
                    if "space" in inputvar and (ticks - previous_tick) > 360 and ammunition > 0:
                        ammunition -= 1
                        SoundVault.play('shot')
                        xmom_miss = object_list[2] + (thrust_vector[0] * missile_accel)
                        ymom_miss = object_list[3] + (thrust_vector[1] * missile_accel)
                        front_pointlist = RotatePoint(object_list[0], object_list[1],
                                                      [object_list[0], object_list[1]-30*scalar3], object_list[5].getRotation())
                        object_list_addition = [front_pointlist[0][0], front_pointlist[0][1], xmom_miss, ymom_miss, 2,
                                                RotationState(-1,-1), "NA", missile_lifespan]
                        object_list += object_list_addition
                        previous_tick = ticks
                if "shift" in inputvar and "c" in inputvar and (ticks - previous_tick2) > 360:
                    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while color[0] + color[1] + color[2] > 150:
                        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    previous_tick2 = ticks
                if "m" in inputvar and timer_popupmenu > 25 and status == "game":
                    timer_popupmenu = 0
                    status = "mapscreeninit"
                if ("escape" in inputvar or "p" in inputvar or "windows" in inputvar) and len(inputvar) == 1:
                    if timer_popupmenu > 25:
                        timer_popupmenu = 0
                        if status == "game":
                            status = "pauseinit"
                        if status == "arcade":
                            status = "arcadepauseinit"
                lasttransit += 1
                if "shift" in inputvar and "d" in inputvar and (ticks - previous_tick2) > 360 and file_settings[4]:
                    DEVMODE = not DEVMODE #switches booleans
                    previous_tick2 = ticks
                if "t" in inputvar and timer_portal_toggle > 30:
                    portal_toggle = not portal_toggle
                    timer_portal_toggle = 0
            # input handling
        
        if status == "game":
            screen.fill(color)
            AnnouncementBox.play(screen)
            Font.timerhelper() #once a game loop update to a scramble timer
            
            # quest handling
            if filehelper.get(0)[3] == 4:
                object_list += [0.43*width, 0.39*height, 0, 0, 110, RotationState("NA", "NA"), "NA", 1]
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "Thanks for the help " + filehelper.get(1)[0] + ". Have 100 credits for your trouble.")
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "So fellow traveler, what did you do to get banished up here?")
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "You've got dirt on the president of the world you say? That's splendid!")
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                ("If you could get me 10 circuits I could hack the gps, the global propaganda system, "
                                 "and the president would really be pissed then!"))
                shipInventory[3] += 100
                filehelper.setElement(5, 0, 3)
            if filehelper.get(0)[3] == 6:
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                ("Lets go team! Now the whole world will find out the President's crimes. "
                                 "What did she do again?"))
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "Conspiring with aliens! The humanity! She must be stopped! I'll get to work on the hack.")
                filehelper.setElement(7, 0, 3)
            if filehelper.get(0)[3] == 7:
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "I'm in! We've transmitted an account of the President's crimes to the whole world.")
                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "Oh boy you're in trouble now.")
                AnnouncementBox(loadImage("Assets\\announcements\\ai.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "Large inbound contact detected, seems to be holding position in sector 19.")
                AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                loadSound("Assets\\sounds\\click.ogg"),
                                "The president has come for us. You must go defeat her.")
                sector19 = getObjects(19, width, height)
                sector19 += [width*0.5, height*0.5, 0, 0, 666, RotationState(0, 0), PrezAI(), 1]
                saveGame(19, sector19, width, height)
                filehelper.setElement(8, 0, 3)
            # quest handling

        if status == "game" or status == "arcade":
            # collision detection
            Collisions.prime(object_list, screen, graphlist, DEVMODE, cheats_settings)
            numExaminations = int(len(object_list)/8)
            for i in range(numExaminations):
                i2 = i + 1
                while i2 < numExaminations:                   
                    if Collisions.doCollide(i, i2, object_list):
                        printerlist_add = []
                        drops = [0,0,0,0] #why is this here?
                        ID1 = object_list[4+(i*8)]
                        ID2 = object_list[4+(i2*8)]
                        if ID1 in ship_id and ID2 in d_sats: #ship v satellite
                            xForce = abs(object_list[2+(i*8)] - object_list[2+(i2*8)]) 
                            yForce = abs(object_list[3+(i*8)] - object_list[3+(i2*8)])
                            force = (xForce + yForce)*2
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                             object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            drops = satelliteDrops(ShipLv)
                            if drops[3]: #if currency is dropped
                                SoundVault.play('money')
                            #merges the two lists by adding their like elements together
                            shipInventory = [a + b for a, b in zip(shipInventory, drops)]
                        elif ID1 in ship_id and ID2 in d_parts: #ship v debris
                           printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                            object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                           object_list[(i2*8)+7] = -1
                           if object_list[(4+(i2*8))] == 31: #supply drop
                               ammunition = totalammunition #fills your ammo
                               currentfuel = totalfuel #tops off your fuel
                               drops = satelliteDrops(ShipLv)
                               drops = [i*3 for i in drops] #multiplies satellite drop by 3
                           else: 
                               drops = solarPanelDrops(ShipLv)
                           shipInventory = [a + b for a, b in zip(shipInventory, drops)]                            
                        elif ID1 in ship_id and ID2 == 0: #going to garage
                            Texthelper.writeBox(screen, [(800,500), "press enter", 1], color = (0,100,200))
                            if "enter" in inputvar:
                                status = "homeinit"
                        elif ID1 in ship_id and ID2 in d_fighters: #ship vs fighters
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)],
                                                             object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            drops = satelliteDrops(ShipLv)
                            if drops[3]: #if currency is dropped
                                SoundVault.play('money')
                            #merges the two lists by adding their like elements together
                            shipInventory = [a + b for a, b in zip(shipInventory, drops)]                            
                        #ship v asteroid or spiker or drone
                        elif ID1 in ship_id and (69 < ID2 < 100 or ID2 == 121 or ID2 == 120):
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
                        elif ID1 in ship_id and ID2 == 123: #ship vs alienbomb
                            currentarmor -= 7
                            object_list[(i2*8)+6].explode(object_list, i2*8)
                            explosion_sounds()
                        elif ID2 == 2 and ID1 == 123: #missile vs alienbomb
                            object_list[(i*8)+6].explode(object_list, i*8)
                            explosion_sounds()
                        #missile v asteroid or spiker or drone
                        elif ID2 == 2 and (69 < ID1 < 100 or ID1 == 121 or ID1 == 120): 
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
                        elif ID2 == 2 and ID1 in d_fighters: #missile v derelict fighters
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                            explosion_sounds()                            
                        elif object_list[4 + (i2 * 8)] == 2 and object_list[4 + (i * 8)] == 7: #missile v mine
                            printerlist_add += [object_list[(i * 8)], object_list[1+(i * 8)], object_list[2+(i*8)],
                                                object_list[3+(i*8)], 9, RotationState("NA", "NA"), "NA", 300]
                            object_list[(i*8)+7] = -1
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] == 7: #ship v mine
                            printerlist_add += [object_list[(i2 * 8)], object_list[1+(i2 * 8)], object_list[2+(i2*8)],
                                                object_list[3+(i2*8)], 9, RotationState("NA", "NA"), "NA", 300]
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
                        elif object_list[4 + (i * 8)] in ship_id and object_list[4 + (i2 * 8)] == 122: #ship v spike
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            currentarmor -= 1
                            object_list[(i2*8)+7] = -1
                        elif object_list[4 + (i * 8)] == 2 and object_list[4 + (i2 * 8)] == 122: #missile v spike
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)],
                                                             object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i*8)+7] = -1
                            object_list[(i2*8)+7] = -1
                        #if debris hits anything thats not a star
                        elif object_list[4 + (i2 * 8)] == 4 and object_list[4+i*8] not in (d_stars + [4]):
                            object_list[i2*8+7] = -1
                        object_list += printerlist_add                            
                    i2 += 1            
            # collision detection

        if status == "game":
            #special entity behaviors
            for i in range(0, len(object_list), 8):
                if not isinstance(object_list[i+6], str):
                    try:
                        object_list[i+6].update(object_list, i)
                    except:
                       pass
            #special entity behaviors

            #portals
            if portal_toggle: # ship collision with portal
                destinations = sectorDestinations(sectornum)
                for i in range(4):
                    if destinations[i] != -1:
                        pygame.gfxdraw.aapolygon(screen, portalcoordsRevised[i], (100,149,237))
                        pygame.gfxdraw.filled_polygon(screen, portalcoordsRevised[i], (100,149,237))
                        isValidTransfer = object_list[4] == 1 or object_list[4]==5 #if the first thing in object_list is allowed to transit
                        isValidTime = lasttransit > 70
                        isValidCollision = portalRects[i].collidepoint((object_list[0], object_list[1]))                        
                        if isValidTransfer and isValidTime and isValidCollision:
                            SoundVault.play('portal')
                            saveGame(sectornum, object_list[8:], width, height)
                            sectornum = destinations[i]
                            lasttransit = 0
                            new_objects = getObjects(sectornum, width, height)
                            if new_objects == ["PLEASE GENERATE"]:
                                object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height,
                                                      d_sats, d_parts, d_asteroids, d_fighters, sectornum)
                            else:
                                object_list = object_list[:8] + new_objects
                            if discoverSector[sectornum] == False:
                                if sectornum == 4:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\3r.ogg"),
                                                    "Jesus! Took you long enough to get here. Now get to work on this sector.")
                                if sectornum == 6:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\4r.ogg"),
                                                    ("I see you finally decided to travel further. Better pray to the "
                                                     "Virgin Mary that you don't die."))
                                if sectornum == 9:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\5r.ogg"),
                                                    "Congratulations, you made it to the land of explosives. My favorite part!")
                                if sectornum == 11:
                                    AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                                    loadSound("Assets\\sounds\\click.ogg"),
                                                    "Is someone out there? I've been stuck out here for so long")
                                    AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                                    loadSound("Assets\\sounds\\click.ogg"),
                                                    ("If you would give me some gas to get back to station I would be "
                                                     "eternally grateful"))
                                    AnnouncementBox(loadImage("Assets\\announcements\\airman.png"),
                                                    loadSound("Assets\\sounds\\click.ogg"),
                                                    "Just go back to station and find the button to send me some fuel")
                                    file_settings[3] = 3
                                    filehelper.set(file_settings, 0)
                                if sectornum == 12:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\6r.ogg"),
                                                    ("Damn, you're slow. Clean this mess up before I get bored and "
                                                     "launch rockets at you!"))
                                if sectornum == 17:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\7r.ogg"),
                                                    "I see you found some more debris to clean up. make it quick!")
                                if sectornum == 19:
                                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                                    loadSound("Assets\\announcements\\8r.ogg"),
                                                    ("Holy Jesus, look at that! You finally made it to the edge of your"
                                                     " cleaning zone. But wait... there's more! You're going to keep "
                                                     "cleaning for the rest of your life!"))
                                discoverSector[sectornum] = True


            # reward for killing a sector
            numdebris = 0
            for i in range(0, len(object_list), 8):
                if object_list[i+4] in d_debris:
                    numdebris += 1
            if numdebris == 0 and clearedSector[sectornum] == False:
                shipInventory[3] += 50 #adds 50 credits to ship inventory
                SoundVault.play('money')
                clearedSector[sectornum] = True
                sectorsCleared = 0
                for n in clearedSector.values():
                    if n:
                        sectorsCleared += 1
                if sectorsCleared == 2: #one sector is cleared by default, so 2 means player has actually cleared a sector
                    AnnouncementBox(loadImage("Assets\\announcements\\warden.png"),
                                    loadSound("Assets\\announcements\\2r.ogg"),                             
                                    ("Finally! You've cleared your first sector! Now here's a reward for your obedience."
                                     " Don't get lazy now!"))

            # deaderizer
            object_list = deaderizer(object_list)
            
            # fuel consumption
            if flame:
                currentfuel -= 1

            #HACKZ
            if DEVMODE:
                if cheats_settings[0]:
                    currentarmor = totalarmor
                if cheats_settings[1]: 
                    currentfuel = totalfuel
                if cheats_settings[2]:
                    ammunition = totalammunition
                
            #ship death
            if currentarmor <= 0 or currentfuel <= 0:
                saveGame(sectornum, object_list[8:], width, height)
                object_list += particlemaker(object_list[0], object_list[1], object_list[2], object_list[3])
                object_list += particlemaker(object_list[0], object_list[1], object_list[2], object_list[3])
                SoundVault.play('death')
                object_list[4] = 5   #sets the ship to be objID 5 for 200 ticks
                object_list[7] = 200 #meaning the player is paralyzed
                currentfuel = totalfuel
                currentarmor = totalarmor
                shipInventory = [0,0,0,0]
                lasttransit = 0
                timer_shipdeath = 0

            if timer_shipdeath == 200:
                sectornum = 1
                shipObj = object_list[:8]
                object_list = shipObj + getObjects(sectornum, width, height)
                object_list[0] = width/2 - width*0.3
                object_list[1] = height/2 - height*0.2
                object_list[2] = 0
                object_list[3] = 0
                object_list[4] = 1

            #physics!
            doPhysics(object_list)

            #ship durability state
            updateShipGraphics(currentarmor, totalarmor)
            
            # printer
            graphics.printer(screen, object_list, scalar3, graphlist, scalarscalar, flame)
            graphics.InfoBars.draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition, totalammunition)
            graphics.drawInventory(screen, shipInventory)
            if file_settings[6]:
                Texthelper.write(screen, [(file_settings[0] - 50, 10), str(round(clock.get_fps())), 2]) 
            flame = False
            if DEVMODE:
                Texthelper.write(screen, [(10, file_settings[1] - 30), "Cheats On", 2], color = (125, 15, 198))
            pygame.display.flip()
            # printer

        if status == "arcadeinit":
            object_list = [0.5*width, 0.5*height, 0, 0, 1, RotationState(0,0), "NA", 1] #constructing a ship
            object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, d_parts,
                                  d_asteroids, d_fighters, 1)
            arcade_level = 1

            ShipLv = [1,1,1,0]
            fuelHelp = upgrades.get(ShipLv[1]+20)
            totalfuel = fuelHelp[4]
            currentfuel = totalfuel
            armorHelp = upgrades.get(ShipLv[0])
            totalarmor = armorHelp[4]
            currentarmor = totalarmor
            totalammunition = 0
            if ShipLv[2] == 0:
                totalammunition = 0
            else:
                ammunitionHelp = upgrades.get(ShipLv[2]+40)
                totalammunition = ammunitionHelp[4]
            ammunition = totalammunition

            #initializes printouts of fuel and armor and ammo
            graphics.InfoBars.init(graphics.FlashyBox([1590, 990, 280, 70], 0.2, (255,0,0)),
                                   graphics.FlashyBox([1590, 920, 280, 70], 0.2, (255,0,0)))

            previous_tick = 0
            previous_tick2 = 0
            pygame.mouse.set_visible(False)
            #inventory
            shipInventory = [0,0,0,0]

            status = "arcade"

        if status == "arcade":
            screen.fill(color)
            AnnouncementBox.play(screen)
            Font.timerhelper() #once a game loop update to a scramble timer

            #special entity behaviors
            for i in range(0, len(object_list), 8):
                if not isinstance(object_list[i+6], str):
                    try:
                        object_list[i+6].update(object_list, i)
                    except:
                       pass

            # deaderizer
            object_list = deaderizer(object_list)

            #progression
            numdebris = 0
            for i in range(0, len(object_list), 8):
                if object_list[i+4] in d_debris:
                    numdebris += 1
            if numdebris == 0:
                arcade_level += 1
                object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, d_parts,
                                  d_asteroids, d_fighters, arcade_level)                        
            # fuel consumption
            if flame:
                currentfuel -= 1

            #ship death
            if currentarmor <= 0 or currentfuel <= 0:
                status = "menuinit"

            #physics!
            doPhysics(object_list)

            #ship durability state
            updateShipGraphics(currentarmor, totalarmor)
            
            # printer
            graphics.printer(screen, object_list, scalar3, graphlist, scalarscalar, flame)
            graphics.InfoBars.draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition, totalammunition)
            graphics.drawInventory(screen, shipInventory)
            if file_settings[6]:
                Texthelper.write(screen, [(file_settings[0] - 50, 10), str(round(clock.get_fps())), 2]) 
            flame = False
            if DEVMODE:
                Texthelper.write(screen, [(10, file_settings[1] - 30), "Cheats On", 2], color = (125, 15, 198))
            pygame.display.flip()

        if status == "arcadepauseinit":
            optionsScreenshot = screen.copy()
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
            Font.set_scramble_paused(True) #pauses any scrambling going on
            drawPauseUI(screen, "arcadepauseinit", True)
            status = "arcadepaused"

        if status == "arcadepaused":
            status = drawPauseUI(screen, "arcadepauseinit", False)
            inputvar = keyboard()
            if ("p" in inputvar or "escape" in inputvar) and timer_popupmenu > 25:
                status = "arcade"
                timer_popupmenu = 0
            if status != "paused":
                Font.set_scramble_paused(False) #resumes any scrambling going on
                pygame.mouse.set_visible(False)
            if status == "menuinit":
                Font.endScramble()
        
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
