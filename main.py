import random
import pygame
from player import *


#start the pygame engine
pygame.init()

#start the pygame font engine
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 23) #load a font for use

#start the sound engine
pygame.mixer.init();

#game variables
simOver = False
p1 = Player()
map1 = Map()
camera_offset = (0,0)

#game independent variables (needed for every pygame)
FPS = 60 #60 Frames Per Second for the game update cycle
fpsClock = pygame.time.Clock() #used to lock the game to 60 FPS
screen = pygame.display.set_mode((1280,720)) #initialize the game window
world = pygame.Surface((3000,3000))

def create_map_1():
    map1.add(Platform(0,690,2400,30,(0,255,0)))
    map1.add(Platform(100,600,400,30,(0,255,0)))
    map1.add(Platform(200,500,400,30,(0,255,0)))
    map1.add(Platform(100,350,200,30,(0,255,0)))
    map1.add(Platform(270,250,200,30,(0,255,0)))
    map1.add(Platform(600,200,30,400,(0,255,0)))
    map1.add(Platform(715,120,300,30,(0,255,0)))
    map1.add(Platform(740,700,300,30,(0,255,0)))
    map1.addCoin(Coin(600, 650))
    map1.addCoin(Coin(220, 450))
    map1.addCoin(Coin(730, 90))
    map1.set_gravity(-4)

def draw_mouse_coords():
    textSurface = myfont.render(str(pygame.mouse.get_pos()), True, (255,255,255))
    world.blit(textSurface, (50, 30))

def clear_screen():
    pygame.draw.rect(world, (0,0,0), (0, 0, world.get_rect().width, world.get_rect().height))

# initialize all data before gameplay
create_map_1()
p1.setMap(map1)

#main while loop
while not simOver:
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            simOver = True

    # draw code
    clear_screen()
    map1.draw(world)
    p1.draw(world)
    draw_mouse_coords()

    # player update code
    player_pos = p1.act()
    x_offset = 0
    y_offset = 0
    if player_pos[0] > 640:
        x_offset = 640 - player_pos[0]
    if player_pos[1] < 350:
        y_offset = 350 - player_pos[1]
    camera_offset = (x_offset, y_offset)
    #camera_pos = ((player_pos[0], player_pos[1] - 900))

    #put all the graphics on the screen
    #should be the LAST LINE of game code
    screen.blit(world,camera_offset)
    pygame.display.flip()
    fpsClock.tick(FPS) #slow the loop down to 60 loops per second