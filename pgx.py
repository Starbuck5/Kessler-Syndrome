#just a file to de-clutter the main script
import pygame
import random
OS = "windows" #other option = "mac"
SELCOLOR = (112,128,144) #color for moused over buttons

def keyboard():
    inputvar = []
    keyboard_list = ["", "", "", "", "", "", "", "", "back", "tab", "", "", "", "enter", "", "", "", "", "", "pause break", "", "", "", "", "", "",
                    "", "escape", "", "", "", "", "space", "", "", "", "", "", "", "", "", "", "", "", ",", "-", ".", "/", "0", "1", "2", "3", "4",
                    "5", "6", "7", "8", "9", "", ";", "", "=", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                    "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "", "", "", "", "delete", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "0", "1", "2", "3", "4", "5", "6", "7", "8",
                    "9", "delete", "/", "*", "-", "+", "enter", "", "uparrow", "downarrow", "rightarrow", "leftarrow", "insert", "home", "end",
                    "page up", "page down", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "", "", "", "", "", "", "",
                    "control", "", "shift", "shift", "control", "control", "", "alt", "", "", "windows", "", "", "", "", "", "", "", "", "", "", "",
                    "", ""]

    if pygame.key.get_focused():
        raw_input = pygame.key.get_pressed()
        for i in range(len(raw_input)):
            if raw_input[i] == 1:
                inputvar.append(keyboard_list[i])
    else:
        inputvar = ""
    return inputvar

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

