import pygame
import random

from pgx import *
from graphics import change_color
from game import generateStars
import graphics

def level1(screen, width, height, scalarscalar):
    clock = pygame.time.Clock()
    soyuz = loadImage("Assets\\images\\soyuz2.tif")  
    soyuzscalar = scalarscalar
    soyuz = scaleImage(soyuz, soyuzscalar)
    soyuzsize = soyuz.get_size()
    pygame.mouse.set_visible(True)

    star_list = generateStars(width, height)

    mountains = loadImage("Assets\\images\\cutsceneback.tif")
    mountainsize = mountains.get_size()
    mountains = pygame.transform.scale(mountains, (width, int(width/mountainsize[0]*mountainsize[1])))
    mountainsize = mountains.get_size()

    flamesheet = loadImage("Assets\\images\\flames.tif")
    all_flames = spriteSheetBreaker(flamesheet, 8, 15, 0, 0, 2, 4)
    for i in range(len(all_flames)):
        all_flames[i] = scaleImage(all_flames[i], soyuzscalar*2)
    
    startflamelist = all_flames[:2]
    flame_list = all_flames[2:]      

    def randomflame(ypos):
        if (ypos+1400) < (height - height*0.2):
           return flame_list[random.randint(0, len(flame_list)-1)]
        else:
            return startflamelist[random.randint(0, len(startflamelist)-1)]

    opening_crawl = [line.rstrip('\n') for line in open(handlePath("assets\\data\\opening_crawl.txt"))]
    line_spacing = 80
    
    xpos = width/2 - soyuzsize[0]/2
    ypos = height
    dy = height/700
    namebox = InputGetter([("center", 490), "name", 3], "str")
    running = True
    while running:
        clock.tick(100)
        screen.fill((0,0,0))

        graphics.printer(screen, star_list, 0, "na", scalarscalar, False)
        
        screen.blit(mountains, (0, height-mountainsize[1]))

        for i in range(len(opening_crawl)):
            Texthelper.write(screen, [("center", ypos + line_spacing * i), opening_crawl[i], 3])

        screen.blit(soyuz, (xpos, ypos + line_spacing * len(opening_crawl) + 100))
        screen.blit(randomflame(ypos), (xpos-4*soyuzscalar, ypos+soyuzsize[1] + line_spacing *
                                        len(opening_crawl) + 100))
        screen.blit(randomflame(ypos), (xpos+6*soyuzscalar, ypos+soyuzsize[1] + line_spacing *
                                        len(opening_crawl) + 100))
        screen.blit(randomflame(ypos), (xpos+10*soyuzscalar, ypos+soyuzsize[1] + line_spacing *
                                        len(opening_crawl) + 100))
        screen.blit(randomflame(ypos), (xpos+20*soyuzscalar, ypos+soyuzsize[1] + line_spacing *
                                        len(opening_crawl) + 100))

        
        if not (ypos + line_spacing * len(opening_crawl) + 400 > height/2-100):
            namebox.update(screen)
            namebox.clicked = True
            namebox.currenttext = [("center", 490), namebox.getData()[1], namebox.getData()[2]]
            Texthelper.write(screen, [("center", 440), "enter name to continue", 2])
            if len(namebox.getText()) > 11:
                Texthelper.write(screen, [("center", 570), "name should be less than 12 characters", 1])
            isValidInput = namebox.getText() != "name" and len(namebox.getText()) < 12
            isPressed = Texthelper.writeButton(screen, [("center", 540), "then press here or enter", 2])
            isKeyed = len(keyboard()) == 1 and keyboard()[0] == "enter"
            if (isPressed or isKeyed) and isValidInput:
                running = False
                filehelper.setElement(namebox.getText(), 1, 0)           
            
        collect_inputs()
        
        ypos -= dy        
        pygame.display.flip()

        
        for event in AllEvents.TICKINPUT:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit

    pygame.mouse.set_visible(False)
        
