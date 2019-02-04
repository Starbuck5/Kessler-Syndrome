from pgx import *
waitTime = 300
upgrades = Filehelper("assets\\upgrades.txt")

def timedFlip():
    pygame.display.flip()
    pygame.time.wait(waitTime)

class UpgradeScreenStorage():
    currentStat = -1
    addedStat = -1
    cost = -1
    editingIndex = -1
    

def drawUpgradeScreen(screen, ShipLv, inventory, mode, name, status): #mode = true/false init, name = fuel/armor/etc.   
    if mode: #whether it should be init-ing or not
        driveHead = 0
        if name == "armor":
            driveHead = 0
            editingIndex = 0
            pointName = "hp"
        if name == "fuel":
            driveHead = 20
            editingIndex = 1
            pointName = "fp"
        if name == "torpedoe":
            driveHead = 40
            editingIndex = 2
            pointName = "ammo"
        UpgradeScreenStorage.currentStat = upgrades.get(ShipLv[0]+driveHead)[4] 
        UpgradeScreenStorage.cost = upgrades.get(ShipLv[0]+driveHead+1)
        UpgradeScreenStorage.addedStat = UpgradeScreenStorage.cost[4] - UpgradeScreenStorage.currentStat
        UpgradeScreenStorage.editingIndex = editingIndex

    currentStat = UpgradeScreenStorage.currentStat
    cost = UpgradeScreenStorage.cost
    addedStat = UpgradeScreenStorage.addedStat
    editingIndex = UpgradeScreenStorage.editingIndex
    
    pygame.mouse.set_visible(True) #necessary?
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]) + "  torpedoes:" + str(inventory[4]),3])
    Texthelper.write(screen, [("center", 540-235), name + " upgrade", 6])

    if mode:
        timedFlip()       
    Texthelper.write(screen, [("center", 540-110), "lv: " + str(ShipLv[0]) + " +1   " + "Stats: " + str(currentStat) + " +" + str(addedStat) + pointName, 3])
    
    if mode:
        timedFlip()        
    Texthelper.write(screen, [("center", 540), "cost:", 3])
    
    if mode:
        timedFlip()
    Texthelper.write(screen, [(600, 540+55), str(cost[0]) + " metal", 3])
    Texthelper.write(screen, [(1000, 540+55), str(cost[1]) + " gas", 3])

    if mode:
        timedFlip()       
    Texthelper.write(screen, [(600, 540+110), str(cost[2]) + " circuits", 3])
    Texthelper.write(screen, [(1000, 540+110), str(cost[3]) + " currency", 3])

    if mode:
        timedFlip()        
    if inventory[0] > cost[0] and inventory[1] > cost[1] and inventory[2] > cost[2] and inventory[3] > cost[3]:
        if Texthelper.writeButton(screen, [("center", 540+220), "Upgrade", 3]):
            inventory[0] -= cost[0]
            inventory[1] -= cost[1]
            inventory[2] -= cost[2]
            inventory[3] -= cost[3]
            ShipLv[editingIndex] += 1
            status = "garageinit"
            filehelper.set(inventory, 2)
            filehelper.set(ShipLv, 3)
    else:
        Texthelper.write(screen, [("center", 540+220), "sorry", 3])

    if mode:
        timedFlip()        
    if Texthelper.writeButton(screen, [("center", 540+275), "back", 3]):
        status = "garageinit"
    
    if mode:
        pygame.display.flip()

    return status

def homeinitUI(screen, inventory):
    pygame.mouse.set_visible(True)
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]) + "  torpedoes:" + str(inventory[4]),3])
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
        #status = "marketinit"
        pass
    if  Texthelper.writeButton(screen, [("center", 540+110), "empty ship inventory", 3]):
        homeInventory[0] = homeInventory[0] + shipInventory[0]
        homeInventory[1] = homeInventory[1] + shipInventory[1]
        homeInventory[2] = homeInventory[2] + shipInventory[2]
        homeInventory[3] = homeInventory[3] + shipInventory[3]
        homeInventory[4] = homeInventory[4] + shipInventory[4]
        filehelper.set(homeInventory, 2)
        shipInventory = [0,0,0,0,0]
        status = "homeinit"
    if Texthelper.writeButton(screen, [("center", 540+165), "Resume", 3]):
        status = "game"
    return [status, shipInventory]

def repairShopinitUI(screen, currentarmor, currentfuel, ammunition, totalarmor, totalfuel, totalammunition, inventory):
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)
    armorpic = loadImage("Assets\\armor.tif")
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]) + "  torpedoes:" + str(inventory[4]),3])
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
    if currentarmor == totalarmor:
        Texthelper.write(screen, [(1000, 540-55), "full", 3])
    elif inventory[0] == 0:
        Texthelper.write(screen, [(1000, 540-55), "sorry", 3])
    else:
        Texthelper.write(screen, [(1000, 540-55), "repair", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(600, 540), "Fuel:", 3])
    if currentfuel == totalfuel:
        Texthelper.write(screen, [(1000, 540), "full", 3])
    elif inventory[1] == 0:
        Texthelper.write(screen, [(1000, 540), "sorry", 3])
    else:
         Texthelper.write(screen, [(1000, 540), "refill", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(600, 540+55), "Torpedoes:", 3])
    if ammunition == totalammunition:
        Texthelper.write(screen, [(1000, 540+55), "full", 3])
    elif inventory[4] == 0:
        Texthelper.write(screen, [(1000, 540+55), "sorry", 3])
    else:
        Texthelper.write(screen, [(1000, 540+55), "refill", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+110), "back", 3])
    pygame.display.flip()

