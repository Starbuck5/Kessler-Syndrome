import pygame
import random
from textwrap import wrap
import pickle
import codecs
import os
import platform
import sys

if getattr(sys, 'frozen', False):
    BASEPATH = os.path.dirname(sys.executable)
else:
    BASEPATH = os.path.dirname(os.path.abspath(__file__))

#keyboard for continuous keypresses
def keyboard():
    inputvar = []
    keyboard_list = ["", "", "", "", "", "", "", "", "back", "tab", "", "", "", "enter", "", "", "", "", "",
                     "pause break", "", "", "", "", "", "","", "escape", "", "", "", "", "space", "", "", "", "", "",
                     "", "", "", "", "", "", ",", "-", ".", "/", "0", "1", "2", "3", "4","5", "6", "7", "8", "9", "",
                     ";", "", "=", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                     "", "", "", "", "", "", "", "", "", "", "", "", "", "`", "a", "b", "c", "d", "e", "f", "g", "h",
                     "i", "j", "k", "l", "m", "n","o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "", "",
                     "", "", "delete", "", "", "", "", "", "", "", "", "", "", "","", "", "", "", "", "", "", "", "",
                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","", "",
                     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                     "", "", "", "", "","", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                     "", "", "", "", "", "", "", "", "", "", "", "","", "", "", "", "", "", "", "", "", "", "", "", "",
                     "", "", "", "", "", "", "", "", "0", "1", "2", "3", "4", "5", "6", "7", "8","9", "delete", "/",
                     "*", "-", "+", "enter", "", "uparrow", "downarrow", "rightarrow", "leftarrow", "insert", "home",
                     "end","page up", "page down", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11",
                     "f12", "", "", "", "", "", "", "","control", "", "shift", "shift", "control", "control", "", "alt",
                     "", "", "windows", "", "", "", "", "", "", "", "", "", "", "", "", ""]

    if pygame.key.get_focused():
        raw_input = pygame.key.get_pressed()
        for i in range(len(raw_input)):
            if raw_input[i] == 1:
                inputvar.append(keyboard_list[i])
    else:
        inputvar = ""
    return inputvar

#because processing events deletes them in the process, centralized space to get them from
class AllEvents():
    TICKINPUT = []    
    def contains(eventType):
        for event in AllEvents.TICKINPUT:
            if event.type == eventType:
                return True
        return False
            
#called from mainloop to stick events from queue into AllEvents.TICKINPUT
def collect_inputs():
    AllEvents.TICKINPUT = []
    for event in pygame.event.get():
        AllEvents.TICKINPUT.append(event)

#version of the keyboard not for controlling things, but for entering text
def keyboard_queued():
    systemEvents = AllEvents.TICKINPUT
    chars_out = []
    for event in systemEvents:
        if event.type == pygame.KEYDOWN:
            chars_out.append(event.unicode)
    return chars_out

#keyboard that is finally the intended way to do keyboard input, I believe
def keydowns():
    systemEvents = AllEvents.TICKINPUT
    chars_out = []
    for event in systemEvents:
        if event.type == pygame.KEYDOWN:
            chars_out.append(event.key)
    return chars_out
    
#returns some stuff about the mouse
def mouse():
    if pygame.mouse.get_focused():
        if 1 in pygame.mouse.get_pressed():
            if pygame.mouse.get_pressed()[0] == 1:
                click = ["leftclick"]
            if pygame.mouse.get_pressed()[1] == 1:
                click = ["middleclick"]
            if pygame.mouse.get_pressed()[2] == 1:
                click = ["rightclick"]
            click.append(pygame.mouse.get_pos()[0])
            click.append(pygame.mouse.get_pos()[1])
        else:
            click = (0, 0, 0)
    else:
        click = (0, 0, 0)
    return click

def scaleImage(image, scalar):
    size = image.get_size()
    newsize = [round(size[0]*scalar), round(size[1]*scalar)]
    for i in range(2):
        if not newsize[i]:
            newsize[i] = 1
    image = pygame.transform.scale(image, newsize)
    return image

def stretchImage(image, size):
    image = pygame.transform.scale(image, (round(size[0]), round(size[1])))
    return image