# missing texture surface setup
missingTexture = pygame.Surface((8,12))
missingTexture.fill((255, 0, 220))
pygame.draw.rect(missingTexture, (0,0,0), (0,0,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (4,0,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (2,2,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (6,2,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (0,4,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (4,4,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (2,6,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (6,6,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (0,8,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (4,8,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (2,10,2,2), 0)
pygame.draw.rect(missingTexture, (0,0,0), (6,10,2,2), 0)

class Font():
    char_index = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                  "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ":", ",", "[", "]", "?", "+", "%", "|", "-", "&"]
    fontsheet = 1 #1 is placeholder for image
    char_list = [] #holder for all the surfaces that are the letters
    DEFAULT = (255,255,255) #default color for the font
    COLOR = DEFAULT
    SCRAMBLED = False
    scrambleTimeLeft = -1
    def getReady(): #'poor mans __init__'
        Font.fontsheet = loadImage("Assets\\font.gif")
        fontsheet = Font.fontsheet
        Font.splitSheet(fontsheet)

    def splitSheet(fontsheet): #moves the stuff from one file into all of their separate surfaces
        rows = 5 #number of character rows in font.gif
        length_definitions = [10, 10, 10, 6, 10] #length of each row in font.gif
        Font.char_list = []
        for i in range(rows):
            for j in range(length_definitions[i]):
                Font.char_list.append(fontsheet.subsurface((2+10*j, 2+14*i, 8, 13)))

    def changeColor(color):
        Font.COLOR = color
        fontsheet = Font.fontsheet
        palette = list(fontsheet.get_palette())
        palette[1] = color
        fontsheet.set_palette(palette)
        Font.splitSheet(fontsheet)
        
    def getChar(char, scale, mode):
        if mode:
            if Font.COLOR != SELCOLOR:
                Font.changeColor(SELCOLOR)
        elif Font.COLOR != Font.DEFAULT:
            Font.changeColor(Font.DEFAULT)
            
        if Font.SCRAMBLED:
            charImage = scaleImage(Font.char_list[random.randint(0,len(Font.char_list)-1)], scale)
        elif char in Font.char_index:
            charImage = scaleImage(Font.char_list[Font.char_index.index(char)], scale)
        else:
            charImage = scaleImage(missingTexture, scale)
        return charImage

    def scramble(duration): #unscrambles with an input of -1
        if duration != -1:
            Font.scrambleTimeLeft = duration
            Font.SCRAMBLED = True
        else:
            Font.scrambleTimeLeft = -1
            Font.SCRAMBLED = False

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
    def __init__ (self, initialtext, inputtype):
        self.initialtext = initialtext
        self.inputtype = inputtype
        self.currenttext = initialtext
        self.rawtext = initialtext[1]
        self.clicked = False
        self.blink = 0
        self.last_input = ["getready"]
        
    def update(self, screen):
        if self.clicked == False:
            if Texthelper.writeButton(screen, self.currenttext) == True:
                self.clicked = True
        if self.clicked == True:
            InputGetter.timerhelper(self)
            specialtext = self.currenttext[:]
            if self.blink < InputGetter.BLINKSPEED/2:
                specialtext[1] += "|"
            if Texthelper.writeNullButton(screen, specialtext) == False:
                self.clicked = False
            InputGetter.handleThisShit(self, self.inputtype)

    def handleThisShit(self, inputtype):
        last_input = self.last_input
        inputvar = keyboard()
        self.rawtext = self.currenttext[1]
        
        if inputvar and last_input == ["getready"]:
            self.rawtext = "" 
        if inputvar != last_input:
            if "back" in inputvar or "delete" in inputvar:
                self.rawtext = self.rawtext[:-1]
            if inputtype == "int":
                if len(inputvar) == 1 and len(inputvar[0]) == 1 and inputvar[0].isdigit() == True:
                    self.rawtext += inputvar[0]
            if inputtype == "str":
                if len(inputvar) == 1 and len(inputvar[0]) == 1 and inputvar[0] in InputGetter.ALPHABETCHECK:
                    self.rawtext += inputvar[0]
            else: #maybe inputtype of 'all' for everyting; or maybe 'str' should mean all
                if len(inputvar) == 1 and len(inputvar[0]) == 1:
                    self.rawtext += inputvar[0]
        
        self.currenttext = [self.currenttext[0], self.rawtext, self.currenttext[2]]
        if last_input != ["getready"]:
            self.last_input = inputvar
        elif inputvar:
            self.last_input = inputvar
            
    def timerhelper(self):
        if self.blink < InputGetter.BLINKSPEED:
            self.blink += 1
        if self.blink == InputGetter.BLINKSPEED:
            self.blink = 0
        
    def getText(self):
        return self.rawtext

    def getData(self):
        return self.currenttext


class AnnouncementBox():
    width = 1
    height = 1
    upcoming = []
    #image = portrait next to text, sound = whatever should play, text = text
    def __init__(self, image, sound, text):
        self.image = scretchImage(image, (round(AnnouncementBox.height*0.1), round(AnnouncementBox.height*0.1)))
        self.sound = sound
        self.text = text
        self.currenttext = self.text.split()[0]
        self.besttext = [self.text.split()[0]]
        self.time = 0
        self.runningtotal = 0 #used for line break stuff
        self.ended = False
        AnnouncementBox.upcoming.append(self)

    def play(screen):
        if AnnouncementBox.upcoming != []:
            AnnouncementBox.upcoming[0].draw(screen)
        if AnnouncementBox.upcoming != []: ##entire entry can be deleted from draw, so this text actually is necessary
            if AnnouncementBox.upcoming[0].time == 0:
                AnnouncementBox.upcoming[0].sound.play()
            AnnouncementBox.upcoming[0].timehelper()

    def draw(self, screen):
        screen.blit(self.image, (round(AnnouncementBox.width*0.3), round(AnnouncementBox.height*0.1)))
        pygame.draw.rect(screen, (255,255,255), (round(AnnouncementBox.width*0.3), round(AnnouncementBox.height*0.1), round(AnnouncementBox.width*0.4),
                                                 round(AnnouncementBox.height*0.1)), 4)
        pygame.draw.rect(screen, (255,255,255), (round(AnnouncementBox.width*0.3), round(AnnouncementBox.height*0.1), round(AnnouncementBox.height*0.1),
                                                 round(AnnouncementBox.height*0.1)), 4)
        for i in range(len(self.besttext)):
            Texthelper.write(screen, [(round(AnnouncementBox.width*0.31+self.image.get_size()[0]),round(AnnouncementBox.height*0.11)+round(AnnouncementBox.height*0.03*i)), self.besttext[i], 2])
        if self.ended:
            Texthelper.write(screen, [(round(AnnouncementBox.width*0.40), round(AnnouncementBox.height*0.21)), "Press Enter to Continue", 1.5])
            inputvar = keyboard()
            if "enter" in inputvar:
                del AnnouncementBox.upcoming[0]

    def timehelper(self):
        BREAKPOS = 32
        self.time += 1
        if self.time % 20 == 0 and len(self.currenttext) < len(self.text):
            self.currenttext += " " + self.text[len(self.currenttext):].split()[0]
            position = len(self.besttext)-1
            self.besttext[position] += " " + self.text[len(self.besttext[position])+self.runningtotal:].split()[0]
            if len(self.besttext[position]) > BREAKPOS:
                linebreak = self.besttext[position].rindex(" ")
                linestuff = self.besttext[position][linebreak:]
                self.besttext[position] = self.besttext[position][:linebreak]
                self.runningtotal += len(self.besttext[position])
                self.besttext.append(linestuff)
        if len(self.currenttext) >= len(self.text):
            self.ended = True
    
   
class Texthelper():
    scalar = 1
    width = 1
    height = 1
    last_click = () 

    def interpretcoords(text_input):
        text_location = text_input[0]
        location_list = [text_location[0], text_location[1]]
        scale = text_input[2] * Texthelper.scalar
        text_input2 = text_input[0:] #very important line
        if str(location_list[0]).isdigit() == False:
            if location_list[0] == "center":
                location_list[0] = Texthelper.width / 2 - Texthelper.textlength(text_input) / 2
            elif location_list[0] == "right":
                location_list[0] = Texthelper.width - Texthelper.textlength(text_input)
            else:
                location_list[0] = 0
            location_list[1] *= Texthelper.scalar
        else:
            location_list[0] *= Texthelper.scalar
            location_list[1] *= Texthelper.scalar
        text_input2[0] = (location_list[0], location_list[1])
        return text_input2

    # text_input = [(x, y), "text", text_scale]
    # text placed from upper left corner # pixels of text (1x scale) == (11 * # of characters) + (3 * # of spaces) - 3
    def write(screen, text_input, *args):
        text_location = Texthelper.interpretcoords(text_input)[0]
        text = text_input[1]
        scale = text_input[2] * Texthelper.scalar
        text = text.lower()

        #displayer
        horizontal_pos = text_location[0]
        for i in range(len(text)):
            if text[i] != " ":
                text3 = Font.getChar(text[i], scale, "pressed" in args)                
                screen.blit(text3, (horizontal_pos, text_location[1]))
                horizontal_pos += 11 * scale
            if text[i] == " " and text[i-1] != " " and i != 0:
                horizontal_pos += 3 * scale #would be 6 but each character automatically gives a 3 pixel * scale space until the next character
            if text[i] == " " and text[i-1] == " " and i != 0:
                horizontal_pos += 11 * scale

    def writeBox(screen, text_input, **kwargs):
        padding = 18 * Texthelper.scalar
        color = (255,255,255)
        if 'color' in kwargs:
            color = kwargs['color']
        if 'padding' in kwargs:
            padding = kwargs['padding']

        if 'pressed' in kwargs:
            Texthelper.write(screen, text_input, "pressed")
        else:
            Texthelper.write(screen, text_input)
        
        x, y = text_input[0]
        pygame.draw.rect(screen, color, [x-padding, y-padding/2, Texthelper.textlength(text_input)+padding*2, 12*Texthelper.scalar*text_input[2]+padding],
                         int(2*Texthelper.scalar))

    def writeButton(screen, text_input):
        click = mouse()

        text_location = Texthelper.interpretcoords(text_input)[0]
        text = text_input[1]
        scale = text_input[2] * Texthelper.scalar
        x_range = Texthelper.textlength(text_input)
        y_range = 12 * scale

        if text_location[0] < pygame.mouse.get_pos()[0] < (text_location[0]+x_range) and text_location[1]<pygame.mouse.get_pos()[1]<(text_location[1]+y_range):
            Texthelper.write(screen, text_input, "pressed")
        else:
            Texthelper.write(screen, text_input)

        #print(text_input[1] + ", click: " + str(click) + " last click: " + str(Texthelper.last_click))
        if click != Texthelper.last_click:
            if text_location[0] < click[1] < (text_location[0] + x_range) and text_location[1] < click[2] < (text_location[1] + y_range):
                Texthelper.last_click = click
                return True
            else:
                return False

    def writeButtonBox(screen, text_input, **kwargs):
        padding = 18 * Texthelper.scalar
        color = (255,255,255)
        if 'color' in kwargs:
            color = kwargs['color']
        if 'padding' in kwargs:
            padding = kwargs['padding']
            
        click = mouse()
        x, y = text_input[0]
        if x-padding < pygame.mouse.get_pos()[0] < x+Texthelper.textlength(text_input)+padding*2 and (y-padding/2 < pygame.mouse.get_pos()[1] < y+12*Texthelper.scalar*text_input[2]+padding):
           Texthelper.writeBox(screen, text_input, color=SELCOLOR, padding=padding, pressed=True)
        else:
            Texthelper.writeBox(screen, text_input, color=color, padding=padding)

        if click != Texthelper.last_click:            
            if x-padding < click[1] < x+Texthelper.textlength(text_input)+padding*2 and y-padding/2 < click[2] < y+12*Texthelper.scalar*text_input[2]+padding:
                Texthelper.last_click = click
                return True
            else:
                return False
        
    def writeNullButton(screen, text_input):
        Texthelper.write(screen, text_input)
        text_location = Texthelper.interpretcoords(text_input)[0]
        text = text_input[1]
        scale = text_input[2] * Texthelper.scalar

        x_range = Texthelper.textlength(text_input)
        y_range = 12 * scale
        
        click = mouse()
        if text_location[0] < click[1] < (text_location[0] + x_range) and text_location[1] < click[2] < (text_location[1] + y_range):
            return True
        elif click == (0,0,0):
            return True
        else:
            return False        

    def textlength(text_input):
        text = text_input[1]
        if text and text[-1] == "|":
            text = text[:-1]
        scale = text_input[2] * Texthelper.scalar
        x_range = 0
        for i in range(len(text)):
            if text[i] != " ":
                x_range += 11 * scale
            elif text[i-1] != " " and text[i] == " " and i != 0:
                x_range += 3 * scale
            elif text[i] == " " and text[i-1] == " " and i != 0:
                x_range += 11 * scale
        x_range -= 3 * scale
        return x_range


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
        parse_line = parse_line[:-1] #gets rid of ending bracket
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
    def set(self, content, line): #line is line # in file being written to
        content = str(content)
        content = content.split("'")
        content = "".join(content)
        content += "\n"

        file = open(self.info_file, "r")
        contents = file.readlines()
        file.close()
        contents[line] = content

        file = open(self.info_file, "w")
        file.writelines(contents)
        file.close()


filehelper = Filehelper("Assets\\gamedata.txt") #makes lowercase filehelper used throughtout work with the class
