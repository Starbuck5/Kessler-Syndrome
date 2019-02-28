from pgx import *
waitTime = 175
upgrades = Filehelper("assets\\upgrades.txt")

def drawInventory(screen, inventory):
    writestring = "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3])
    Texthelper.write(screen, [(0, 0), writestring,3])

#def drawBars()

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
            ##status = "garageinit"
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
    drawInventory(screen, inventory)
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
    drawInventory(screen, homeInventory)
    Texthelper.write(screen, [("center", 540-180), "home base", 6])
    if Texthelper.writeButton(screen, [("center", 540-55), "upgrade shop", 3]):
        status = "garageinit"
    if Texthelper.writeButton(screen, [("center", 540), "repair & refill shop", 3]):
        status = "shopinit"
    if Texthelper.writeButton(screen, [("center", 540+55), "market", 3]):
        status = "marketinit"
    message = "empty ship inventory"
    if shipInventory != [0,0,0,0]:
        message = "-+-empty ship inventory-+-" 
    if Texthelper.writeButton(screen, [("center", 540+110), message, 3]):
        homeInventory[0] += shipInventory[0]
        homeInventory[1] += shipInventory[1]
        homeInventory[2] += shipInventory[2]
        homeInventory[3] += shipInventory[3]
        for i in range(4): #can't just do = [0,0,0,0] because of scope and lists
            shipInventory[i] = 0
        status = "homeinit"
    if Texthelper.writeButton(screen, [("center", 540+165), "Resume", 3]):
        status = "game"
        pygame.mouse.set_visible(False)
    return status


class repairScreenStorage():
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)  #these really should be loaded only once
    armorpic = loadImage("Assets\\armor.tif")                       #they're already loaded in main
    

def drawRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, mode):   
    drawInventory(screen, homeInventory)
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

#increments or decrements an instance of inputgetter
def incrementBox(inputgetter, value):
    text = inputgetter.getData()
    number = inputgetter.getIntText()
    number += value
    text[1] = str(number)
    inputgetter.currenttext = text

#writes out a line with a -1, an inputgetter box, and a +1
def plusminusrow(screen, inputgetter, height):
    inputgetter.update(screen)
    if Texthelper.writeButtonBox(screen, [(900, height), "-1", 3]) and inputgetter.getIntText() > 0:
        incrementBox(inputgetter, -1)
    if Texthelper.writeButtonBox(screen, [(1100, height), "+1", 3]):
        incrementBox(inputgetter, 1)

def isoverfull(inputgetter, cap):
    if inputgetter.getIntText() <= cap:
        return True
    return False

TRADELIST = ["metal", "gas", "circuits"]
BUYVALUE = [10, 40, 120]
SELLVALUE = [5, 20, 60]

class marketStorage():
    metal = ""
    gas = ""
    circuits = ""
    def __init__(self):
        marketStorage.metal = InputGetter([(1000, 430), "0", 3], "int")
        marketStorage.gas = InputGetter([(1000, 485), "0", 3], "int")
        marketStorage.circuits = InputGetter([(1000, 540), "0", 3], "int")

#the currency to resource market of the galaxy, or at least this chunk of LEO      
def marketUI(screen, inventory, mode):
    if mode:
        marketStorage()
    metalbox = marketStorage.metal
    gasbox = marketStorage.gas
    circuitbox = marketStorage.circuits
    
    drawInventory(screen, inventory)
    Texthelper.write(screen, [("center", 540-235), "market", 6])
    if mode:
        timedFlip()

    status = "market"

    Texthelper.write(screen, [(500, 430), "metal:", 3])
    plusminusrow(screen, metalbox, 430)
    if mode:
        timedFlip()

    Texthelper.write(screen, [(500, 485), "gas:", 3])
    plusminusrow(screen, gasbox, 485)
    if mode:
        timedFlip()
        
    Texthelper.write(screen, [(500, 540), "circuits:", 3])
    plusminusrow(screen, circuitbox, 540)
    if mode:
        timedFlip()

    ableToSell = isoverfull(metalbox, inventory[0]) and isoverfull(gasbox, inventory[1]) and isoverfull(circuitbox, inventory[2])
    sellvalue = metalbox.getIntText()*SELLVALUE[0] + gasbox.getIntText() * SELLVALUE[1] + circuitbox.getIntText() * SELLVALUE[2]
    if not ableToSell:
        Texthelper.write(screen, [(900, 670), "you cannot sell what you do not have", 1])
    if Texthelper.writeButtonBox(screen, [("center", 625), "sell for " + str(sellvalue) + " credits", 3]) and ableToSell:
        inventory[0] -= metalbox.getIntText()
        inventory[1] -= gasbox.getIntText()
        inventory[2] -= circuitbox.getIntText()
        inventory[3] += sellvalue
        marketStorage()

    buyvalue = metalbox.getIntText()*BUYVALUE[0] + gasbox.getIntText() * BUYVALUE[1] + circuitbox.getIntText() * BUYVALUE[2]
    if Texthelper.writeButtonBox(screen, [("center", 700), "buy for " + str(buyvalue) + " credits", 3]) and inventory[3] >= buyvalue:
        inventory[0] += metalbox.getIntText()
        inventory[1] += gasbox.getIntText()
        inventory[2] += circuitbox.getIntText()
        inventory[3] -= buyvalue
        marketStorage()
        
    
    if Texthelper.writeButton(screen, [("center", 760), "back", 3]):
        status = "homeinit"        
    return status

