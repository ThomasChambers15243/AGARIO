import copy, random
from data import *

def createOrbs(orbAmount, orbArray,c1,orbType,ORBCOLOURS, circleCollision,xBoundry,yBoundry):
    for i in range(0, (orbAmount - len(orbArray))):
        orbArray.append(spawnOrb(c1,orbType,ORBCOLOURS, circleCollision,xBoundry,yBoundry))

def spawnOrb(c1,orbType,ORBCOLOURS, circleCollision,xBoundry,yBoundry):
    orb = copy.deepcopy(entityStats[orbType])

    randX = random.randint(-xBoundry + orb["radius"],xBoundry - orb["radius"])
    randY = random.randint(-yBoundry + orb["radius"], yBoundry - orb["radius"])
    orb["colour"] = ORBCOLOURS[random.randint(0,len(ORBCOLOURS)-1)]
    orb["x"] = randX
    orb["y"] = randY
    #while circleCollision(c1, orb) == True:
     #   orb = spawnOrb(c1,orbType,ORBCOLOURS, circleCollision,xBoundry,yBoundry) # recursively call spawnOrb unit not colliding with player
    return orb

def createAIEntities(AIAmount, aiArray, c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry):
    for i in range(0, (AIAmount - len(aiArray))):
        aiArray.append(spawnEntitiesAI(c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry))

def spawnEntitiesAI(c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry):
    ai = copy.deepcopy(entityStats[0])
    randX = random.randint(-xBoundry + ai["radius"],xBoundry - ai["radius"])#c1["x"] + 200#r
    randY = random.randint(-yBoundry + ai["radius"], yBoundry - ai["radius"])#c1["y"]
    ai["x"] = randX
    ai["y"] = randY
    ai["colour"] = ORBCOLOURS[random.randint(0,len(ORBCOLOURS)-1)]

   # for i in range(0, len(c3)):
    #    while circleCollision(ai,c2[i]) or circleCollision(ai, c1):
    #        print("cs collsion")
    #        ai = spawnEntitiesAI(c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry)
    # for j in range(0,len(c3)):
    #     while circleCollision(ai,c3[j]) == True:
    #         ai = spawnEntitiesAI(c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry)
    # while circleCollision(ai, c1) == True:
    #     ai = spawnEntitiesAI(c1,c2,c3,entityType, ORBCOLOURS, circleCollision,xBoundry,yBoundry)
    return ai


