
entityStatNums = {
    "player" : 0,
    "AI" : 0,
    "pointOrb" : 1,
    "dangerOrb" : 2
}

playerStats = {
    "name" : "player",
    "points" : 30,
    "colour" : "GREEN",
    "kills" : 0,
    "direction" : "N",
    "radius" : 15,
    "speed" : 7,
    "timeLostMass" : 0,
    "x" : 0,
    "y" : 0
}

entityStats = [
    {
        "name" : "AI",          #AI
        "points" : 30,
        "colour" : "GREEN",
        "radius" : 15,
        "speed" : 7,
        "timeLostMass": 0,
        "state" : "feed",
        "direction": "N",
        "isMoving" : False,
        "x" : 0,
        "y" : 0,
        "targetX" : 0,
        "targetY" : 0
    },
    {                           #point orbs
        "name" : "pointOrb",
        "points" : 10,
        "colour" : "GREEN",
        "radius" : 10,
        "x" : 0,
        "y" : 0,
    },                          #danger Orb
    {
        "name" : "dangerOrb",
        "img" : "dangerOrb",
        "radius" : 64,
        "x" : 0,
        "y" : 0
    }

]
