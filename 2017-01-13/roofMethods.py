from pyplasm import *
from supportMethods import *

# Definizione delle texture
TILES_TXT = "./textures/tiles_txt.jpg"
TERRACE_TXT = "./textures/terrace_txt.jpg"

# Funzione per la costruzione del tetto
def myRoofTerrace(house,angle,length):
    dimAndPos=getDimensionAndPosition(house)
    vertexs=[]
    vertexs.append([dimAndPos[1][0]*.03,dimAndPos[1][1]*.02])
    vertexs.append([dimAndPos[1][0]*.03,+dimAndPos[0][1]-dimAndPos[1][1]*.4])
    vertexs.append([dimAndPos[0][0]+dimAndPos[1][0]/4,dimAndPos[0][1]-dimAndPos[1][1]*.4])
    vertexs.append([dimAndPos[0][0]+dimAndPos[1][0]/4,dimAndPos[1][1]*.02])
    roof=createRoof(vertexs,angle,length)
    return roof


def createRoof(vertexes,angle,length):
    directions = getDirections(vertexes)
    listOfPlan = getListOfPlan(vertexes, directions, angle, length)
    lines = getLines(listOfPlan)
    intersections = getIntersections(lines)
    drawListOfPlan = createListOfPlan(directions, intersections, listOfPlan)
    vertexsOfTerrace = getVertexsOfTerrace(intersections)
    subroof = POLYLINE(vertexes)
    subroof = SOLIDIFY(subroof)
    subroof = COLOR([1,1,1,1])(subroof)
    terrace = POLYLINE(vertexsOfTerrace)
    terrace = SOLIDIFY(terrace)
    terrace = T(3)(listOfPlan[0][2][2])(terrace)
    terrace = TEXTURE([TERRACE_TXT, TRUE, FALSE, 1, 1, 0, 15, 15])(terrace)
    roof = STRUCT(drawListOfPlan)
    roof=TEXTURE([TILES_TXT, TRUE, FALSE, 1, 1, 0, 15, 15])(roof)
    return STRUCT([terrace,roof,subroof])