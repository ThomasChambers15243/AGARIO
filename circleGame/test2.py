import math

def safeCirlceCollisionResolve(c1, orb):
    distanceX = c1["x"] - orb["x"]
    distanceY = c1["y"] - orb["y"]
    radiusSum = c1["radius"] + orb["radius"]
    distance = math.sqrt(distanceX**2 + distanceY**2)
    unitX = distanceX / distance
    unitY = distanceY / distance
    c1["x"] = orb["x"] + (radiusSum + 1) * unitX
    c1["y"] = orb["y"] + (radiusSum + 1) * unitY
    c1["testVar"] = "changeds"


circle1 = {
    "x" : 100,
    "y" : 100,
    "radius" : 2,
    "testVar" : "t"
}

circle2 = {
    "x" : 200,
    "y" : 200,
    "radius" : 2
}
print(circle1)
safeCirlceCollisionResolve(circle1,circle2)
print(circle1)
