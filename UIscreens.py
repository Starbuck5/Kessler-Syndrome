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
    pointName = -1
    
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
        UpgradeScreenStorage.pointName = pointName

    currentStat = UpgradeScreenStorage.currentStat
    cost = UpgradeScreenStorage.cost
    addedStat = UpgradeScreenStorage.addedStat
    editingIndex = UpgradeScreenStorage.editingIndex
    pointName = UpgradeScreenStorage.pointName
    
    pygame.mouse.set_visible(True) #necessary?
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-235), name + " upgrade", 6])

    if mode:
        timedFlip()       
    Texthelper.write(screen, [("center", 540-110), "lv: " + str(ShipLv[0]) + " +1   " + "Stats: " + str(currentStat) + " +" + str(addedStat) + " " + pointName, 3])
    
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
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]),3])
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
        shipInventory = [0,0,0,0,0]
        status = "homeinit"
    if Texthelper.writeButton(screen, [("center", 540+165), "Resume", 3]):
        status = "game"
        pygame.mouse.set_visible(False)
    return [status, shipInventory]


class repairScreenStorage():
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)  #these really should be loaded only once
    armorpic = loadImage("Assets\\armor.tif")                       #they're already loaded in main
    

def drawRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, mode):   
    Texthelper.write(screen, [(0, 0), "metal:" + str(homeInventory[0]) + "  gas:" + str(homeInventory[1]) + "  circuits:" + str(homeInventory[2]) +
                              "  currency:" + str(homeInventory[3]),3])
    Texthelper.write(screen, [("center", 540-180), "repair & refill shop", 6])
    status = "shop"                         
    fuelpic = repairScreenStorage.fuelpic
    armorpic = repairScreenStorage.armorpic
    currentarmor, currentfuel, ammunition = currentStats
    totalarmor, totalfuel, totalammunition = totalStats
    if mode:
        timedFlip()
        
    #armor
    screen.blit(armorpic, (1600, 930))
    pygame.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
    pygame.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])
    Texthelper.write(screen, [(600, 540-55), "Armor:", 3])   
    if Texthelper.writeButton(screen, [(1000, 540-55), "repair", 3]):
        status = "armorRepairinit"
    if mode:
        timedFlip()

    #fuel
    screen.blit(fuelpic, (1600, 1000))
    pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
    pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])        
    Texthelper.write(screen, [(600, 540), "Fuel:", 3])   
    if Texthelper.writeButton(screen, [(1000, 540), "refill", 3]):
        status = "fuelRefillinit"
    if mode:
        timedFlip()

    #ammunition
    Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])
    Texthelper.write(screen, [(600, 540+55), "Torpedoes:", 3])  
    if Texthelper.writeButton(screen, [(1000, 540+55), "refill", 3]):
        status = "ammoRefillinit"
    if mode:
        timedFlip()
        
    if Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    if mode:
        pygame.display.flip()
    return status

class allRepairScreenStorage():
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)  #these really should be loaded only once
    armorpic = loadImage("Assets\\armor.tif")                       #they're already loaded in main
    editingIndex = -1
    repairRefill = -1
    pointName = -1
    missingStat = -1
    costRatio = -1
    amountBox = -1

def drawAllRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, mode, name, status, color):
    screen.fill(color)
    inputvar = keyboard()
    currentarmor = currentStats[0]
    currentfuel = currentStats[1]
    ammunition = currentStats[2]
    totalarmor = totalStats[0]
    totalfuel = totalStats[1]
    if mode: #whether it should be init-ing or not\
        if name == "armor":
            editingIndex = 0
            pointName = "hp"
            costRatio = 1/3
            repairRefill = "repair"
        if name == "fuel":
            editingIndex = 1
            pointName = "fp"
            costRatio = 1/250
            repairRefill = "refill"
        if name == "torpedoes":
            editingIndex = 2
            pointName = "ammo"
            costRatio = 1/5
            repairRefill = "refill"
        allRepairScreenStorage.editingIndex = editingIndex
        allRepairScreenStorage.repairRefill = repairRefill
        allRepairScreenStorage.pointName = pointName
        allRepairScreenStorage.costRatio = costRatio
        missingStat = totalStats[editingIndex] - currentStats[editingIndex]
        allRepairScreenStorage.missingStat = missingStat
        amountBox = InputGetter([("center", 540+165), str(missingStat), 3], "int")
        allRepairScreenStorage.amountBox = amountBox

    editingIndex = allRepairScreenStorage.editingIndex
    repairRefill = allRepairScreenStorage.repairRefill
    pointName = allRepairScreenStorage.pointName
    missingStat = allRepairScreenStorage.missingStat
    costRatio = allRepairScreenStorage.costRatio
    amountBox = allRepairScreenStorage.amountBox
    if amountBox.currenttext[1] != "":
        cost = int(costRatio * int(amountBox.currenttext[1])) + 1
        if cost - 1 == costRatio * int(amountBox.currenttext[1]):
            cost -= 1
    else:
        cost = 0
    if editingIndex == 0:
        metalCost = cost
        gasCost = 0
    elif editingIndex == 1:
        metalCost = 0
        gasCost = cost
    else:
        metalCost = cost
        gasCost = cost
    fuelpic = allRepairScreenStorage.fuelpic
    armorpic = allRepairScreenStorage.armorpic

    Texthelper.write(screen, [(0, 0), "metal:" + str(homeInventory[0]) + "  gas:" + str(homeInventory[1]) + "  circuits:" + str(homeInventory[2]) +
                              "  currency:" + str(homeInventory[3]),3])
    Texthelper.write(screen, [("center", 540-235), repairRefill + " " + name, 6])

    if mode:
        timedFlip()       
    Texthelper.write(screen, [("center", 540-110),  "missing: " + str(missingStat) + " " + pointName, 3])

    if mode:
        timedFlip()
    Texthelper.write(screen, [("center", 540),  "cost:", 3])
    screen.blit(armorpic, (1600, 930))
    pygame.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
    pygame.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])

    if mode:
        timedFlip()
    Texthelper.write(screen, [(700, 540+55),  str(metalCost) + " metal" , 3])
    Texthelper.write(screen, [(1100, 540+55),  str(gasCost) + " gas" , 3])
    screen.blit(fuelpic, (1600, 1000))
    pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
    pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])

    if mode:
        timedFlip()
    Texthelper.write(screen, [("center", 540+110),  "amount:" , 3])

    if mode:
        timedFlip()
    amountBox.currenttext = [("center", 540+165), amountBox.getData()[1], amountBox.getData()[2]]
    amountBox.update(screen)
    allRepairScreenStorage.amountBox = amountBox

    if mode:
        timedFlip()
    if amountBox.currenttext[1] != "":
        if metalCost <= homeInventory[0] and gasCost <= homeInventory[1] and missingStat != 0 and int(amountBox.currenttext[1]) <= missingStat:
            if Texthelper.writeButton(screen, [("center", 540+220), repairRefill, 3]):
                currentStats[editingIndex] += int(amountBox.currenttext[1])
                homeInventory[0] -= metalCost
                homeInventory[1] -= gasCost
                status = "shopinit"
        elif missingStat == 0:
            Texthelper.write(screen, [("center", 540+220), "full", 3])
        elif int(amountBox.currenttext[1]) > missingStat:
            Texthelper.write(screen, [("center", 540+220), "excess", 3])
        else:
            Texthelper.write(screen, [("center", 540+220), "sorry", 3])
        Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])
    else:
        if metalCost <= homeInventory[0] and gasCost <= homeInventory[1] and missingStat != 0:
            if Texthelper.writeButton(screen, [("center", 540+220), repairRefill, 3]):
                status = "shopinit"
        elif missingStat == 0:
            Texthelper.write(screen, [("center", 540+220), "full", 3])
        Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])

    if mode:
        timedFlip()
    if Texthelper.writeButton(screen, [("center", 540+275), "back", 3]):
        status = "shopinit"

    if mode:
        pygame.display.flip()

    if not mode:
        filehelper.set(homeInventory,2)
        filehelper.set(currentStats,4)

    return status
    
def marketinitUI(screen, inventory):
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-235), "market", 6])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [(500, 540-110), "metal:", 3])
    Texthelper.write(screen, [(900, 540-110), "buy", 3])
    Texthelper.write(screen, [(1100, 540-110), "sell", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [(500, 540-55), "gas:", 3])
    Texthelper.write(screen, [(900, 540-55), "buy", 3])
    Texthelper.write(screen, [(1100, 540-55), "sell", 3])
    pygame.display.flip()

    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [(500, 540), "circuits:", 3])
    Texthelper.write(screen, [(900, 540), "buy", 3])
    Texthelper.write(screen, [(1100, 540), "sell", 3])
    pygame.display.flip()
    
    pygame.time.wait(waitTime)   
    Texthelper.write(screen, [("center", 540+110), "back", 3])
    pygame.display.flip()