def fitImage(image, size):
    returnImage = pygame.Surface(size)
    scale = max(image.get_size()[0]/size[0], image.get_size()[1]/size[1])
    scale = 1/scale
    image = scaleImage(image, scale)
    if image.get_size()[0] == size[0]:
        returnImage.blit(image, (0,(size[1]-image.get_size()[1])/2))
    elif image.get_size()[1] == size[1]:
        returnImage.blit(image, ((size[0]-image.get_size()[0])/2,0))
    else:
        raise RuntimeError("it seems fitImage was unable to scale the image :(")
    return returnImage

def handlePath(path):
    path = path.split("\\")
    return os.path.join(BASEPATH, *path)

def loadImage(path):
    path = handlePath(path)
    image = pygame.image.load(path)
    return image

def rotatePixelArt(image, degrees):
    image = scaleImage(image, 4)
    image = pygame.transform.rotate(image, degrees)
    image = scaleImage(image, 0.25)
    return image

#takes a pointlist and returns a bounding box rectangle
def pointsToRect(pointlist):
    xmin, xmax = (10000, -10000)
    ymin, ymax = xmin, xmax
    for x, y in pointlist:
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    return pygame.Rect(xmin, ymin, xmax-xmin, ymax-ymin)

#breaks up sprite sheets into their separate images
#columns can be a list, if multiple numbers of columns exist on separate rows
def spriteSheetBreaker(sheet, width, height, margin, vertmargin, rows, columns):
    if not isinstance(columns, list):
        relcolumns = []
        for i in range(rows):
            relcolumns.append(columns)
        columns = relcolumns
    if len(columns) != rows:
        raise Exception("column and row mismatch")

    image_list = []
    for i in range(rows):
        for j in range(columns[i]):
            image_list.append(sheet.subsurface(((width+margin)*j, (height+vertmargin)*i, width, height)))
    return image_list

#cool storage for sounds in a dictionary accessed through class methods
class SoundVault():
    storage = {}
    def __init__(self, name, filepath, **kwargs):
        sound = loadSound(filepath)
        if 'volume' in kwargs:
            sound.set_volume(kwargs['volume'])        
        SoundVault.storage[name] = sound
    def get(name):
        return SoundVault.storage[name]
    def play(name):
        SoundVault.storage[name].play()

def loadSound(path, volume=100):
    path = handlePath(path)
    sound = pygame.mixer.Sound(file=path)
    sound.set_volume(volume/100)
    return sound

pygame.mixer.init()
SoundVault('button', "Assets\\sounds\\click.ogg", volume=0.5)

class Font():
    char_index = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o","p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ":", ",", "[", "]",
                  "?", "+", "%", "|", "-", "&", ".", "\'", "!", "/"]
    fontsheet = 1 #1 is placeholder for image
    char_list = [] #holder for all the surfaces that are the letters
    DEFAULT = (255,255,255) #default color for the font
    SELCOLOR = (112,128,144) #color for moused over buttons
    COLOR = DEFAULT
    SCRAMBLED = False
    scrambleTimeLeft = -1
    missingTexture = 1 #1 is placeholder for image
    
    def getReady(): #'poor mans __init__'
        Font.fontsheet = loadImage("Assets\\fonts\\font.gif")
        fontsheet = Font.fontsheet
        Font.splitSheet(fontsheet)
        Font.missingTexture = Font._makeMissingTexture()

    def _makeMissingTexture():
        missingTexture = pygame.Surface((8,12))
        for i in range(6):
            if i % 2 == 0:
                x = 2
            else:                
                x = 0
            pygame.draw.rect(missingTexture, (255, 0, 220), (x,i*2,2,2), 0)
            pygame.draw.rect(missingTexture, (255, 0, 220), (x+4,i*2,2,2), 0)
        return missingTexture
        
    def splitSheet(fontsheet):
        Font.char_list = spriteSheetBreaker(Font.fontsheet, 8, 13, 2, 1, 6, [10, 10, 10, 6, 10, 4]) 

    def changeColor(color):
        if color != Font.COLOR:
            Font.COLOR = color
            fontsheet = Font.fontsheet
            palette = list(fontsheet.get_palette())
            palette[1] = color
            fontsheet.set_palette(palette)
            Font.splitSheet(fontsheet)
        
    def getChar(char, scale):           
        if Font.SCRAMBLED:
            charImage = scaleImage(Font.char_list[random.randint(0,len(Font.char_list)-1)], scale)
        elif char in Font.char_index:
            charImage = scaleImage(Font.char_list[Font.char_index.index(char)], scale)
        else:
            charImage = scaleImage(Font.missingTexture, scale)
        return charImage

    def scramble(duration): #unscrambles with an input of -1
        if duration != -1:
            Font.scrambleTimeLeft = duration
            Font.SCRAMBLED = True
        else:
            Font.endScramble()

    def set_scramble_paused(flag): #True pauses scrambling, False resumes
        if flag:
            Font.SCRAMBLED = False
        if not flag:
            if Font.scrambleTimeLeft > -1:
                Font.SCRAMBLED = True

    def endScramble():
        Font.SCRAMBLED = False
        Font.scrambleTimeLeft = -1
            
    def timerhelper():
        if Font.scrambleTimeLeft >= 0:
            Font.scrambleTimeLeft -= 1
        if Font.scrambleTimeLeft == 0:
            Font.scramble(-1)
        else:
            pass

