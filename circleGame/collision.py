import math

def circleCollision(c1,c2):
    #distance between two points
    #d = ((x2-x1)^2 + (y2-y1)^2)^1/2
    distance = int(math.sqrt((c2["x"] - c1["x"])**2 + (c2["y"] - c1["y"])**2))
    if (int(c1["radius"] + c2["radius"])) >= distance:
        return True
    else:
        return False

def dangerCircleCollisionResolve(c1, dangerOrb):
    distanceX = c1["x"] - dangerOrb["x"]
    distanceY = c1["y"] - dangerOrb["y"]
    distance = math.sqrt(distanceX ** 2 + distanceY ** 2)

    if distance < dangerOrb["radius"]:
        print("dead")


def safeCirlceCollisionResolve(c1, orb):
    distanceX = c1["x"] - orb["x"]
    distanceY = c1["y"] - orb["y"]
    radiusSum = c1["radius"] + orb["radius"]
    distance = math.sqrt(distanceX**2 + distanceY**2)
    unitX = distanceX / distance
    unitY = distanceY / distance
    c1["x"] = orb["x"] + (radiusSum + 1) * unitX
    c1["y"] = orb["y"] + (radiusSum + 1) * unitY
