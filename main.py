import random
import time

import pygame
from player import *
from playerAI import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
# start the pygame engine
pygame.init()

# start the pygame font engine
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 23)  # load a font for use

# start the sound engine
pygame.mixer.init()

# game variables
simOver = False

map1 = Map()
camera_offset = (0, 0)
cameraPos = (500, 500)
initialValue = 100

aiPlayers = []

# game independent variables (needed for every pygame)
FPS = 60  # 60 Frames Per Second for the game update cycle
fpsClock = pygame.time.Clock()  # used to lock the game to 60 FPS
screen = pygame.display.set_mode((1280, 720))  # initialize the game window
world = pygame.Surface((3000, 3000))


def createAIPlayers():
    for i in range(initialValue):
        aiPlayers.append(PlayerAI())


def refillPopulation():
    while len(aiPlayers) != initialValue:
        aiPlayers.append(PlayerAI())
    for a in aiPlayers:
        a.setMap(map1)


def create_map_1():
    ## maze
    map1.add(Platform(0, 690, 3000, 30, (0, 255, 0)))
    # map1.add(Platform(100, 600, 400, 30, (0, 255, 0)))
    map1.add(Platform(200, 500, 400, 30, (0, 255, 0)))
    map1.add(Platform(30, 350, 200, 30, (0, 255, 0)))
    map1.add(Platform(225, 250, 260, 30, (0, 255, 0)))
    # map1.add(Platform(600, 200, 30, 400, (0, 255, 0)))
    map1.add(Platform(650, 420, 300, 30, (0, 255, 0)))
    map1.add(Platform(1380, 500, 200, 30, (0, 255, 0)))
    map1.add(Platform(715, 120, 300, 30, (0, 255, 0)))
    map1.add(Platform(740, 700, 300, 30, (0, 255, 0)))
    map1.add(Platform(0, 0, 40, 720, (0, 255, 0)))
    map1.add(Platform(1080, 590, 300, 30, (0, 255, 0)))
    map1.add(Platform(525, 175, 130, 30, (0, 255, 0)))
    map1.add(Platform(1250, 0, 30, 500, (0, 255, 0)))
    map1.add(Platform(1250, 620, 30, 70, (0, 255, 0)))
    map1.add(Platform(1090, 220, 200, 30, (0, 255, 0)))

    ## coins
    # map1.addCoin(Coin(600, 650))
    map1.addCoin(Coin(385, 400))
    map1.addCoin(Coin(730, 90))
    map1.addCoin(Coin(840, 90))
    map1.addCoin(Coin(950, 90))
    map1.addCoin(Coin(1380, 450))
    map1.addCoin(Coin(1120, 540))
    map1.addCoin(Coin(860, 390))
    map1.addCoin(Coin(720, 390))
    map1.addCoin(Coin(585, 145))
    map1.addCoin(Coin(1170, 190))
    map1.set_gravity(-4)


def resetCoins():
    for c in map1.coins:
        c.resetColor()


def draw_mouse_coords():
    textSurface = myfont.render(str(pygame.mouse.get_pos()), True, WHITE)
    world.blit(textSurface, (50, 30))
    if len(aiPlayers) > 1:
        textSurface = myfont.render((str(aiPlayers[0].currentAllele)), True, WHITE)
        world.blit(textSurface, (50, 60))
    textSurface = myfont.render(str(aiPlayers.__len__()), True, WHITE)
    world.blit(textSurface, (50, 90))
    textSurface = myfont.render("Generation: " + str(genCounter), True, WHITE)
    world.blit(textSurface, (50, 120))


def clear_screen():
    pygame.draw.rect(world, (0, 0, 0), (0, 0, world.get_rect().width, world.get_rect().height))


def updateCamera():
    global cameraPos
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        cameraPos = (cameraPos[0] + 10, cameraPos[1])
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        cameraPos = (cameraPos[0] - 10, cameraPos[1])


