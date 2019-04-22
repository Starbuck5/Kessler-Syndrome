#just a file to de-clutter the main script
import pygame
import random
from textwrap import wrap
OS = "windows" #other option = "mac"

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
    image = pygame.transform.scale(image, (round(size[0]*scalar), round(size[1]*scalar)))
    return image

def scretchImage(image, size):
    image = pygame.transform.scale(image, (size[0], size[1]))
    return image

def handlePath(path):
    newpath = ""
    if OS == "mac":
        for i in range(len(path)):
            if path[i] == "\\":
                newpath += "/"
            else:
                newpath += path[i]
    else:
        for i in range(len(path)):
            if path[i] == "/":
                newpath += "\\"
            else:
                newpath += path[i]
    return newpath

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
        sound = pygame.mixer.Sound(handlePath(filepath))
        if 'volume' in kwargs:
            sound.set_volume(kwargs['volume'])        
        SoundVault.storage[name] = sound
    def get(name):
        return SoundVault.storage[name]
    def play(name):
        SoundVault.storage[name].play()

pygame.mixer.init()
SoundVault('button', "Assets\\sounds\\click.wav", volume=0.5)

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
            if Texthelper.writeButton(screen, self.currenttext) == True:
                self.clicked = True
        if self.clicked == True:
            InputGetter._timerhelper(self)
            specialtext = self.currenttext[:]
            if self.blink < InputGetter.BLINKSPEED/2:
                specialtext[1] += "|"
            if Texthelper.writeNullButton(screen, specialtext) == False:
                self.clicked = False
            InputGetter._handleThisShit(self, self.inputtype)

    def _handleThisShit(self, inputtype):
        last_input = self.last_input
        inputvar = keyboard_queued()    
        if inputvar and last_input == ["getready"]:
            self.rawtext = "" 
        if inputvar != last_input:
            for i in range(len(inputvar)):
                if inputvar[i] == "\x08":
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
    width = 1
    height = 1
    upcoming = []
    BREAKPOS = 32 #amount of chars before a linebreak
    #image = portrait next to text, sound = whatever should play, text = text
    def __init__(self, image, sound, text):
        self.image = scretchImage(image, (round(AnnouncementBox.height*0.1), round(AnnouncementBox.height*0.1)))
        sound.set_volume(0.75)
        self.sound = sound
        self.text = text
        self.linedtext = wrap(text, AnnouncementBox.BREAKPOS)
        lineelements = []
        for i in range(len(self.linedtext)):
            lineelements.append(len(self.linedtext[i].split()))
        self.lineelements = lineelements
        self.time = 0
        self.ended = False
        AnnouncementBox.upcoming.append(self)

    def play(screen):
        if AnnouncementBox.upcoming != []:
            AnnouncementBox.upcoming[0]._draw(screen)
        if AnnouncementBox.upcoming != []: ##entire entry can be deleted from draw, so this test actually is necessary
            if AnnouncementBox.upcoming[0].time == 0:
                AnnouncementBox.upcoming[0].sound.play()
            AnnouncementBox.upcoming[0]._timehelper()

    def _draw(self, screen):
        screen.blit(self.image, (round(AnnouncementBox.width*0.3), round(AnnouncementBox.height*0.1)))
        boxheight = AnnouncementBox.height*0.1
        if len(self.linedtext) > 3:
            length = len(self.linedtext)
            boxheight += AnnouncementBox.height*((length-3)*0.03333)
        boxheight = round(boxheight)
        pygame.draw.rect(screen, (255,255,255), (round(AnnouncementBox.width*0.3+AnnouncementBox.height*0.1), round(AnnouncementBox.height*0.1),
                                                 round(AnnouncementBox.width*0.4-AnnouncementBox.height*0.1), boxheight), 4)
        pygame.draw.rect(screen, (255,255,255), (round(AnnouncementBox.width*0.3), round(AnnouncementBox.height*0.1),
                                                 round(AnnouncementBox.height*0.1),round(AnnouncementBox.height*0.1)), 4)
        words = int(self.time/20)
        if words >= sum(self.lineelements):
            self.ended = True
            words = sum(self.lineelements)
        line = 0
        while words > 0:
            if words >= self.lineelements[line]:
                Texthelper.write(screen, [(round(AnnouncementBox.width*0.31+self.image.get_size()[0]),
                                           round(AnnouncementBox.height*0.11)+round(AnnouncementBox.height*0.03*line)),
                                          self.linedtext[line], 2])
                words -= self.lineelements[line]
                line += 1
            if words > 0:
                if words < self.lineelements[line]:
                    text = self.linedtext[line].split()
                    text = text[:words]
                    text = " ".join(text)
                    Texthelper.write(screen, [(round(AnnouncementBox.width*0.31+self.image.get_size()[0]),
                                               round(AnnouncementBox.height*0.11)+round(AnnouncementBox.height*0.03*line)),
                                              text, 2])
                    words = 0
                    line += 1                                
        if self.ended:
            Texthelper.write(screen, [(round(AnnouncementBox.width*0.40), round(AnnouncementBox.height*0.11 + boxheight)),
                                      "Press Enter to Continue", 1.5])
            inputvar = keyboard()
            if "enter" in inputvar:
                AnnouncementBox.upcoming[0].sound.stop()
                del AnnouncementBox.upcoming[0]

    def _timehelper(self):
        self.time += 1

   
