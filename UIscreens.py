from pgx import *
import graphics
import game
waitTime = 175
maxLevel = 20
upgrades = Filehelper("assets\\data\\upgrades.txt")

def timedFlip(mode):
    if mode:
        pygame.display.flip()
        pygame.time.wait(waitTime)

#draws square of a list of costs [metal, gas, circuits, currency]
#location is (x,y) - x=left column of costs, y=y location of "cost:" printout
def drawCostSquare(screen, location, cost, mode):
    x,y = location
    Texthelper.write(screen, [("center", y), "cost:", 3])
    timedFlip(mode) 

    Texthelper.write(screen, [(x, y+55), str(cost[0]) + " metal", 3], color = (120,120,120))
    Texthelper.write(screen, [(x+400, y+55), str(cost[1]) + " gas", 3], color = (185,20,20))
    timedFlip(mode) 

    Texthelper.write(screen, [(x, y+110), str(cost[2]) + " circuits", 3], color = (20,185,20))
    Texthelper.write(screen, [(x+400, y+110), str(cost[3]) + " credits", 3], color = (230,180,20))
    timedFlip(mode)

class UpgradeScreenStorage():
    currentStat = -1
    addedStat = -1
    cost = -1
    editingIndex = -1
    pointName = -1
    
def drawUpgradeScreen(screen, ShipLv, inventory, mode, upgradeType, status, currentStats, totalStats): #mode = true/false init, upgradeType = fuel/armor/etc.   
    if mode: #whether it should be init-ing or not
        if upgradeType == "armor":
            editingIndex = 0
            pointName = "hp"
        if upgradeType == "fuel":
            editingIndex = 1
            pointName = "fp"
        if upgradeType == "torpedoe":
            editingIndex = 2
            pointName = "ammo"
        driveHead = editingIndex * maxLevel
        UpgradeScreenStorage.currentStat = upgrades.get(ShipLv[editingIndex]+driveHead)[4] 
        UpgradeScreenStorage.cost = upgrades.get(ShipLv[editingIndex]+driveHead+1)
        UpgradeScreenStorage.addedStat = UpgradeScreenStorage.cost[4] - UpgradeScreenStorage.currentStat
        UpgradeScreenStorage.editingIndex = editingIndex
        UpgradeScreenStorage.pointName = pointName

    currentStat = UpgradeScreenStorage.currentStat
    cost = UpgradeScreenStorage.cost
    addedStat = UpgradeScreenStorage.addedStat
    editingIndex = UpgradeScreenStorage.editingIndex
    pointName = UpgradeScreenStorage.pointName
    
    pygame.mouse.set_visible(True) #necessary?
    graphics.drawInventory(screen, inventory)
    Texthelper.write(screen, [("center", 540-235), upgradeType + " upgrade", 6])
    timedFlip(mode)     

    if ShipLv[editingIndex] >= maxLevel:
        Texthelper.write(screen, [("center", 540), "max level", 3])
    else:
        Texthelper.write(screen, [("center", 540-110), "lv: " + str(ShipLv[editingIndex]) + " +1   " + "Stats: " + str(currentStat) + " +" + str(addedStat) + " " + pointName, 3])
        timedFlip(mode)         
        drawCostSquare(screen, (600, 540), cost, mode)

        if inventory[0] >= cost[0] and inventory[1] >= cost[1] and inventory[2] >= cost[2] and inventory[3] >= cost[3]:
            if Texthelper.writeButton(screen, [("center", 540+220), "Upgrade", 3]):
                inventory[0] -= cost[0]
                inventory[1] -= cost[1]
                inventory[2] -= cost[2]
                inventory[3] -= cost[3]
                ShipLv[editingIndex] += 1
                filehelper.set(inventory, 2)
                filehelper.set(ShipLv, 3)

                #prevents bug with stats not updating
                totalStats[editingIndex] = upgrades.get(ShipLv[editingIndex] + editingIndex * maxLevel)[4]            
                currentStats[editingIndex] = totalStats[editingIndex]
                
                UpgradeScreenStorage.currentStat = upgrades.get(ShipLv[editingIndex] + editingIndex * maxLevel)[4] 
                UpgradeScreenStorage.cost = upgrades.get(ShipLv[editingIndex] + editingIndex * maxLevel + 1)
                UpgradeScreenStorage.addedStat = UpgradeScreenStorage.cost[4] - UpgradeScreenStorage.currentStat
                UpgradeScreenStorage.editingIndex = editingIndex
                UpgradeScreenStorage.pointName = pointName
        else:
            Texthelper.write(screen, [("center", 540+220), "sorry", 3])
        timedFlip(mode)       
     
    if Texthelper.writeButton(screen, [("center", 540+275), "back", 3]):
        status = "garageinit"
    
    if mode:
        pygame.display.flip()

    return status