Font.getReady() #initializes the font
       
class InputGetter():
    BLINKSPEED = 45
    ALPHABETCHECK = "abcdefghijklmnopqrstuvwxyz"
    def __init__ (self, initialtext, inputtype): #text = [(x,y),'text', scale]
        self.initialtext = initialtext           #type = 'str' or 'int'
        self.inputtype = inputtype
        self.currenttext = initialtext
        self.rawtext = initialtext[1]
        self.clicked = False
        self.blink = 0
        self.last_input = ["getready"]
        
    def update(self, screen):
        self.rawtext = self.currenttext[1]
        if self.clicked == False:
            if self.currenttext[1] == "":
               self.currenttext = self.initialtext 
            if Texthelper.writeButton(screen, self.currenttext) == True:
                self.clicked = True
        if self.clicked == True:
            InputGetter._timerhelper(self)
            specialtext = self.currenttext[:]
            if self.blink < InputGetter.BLINKSPEED/2:
                specialtext[1] += "|"
            InputGetter._handleThisShit(self, self.inputtype)
            if Texthelper.writeNullButton(screen, specialtext) == False:
                self.clicked = False
                self.last_input = ["getready"]

    def _handleThisShit(self, inputtype):
        last_input = self.last_input
        inputvar = keyboard_queued()
        downs = keydowns()
        if inputvar and last_input == ["getready"]:
            self.rawtext = "" 
        if inputvar != last_input:
            for i in range(len(inputvar)):
                if pygame.K_DELETE in downs or pygame.K_BACKSPACE in downs:
                    self.rawtext = self.rawtext[:-1]
                if inputtype == "int":
                    if len(inputvar[i]) == 1 and inputvar[i].isdigit() == True:
                        self.rawtext += inputvar[i]
                elif inputtype == "str":
                    if len(inputvar[i]) == 1 and inputvar[i] in InputGetter.ALPHABETCHECK:
                        self.rawtext += inputvar[i]
                else: #maybe inputtype of 'all' for everyting; or maybe 'str' should mean all
                    if len(inputvar) == 1 and len(inputvar[i]) == 1:
                        self.rawtext += inputvar[i]
        
        self.currenttext = [self.currenttext[0], self.rawtext, self.currenttext[2]]
        if last_input != ["getready"]:
            self.last_input = inputvar
        elif inputvar:
            self.last_input = inputvar
            
    def _timerhelper(self):
        if self.blink < InputGetter.BLINKSPEED:
            self.blink += 1
        if self.blink == InputGetter.BLINKSPEED:
            self.blink = 0
        
    def getText(self):
        return self.rawtext

    def getIntText(self):
        text = self.rawtext
        if text:
            return int(text)
        return 0

    def getData(self):
        return self.currenttext

 