def marketUI(screen, inventory):
    status = "market"
    if Texthelper.writeButton(screen, [(900, 540-110), "buy", 3]):
        status = "buyMetalinit"
    elif Texthelper.writeButton(screen, [(1100, 540-110), "sell", 3]):
        status = "sellMetalinit"
    elif Texthelper.writeButton(screen, [(900, 540-55), "buy", 3]):
        status = "buyGasinit"
    elif Texthelper.writeButton(screen, [(1100, 540-55), "sell", 3]):
        status = "sellGasinit"
    elif Texthelper.writeButton(screen, [(900, 540), "buy", 3]):
        status = "buyCircuitsinit"
    elif Texthelper.writeButton(screen, [(1100, 540), "sell", 3]):
        status = "sellCircuitsinit"
    elif Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"
    return status

class marketScreenStorage():
    cost = -1
    editingIndex = -1
    pointName = -1
    buySell = -1
    amountBox = -1
    
def drawMarketScreen(screen, inventory, mode, name, status, color):
    screen.fill(color)
    inputvar = keyboard()
    if mode: #whether it should be init-ing or not
        amountBox = InputGetter([("center", 540+110), "1", 3], "int")
        if name == "buyMetal":
            editingIndex = 0
            pointName = "metal"
            cost = 10
            buySell = "buy"
        if name == "buyGas":
            editingIndex = 1
            pointName = "gas"
            cost = 40
            buySell = "buy"
        if name == "buyCircuits":
            editingIndex = 2
            pointName = "circuits"
            cost = 120
            buySell = "buy"
        if name == "sellMetal":
            editingIndex = 0
            pointName = "metal"
            cost = 5
            buySell = "sell"
        if name == "sellGas":
            editingIndex = 1
            pointName = "gas"
            cost = 20
            buySell = "sell"
        if name == "sellCircuits":
            editingIndex = 2
            pointName = "circuits"
            cost = 60
            buySell = "sell"
        marketScreenStorage.cost = cost
        marketScreenStorage.editingIndex = editingIndex
        marketScreenStorage.pointName = pointName
        marketScreenStorage.buySell = buySell
        marketScreenStorage.amountBox = amountBox
        
    editingIndex = marketScreenStorage.editingIndex
    pointName = marketScreenStorage.pointName
    buySell = marketScreenStorage.buySell
    amountBox = marketScreenStorage.amountBox
    if amountBox.currenttext[1] != "":
        cost = marketScreenStorage.cost * int(amountBox.currenttext[1])
    else:
        cost = 0

    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]),3])
    Texthelper.write(screen, [("center", 540-235), buySell + " " + pointName, 6])

    if mode:
        timedFlip()       
    Texthelper.write(screen, [("center", 540-110), pointName + " +" + amountBox.currenttext[1], 3])
    
    if mode:
        timedFlip()
    if buySell == "buy":
        Texthelper.write(screen, [("center", 540),"cost: " + str(cost) + " currency", 3])
    else:
        Texthelper.write(screen, [("center", 540),"value: " + str(cost) + " currency", 3])

    if mode:
        timedFlip()
    Texthelper.write(screen, [("center", 540+55),"amount:", 3])

    if mode:
        timedFlip()
    amountBox.currenttext = [("center", 540+110), amountBox.getData()[1], amountBox.getData()[2]]
    amountBox.update(screen)
    marketScreenStorage.amountBox = amountBox
        
    if mode:
        timedFlip()
    if buySell == "buy":
        if inventory[3] >= cost:
            if Texthelper.writeButton(screen, [("center", 540+165), "buy", 3]):
                inventory[3] -= cost
                if amountBox.currenttext[1] != "":
                    inventory[editingIndex] += int(amountBox.currenttext[1])
                else:
                    pass
                status = "marketinit"
        else:
            Texthelper.write(screen, [("center", 540+165), "sorry", 3])
    else:
        if inventory[editingIndex] != 0:
            if Texthelper.writeButton(screen, [("center", 540+165), "sell", 3]):
                inventory[3] += cost
                inventory[editingIndex] -= 1
                status = "marketinit"
        else:
            Texthelper.write(screen, [("center", 540+165), "sorry", 3])

    if mode:
        timedFlip()
    if Texthelper.writeButton(screen, [("center", 540+220), "back", 3]):
        status = "marketinit"

    if mode:
        timedFlip()
    if not mode:
        filehelper.set(inventory,2)
        
    return status

def garageinitUI(screen, ShipLv, inventory):
    pygame.mouse.set_visible(True)
    Texthelper.write(screen, [(0, 0), "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3]),3])
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
   