#drawSpecialUpgrade pulls these based on shipLv index being modified
upgrade_explanations = [0, 0, 0, "Increases drops by 50%"] 

#these upgrade screens only have one upgrade from 0 to 1 in the shipLv list
def drawSpecialUpgrade(screen, mode, shipLv, index, title, cost, status, inventory):
    graphics.drawInventory(screen, inventory)
    Texthelper.write(screen, [("center", 540-235), title, 6])
    timedFlip(mode)

    if shipLv[index] > 0:
        Texthelper.write(screen, [("center", 540), "max level", 3])
    else:
        Texthelper.write(screen, [("center", 450), upgrade_explanations[index], 2])
        timedFlip(mode)         
        drawCostSquare(screen, (600, 540), cost, mode)
        
        if inventory[0] >= cost[0] and inventory[1] >= cost[1] and inventory[2] >= cost[2] and inventory[3] >= cost[3]:
            if Texthelper.writeButton(screen, [("center", 540+220), "Upgrade", 3]):
                inventory[0] -= cost[0]
                inventory[1] -= cost[1]
                inventory[2] -= cost[2]
                inventory[3] -= cost[3]
                shipLv[index] += 1
                filehelper.set(inventory, 2)
                filehelper.set(shipLv, 3)
        else:
            Texthelper.write(screen, [("center", 540+220), "sorry", 3])
        timedFlip(mode)       
     
    if Texthelper.writeButton(screen, [("center", 540+275), "back", 3]):
        status = "garageinit"

    return status

def homeinitUI(screen, inventory):
    pygame.mouse.set_visible(True)
    graphics.drawInventory(screen, inventory)
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
    graphics.drawInventory(screen, homeInventory)
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

    #Quests
    #refueling the airmans ship
    if filehelper.get(0)[3] == 3:
        if homeInventory[1] >= 20:
            if Texthelper.writeButtonBox(screen, [("center", 540+220), "send 20 gas to the airman", 3], color=(34,178,34)):
                homeInventory[1] -= 20
                filehelper.setElement(4, 0, 3)
                game.deleteObject(110, 11, screen.get_width(), screen.get_height())   
        else:
            Texthelper.writeBox(screen, [("center", 540+220), "send 20 gas to the airman", 3], color=(178,34,34))
    #getting the airman his circuits
    if filehelper.get(0)[3] == 5:
        if homeInventory[2] >= 10:
            if Texthelper.writeButtonBox(screen, [("center", 540+220), "send 10 circuits to the airman", 3], color=(34,178,34)):
                homeInventory[2] -= 10
                filehelper.setElement(6, 0, 3)   
        else:
            Texthelper.writeBox(screen, [("center", 540+220), "send 10 circuits to the airman", 3], color=(178,34,34))

    return status