class AnnouncementBox():
    upcoming = [] # upcoming anouncements that need to be displayed
    BREAKPOS = 31 #amount of chars before a linebreak
    INTEXTSPEED = 4 # frames per character that it displayes at
    OUTTEXTSPEED = 0.5
    #image = portrait next to text, sound = whatever should play, text = text
    def __init__(self, image, sound, text):
        self.image = stretchImage(image, (108*Texthelper.scalar, 108*Texthelper.scalar))
        self.sound = sound
        self.text = text
        self.linedtext = wrap(text, AnnouncementBox.BREAKPOS) # wraps text by linebreak
        lineelements = []
        for i in range(len(self.linedtext)):
            lineelements.append(len(self.linedtext[i]))
        self.lineelements = lineelements
        self.time = 0
        self.bounds = [0,0]
        self.printing = True
        self.ending = False
        AnnouncementBox.upcoming.append(self)

    def play(screen):
        if AnnouncementBox.upcoming != []:
            AnnouncementBox.upcoming[0]._draw(screen)
        if AnnouncementBox.upcoming != []: ##entire entry can be deleted from draw, so this test actually is necessary
            if AnnouncementBox.upcoming[0].time == 0:
                AnnouncementBox.upcoming[0].sound.play()
            AnnouncementBox.upcoming[0]._timehelper()

    def _draw(self, screen):
        draw.sblit(screen, self.image, (576, 108)) #placing image on screen

        #calculating the height the box needs based on how much text there is 
        boxheight = 108
        if len(self.linedtext) > 3:
            length = len(self.linedtext)
            boxheight += 36*(length-3)
        boxheight = round(boxheight)

        #draws the two rectangles that make up the box
        draw.rect(screen, (255,255,255), (684, 108, 660, boxheight), 4)
        draw.rect(screen, (255,255,255), (576, 108, 108, 108), 4)
        
        # trims text to self.bounds and prints it
        total_chars = 0
        for line in range(len(self.linedtext)):
            start = max([0,self.bounds[0]-total_chars])
            end = min([len(self.linedtext[line]),max([0,self.bounds[1]-total_chars])])
            text = self.linedtext[line][start:end]
            Texthelper.write(screen, [(703, 120+round(32.4*line)), text, 2])
            total_chars += len(self.linedtext[line])
        
        if self.bounds[1] >= sum(self.lineelements):
            self.printing = False
        
        if not self.printing:
            Texthelper.write(screen, [(768, 120+boxheight), "Press Enter to Continue", 1.5])
            inputvar = keydowns()
            if pygame.K_RETURN in inputvar:
                self.ending = True
                self.time = 1

    def _timehelper(self):
        self.time += 1
        if self.printing:
            self.bounds[1] = int(self.time/self.INTEXTSPEED)
        inputvar = keydowns()
        if self.printing and pygame.K_RETURN in inputvar: #allows you to skip by pressing enter
            self.bounds[1] = sum(self.lineelements)
        if self.ending:
            self.bounds[0] = int(self.time/self.OUTTEXTSPEED)
            if self.bounds[0] >= self.bounds[1]:
                AnnouncementBox.upcoming[0].sound.stop()
                del AnnouncementBox.upcoming[0]

   
