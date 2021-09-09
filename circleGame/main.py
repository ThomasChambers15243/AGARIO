import copy
import random, sys, time, math, pygame, math
from data import *
from collision import *
from util import *
from pygame.locals import *
import multiprocessing

FPS = 144  # frames per second to update the screen
WINWIDTH = 1920  # width of the program's window, in pixels
WINHEIGHT =1080  # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)


VIRTUAL_WIN_HEIGHT = 2500
VIRTUAL_WIN_WIDTH = 2500

CAMERASLACK = 0




N = "N"
E = "E"
S = "S"
W = "W"
NE = "NE"
SE = "SE"
SW = "SW"
NW = "NW"

DIRECTION = [N, E, S, W, NE, SE, SW, NW]
MOVMENT_KEYS = [K_d, K_RIGHT, K_a, K_LEFT, K_s, K_DOWN, K_w, K_UP]


#MAIN CONSTS#
START_SPEED = 6
DANGER_ORB_DMG_THRESHOLD = 128
MAX_SIZE = 800
MAX_SIZE_FOR_ORB_GAIN = 900

AQUA = (0, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
BLACK = (0,0,0)


#Points Orbs
ORBAMOUNT = 2000
ORBCOLOURS = [AQUA,BLUE,GREEN,PURPLE,RED,BLACK]
global pointOrb
pointOrbs = []

#Danger Orbs
DANGER_ORB_AMOUNT = 30#30
dangerOrbs = []
#Danger Orb img image load
dangerOrbImgs = []
for i in range(1,3):
    dangerOrbImgs.append(pygame.image.load("imgs/" + entityStats[2]["img"] + str(i) + ".png"))

#AI Entities
AI_AMOUNT = 80
aiEntities = []

currentTime = 0


def main():
    pygame.init()
    #set clock
    clock = pygame.time.Clock()
    #set speed
    pygame.key.set_repeat(1, 10)
    playerStats["speed"] = START_SPEED


    #set FONTS
    global FONT_BASIC
    FONT_BASIC = pygame.font.Font('freesansbold.ttf', 32)
    global FONT_SYS
    FONT_SYS = pygame.font.SysFont("monospace", 15)


    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Circle Game')



    # set players start position as the  center of the window
    playerStats["x"] = HALF_WINWIDTH
    playerStats["y"] = HALF_WINHEIGHT

    #spawn in orbs, danger orbs and AI players
    if len(pointOrbs) < ORBAMOUNT:
        #createOrbs(ORBAMOUNT)
        createOrbs(ORBAMOUNT,pointOrbs,playerStats,entityStatNums["pointOrb"],
                   ORBCOLOURS,circleCollision,VIRTUAL_WIN_WIDTH,VIRTUAL_WIN_HEIGHT)

    if len(dangerOrbs) < DANGER_ORB_AMOUNT:
        createOrbs(DANGER_ORB_AMOUNT,dangerOrbs,playerStats,entityStatNums["dangerOrb"],
                   ORBCOLOURS,circleCollision,VIRTUAL_WIN_WIDTH,VIRTUAL_WIN_HEIGHT)
        for i in range(0,len(dangerOrbs)):
            dangerOrbs[i]["img"] = dangerOrbImgs[random.randint(0, 1)]

    if len(aiEntities) < AI_AMOUNT:
        createAIEntities(AI_AMOUNT,aiEntities,playerStats,pointOrbs,dangerOrbs,
                         entityStatNums["AI"], ORBCOLOURS,circleCollision,
                         VIRTUAL_WIN_WIDTH,VIRTUAL_WIN_HEIGHT)
        # createAi()
        # createOrbs(AI_AMOUNT,aiEntities,spawnEntitiesAI)
    camerax = 0
    cameray = 0



    while True:
        runGame(DISPLAYSURF, cameray, camerax,clock)

                    ##Main loop##

def runGame(surface, cameray, camerax,clock):
    currentTime = pygame.time.get_ticks()
    currentTimeInSeconds = str(int(currentTime/1000))
    surface.fill(WHITE)


    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
        else:
            setMovement()



    # adjust camerax and cameray if beyond the "camera slack"
    playerCenterx = playerStats['x']
    playerCentery = playerStats['y']
    if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
        camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
    elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
        camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
    if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
        cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
    elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
        cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT


    update(currentTimeInSeconds)
    draw(surface, camerax, cameray,clock,currentTimeInSeconds)
    pygame.display.update()
    clock.tick(FPS)


def update(currentTimeInSeconds):
    #update player point/danger orb collision, size and speed
    orbCollision(playerStats)
    calculateLossOfBlobMass(playerStats, currentTimeInSeconds)
    updateSize(playerStats)
    updateSpeed(playerStats)
    #update ai point/danger orb collision, size and speed

    for i in range(0, len(aiEntities)):
        #orbCollision(aiEntities[i])
        calculateLossOfBlobMass(aiEntities[i], currentTimeInSeconds)
        updateSize(aiEntities[i])
        updateSpeed(aiEntities[i])
        aiMovment(aiEntities[i])




def aiMovment(blob):
    distance = int(math.sqrt((blob["targetX"] - blob["x"])**2 + (blob["targetY"] - blob["y"])**2))

    if distance > blob["radius"]/2:
        r = 7/distance#blob["speed"] / distance
        xt = r * blob["targetX"] + (1 - r) * blob["x"]
        yt = r * blob["targetY"] + (1 - r) * blob["y"]

        blob["x"] = int(xt)
        blob["y"] = int(yt)
        print(blob["speed"])
    else:
        blob["isMoving"] = False



def setMovement():
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[K_a]) and playerStats["x"] > -VIRTUAL_WIN_WIDTH + playerStats["radius"]:
        playerStats["x"] -= playerStats["speed"]
        #aiEntities[0]["x"]-= playerStats["speed"]
    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[K_d]) and playerStats["x"] < VIRTUAL_WIN_WIDTH - playerStats["radius"]:
        playerStats["x"] += playerStats["speed"]
        #aiEntities[0]["x"] += playerStats["speed"]
    if (keys_pressed[pygame.K_UP] or keys_pressed[K_w]) and playerStats["y"] > -VIRTUAL_WIN_HEIGHT + playerStats["radius"]:
        playerStats["y"] -= playerStats["speed"]
        #aiEntities[0]["y"]-= playerStats["speed"]
    if (keys_pressed[pygame.K_DOWN] or keys_pressed[K_s]) and playerStats["y"] < VIRTUAL_WIN_HEIGHT - playerStats["radius"]:
        playerStats["y"] += playerStats["speed"]
        #aiEntities[0]["y"]+= playerStats["speed"]

