from pgx import *

def homeinitUI(screen, ShipLv, inventory):
    waitTime = 300
    pygame.mouse.set_visible(True)
    if ShipLv[2] != 0:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   containers:" + str(inventory[2]) + "    caps:" + str(inventory[3]),3])
    else:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   caps:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-180), "home base", 6])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540-55), "upgrade shop", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540), "repair & refill shop", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+55), "market", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+110), "empty ship inventory", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+165), "resume", 3])
    pygame.display.flip()

def homeUI(screen, shipInventory, homeInventory):
    status = "home"
    if Texthelper.writeButton(screen, [("center", 540-55), "upgrade shop", 3]):
        status = "garageinit"
    if Texthelper.writeButton(screen, [("center", 540), "repair & refill shop", 3]):
        status = "shopinit"
    if Texthelper.writeButton(screen, [("center", 540+55), "market", 3]):
        status = "marketinit"
    if  Texthelper.writeButton(screen, [("center", 540+110), "empty ship inventory", 3]):
        homeInventory[0] = homeInventory[0] + shipInventory[0]
        homeInventory[1] = homeInventory[1] + shipInventory[1]
        homeInventory[2] = homeInventory[2] + shipInventory[2]
        homeInventory[3] = homeInventory[3] + shipInventory[3]
        filehelper.set(homeInventory, 2)
        shipInventory = [0,0,0,0]
        status = "homeinit"
    if Texthelper.writeButton(screen, [("center", 540+165), "Resume", 3]):
        status = "game"
    return [status, shipInventory]

def repairShopinitUI(screen, currentarmor, currentfuel, ammunition, totalarmor, totalfuel, totalammunition, ShipLv, inventory):
    waitTime = 300
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)
    armorpic = loadImage("Assets\\armor.tif")
    if ShipLv[2] != 0:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   containers:" + str(inventory[2]) + "   caps:" + str(inventory[3]),3])
    else:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   caps:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-180), "repair & refill shop", 6])
    #fuel
    screen.blit(fuelpic, (1600, 1000))
    pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
    pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])
    #armor
    screen.blit(armorpic, (1600, 930))
    pygame.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
    pygame.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])
    #ammunition
    Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(600, 540-55), "Armor:", 3])
    Texthelper.write(screen, [(1000, 540-55), "repair", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(600, 540), "Fuel:", 3])
    Texthelper.write(screen, [(1000, 540), "refill", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(600, 540+55), "Torpedoes:", 3])
    Texthelper.write(screen, [(1000, 540+55), "refill", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+110), "back", 3])
    pygame.display.flip()

def repairShopUI(screen, ShipLv, homeInventory):
    repairRefill = "none"
    status = "shop"
    if Texthelper.writeButton(screen, [(1000, 540-55), "reair", 3]):
        repairRefill = "armor"
        status = "shopinit"
    if Texthelper.writeButton(screen, [(1000, 540), "refill", 3]):
        repairRefill = "fuel"
        status = "shopinit"
    if Texthelper.writeButton(screen, [(1000, 540+55), "refill", 3]):
        repairRefill = "ammunition"
        status = "shopinit"
    if  Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    return [status, repairRefill]