class Texthelper():
    scalar = 1
    width = 1
    height = 1
    lastPressTime = 0
    HALFSIZERS = ["\'", ".", ":" ",", "!", "|"]
    SAFEASPECT = (16,9) #the aspect ratio scaling goes back to for certain algorithms

    #helps interpretcoords
    def __compensateForAspect(x):
        asw, ash = Texthelper.SAFEASPECT
        supposedwidth = Texthelper.height/ash*asw
        blackbarsize = (supposedwidth - Texthelper.width)/2
        if x>Texthelper.width+blackbarsize:
            blackbarsize *= 2
        return (x - blackbarsize if x-blackbarsize > 0 else x)
            
    #part of the input sanitizing process: figures out how to center text mainly
    #styles of coordinate input:
    # (100, 200)
    # ("center", 200) centers text in the screen in the x dimension
    # ("right.350, 100") aligns text rightwards at x=350
    # ("right-200") puts text 200 (scaled) left of the right bound of the screen
    def _interpretcoords(text_input):
        text_location = text_input[0]
        location_list = [text_location[0], text_location[1]]
        text_input2 = text_input[0:] #very important line
        if isinstance(location_list[0], str) and ("-" in location_list[0] or "+" in location_list[0]): #EX: right-110
            if "left" in location_list[0]:
                index = 5 
                startnum = 0     
            elif "right" in location_list[0]:
                index = 6 
                startnum = Texthelper.width
            elif "center" in location_list[0]:
                index = 7
                startnum = Texthelper.width/2
            else:
                raise ValueError("invalid string keyword for relative coordinates")
            offset = int(location_list[0][index:]) * Texthelper.scalar
            if location_list[0][index-1] == "+":
                location_list[0] = startnum + offset
            elif location_list[0][index-1] == "-":
                location_list[0] = startnum - offset
            else:
                raise ValueError("you appear to have entered an incorrect coordinate format")
        elif isinstance(location_list[0], str): #EX: 'center', 'center.600', 'left.20', 'right'
            if "center" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     num = Texthelper.__compensateForAspect(num)
                     location_list[0] = num - Texthelper._textlength(text_input) / 2 
                else:
                    location_list[0] = Texthelper.width / 2 - Texthelper._textlength(text_input) / 2
            elif "left" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     num = Texthelper.__compensateForAspect(num)
                     location_list[0] = num
                else:
                    location_list[0] = 0
            elif "right" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     num = Texthelper.__compensateForAspect(num)
                     location_list[0] = num - Texthelper._textlength(text_input) 
                else:
                    location_list[0] = Texthelper.width - Texthelper._textlength(text_input)                
            else:
                raise ValueError("invalid string keyword for coordinates")            
        else: #EX: 520
            location_list[0] *= Texthelper.scalar
            location_list[0] = Texthelper.__compensateForAspect(location_list[0])
        location_list[1] *= Texthelper.scalar            
        text_input2[0] = (location_list[0], location_list[1])
        return text_input2

    #called internally after input has been sanitized for scale and interpreted coords
    def _drawtext(screen, text_input):
        text_location, text, scale = text_input
        horizontal_pos = text_location[0]
        vertical_pos = text_location[1]
        for i in range(len(text)):
            if text[i] == "\n":
                horizontal_pos = text_location[0]
                vertical_pos += 15 * scale     
            elif text[i] != " " and not text[i] in Texthelper.HALFSIZERS:
                text3 = Font.getChar(text[i], scale)                
                screen.blit(text3, (horizontal_pos, vertical_pos))
                horizontal_pos += 11 * scale
            elif text[i] in Texthelper.HALFSIZERS:
                text3 = Font.getChar(text[i], scale)
                screen.blit(text3, (horizontal_pos, vertical_pos))
                horizontal_pos += 5 * scale                
            elif text[i] == " " and text[i-1] != " " and i != 0:
                horizontal_pos += 6 * scale
                #would be 6 but each character automatically gives a 3 pixel * scale space until the next character
            elif text[i] == " " and text[i-1] == " " and i != 0:
                horizontal_pos += 11 * scale

    #takes in whatever shit we tell it too and makes it standardized
    def _sanitizeinput(proto_input):
        text_input = proto_input[:] #avoids mangling variables passed by reference
        text_input[2] = text_input[2] * Texthelper.scalar
        text_input[1] = text_input[1].lower()
        text_input = Texthelper._interpretcoords(text_input)                
        return text_input
    
    #petitions the font to have the right color
    def _handlecolor(**kwargs):
        #order of precedence low to high:
        # -- default color -- manually selected color -- mouse over color
        #takes a rect as optional keyword
        #takes color as optional keyword
        color = Font.DEFAULT
        if 'color' in kwargs:
            color = kwargs['color']
        if 'colliderect' in kwargs:
            rect = kwargs['colliderect']
            x, y = pygame.mouse.get_pos()
            if rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]:
                color = Font.SELCOLOR
        Font.changeColor(color)
        return color

    #backend for writebox and writebuttonbox
    def _drawbox(screen, rect, color):
        width = int(2*Texthelper.scalar)
        width = width if width > 0 else 1
        pygame.draw.rect(screen, color, rect, width)

    #takes a sanitized text_input
    def _textlength(text_input):
        text = text_input[1]
        if text and text[-1] == "|":
            text = text[:-1]
        scale = text_input[2]
        x_range = 0
        for i in range(len(text)):
            if text[i] != " " and not text[i] in Texthelper.HALFSIZERS:
                x_range += 11 * scale
            elif text[i] in Texthelper.HALFSIZERS:
                x_range += 5 * scale                
            elif text[i] == " " and text[i-1] != " " and i != 0:
                x_range += 6 * scale
                #would be 6 but each character automatically gives a 3 pixel * scale space until the next character
            elif text[i] == " " and text[i-1] == " " and i != 0:
                x_range += 11 * scale
        return x_range

    #tests if mouse is clicked inside the rectangle
    def _buttonlogic(rect):
        click = mouse()
        time = pygame.time.get_ticks()//200 #// = Java integer math - IE truncating the ms to 1/5 seconds
        if time != Texthelper.lastPressTime:
            if AllEvents.contains(pygame.MOUSEBUTTONDOWN):
                if rect[0] < click[1] < rect[0]+rect[2] and rect[1] < click[2] < rect[1]+rect[3]:
                    Texthelper.lastPressTime = time
                    SoundVault.play('button')
                    return True            
        return False        

    # text_input = [(x, y), "text", text_scale]
    # text placed from upper left corner # pixels of text (1x scale) == (11 * # of characters) + (3 * # of spaces) - 3
    def write(screen, text_input, **kwargs):
        Texthelper._handlecolor(**kwargs)
        text_input = Texthelper._sanitizeinput(text_input)
        Texthelper._drawtext(screen, text_input)

    def writeBox(screen, text_input, **kwargs):
        padding = 18 /1920 * Texthelper.height * Texthelper.scalar #default value
        color = Texthelper._handlecolor(**kwargs)
        if 'padding' in kwargs:
            padding = kwargs['padding'] * Texthelper.scalar

        text_input = Texthelper._sanitizeinput(text_input)        
        Texthelper._drawtext(screen, text_input)
        x, y = text_input[0]
        boxrect = [x-padding, y-padding/2, Texthelper._textlength(text_input)+padding*2, 13*text_input[2]+padding]
        Texthelper._drawbox(screen, boxrect, color)

    def writeButton(screen, text_input, **kwargs):        
        text_input = Texthelper._sanitizeinput(text_input)
        x_range = Texthelper._textlength(text_input)
        y_range = 12 * text_input[2]
        text_location = text_input[0]

        mouseoverrect = [text_location[0], text_location[1], x_range, y_range]        
        Texthelper._handlecolor(colliderect = mouseoverrect, **kwargs)
        Texthelper._drawtext(screen, text_input)
        return Texthelper._buttonlogic(mouseoverrect)
        

    def writeButtonBox(screen, text_input, **kwargs):
        padding = 18 /1920 * Texthelper.height * Texthelper.scalar #default value      
        if 'padding' in kwargs:
            padding = kwargs['padding'] * Texthelper.scalar
            
        text_input = Texthelper._sanitizeinput(text_input)
        x, y = text_input[0]
        mouseoverrect = [x-padding, y-padding/2, Texthelper._textlength(text_input)+padding*2, 13*text_input[2]+padding]
        color = Texthelper._handlecolor(colliderect = mouseoverrect, **kwargs)          
        Texthelper._drawtext(screen, text_input)
        Texthelper._drawbox(screen, mouseoverrect, color)
        return Texthelper._buttonlogic(mouseoverrect)

    #the special child of the button family                
    def writeNullButton(screen, text_input):
        Font.changeColor(Font.DEFAULT)
        text_input = Texthelper._sanitizeinput(text_input)
        Texthelper._drawtext(screen, text_input)
        x_range = Texthelper._textlength(text_input)
        y_range = 12 * text_input[2]
        text_location = text_input[0]
        
        click = mouse()
        if text_location[0] < click[1] < (text_location[0] + x_range) and text_location[1] < click[2] <(text_location[1] + y_range):
            return True
        elif click == (0,0,0):
            return True
        else:
            return False        

    def textlength(text_input):
        if len(text_input) < 3:
            return len(text_input)
        text_input = Texthelper._sanitizeinput(text_input)
        return Texthelper._textlength(text_input)