def sortAIByScore():
    for i in range(len(aiPlayers) - 1):
        for j in range(len(aiPlayers) - 2):
            p1 = aiPlayers[j]
            p2 = aiPlayers[j + 1]
            if p1.getScore() < p2.getScore():
                temp = p1
                aiPlayers[j] = p2
                aiPlayers[j] = temp


# helper method to get each player score
def sortScore(playerAI):
    return playerAI.getScore()


def sortAllScore():
    aiPlayers.sort(key=sortScore, reverse=True)
    #sorted(aiPlayers, key=lambda playerAI: playerAI.player.score)
    for a in aiPlayers:
        print(a.getScore())



def drawCurrentHighest():
    global sortedPlayers
    textSurface = myfont.render("Current Highest Score: " + str(sortedPlayers[0].getScore()), True, WHITE)
    world.blit(textSurface, (400, 30))

    pygame.draw.circle(world, (255, 0, 0), (
        sortedPlayers[0].player.x + (sortedPlayers[0].player.width / 2),
        sortedPlayers[0].player.y + (sortedPlayers[0].player.height / 2)),
           30, 3)



# no worky
def killBottomHalf():
    global aiPlayers
    aiPlayers = aiPlayers[:int(len(aiPlayers) / 2)]


def mateParents(remaining):

    '''
    for a in range(len(remaining)):
        parent1 = remaining[a]
        parent2 = remaining[a + 1]
        child = PlayerAI()
        newDna = child.dna
        p1DNA = parent1.getDNASequence()
        for i in p1DNA:
            randNum = random.randint(1, 2)
            if randNum == 1:
                newDna.append(parent1.getDNAValue(i))
            else:
                newDna.append(parent2.getDNAValue(i))

        aiPlayers.append(child)
        a += 1
'''

    for a in range(len(remaining)):
        parent1 = remaining[a]
        parent2 = remaining[a + 1]
        child = PlayerAI()
        newDna = child.dna
        p1DNA = parent1.getDNASequence()
        randNum = random.randrange(0, parent1.alleleCount)
        for i in range(randNum):
            newDna.append(parent1.getDNAValue(i))
        for i in range(randNum+1, parent1.alleleCount +1):
            newDna.append(parent2.getDNAValue(i))

        aiPlayers.append(child)
        a +=1

def setMap():
    for a in aiPlayers:
        a.setMap(map1)


genCounter = 1

# initialize all data before gameplay
create_map_1()
createAIPlayers()
sortedPlayers = aiPlayers.copy()
for a in aiPlayers:
    a.setMap(map1)

# main while loop
while not simOver:
    # loop through and empty the event queue, key presses
    # buttons, clicks, etc.
    for event in pygame.event.get():
        # if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            simOver = True

    # draw code
    clear_screen()
    map1.draw(world)

    for a in aiPlayers:
        a.draw(world)
    draw_mouse_coords()
    drawCurrentHighest()

    # player update code
    updateCamera()

    if aiPlayers[0].isDone():
        sortAllScore()
        killBottomHalf()
        for a in aiPlayers:
            # sortAIByScore()
            a.reset()
        mateParents(aiPlayers)
        setMap()
        genCounter += 1
        resetCoins()
        sortedPlayers = aiPlayers.copy()

    for a in aiPlayers:
        a.act()

    x_offset = 0
    y_offset = 0
    if cameraPos[0] > 640:
        x_offset = 640 - cameraPos[0]
    if cameraPos[1] < 350:
        y_offset = 350 - cameraPos[1]
    camera_offset = (x_offset, y_offset)
    # camera_pos = ((player_pos[0], player_pos[1] - 900))

    sortedPlayers.sort(key=sortScore, reverse=True)

    # put all the graphics on the screen
    # should be the LAST LINE of game code
    screen.blit(world, camera_offset)
    pygame.display.flip()

    fpsClock.tick(FPS)  # slow the loop down to 60 loops per second
