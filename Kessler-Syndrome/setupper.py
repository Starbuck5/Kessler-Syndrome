import pygame

from pgx import Texthelper
from pgx import InputGetter
from pgx import collect_inputs
from pgx import AllEvents
from pgx import filehelper
from pgx import platform
from pgx import loadImage

def setup():
    pygame.init()

    scrInfo = pygame.display.Info()
    suggestedRes = scrInfo.current_w, scrInfo.current_h
    if suggestedRes[0] < 0 or platform.system() == "Darwin":
        suggestedRes = pygame.display.list_modes()[0]
    
    widthBox = InputGetter([(110,75), str(suggestedRes[0]), 1.5], "int")
    heightBox = InputGetter([(230,75), str(suggestedRes[1]), 1.5], "int")

    logo = loadImage("images/icon.png")
    logo.set_colorkey((255,0,0))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Kessler First Time Setup")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([600, 450])
    
    Texthelper.width = 600
    Texthelper.height = 450
    Texthelper.scalar = 1.5
    Texthelper.SAFEASPECT = (4,3)
    
    full = True

    color = (20,110,230)


    running = True
    while running:
        clock.tick(100)
        screen.fill(color)

        Texthelper.write(screen, [("center",20), "Welcome to Kessler Syndrome", 1.4])
        Texthelper.write(screen, [("center", 50), "Resolution reported by your system:", 1])
        widthBox.update(screen)
        Texthelper.write(screen, [(190, 75), "by", 1.5])
        heightBox.update(screen)
        Texthelper.write(screen, [("center", 110), "Please change to your desired resolution", 0.9])

        Texthelper.write(screen, [(50, 170), "Fullscreen:", 1.5])
        if Texthelper.writeButton(screen, [(240, 170), str(full), 1.5]):
            full = not full
        Texthelper.write(screen, [(2, 200), "Note: If you are going to do fullscreen,", 1])
        Texthelper.write(screen, [(2, 215), "the resolution set should be the same", 1])
        Texthelper.write(screen, [(27, 230), "as your monitors resolution", 1])

        if Texthelper.writeButton(screen, [("center", 270), "Continue", 1.25]):
            contents = filehelper.get(0)
            contents[0] = widthBox.getText()
            contents[1] = heightBox.getText()
            contents[2] = full
            filehelper.set(contents, 0)
            running = False

        collect_inputs()

        pygame.display.flip()
        for event in AllEvents.TICKINPUT:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit

    pygame.quit()

if __name__ == "__main__":
    setup()