def garageinitUI(screen, ShipLv, inventory):
    waitTime = 300
    pygame.mouse.set_visible(True)
    if ShipLv[2] != 0:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   containers:" + str(inventory[2]) + "    caps:" + str(inventory[3]),3])
    else:
        Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "   gas:" + str(inventory[1]) + "   caps:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-180), "upgrade shop", 6])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [(600, 540-55), "Armor: lv " + str(ShipLv[0]), 3])
    if inventory[0] >= ShipLv[0]*3:
        Texthelper.write(screen, [(1000, 540-55), "Upgrade", 3])
    else:
        Texthelper.write(screen, [(1000, 540-55), "sorry", 3])
    Texthelper.write(screen, [(1300, 540-55), "cost:" + str(ShipLv[0]*3)+ " metal", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(635, 540), "Fuel: lv " + str(ShipLv[1]), 3])
    if inventory[1] >= ShipLv[1]*3:
        Texthelper.write(screen, [(1000, 540), "Upgrade", 3])
    else:
        Texthelper.write(screen, [(1000, 540), "sorry", 3])
    Texthelper.write(screen, [(1300, 540), "cost:" + str(ShipLv[1]*3)+ " gas", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(470, 540+55), "torpedoes:", 3])
    Texthelper.write(screen, [(810, 540+55), "lv " + str(ShipLv[2]), 3])
    if ShipLv[2] != 0:
        if inventory[2] >= ShipLv[2]*3:
            Texthelper.write(screen, [(1000, 540+55), "Upgrade", 3])
        else:
            Texthelper.write(screen, [(1000, 540+55), "sorry", 3])
        Texthelper.write(screen, [(1300, 540+55), "cost:" + str(ShipLv[2]*3)+ " containers", 3])
    else:
        Texthelper.write(screen, [(1000, 540+55), "locked", 3])
    pygame.display.flip()
        
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+110), "back", 3])
    pygame.display.flip()


def GarageUI(screen, ShipLv, inventory):
    status = "garage"
    if inventory[0] >= ShipLv[0]*3:
        if Texthelper.writeButton(screen, [(1000, 540-55), "Upgrade", 3]):
            inventory[0] = inventory[0] - (ShipLv[0]*3)
            ShipLv[0] += 1
            status = "garageinit"
    if inventory[1] >= ShipLv[1]*3:
        if Texthelper.writeButton(screen, [(1000, 540), "Upgrade", 3]):
            inventory[1] = inventory[1] - (ShipLv[1]*3)
            ShipLv[1] += 1
            status = "garageinit"
    if inventory[2] >= ShipLv[2]*3:
        if Texthelper.writeButton(screen, [(1000, 540+55), "Upgrade", 3]):
            inventory[2] = inventory[2] - (ShipLv[2]*3)
            ShipLv[2] += 1
            status = "garageinit"
    if Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    return [status, ShipLv, inventory]

def pauseinitUI(screen):
    Texthelper.write(screen, [("center", 540-136), "Paused", 6])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540-55), "Resume", 2])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540-20), "Restart", 2])
    pygame.display.flip()
    pygame.time.wait(200)            
    Texthelper.write(screen, [("center", 540+15), "Quit to desktop", 2])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540+50), "Quit to menu", 2])
    pygame.display.flip()

def gameoverinitUI(screen):
    text_input = [("center", 540-136), "Game over", 6]
    Texthelper.write(screen, text_input)            
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540-55), "Play again", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540-20), "Quit to desktop", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540+15), "Quit to menu", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()    

def pauseUI(screen):
    status = "paused"
    if Texthelper.writeButton(screen, [("center", 540-55), "Resume", 2]):
        pygame.mouse.set_visible(False)
        status = "game"
    elif Texthelper.writeButton(screen, [("center", 540-20), "Restart", 2]):
        status = "gameinit"   
    elif Texthelper.writeButton(screen, [("center", 540+15), "Quit to desktop", 2]):
        status = "exiting"
    elif Texthelper.writeButton(screen, [("center", 540+50), "Quit to menu", 2]):
        status = "menuinit"
    return status

def gameoverUI(screen):
    status = "gameover"
    if Texthelper.writeButton(screen, [("center", 540-55), "Play again", 2]):
        status = "gameinit"                
    elif Texthelper.writeButton(screen, [("center", 540-20), "Quit to desktop", 2]):
        status = "exiting"            
    elif Texthelper.writeButton(screen, [("center", 540+15), "Quit to menu", 2]):
        status = "menuinit"
    return status

def mapscreenUI(screen):
    status = "mapscreen"
    if Texthelper.writeButton(screen, [(180, 520), "[Commence Flying]", 2.5]):
        status = "game"
        pygame.mouse.set_visible(False)
    return status
   