def repairShopUI(screen, ShipLv, currentarmor, currentfuel, ammunition, totalarmor, totalfuel, totalammunition, homeInventory):
    upgrades = Filehelper("assets\\upgrades.txt")
    repairRefill = "none"
    status = "shop"
    if currentarmor != totalarmor and homeInventory[0] != 0:
        if Texthelper.writeButton(screen, [(1000, 540-55), "repair", 3]):
            if homeInventory[0] < int((totalarmor-currentarmor)/5):
                currentarmor += homeInventory[0] * 5
                homeInventory[0] = 0
            else:
                homeInventory[0] -= int((totalarmor-currentarmor)/5)
                currentarmor = totalarmor
            status = "shopinit"
    elif homeInventory[0] == 0:
        Texthelper.write(screen, [(1000, 540-55), "sorry", 3])
    else:
        Texthelper.write(screen, [(1000, 540-55), "full", 3])

    if currentfuel != totalfuel and homeInventory[1] != 0:
        if Texthelper.writeButton(screen, [(1000, 540), "refill", 3]):
            if homeInventory[1] < int((totalfuel-currentfuel)/250):
                currentfuel += homeInventory[1] * 250
                homeInventory[1] = 0
            else:
                homeInventory[1] -= int((totalfuel-currentfuel)/250)
                currentfuel = totalfuel
            status = "shopinit"
    elif homeInventory[1] == 0:
        Texthelper.write(screen, [(1000, 540), "sorry", 3])
    else:
        Texthelper.write(screen, [(1000, 540), "full", 3])

    if ammunition != totalammunition and homeInventory[4] != 0: 
        if Texthelper.writeButton(screen, [(1000, 540+55), "refill", 3]):
            if homeInventory[4] < int(totalammunition - ammunition):
                ammunition += homeInventory[4] 
                homeInventory[4] = 0
            else:
                homeInventory[4] -= int(totalammunition-ammunition)
                ammunition = totalammunition
            status = "shopinit"
    elif homeInventory[4] == 0:
        Texthelper.write(screen, [(1000, 540+55), "sorry", 3])
    else:
        Texthelper.write(screen, [("center", 540+55), "full", 3])
    
    if  Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    filehelper.set([currentarmor, currentfuel, ammunition],4)
    filehelper.set(homeInventory,2)
    return status

def garageinitUI(screen, ShipLv, inventory):
    pygame.mouse.set_visible(True)
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]) + "  torpedoes:" + str(inventory[4]),3])
    Texthelper.write(screen, [("center", 540-180), "upgrade shop", 6])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [(600, 540-55), "Armor: lv " + str(ShipLv[0]), 3])
    Texthelper.write(screen, [(1000, 540-55), "Upgrade", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(635, 540), "Fuel: lv " + str(ShipLv[1]), 3])
    Texthelper.write(screen, [(1000, 540), "Upgrade", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [(470, 540+55), "torpedoes:", 3])
    Texthelper.write(screen, [(810, 540+55), "lv " + str(ShipLv[2]), 3])
    if ShipLv[2] != 0:
        Texthelper.write(screen, [(1000, 540+55), "Upgrade", 3])
    else:
        Texthelper.write(screen, [(1000, 540+55), "locked", 3])
    pygame.display.flip()
        
    pygame.time.wait(waitTime)
    Texthelper.write(screen, [("center", 540+110), "back", 3])
    pygame.display.flip()


def GarageUI(screen):
    status = "garage"
    if Texthelper.writeButton(screen, [(1000, 540-55), "Upgrade", 3]):
        status = "armorUpgradeinit"
    elif Texthelper.writeButton(screen, [(1000, 540), "Upgrade", 3]):
        status = "fuelUpgradeinit"
    elif Texthelper.writeButton(screen, [(1000, 540+55), "Upgrade", 3]):
        status = "ammoUpgradeinit"
    elif Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    return status

def armorUpgradeinitUI(screen, ShipLv, inventory):
    drawUpgradeScreen(screen, ShipLv, inventory, True, "armor", "N/A")

def armorUpgradeUI(screen, ShipLv, inventory):
    return drawUpgradeScreen(screen, ShipLv, inventory, False, "armor", "armorUpgrade") #returns status

def fuelUpgradeinitUI(screen, ShipLv, inventory):
    drawUpgradeScreen(screen, ShipLv, inventory, True, "fuel", "N/A")

def fuelUpgradeUI(screen, ShipLv, inventory):
    return drawUpgradeScreen(screen, ShipLv, inventory, False, "fuel", "fuelUpgrade") #returns status

def ammoUpgradeinitUI(screen, ShipLv, inventory):
    drawUpgradeScreen(screen, ShipLv, inventory, True, "torpedoe", "N/A")

def ammoUpgradeUI(screen, ShipLv, inventory):
    return drawUpgradeScreen(screen, ShipLv, inventory, False, "torpedoe", "ammoUpgrade")
    
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
   
