import copy
import random, sys, time, math, pygame, math
from data import *
from pygame.locals import *

FPS = 144  # frames per second to update the screen
WINWIDTH = 1920  # width of the program's window, in pixels
WINHEIGHT =1080  # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)


VIRTUAL_WIN_HEIGHT = 2500
VIRTUAL_WIN_WIDTH = 2500

CAMERASLACK = 0




LEFT = "left"
RIGHT = "right"
DOWN = "down"
UP = "up"

MOVMENT_KEYS = [K_d, K_RIGHT, K_a, K_LEFT, K_s, K_DOWN, K_w, K_UP]


#MAIN CONSTS#
START_SPEED = 10
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
DANGER_ORB_AMOUNT = 30
dangerOrbs = []
#Danger Orb img image load
dangerOrbImgs = []
for i in range(1,3):
    dangerOrbImgs.append(pygame.image.load("imgs/" + entityStats[2]["img"] + str(i) + ".png"))

currentTime = 0



#    Fuchsia (255, 0, 255)
#   Gray (128, 128, 128)
#    Green ( 0, 128, 0)
#    Lime ( 0, 255, 0)
#    Maroon (128, 0, 0)
#    Navy Blue ( 0, 0, 128)
#    Olive (128, 128, 0)

#    Silver (192, 192, 192)
#    Teal ( 0, 128, 128)
#    White (255, 255, 255)
#    Yellow (255, 255, 0)




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
        createOrbs(ORBAMOUNT)
    if len(dangerOrbs) < DANGER_ORB_AMOUNT:
        createDangerOrbs()
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



    if playerStats["points"] <= MAX_SIZE_FOR_ORB_GAIN:
        for i in range(0,len(pointOrbs)):
            if circleCollision(playerStats,pointOrbs[i]):
                playerAddPoints(playerStats, pointOrbs[i]["points"])
                pointOrbs.pop(i)
                pointOrbs.append(spawnOrb())
    for i in range(0, len(dangerOrbs)):
        if circleCollision(playerStats, dangerOrbs[i]):
            if playerStats["points"] > DANGER_ORB_DMG_THRESHOLD:
                print("DEAD")

    calculateLossOfPlayerMass(currentTimeInSeconds)
    setPlayerSize()
    updatePlayerSpeed()
    draw(surface, camerax, cameray)
    drawPlayerHUD(surface,clock,currentTimeInSeconds)
    pygame.display.update()
    clock.tick(FPS)


def updateFpsCounter(isint, font, clock):
    if isint == True:
        currentFps = int(clock.get_fps())
    else:
        currentFps = clock.get_fps()
    label = font.render(str(currentFps), 1, BLACK)
    return label



def SsetMovement(surface,camerax,cameray):
    mousePos = pygame.mouse.get_pos() #mousePos[0] = x mousePos[1] = y
    #print(mousePos[0] + mousePos[1])
    #distance between two points
    #d = ((x2-x1)^2 + (y2-y1)^2)^1/2

    distance = int(math.sqrt((mousePos[0] - playerStats["x"])**2 + (mousePos[1] - playerStats["y"])**2))
    #playerVector = pygame.math.Vector2(playerStats["x"], playerStats["y"])
    #vel = pygame.math.Vector2(mousePos[0],mousePos[1])
    #vel = vel - playerVector
    #vel.scale_to_length(2)
    #playerVector += vel
    #playerStats["x"] = playerVector.x
    #playerStats["y"] = playerVector.y
    if distance > 0:


        r = playerStats["speed"]/distance
        xt = r * mousePos[0] + (1 - r) * playerStats["x"] - camerax
        yt = r * mousePos[1] + (1 - r) * playerStats["y"] - cameray

        pygame.draw.line(surface,BLACK,(playerStats["x"] - camerax,playerStats["y"] - cameray),(xt ,yt ),5)
        playerStats["x"] = xt
        playerStats["y"] = yt
        #pygame.draw.line()
        print("player x and y is: " + str(playerStats["x"]) + "   " + str(playerStats["y"]))
        print("mouse x and y is: " + str(mousePos[0]) + "   " + str(mousePos[0]))












def setMovement():
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[K_a]) and playerStats["x"] > -VIRTUAL_WIN_WIDTH + playerStats["radius"]:
        playerStats["x"] -= playerStats["speed"]
    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[K_d]) and playerStats["x"] < VIRTUAL_WIN_WIDTH - playerStats["radius"]:
        playerStats["x"] += playerStats["speed"]
    if (keys_pressed[pygame.K_UP] or keys_pressed[K_w]) and playerStats["y"] > -VIRTUAL_WIN_HEIGHT + playerStats["radius"]:
        playerStats["y"] -= playerStats["speed"]
    if (keys_pressed[pygame.K_DOWN] or keys_pressed[K_s]) and playerStats["y"] < VIRTUAL_WIN_HEIGHT - playerStats["radius"]:
        playerStats["y"] += playerStats["speed"]