class repairScreenStorage():
    armorcost = 1/3
    fuelcost = 1/250
    torpedocost = 1/5
    costlist = [1/3, 1/250, 1/5]
    costnamelist = ["metal", "gas", "metal"]
    namelist = ["Armor", "Fuel", "Torpedoes"]
    shortattribute = ["HP", "FP", "Shots"]
    wordlist = ["repair", "refill", "refill"]
    applycost = [(1,0,0,0), (0,1,0,0), (1,1,0,0)]

def canAfford(homeInventory, costSpread, cost):
    flag = True
    for i in range(len(costSpread)):
        if costSpread[i] == 1:
            if not homeInventory[i] >= cost:
                flag = False
    return flag

def applyCosts(homeInventory, costSpread, cost):
    for i in range(len(costSpread)):
        if costSpread[i] == 1:
            homeInventory[i] -= cost
    return homeInventory

def buttonRow(screen, index, x, y, currentStats, totalStats, homeInventory):
    Texthelper.write(screen, [("right." + str(x+100), y), repairScreenStorage.namelist[index]+":", 3])
    
    totalrepaircost = int((totalStats[index] - currentStats[index]) * repairScreenStorage.costlist[index])
    repair1cost = 3
    repair1effect = int(1/repairScreenStorage.costlist[index]*repair1cost)
    repair2cost = 1
    repair2effect = int(1/repairScreenStorage.costlist[index]*repair2cost)

    costname = repairScreenStorage.costnamelist[index]
    totalRepairStr = "for " + str(totalrepaircost) + " " + costname
    repair1Str = "for " + str(repair1cost) + " " + costname
    repair2Str = "for " + str(repair2cost) + " " + costname
    if index == 2: #if torpedoes are being refilled    
        totalRepairStr += " and " + str(totalrepaircost) + " gas"
        repair1Str += " and " + str(repair1cost) + " gas"
        repair2Str +=" and " + str(repair2cost) + " gas"
        
    
    attribute = " " + repairScreenStorage.shortattribute[index]
    verb = repairScreenStorage.wordlist[index]
    costSpread = repairScreenStorage.applycost[index]
    
    if currentStats[index] < totalStats[index]:
        #full repair
        if canAfford(homeInventory, costSpread, totalrepaircost):
            if Texthelper.writeButtonBox(screen, [(x+130, y), verb + " all", 3], color=(34,178,34)):
                applyCosts(homeInventory, costSpread, totalrepaircost)
                currentStats[index] = totalStats[index]
        else:
            Texthelper.writeBox(screen, [(x+130, y), verb + " all", 3], color=(178,34,34))

        #repair1    
        if canAfford(homeInventory, costSpread, repair1cost):
            if Texthelper.writeButtonBox(screen, [(x+520, y), verb + " " + str(repair1effect) + attribute, 3], color=(34,178,34)):
                applyCosts(homeInventory, costSpread, repair1cost)
                currentStats[index] = min(currentStats[index]+repair1effect, totalStats[index])
        else:
            Texthelper.writeBox(screen, [(x+520, y), verb + " " + str(repair1effect) + attribute, 3], color=(178,34,34))

        #repair2
        if canAfford(homeInventory, costSpread, repair2cost):
            if Texthelper.writeButtonBox(screen, [(x+1000, y), verb + " " + str(repair2effect) + attribute, 3], color=(34,178,34)):
                applyCosts(homeInventory, costSpread, repair2cost)
                currentStats[index] = min(currentStats[index]+repair2effect, totalStats[index])
        else:
            Texthelper.writeBox(screen, [(x+1000, y), verb + " " + str(repair2effect) + attribute, 3], color=(178,34,34))
    
    else:
        Texthelper.writeBox(screen, [(x+130, y), verb + " all", 3], color=(34,34,178))
        Texthelper.writeBox(screen, [(x+520, y), verb + " " + str(repair1effect) + attribute, 3], color=(34,34,178))
        Texthelper.writeBox(screen, [(x+1000, y), verb + " " + str(repair2effect) + attribute, 3], color=(34,34,178))
    Texthelper.write(screen, [(x+180, y+45), totalRepairStr, 1])
    Texthelper.write(screen, [(x+570, y+45), repair1Str, 1])
    Texthelper.write(screen, [(x+1050, y+45), repair2Str, 1])

def drawRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, mode):   
    graphics.drawInventory(screen, homeInventory)

    #draws fuel and armor and shots
    currentarmor, currentfuel, ammunition = currentStats
    totalarmor, totalfuel, totalammunition = totalStats
    graphics.InfoBars.draw(screen, currentfuel, totalfuel, currentarmor, totalarmor, ammunition, totalammunition)
        
    Texthelper.write(screen, [("center", 540-180), "repair & refill shop", 6])
    status = "shop"                         
    timedFlip(mode)
        
    #armor
    buttonRow(screen, 0, 360, 480, currentStats, totalStats, homeInventory)
    timedFlip(mode)
    
    #fuel     
    buttonRow(screen, 1, 360, 580, currentStats, totalStats, homeInventory)
    timedFlip(mode)

    #ammunition
    buttonRow(screen, 2, 360, 680, currentStats, totalStats, homeInventory)
    timedFlip(mode)
        
    if Texthelper.writeButton(screen, [("center", 820), "back", 3]):
        status = "homeinit"
    if mode:
        pygame.display.flip()
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
    if Texthelper.writeButtonBox(screen, [(850, height), "-10", 3]):
        if inputgetter.getIntText() >= 10:
            incrementBox(inputgetter, -10)
        else:
            incrementBox(inputgetter, -1 * inputgetter.getIntText())
    if Texthelper.writeButtonBox(screen, [(975, height), "-1", 3]) and inputgetter.getIntText() > 0:
        incrementBox(inputgetter, -1)
    if Texthelper.writeButtonBox(screen, [(1200, height), "+1", 3]):
        incrementBox(inputgetter, 1)
    if Texthelper.writeButtonBox(screen, [(1295, height), "+10", 3]):
        incrementBox(inputgetter, 10)

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
        marketStorage.metal = InputGetter([("center.1125", 430), "0", 3], "int")
        marketStorage.gas = InputGetter([("center.1125", 485), "0", 3], "int")
        marketStorage.circuits = InputGetter([("center.1125", 540), "0", 3], "int")