class Texthelper():
    scalar = 1
    width = 1
    height = 1
    lastPressTime = 0
    HALFSIZERS = ["\'", ".", ":" ",", "!", "|"]

    #part of the input sanitizing process: figures out how to center text mainly
    def _interpretcoords(text_input):
        text_location = text_input[0]
        location_list = [text_location[0], text_location[1]]
        text_input2 = text_input[0:] #very important line
        if isinstance(location_list[0], str):
            if "center" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     location_list[0] = num - Texthelper._textlength(text_input) / 2 
                else:
                    location_list[0] = Texthelper.width / 2 - Texthelper._textlength(text_input) / 2
            elif "left" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     location_list[0] = num
                else:
                    location_list[0] = 0
            elif "right" in location_list[0]:
                if location_list[0][-1].isdigit():
                     num = int(location_list[0][location_list[0].rfind(".")+1:])
                     num *= Texthelper.scalar
                     location_list[0] = num - Texthelper._textlength(text_input) 
                else:
                    location_list[0] = Texthelper.width - Texthelper._textlength(text_input)                
            else:
                raise ValueError("invalid string keyword for coordinates")
        else:
            location_list[0] *= Texthelper.scalar
        location_list[1] *= Texthelper.scalar            
        text_input2[0] = (location_list[0], location_list[1])
        return text_input2

    #called internally after input has been sanitized for scale and interpreted coords
    def _drawtext(screen, text_input):
        text_location, text, scale = text_input
        horizontal_pos = text_location[0]
        for i in range(len(text)):
            if text[i] != " " and not text[i] in Texthelper.HALFSIZERS:
                text3 = Font.getChar(text[i], scale)                
                screen.blit(text3, (horizontal_pos, text_location[1]))
                horizontal_pos += 11 * scale
            elif text[i] in Texthelper.HALFSIZERS:
                text3 = Font.getChar(text[i], scale)
                screen.blit(text3, (horizontal_pos, text_location[1]))
                horizontal_pos += 5 * scale                
            elif text[i] == " " and text[i-1] != " " and i != 0:
                horizontal_pos += 3 * scale
                #would be 6 but each character automatically gives a 3 pixel * scale space until the next character
            elif text[i] == " " and text[i-1] == " " and i != 0:
                horizontal_pos += 11 * scale

    #takes in whatever shit we tell it too and makes it standardized
    def _sanitizeinput(proto_input):
        text_input = proto_input[:] #avoids mangling variables passed by reference
        text_input[2] = text_input[2] * Texthelper.scalar
        text_input = Texthelper._interpretcoords(text_input)        
        text_input[1] = text_input[1].lower()
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
        pygame.draw.rect(screen, color, rect, int(2*Texthelper.scalar))

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
                x_range += 3 * scale
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


filehelper = Filehelper("Assets\\saves\\gamedata.txt") #makes lowercase filehelper used throughtout work with the class

class draw:
    def rect(Surface, color, Rect, width = 0):
        try:
            Rect = Rect.copy() #works for lists of coords and rects
            for i in range(4):
                Rect[i] = round(Rect[i]*Texthelper.scalar)
        except:
            Rect = list(Rect)
            for i in range(4):
                Rect[i] = round(Rect[i]*Texthelper.scalar)
        width = round(width*Texthelper.scalar)
        pygame.draw.rect(Surface, color, Rect, width)

    def aaline(Surface, color, startpos, endpos, blend=1):
        startpos = list(startpos)
        endpos = list(endpos)
        for i in range(2):
            startpos[i] *= Texthelper.scalar
            endpos[i] *= Texthelper.scalar
        pygame.draw.aaline(Surface, color, startpos, endpos, blend)
        