def garageUI(screen, ShipLv, homeInventory, mode):
    status = "garage"
    inventory = homeInventory
    largestring = "metal:" + str(inventory[0]) + "  gas:" + str(inventory[1]) + "  circuits:" + str(inventory[2]) + "  currency:" + str(inventory[3])
    Texthelper.write(screen, [(0, 0), largestring, 3])
    Texthelper.write(screen, [("center", 540-180), "upgrade shop", 6])
    if mode:
        timedFlip()

    Texthelper.write(screen, [(600, 540-55), "Armor: lv " + str(ShipLv[0]), 3])
    if Texthelper.writeButton(screen, [(1000, 540-55), "Upgrade", 3]):
        status = "armorUpgradeinit"
    if mode:
        timedFlip()

    Texthelper.write(screen, [(635, 540), "Fuel: lv " + str(ShipLv[1]), 3])
    if Texthelper.writeButton(screen, [(1000, 540), "Upgrade", 3]):
        status = "fuelUpgradeinit"
    if mode:
        timedFlip()

    Texthelper.write(screen, [(470, 540+55), "torpedoes: lv " + str(ShipLv[2]), 3])
    if ShipLv[2] != 0:
        if Texthelper.writeButton(screen, [(1000, 540+55), "Upgrade", 3]):
            status = "ammoUpgradeinit"    
    else:
        Texthelper.write(screen, [(1000, 540+55), "locked", 3])
    if mode:
        timedFlip()

    if Texthelper.writeButton(screen, [("center", 540+110), "back", 3]):
        status = "homeinit"

    return status
        

class shopStorage():
    shopStatus = "home"
    shipLv = []
    shipInventory = []
    homeInventory = []
    currentStats = []
    totalStats = []
    color = ()

#actually the setup for home, not shop \< sorry for the confused naming
def setupShop(shipLv, shipInventory, homeInventory, currentStats, totalStats, color):
    shopStorage.shopStatus = "home"
    shopStorage.shipLv = shipLv
    shopStorage.shipInventory = shipInventory
    shopStorage.homeInventory = homeInventory
    shopStorage.currentStats = currentStats
    shopStorage.totalStats = totalStats
    shopStorage.color = color

#subsection of the great big main loop that deals with the various shops of zvezda
def home(screen):
    shopStatus = shopStorage.shopStatus
    shipLv = shopStorage.shipLv
    shipInventory = shopStorage.shipInventory
    homeInventory = shopStorage.homeInventory
    currentStats = shopStorage.currentStats
    totalStats = shopStorage.totalStats
    color = shopStorage.color
    screen.fill(color)

    ####MARKET#SECTION####
    if shopStatus == "marketinit":
        marketUI(screen, homeInventory, True)
        shopStatus = "market"

    elif shopStatus == "market":
        shopStatus = marketUI(screen, homeInventory, False)
    ####MARKET#SECTION####

    ####REPAIR#SECTION####
    elif shopStatus == "armorRepairinit":
        drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, True, "armor", "N/A", color)
        shopStatus = "armorRepair"   

    elif shopStatus == "armorRepair":
        shopStatus = drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, False, "armor", shopStatus, color)

    elif shopStatus == "fuelRefillinit":
        drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, True, "fuel", "N/A", color)
        shopStatus = "fuelRefill"

    elif shopStatus == "fuelRefill":
        shopStatus = drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, False, "fuel", shopStatus, color)

    elif shopStatus == "ammoRefillinit":
        drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, True, "torpedoes", "N/A", color)
        shopStatus = "ammoRefill"

    elif shopStatus == "ammoRefill":
        shopStatus = drawAllRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, False, "torpedoes", shopStatus, color)

    elif shopStatus == "shopinit":
        drawRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, True)
        shopStatus = "shop"

    elif shopStatus == "shop":
        shopStatus = drawRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, False)
    ####REPAIR#SECTION####

    ####UPGRADE#SECTION####
    elif shopStatus == "armorUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "armor", "N/A")
        shopStatus = "armorUpgrade"

    elif shopStatus == "armorUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "armor", "armorUpgrade")

    elif shopStatus == "fuelUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "fuel", "N/A")
        shopStatus = "fuelUpgrade"

    elif shopStatus == "fuelUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "fuel", "fuelUpgrade")

    elif shopStatus == "ammoUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "torpedoe", "N/A")
        shopStatus = "ammoUpgrade"

    elif shopStatus == "ammoUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "torpedoe", "ammoUpgrade")

    elif shopStatus == "garageinit":
        garageUI(screen, shipLv, homeInventory, True)
        shopStatus = "garage"

    elif shopStatus == "garage":
        shopStatus = garageUI(screen, shipLv, homeInventory, False)
    ####UPGRADE#SECTION####

    elif shopStatus == "homeinit":
        shopStatus = "home"
    
    elif shopStatus == "home":
        shopStatus = homeUI(screen, shipInventory, homeInventory)
    
    shopStorage.shopStatus = shopStatus
    pygame.display.flip()
    if shopStatus != "game":
        return "home"
    else:
        return shopStatus


def drawPauseUI(screen, mode):
    status = "paused"
    Texthelper.write(screen, [("center", 540-136), "Paused", 6])
    if mode:
        timedFlip()
        
    if Texthelper.writeButton(screen, [("center", 540-55), "Resume", 2]):
        status = "game"
    if mode:
        timedFlip()

    if Texthelper.writeButton(screen, [("center", 540-20), "Restart", 2]):
        status = "gameinit"
    if mode:
        timedFlip()

    if Texthelper.writeButton(screen, [("center", 540+15), "Quit to menu", 2]):
        status = "menuinit"
    if mode:
        timedFlip()

    if Texthelper.writeButton(screen, [("center", 540+50), "Quit to desktop", 2]):
        status = "exiting"
    pygame.display.flip()
    return status

def mapscreenUI(screen):
    status = "mapscreen"
    if Texthelper.writeButton(screen, [(180, 520), "[Commence Flying]", 2.5]):
        status = "game"
        pygame.mouse.set_visible(False)
    return status
