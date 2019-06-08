import pygame
import random

import graphics
from pgx import SoundVault

everyHitbox = []

#sound effects for collision        
def explosion_sounds():
    explosion_picker = random.randint(0,1)
    if explosion_picker == 0:
        SoundVault.play('explosion1')
    if explosion_picker == 1:
        SoundVault.play('explosion2')

#backened for collinfo, returns hitboxes when given an index of the objectlist
def getHitbox(object_list, object_location, graphlist):
    xpos = object_list[object_location*8]
    ypos = object_list[1+object_location*8]
    objectID = object_list[4+object_location*8]
    rotation = object_list[5+object_location*8]
    
    hitBox = [xpos, ypos, 0,0]
    if objectID == 1 or objectID == 5: #main ship
        #objectID as 1.1 because thats full health ship and ship size doesn't change between states
        hitBox = graphics.Images.getHitbox(xpos, ypos, 1.1, -rotation.getRotation(), True, True, True)
    elif objectID == 2 or objectID == 8 or objectID == 4: #shots and debris particles
        hitBox = [xpos-2, ypos-2, 4, 4]
    elif objectID == 6: #aliens
        hitBox = [xpos, ypos, 60, 60]
    elif objectID == 0: #zvezda
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation(), False)
    elif 9 < objectID < 40: #pixel things
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
    elif objectID == 7: #alien mines
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
    elif objectID == 9: #mine explosion
        scale = 1 + (.1 * (300 - object_list[object_location*8+7]))
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
        graphics.Images.scaleHitbox(hitBox, scale)     
    elif 69 < objectID < 100: #asteroids
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
    elif objectID == 110: #derelict ship
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
    elif objectID == 120: #alien drone
        hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
    else:
        try:
            hitBox = graphics.Images.getHitbox(xpos, ypos, objectID, rotation.getRotation())
        except:
            pass
    return hitBox

#called once per tick, gets all the hitboxes ready for examination
def prime(object_list, screen, graphlist, DEVMODE, cheats_settings):
    everyHitbox.clear()
    for i in range(int(len(object_list)/8)):
        hitbox = getHitbox(object_list, i, graphlist)
        everyHitbox.append(hitbox)
        if DEVMODE and cheats_settings[5]:
           pygame.draw.rect(screen, (255,255,255), hitbox, 1)

#tests if two objects collide by location in the object list and returns a boolean
def doCollide(object_number1, object_number2, object_list):
    if object_number1 != object_number2: #exempts object intersecting itself
        hitBox1 = everyHitbox[object_number1]
        hitBox2 = everyHitbox[object_number2]
        if hitBox1[2] != 0 and hitBox1[3] != 0 and hitBox2[2] != 0 and hitBox1[3] != 0:
            if pygame.Rect(hitBox1).colliderect(pygame.Rect(hitBox2)):
                return True
    return False