#the currency to resource market of the galaxy, or at least this chunk of LEO      
def marketUI(screen, inventory, mode):
    if mode:
        marketStorage()
    metalbox = marketStorage.metal
    gasbox = marketStorage.gas
    circuitbox = marketStorage.circuits
    
    graphics.drawInventory(screen, inventory)
    Texthelper.write(screen, [("center", 540-235), "market", 6])
    timedFlip(mode)

    status = "market"

    Texthelper.write(screen, [(500, 430), "metal:", 3], color=(120,120,120))
    plusminusrow(screen, metalbox, 430)
    timedFlip(mode)

    Texthelper.write(screen, [(500, 485), "gas:", 3], color=(185,20,20))
    plusminusrow(screen, gasbox, 485)
    timedFlip(mode)
        
    Texthelper.write(screen, [(500, 540), "circuits:", 3], color=(20,185,20))
    plusminusrow(screen, circuitbox, 540)
    timedFlip(mode)

    ableToSell = isoverfull(metalbox, inventory[0]) and isoverfull(gasbox, inventory[1]) and isoverfull(circuitbox, inventory[2])
    sellvalue = metalbox.getIntText()*SELLVALUE[0] + gasbox.getIntText() * SELLVALUE[1] + circuitbox.getIntText() * SELLVALUE[2]
    buyvalue = metalbox.getIntText()*BUYVALUE[0] + gasbox.getIntText() * BUYVALUE[1] + circuitbox.getIntText() *BUYVALUE[2]
    if (sellvalue > 0):
        if not ableToSell:
            Texthelper.write(screen, [("center", 670), "you cannot sell what you do not have", 1], color=(178,34,34))
            Texthelper.writeBox(screen, [("center", 625), "sell for " + str(sellvalue) + " credits", 3], color=(178,34,34))
        elif Texthelper.writeButtonBox(screen, [("center", 625), "sell for " + str(sellvalue) + " credits", 3], color=(34, 178, 34)):
            inventory[0] -= metalbox.getIntText()
            inventory[1] -= gasbox.getIntText()
            inventory[2] -= circuitbox.getIntText()
            inventory[3] += sellvalue
            marketStorage()

        timedFlip(mode)

        if buyvalue > inventory[3]:
            Texthelper.write(screen, [("center", 745), "you cannot afford this", 1], color=(178,34,34))
            Texthelper.writeBox(screen, [("center", 700), "buy for " + str(buyvalue) + " credits", 3], color=(178,34,34))
        elif Texthelper.writeButtonBox(screen, [("center", 700), "buy for " + str(buyvalue) + " credits", 3], color=(34, 178, 34)):
            inventory[0] += metalbox.getIntText()
            inventory[1] += gasbox.getIntText()
            inventory[2] += circuitbox.getIntText()
            inventory[3] -= buyvalue
            marketStorage()
    else: #text is blue if all inputs are zero
        Texthelper.writeBox(screen, [("center", 625), "sell for " + str(sellvalue) + " credits", 3], color=(34, 34, 178))
        timedFlip(mode)
        Texthelper.writeBox(screen, [("center", 700), "buy for " + str(buyvalue) + " credits", 3], color=(34, 34, 178))
        
    timedFlip(mode)

    if Texthelper.writeButton(screen, [("center", 780), "back", 3]):
        status = "homeinit"        
    return status

def garageUI(screen, ShipLv, homeInventory, mode):
    status = "garage"
    inventory = homeInventory
    graphics.drawInventory(screen, inventory)
    Texthelper.write(screen, [("center", 540-180), "upgrade shop", 6])
    timedFlip(mode)

    Texthelper.write(screen, [(600, 540-55), "Armor: lv " + str(ShipLv[0]), 3])
    if Texthelper.writeButton(screen, [(1000, 540-55), "Upgrade", 3]):
        status = "armorUpgradeinit"
    timedFlip(mode)

    Texthelper.write(screen, [(635, 540), "Fuel: lv " + str(ShipLv[1]), 3])
    if Texthelper.writeButton(screen, [(1000, 540), "Upgrade", 3]):
        status = "fuelUpgradeinit"
    timedFlip(mode)

    Texthelper.write(screen, [(470, 540+55), "torpedoes: lv " + str(ShipLv[2]), 3])
    if ShipLv[2] != 0:
        if Texthelper.writeButton(screen, [(1000, 540+55), "Upgrade", 3]):
            status = "ammoUpgradeinit"    
    else:
        Texthelper.write(screen, [(1000, 540+55), "locked", 3])
    timedFlip(mode)
    
    if ShipLv[3] == 0:
        Texthelper.write(screen, [(1200, 660), "[onetime]", 1])
        if Texthelper.writeButton(screen, [("center", 675), "upgrade scavenging module", 3]):
            status = "scavengeUpgradeinit"
    else:
        Texthelper.write(screen, [("center", 675), "superior scavenging module", 3])
        
    

    if Texthelper.writeButton(screen, [("center", 850), "back", 3]):
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
    elif shopStatus == "shopinit":
        drawRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, True)
        shopStatus = "shop"

    elif shopStatus == "shop":
        shopStatus = drawRepairScreen(screen, shipLv, currentStats, totalStats, homeInventory, False)
    ####REPAIR#SECTION####

    ####UPGRADE#SECTION####
    elif shopStatus == "armorUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "armor", "N/A", currentStats, totalStats)
        shopStatus = "armorUpgrade"

    elif shopStatus == "armorUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "armor", "armorUpgrade", currentStats, totalStats)

    elif shopStatus == "fuelUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "fuel", "N/A", currentStats, totalStats)
        shopStatus = "fuelUpgrade"

    elif shopStatus == "fuelUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "fuel", "fuelUpgrade", currentStats, totalStats)

    elif shopStatus == "ammoUpgradeinit":
        drawUpgradeScreen(screen, shipLv, homeInventory, True, "torpedoe", "N/A", currentStats, totalStats)
        shopStatus = "ammoUpgrade"

    elif shopStatus == "ammoUpgrade":
        shopStatus = drawUpgradeScreen(screen, shipLv, homeInventory, False, "torpedoe", "ammoUpgrade", currentStats, totalStats)

    elif shopStatus == "scavengeUpgradeinit":
        shopStatus = drawSpecialUpgrade(screen, True, shipLv, 3, "Upgrade Scavenging Module", [10, 2, 2, 35], "scavengeUpgrade", homeInventory)

    elif shopStatus == "scavengeUpgrade":
        shopStatus = drawSpecialUpgrade(screen, False, shipLv, 3, "Upgrade Scavenging Module", [10, 2, 2, 35], shopStatus, homeInventory)

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
    Texthelper.write(screen, [("center", 400), "Paused", 6])
    timedFlip(mode)
        
    spacing = 35
    if Texthelper.writeButton(screen, [("center", 485), "Resume", 2]):
        status = "game"
    timedFlip(mode)

    if Texthelper.writeButton(screen, [("center", 485 + spacing), "Options", 2]):
        status = "optionsinit"
        OptionsInput.backStatus = "pauseinit"
    timedFlip(mode)

    if Texthelper.writeButton(screen, [("center", 485 + spacing * 2), "Quit to menu", 2]):
        status = "menuinit"
    timedFlip(mode)

    if Texthelper.writeButton(screen, [("center", 485 + spacing * 3), "Quit to desktop", 2]):
        status = "exiting"
    pygame.display.flip()
    return status