class Screenhelper():
    greyout = 1
    def __init__(self,width, height):
        Screenhelper.greyout = pygame.Surface((width,height))
        Screenhelper.greyout.fill((80,80,80))
        Screenhelper.greyout.set_alpha(70)
        
    #puts a transparent gray pane over the screen
    def greyOut(screen):
        screen.blit(Screenhelper.greyout, (0,0))


class Filehelper():
    def __init__(self, filepath):
        self.info_file = handlePath(filepath)
        
    #converts file contents back to the ints and strings they started as and returns them by line
    def get(self, line): #line is line # in file being extracted
        file = open(self.info_file, "r")
        contents = file.readlines()
        file.close()

        parse_line = contents[line]
        parse_line = parse_line[1:] #gets rid of leading bracket
        parse_line = parse_line.rstrip() #gets rid of any trailing whitespace
        parse_line = parse_line[:parse_line.rfind("]")] #gets rid of ending bracket
        parse_line = parse_line.split(", ") #turns it into a list of string elements
       
        for i in range(len(parse_line)): #goes through the list guessing the types of the elements
            if parse_line[i].isdigit():
                    parse_line[i] = int(parse_line[i])
            elif "." in parse_line[i]:
                if parse_line[i][-1].isdigit():
                    parse_line[i] = float(parse_line[i])
            elif parse_line[i] != "" and parse_line[i][0] == "-" and parse_line[i][-1].isdigit():
                parse_line[i] = -int(parse_line[i][1:])
            elif parse_line[i] == "True":
                parse_line[i] = True
            elif parse_line[i] == "False":
                parse_line[i] = False
        return parse_line

    #takes another filehelper or path
    #overwrites it (or creates it if it doesn't exist) with no processing or modification
    def copyTo(self, other):
        file = open(self.info_file, "r")
        contents = file.read()
        file.close()

        if isinstance(other, Filehelper):
            otherFile = open(other.info_file, "w+")
            otherFile.write(contents)
        else:
            otherFile = open(handlePath(other), "w+")
            otherFile.write(contents)
        otherFile.close()

    #allows the program to set lines to whatever they want, within what I think they will           
    def set(self, content, line, **kwargs): #line is line # in file being written to
        file = open(self.info_file, "r")
        contents = file.readlines()
        file.close()

        if 'override' in kwargs: #tests for optional argument that ditches any and all comments
            override = kwargs['override']
        else:
            override = False
        comment = ""
        if not override:
            if "#" in contents[line]:
                if "]" in contents[line]:
                    if contents[line].index("]") < contents[line].index("#"):
                        comment = contents[line][contents[line].index("#"):]
                        comment = comment.rstrip() #removes trailing \n

        content = str(content)
        content = content.split("'")
        content = "".join(content)
        content += comment
        content += "\n"

        contents[line] = content

        file = open(self.info_file, "w")
        file.writelines(contents)
        file.close()

    #sets a specific element of one of the lists to a new value
    def setElement(self, content, line, column):
        lineData = Filehelper.get(self, line)
        lineData[column] = content
        Filehelper.set(self, lineData, line)

    def saveObj(self, content, line):
        saveline = codecs.encode(pickle.dumps(content), "base64").decode()
        saveline = str(saveline)
        file = open(self.info_file, "r")
        lines = file.readlines()
        file.close()
        
        saveline = "".join(saveline.splitlines()) + "\n"
        lines[line] = saveline

        file = open(self.info_file, "w")
        file.writelines(lines)
        file.close()
         
    def loadObj(self, line):
        file = open(self.info_file, "r")
        lines = file.readlines()
        file.close()
        pickled = lines[line]
        return pickle.loads(codecs.decode(pickled.encode(), "base64"))