def orbCollision(blob):
    if blob["points"] <= MAX_SIZE_FOR_ORB_GAIN:
        for i in range(0,len(pointOrbs)):
            if circleCollision(blob,pointOrbs[i]):
                playerAddPoints(blob, pointOrbs[i]["points"])
                pointOrbs.pop(i)
                pointOrbs.append(spawnOrb(blob,entityStatNums["pointOrb"],ORBCOLOURS, circleCollision,VIRTUAL_WIN_WIDTH,VIRTUAL_WIN_HEIGHT))
    for i in range(0, len(dangerOrbs)):
        if circleCollision(blob, dangerOrbs[i]):
            if blob["points"] > DANGER_ORB_DMG_THRESHOLD:
                dangerCircleCollisionResolve(blob,dangerOrbs[i])


def updateSpeed(blob):
    blobPoints = blob["points"]    # X value
    blobSpeed = blob["speed"]      # Y value

    #speed = 500/playerPoints               #y = 500/x
    speed = blobSpeed
    if blobSpeed > 2:
        speed = -0.01*(blobPoints) + START_SPEED

    if speed > 2:
        blob["speed"] = int(speed)

def updateFpsCounter(isint, font, clock):
    if isint == True:
        currentFps = int(clock.get_fps())
    else:
        currentFps = clock.get_fps()
    label = font.render(str(currentFps), 1, BLACK)
    return label

def calculateLossOfBlobMass(blob, currentTimeInSeconds):
    if blob["points"] > DANGER_ORB_DMG_THRESHOLD:
        if int(blob["timeLostMass"]) < int(currentTimeInSeconds):
            blob["timeLostMass"] = int(currentTimeInSeconds)
            blob["points"] = blob["points"] - int(blob["points"]*0.01)



def playerAddPoints(player, points):
    #points that player gets is based on a ratio of their point to what they've eaten
    #This means that the more youn eat, the less you gain from smaller things, making you
    #target bigger things
    pointRatio = points/player["points"]
    pointGain = points*pointRatio
    if pointGain < 1:
        pointGain = 1
    player["points"]+=int(pointGain)

def updateSize(blob):
    if blob["points"] < MAX_SIZE:
        blob["radius"] = blob["points"] / 2

def drawPlayerHUD(surface,clock,currentTimeInSeconds):
    #draw players Score
    pygame.draw.rect(surface,BLACK, pygame.Rect(10,12,110,20),2)
    label = FONT_SYS.render("Score:" + str(playerStats["points"]), 1, BLACK)

    #Get fps in int format
    fpsLabel = updateFpsCounter(True, FONT_SYS,clock)
    fpsLabel = fpsLabel

    #Draw FPS counter top-right of the screen
    surface.blit(label,(12,13))
    surface.blit(fpsLabel, (WINWIDTH - 100,10))

    #Draw Timer
    currentTimeLabel = FONT_BASIC.render("Time: " + currentTimeInSeconds, 1, BLACK)
    surface.blit(currentTimeLabel,(HALF_WINWIDTH - 50,HALF_WINWIDTH))



def draw(surface, camerax, cameray,clock, currentTimeInSeconds):

    pygame.draw.circle(surface, GREEN, (playerStats["x"] - camerax, playerStats["y"] - cameray), playerStats["radius"],0)   #PLAYER

    for orb in pointOrbs:
        pygame.draw.circle(surface, orb["colour"], (orb["x"] - camerax, orb["y"] - cameray), orb["radius"])                 #pointOrbs

    for entity in aiEntities:                                                                                               #AI Players
        pygame.draw.circle(surface,entity["colour"],(entity["x"]  - camerax,entity["y"] - cameray), entity["radius"],1)

    for i in range(0,len(dangerOrbs)):
        surface.blit(dangerOrbs[i]["img"],((dangerOrbs[i]["x"] - 64) - camerax, (dangerOrbs[i]["y"] - 64) - cameray))

    drawPlayerHUD(surface, clock ,currentTimeInSeconds)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