def updatePlayerSpeed():
    playerPoints = playerStats["points"]    # X value
    playerSpeed = playerStats["speed"]      # Y value

    #speed = 500/playerPoints               #y = 500/x
    speed = playerSpeed
    if playerSpeed > 2:
        speed = -0.01*(playerPoints) + START_SPEED

    if speed > 2:
        playerStats["speed"] = int(speed)




def calculateLossOfPlayerMass(currentTimeInSeconds):
    if playerStats["points"] > DANGER_ORB_DMG_THRESHOLD:
        if int(playerStats["timeLostMass"]) < int(currentTimeInSeconds):
            playerStats["timeLostMass"] = int(currentTimeInSeconds)
            #playerStats["points"] = playerStats["points"] - int(playerStats["points"]*0.01)
            print(playerStats["timeLostMass"])



def playerAddPoints(player, points):
    #points that player gets is based on a ratio of their point to what they've eaten
    #This means that the more youn eat, the less you gain from smaller things, making you
    #target bigger things
    pointRatio = points/player["points"]
    pointGain = points*pointRatio
    if pointGain < 1:
        pointGain = 1
    player["points"]+=int(pointGain)







def circleCollision(player,orb):
    #distance between two points
    #d = ((x2-x1)^2 + (y2-y1)^2)^1/2
    distance = int(math.sqrt((orb["x"] - player["x"])**2 + (orb["y"] - player["y"])**2))
    if (int(player["radius"] + orb["radius"])) >= distance:
        return True
    else:
        return False

def safeCirlceCollisionResolve(player, orb):
    distanceX = player["x"] - orb["x"]
    distanceY = player["y"] - orb["y"]
    radiusSum = player["radius"] + orb["radius"]
    distance = math.sqrt(distanceX**2 + distanceY**2)
    unitX = distanceX / distance
    unitY = distanceY / distance
    player["x"] = orb["x"] + (radiusSum + 1) * unitX
    player["y"] = orb["y"] + (radiusSum + 1) * unitY




def createOrbs(ORBAMOUNT):
    for i in range(0, (ORBAMOUNT - len(pointOrbs))):
        pointOrbs.append(spawnOrb())

def spawnOrb():
    orb = copy.deepcopy(entityStats[1])
    randX = random.randint(-VIRTUAL_WIN_WIDTH + orb["radius"],VIRTUAL_WIN_WIDTH - orb["radius"])
    randY = random.randint(-VIRTUAL_WIN_HEIGHT + orb["radius"], VIRTUAL_WIN_HEIGHT - orb["radius"])
    orb["colour"] = ORBCOLOURS[random.randint(0,len(ORBCOLOURS)-1)]
    orb["x"] = randX
    orb["y"] = randY

    while circleCollision(playerStats, orb) == True:
        orb = spawnOrb() # recursively call spawnOrb unit not colliding with player
    return orb

def createDangerOrbs():
    for i in range(0, (DANGER_ORB_AMOUNT - len(dangerOrbs))):
        dangerOrbs.append(spawnDangerOrb())

def spawnDangerOrb():
    dangerOrb = copy.deepcopy(entityStats[2])
    randX = random.randint(-VIRTUAL_WIN_WIDTH + dangerOrb["radius"],VIRTUAL_WIN_WIDTH - dangerOrb["radius"])
    randY = random.randint(-VIRTUAL_WIN_HEIGHT + dangerOrb["radius"], VIRTUAL_WIN_HEIGHT - dangerOrb["radius"])
    dangerOrb["img"] = dangerOrbImgs[random.randint(0,1)]
    dangerOrb["x"] = randX
    dangerOrb["y"] = randY

    while circleCollision(playerStats, dangerOrb) == True:
        dangerOrb = spawnDangerOrb()
    return dangerOrb





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

def setPlayerSize():
    if playerStats["points"] < MAX_SIZE:
        playerStats["radius"] = playerStats["points"] / 2

def drawPlayer(surface, camerax, cameray):
    pygame.draw.circle(surface, GREEN, ((playerStats["x"] - playerStats["radius"]) - camerax, (playerStats["y"] - playerStats["radius"]) - cameray), playerStats["radius"],
                       2)
def draw(surface, camerax, cameray):
    for orb in pointOrbs:
        pygame.draw.circle(surface, orb["colour"], (orb["x"] - camerax, orb["y"] - cameray), orb["radius"])                 #pointOrbs
    #pygame.draw.rect(surface, GREEN, pygame.Rect(HALF_WINWIDTH - camerax, HALF_WINHEIGHT - cameray, 60, 60))                #RECTANGLE

    #pygame.draw.circle(surface, BLACK, (HALF_WINWIDTH - 5, HALF_WINHEIGHT - 5), 10, 0)
    #pygame.draw.circle(surface,BLACK,(playerStats["x"]-camerax,playerStats["y"]-cameray),10,0)
    pygame.draw.circle(surface, GREEN, (playerStats["x"] - camerax, playerStats["y"] - cameray), playerStats["radius"],2)   #PLAYER


    for i in range(0,len(dangerOrbs)):
        surface.blit(dangerOrbs[i]["img"],((dangerOrbs[i]["x"] - 64) - camerax, (dangerOrbs[i]["y"] - 64) - cameray))



def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
