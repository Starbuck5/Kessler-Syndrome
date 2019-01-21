#just a file to de-clutter the main script
import pygame
import random
OS = "windows" #other option = "mac"
LEGIBLE = True

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

# font setup
fontLocation = ["number0", "number1", "number2", "number3", "number4", "number5", "number6", "number7", "number8", "number9", "lettera", "letterb",
                "letterc", "letterd", "lettere", "letterf", "letterg", "letterh", "letteri", "letterj", "letterk", "letterl", "letterm", "lettern",
                "lettero", "letterp", "letterq", "letterr", "letters", "lettert", "letteru", "letterv", "letterw", "letterx",
                "lettery", "letterz", "colon", "minus", "plus", "question", "leftbracket", "rightbracket"]
if LEGIBLE != True:
    random.shuffle(fontLocation)


char_list = []
for pathID in fontLocation:
    try:
        holdervar = loadImage("Assets\\font\\" + pathID + ".tif")
    except:
        print("error loading " + pathID + ".tif")
        holdervar = missingTexture
    char_list.append(holdervar)


class InputGetter():
    last_input = []
    def __init__ (self, initialtext, inputtype):
        self.initialtext = initialtext
        self.inputtype = inputtype
        self.currenttext = initialtext
        self.rawtext = initialtext[1]
        self.clicked = False

    def update(self, screen):
        if self.clicked == False:
            if Texthelper.writeButton(screen, self.currenttext) == True:
                self.clicked = True
        if self.clicked == True:
            if Texthelper.writeNullButton(screen, self.currenttext) == False:
                self.clicked = False
            if self.inputtype == "int":
                InputGetter.handleThisInt(self)
            if self.inputtype == "str":
                InputGetter.handleThisString(self)

    def handleThisString(self):
        last_input = InputGetter.last_input
        inputvar = keyboard()
        self.rawtext = self.currenttext[1]
        alphabet_check = "abcdefghijklmnopqrstuvwxyz"

        if inputvar != last_input:
            if "back" in inputvar or "delete" in inputvar:
                self.rawtext = self.rawtext[:-1]
            elif len(inputvar) == 1 and len(inputvar[0]) == 1 and inputvar[0] in alphabet_check:
                self.rawtext += inputvar[0]
            
        self.currenttext = [self.currenttext[0], self.rawtext, self.currenttext[2]]
        InputGetter.last_input = inputvar


    def handleThisInt(self):
        last_input = InputGetter.last_input
        inputvar = keyboard()
        self.rawtext = self.currenttext[1]

        if inputvar != last_input:
            if "back" in inputvar or "delete" in inputvar:
                self.rawtext = self.rawtext[:-1]
            elif len(inputvar) == 1 and len(inputvar[0]) == 1 and inputvar[0].isdigit() == True:
                self.rawtext += inputvar[0]
            
        self.currenttext = [self.currenttext[0], self.rawtext, self.currenttext[2]]
        InputGetter.last_input = inputvar

    def getText(self):
        return self.rawtext

    def getData(self):
        return self.currenttext
   
class Texthelper():
    scalar = 1
    width = 1
    height = 1
    last_click = ()
    missingTexture = missingTexture

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
    def write(screen, text_input):
        char_index = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                      "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ":", "-", "+", "?", "[", "]"]
        text_location = Texthelper.interpretcoords(text_input)[0]
        text = text_input[1]
        scale = text_input[2] * Texthelper.scalar
        text = text.lower()

        #displayer
        horizontal_pos = text_location[0]
        for i in range(len(text)):
            if text[i] != " ":
                if text[i] in char_index:
                    text3 = scaleImage(char_list[char_index.index(text[i])], scale)
                else:
                    text3 = scaleImage(Texthelper.missingTexture, scale)
                screen.blit(text3, (horizontal_pos, text_location[1]))
                horizontal_pos += 11 * scale
            if text[i] == " " and text[i-1] != " " and i != 0:
                horizontal_pos += 3 * scale #would be 6 but each character automatically gives a 3 pixel * scale space until the next character
            if text[i] == " " and text[i-1] == " " and i != 0:
                horizontal_pos += 11 * scale


    def writeButton(screen, text_input):
        Texthelper.write(screen, text_input)
        text_location = Texthelper.interpretcoords(text_input)[0]
        text = text_input[1]
        scale = text_input[2] * Texthelper.scalar

        x_range = Texthelper.textlength(text_input)
        y_range = 12 * scale

        click = mouse()
        #print(text_input[1] + ", click: " + str(click) + " last click: " + str(Texthelper.last_click))
        if click != Texthelper.last_click:
            if text_location[0] < click[1] < (text_location[0] + x_range) and text_location[1] < click[2] < (text_location[1] + y_range):
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

class Filehelper():
    info_file = handlePath("Assets\\gamedata.txt")
    #converts file contents back to the ints and strings they started as and returns them by line
    def get(self, line): #line is line # in file being extracted
        file = open(Filehelper.info_file, "r")
        contents = file.readlines()
        file.close()

        parse_line = contents[line]
        parse_line = parse_line[1:]
        whitespace = len(parse_line) - parse_line.rindex("]")
        parse_line = parse_line[:-whitespace]
        parse_line = parse_line.split(", ")
        end = 0
        start = 0
        for i in range(len(parse_line)):
            if isinstance(parse_line[i], list) != True:
                if parse_line[i].rfind("[") != -1:
                    start = i
                    parse_line[i] = parse_line[i][1:]
                if parse_line[i].rfind("]") != -1:
                    end = i + 1
                    parse_line[i] = parse_line[i][:-1]
        if end != 0:
            parse_line_sub = []
            for i in range(end-start):
                parse_line_sub.append(parse_line[i+start])
            parse_line = parse_line[:start] + [parse_line_sub] + parse_line[end:]
       
        for i in range(len(parse_line)):
            if isinstance(parse_line[i], list):
                for j in range(len(parse_line[i])):
                    if parse_line[i][j].isdigit() == True:
                        parse_line[i][j] = int(parse_line[i][j])
                    elif "." in parse_line[i][j]:
                        if parse_line[i][j][-1].isdigit():
                            parse_line[i][j] = float(parse_line[i][j])  
                    elif parse_line[i][j] == "True":
                        parse_line[i][j] = True
                    elif parse_line[i][j] == "False":
                        parse_line[i][j] = False
            else:
                if parse_line[i].isdigit() == True:
                        parse_line[i] = int(parse_line[i])
                elif "." in parse_line[i]:
                    if parse_line[i][-1].isdigit():
                        parse_line[i] = float(parse_line[i])                        
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

        file = open(Filehelper.info_file, "r")
        contents = file.readlines()
        file.close()
        contents[line] = content

        file = open(Filehelper.info_file, "w")
        file.writelines(contents)
        file.close()


filehelper = Filehelper() #makes lowercase filehelper used throughtout work with the class