def mapscreenUI(screen, sector_map_coordinates, discoveredSectors, sectornum, DEVMODE, clearedSector):
    status = "mapscreen"

    line_color = (255, 255, 255)
    infinitypic = graphics.Images.get("infinity")
    for i in sector_map_coordinates.keys():
        if discoveredSectors[i] or DEVMODE: #only visited sectors are drawn
            graphics.drawSector(screen, sector_map_coordinates[i], i, sectornum, clearedSector[i])
            if game.sectorGeneration(i): #draws infinity signs on map if regenerating sector
                screen.blit(infinitypic, (sector_map_coordinates[i][0] - 10, sector_map_coordinates[i][1] + 15)) 
            #draws all links between sectors
            connections = game.sectorDestinations(i)
            for j in range(4):
                adjacentSector = connections[j]
                if adjacentSector != -1:
                    if j == 0:
                        line_start = (sector_map_coordinates[i][0] - 40, sector_map_coordinates[i][1])
                        line_end = (sector_map_coordinates[adjacentSector][0] + 40,
                                    sector_map_coordinates[adjacentSector][1])
                    elif j == 1:
                        line_start = (sector_map_coordinates[i][0], sector_map_coordinates[i][1] - 40)
                        line_end = (sector_map_coordinates[adjacentSector][0],
                                    sector_map_coordinates[adjacentSector][1] + 40)
                    elif j == 2:
                        line_start = (sector_map_coordinates[i][0] + 40, sector_map_coordinates[i][1])
                        line_end = (sector_map_coordinates[adjacentSector][0] - 40,
                                    sector_map_coordinates[adjacentSector][1])
                    elif j == 3:
                        line_start = (sector_map_coordinates[i][0], sector_map_coordinates[i][1] + 40)
                        line_end = (sector_map_coordinates[adjacentSector][0],
                                    sector_map_coordinates[adjacentSector][1] - 40)
                    draw.aaline(screen, line_color, line_start, line_end)
                    #if an adjacent sector has not been visited, it is drawn with a ?
                    if (not discoveredSectors[adjacentSector]) and (not DEVMODE):
                        graphics.drawSector(screen, sector_map_coordinates[adjacentSector], "?", sectornum, False)
                        
    if Texthelper.writeButton(screen, [(180, 520), "[Commence Flying]", 2.5]):
        status = "game"
        pygame.mouse.set_visible(False)
        
    return status