filehelper = Filehelper("Assets\\saves\\gamedata.txt") #makes lowercase filehelper used throughtout work with the class

#special scaled draws reliant on Texthelper scaling
class draw:
    #calls Texthelper interpret coords but takes care of some things automatically
    #location is (x, y) or [x, y]
    def _interpretcoords(location):
        return Texthelper._interpretcoords([location])[0]
    
    def rect(Surface, color, Rect, width = 0):
        Rect = list(Rect)
        Rect[0], Rect[1] = draw._interpretcoords((Rect[0], Rect[1]))
        Rect[2] *= Texthelper.scalar
        Rect[3] *= Texthelper.scalar                                         
        width = round(width*Texthelper.scalar)
        pygame.draw.rect(Surface, color, Rect, width)

    def aaline(Surface, color, startpos, endpos, blend=1):
        startpos = draw._interpretcoords(startpos)
        endpos = draw._interpretcoords(endpos)
        pygame.draw.aaline(Surface, color, startpos, endpos, blend)

    def circle(Surface, color, pos, radius, width=0):
        pos = draw._interpretcoords(pos)
        pos = round(pos[0]), round(pos[1])
        adjusted_radius = round(Texthelper.scalar * radius)
        radius = adjusted_radius if adjusted_radius > 0 else 1
        adjusted_width = round(Texthelper.scalar * width)
        width = adjusted_width if (adjusted_width > 0 or width == 0) else 1
        pygame.draw.circle(Surface, color, pos, radius, width)

    #static version of normal blit except it moves coordinates based on screen size
    #because it uses texthelper the location tuple/list can use fancy things like center
    def sblit(baseSurface, secondSurface, location):
        location = draw._interpretcoords(location)
        baseSurface.blit(secondSurface, location)
   