class OptionsInput():
    width = ""
    height = ""
    
    #directly set by main before options is called, controls what status is called by the back button
    backStatus = "OptionsInput.backStatus needs to be set before use"

    def __init__(self, resolution):
        OptionsInput.width = InputGetter([(1000, 400), str(resolution[0]), 3], "int")
        OptionsInput.height = InputGetter([(1000 + 250, 400), str(resolution[1]), 3], "int")

def optionsUIinit(screen, file_settings):
    pygame.mouse.set_visible(True)
    OptionsInput([file_settings[0], file_settings[1]])

def drawSettingsOption(screen, settingName, x, y, file_settings, settingsIndex, *argv): #settingsIndex is the index of the setting in file_settings
    #*argv is for specifying the on/off text of the setting. Default is "On"/"Off"
    Texthelper.write(screen, [(x, y), settingName + ":", 3])
    if len(argv) > 0 and file_settings[settingsIndex]:
        text = argv[0]
    elif len(argv) > 0 and not file_settings[settingsIndex]:
        text = argv[1]
    elif file_settings[settingsIndex]:
        text = "On"
    else:
        text = "Off"
    if Texthelper.writeButton(screen, [(x + 400, y), text, 3]):
        file_settings[settingsIndex] = not file_settings[settingsIndex]

def optionsUI(screen, spacing, file_settings):
    status = "options"

    screen.fill((0, 0, 0))

    Texthelper.write(screen, [("center", 200), "Options", 6])

    Texthelper.write(screen, [(600, 400), "Resolution:", 3])

    OptionsInput.width.update(screen)
    OptionsInput.height.update(screen)
    Texthelper.write(screen, [(1000 + 175, 400), "x", 3])
    file_settings[0] = OptionsInput.width.getIntText()
    file_settings[1] = OptionsInput.height.getIntText()

    drawSettingsOption(screen, "Cheats", 600, 400 + spacing * 1, file_settings, 4, "Enabled", "Disabled")

    drawSettingsOption(screen, "Fullscreen", 600, 400 + spacing * 2, file_settings, 2)

    drawSettingsOption(screen, "Ship Drag", 600, 400 + spacing * 3, file_settings, 5)

    drawSettingsOption(screen, "FPS Counter", 600, 400 + spacing * 4, file_settings, 6)

    if Texthelper.writeButtonBox(screen, [("center", 400 + spacing * 5.5), "Reset Gamedata", 3], color = (178, 34, 34)):
        status = "menuinit"
        default = Filehelper("Assets\\saves\\defaultgamedata.txt")
        default.copyTo(filehelper)

        filehelper.setElement("2", 0, 3)

    if Texthelper.writeButtonBox(screen, [("center", 400 + spacing * 7), "Restore Default Settings", 3]):
        default = Filehelper("Assets\\saves\\defaultgamedata.txt")
        default_settings = default.get(0)
        default_settings[3] = file_settings[3] #don't want to change gamestate
        for i in range(len(file_settings)): #has to be like this becuase of scope
            file_settings[i] = default_settings[i]

    Texthelper.write(screen, [("center", 1000), "some settings may not update until game is restarted", 1])

    if Texthelper.writeButton(screen, [("center", 900), "Back", 2]):
        screen.fill((0, 0, 0))
        status = OptionsInput.backStatus

    pygame.display.flip()
    return status

