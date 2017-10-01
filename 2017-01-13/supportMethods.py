from pyplasm import *
from scipy import *
from numpy import *

# Funzione che ritorna i vertici di un lato del tetto
def getPlanOfRoof(v1, v2, angle, length, direction):
    d12 = sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
    d23 = abs(v2[1] - v1[1])
    angle2 = PI / 2 - math.asin(d23 / d12)
    d24 = length * math.cos(angle)
    heightOfPlan = sqrt(length ** 2 - d24 ** 2)
    d25 = d24 * math.cos(angle2)
    d45 = sqrt(d24 ** 2 - d25 ** 2)
    if direction == "sx-su":
        v3 = [v2[0] + d25, v2[1] + d45, heightOfPlan]
        v4 = [v1[0] + d25, v1[1] + d45, heightOfPlan]
    elif direction == "sx-giu" or direction == "sx":
        v3 = [v2[0] - d25, v2[1] + d45, heightOfPlan]
        v4 = [v1[0] - d25, v1[1] + d45, heightOfPlan]
    elif direction == "dx-giu" or direction == "giu" or direction == "dx":
        v3 = [v2[0] - d25, v2[1] - d45, heightOfPlan]
        v4 = [v1[0] - d25, v1[1] - d45, heightOfPlan]
    elif direction == "dx-su" or direction == "su":
        v3 = [v2[0] + d25, v2[1] - d45, heightOfPlan]
        v4 = [v1[0] + d25, v1[1] - d45, heightOfPlan]
    vertexes = [v1, v2, v3, v4]
    return vertexes


# Funzione che, dati due vertici, restituisce la direzione verso cui va la retta che li unisce
def getDir(v1, v2):
    if v2[0] > v1[0]:
        if v2[1] > v1[1]:
            return "dx-su"
        elif v2[1] == v1[1]:
            return "dx"
        else:
            return "dx-giu"
    elif v2[0] == v1[0]:
        if v2[1] > v1[1]:
            return "su"
        else:
            return "giu"
    else:
        if v2[1] > v1[1]:
            return "sx-su"
        elif v2[1] == v1[1]:
            return "sx"
        else:
            return "sx-giu"

# Funzione che, dato un array di vertixi, restituisce un array di direzioni
def getDirections(vertexs):
    directions = []
    for i in range(0, len(vertexs) - 1):
        directions.append(getDir(vertexs[i], vertexs[i + 1]))
    directions.append(getDir(vertexs[len(vertexs) - 1], vertexs[0]))
    return directions

# Funzione che restituisce la lista dei piani che compongono il tetto
def getListOfPlan(vertexes, directions, angle, length):
    listOfPlan = []  # lista delle falde
    for i in range(len(directions) - 1):
        listOfPlan.append(getPlanOfRoof(vertexes[i], vertexes[i + 1], angle, length, directions[i]))
    listOfPlan.append(
        getPlanOfRoof(vertexes[len(directions) - 1], vertexes[0], angle, length, directions[len(directions) - 1]))
    return listOfPlan

# Funzione che restituisce una lista di linee [x,y] data una lista di piani
def getLines(listOfPlan):
    lines = []
    for i in range(len(listOfPlan)):
        lines.append(getLine(listOfPlan[i][2], listOfPlan[i][3]))
    return lines

# Funzione che, data una lista di linee, restituisce una lista di intersezioni tra esse
def getIntersections(lines):
    intersections = []
    for i in range(len(lines) - 1):
        intersections.append(linesIntersection(lines[i], lines[i + 1]))
    intersections.append(linesIntersection(lines[len(lines) - 1], lines[0]))
    return intersections

# Funzione che disegna i piani che compongono il tetto e li restituisce in una lista
def createListOfPlan(directions, intersections, listOfPlan):
    drawListOfPlan = []
    for i in range(len(directions)):
        if i == 0:
            app = [[listOfPlan[i][0][0], listOfPlan[i][0][1], 0], [listOfPlan[i][1][0], listOfPlan[i][1][1], 0],
                   [intersections[i][0], intersections[i][1], listOfPlan[1][2][2]],
                   [intersections[len(directions) - 1][0], intersections[len(directions) - 1][1], listOfPlan[0][2][2]]]
        else:
            app = [[listOfPlan[i][0][0], listOfPlan[i][0][1], 0], [listOfPlan[i][1][0], listOfPlan[i][1][1], 0],
                   [intersections[i][0], intersections[i][1], listOfPlan[1][2][2]],
                   [intersections[i - 1][0], intersections[i - 1][1], listOfPlan[0][2][2]]]
        f = MKPOL([app, [[4, 3, 2, 1]], None])
        drawListOfPlan.append(f)
    return drawListOfPlan

# Funzione che restituisce i vertici superiori del tetto, che compongono il terrazzo
def getVertexsOfTerrace(intersections):
    vertexsOfTerrace = [[] for _ in range(len(intersections) + 1)]
    for i in range(len(intersections)):
        vertexsOfTerrace[i].append(intersections[i][0])
        vertexsOfTerrace[i].append(intersections[i][1])
        if i == len(intersections) - 1:
            vertexsOfTerrace[i + 1].append(intersections[0][0])
            vertexsOfTerrace[i + 1].append(intersections[0][1])
    return vertexsOfTerrace

# Funzione che ruota, dato un oggetto e una direzione, ruota questo secondo la direzione desiderata
# if(dir==1) --> ruota a destra di 90 gradi
# if(dir==2) --> ruota a destra di 180 gradi
# if(dir==3) --> ruota a destra di 270 gradi
# if(dir==4) --> ruota a destra di 360 gradi
def rotation(HPCObject, dir):
    if (dir > 0 and dir < 4):
        c = CUBOID([0.1, 0.1, 0.1])
        sizeObj = SIZE([1, 2])(HPCObject)
        box = STRUCT([c, HPCObject])
        box = BOX([1, 2, 3])(box)
        distance = SIZE([1, 2, 3])(box)
        position = [distance[0] - sizeObj[0], distance[1] - sizeObj[1]]
        elem = STRUCT([T([1, 2])([-position[0], -position[1]]), HPCObject])
        if dir == 1:
            elem = STRUCT([R([1, 2])(PI / 2), elem])
            elem = STRUCT([T([1])(sizeObj[1]), elem])
            elem = STRUCT([T([1, 2])([position[0], position[1]]), elem])
        if dir == 2:
            elem = STRUCT([R([1, 2])(PI), elem])
            elem = STRUCT([T([1, 2])([sizeObj[0], sizeObj[1]]), elem])
            elem = STRUCT([T([1, 2])([position[0], position[1]]), elem])
        if dir == 3:
            elem = STRUCT([R([1, 2])(PI * 3 / 2), elem])
            elem = STRUCT([T([2])(sizeObj[0]), elem])
            elem = STRUCT([T([1, 2])([position[0], position[1]]), elem])
        if dir == 4:
            elem = STRUCT([R([1, 2])(PI * 2), elem])
        return elem
    return HPCObject

# Funzione che, dati due punti, ritorna una retta
def getLine(v1, v2):
    if v1[0] == v2[0]:
        line = [1, 0, v1[0]]
    elif v1[1] == v2[1]:
        line = [0, 1, v1[1]]
    else:
        m = (float(v2[1]) - float(v1[1])) / (float(v2[0]) - float(v1[0]))
        q = float(v1[1]) - m * float(v1[0])
        line = [-m, 1, q]
    return line

# Funzione che, dato file *.lines, calcola e restituisce i suoi vertici
def getVertexes(pathFileLines):
    with open(pathFileLines, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        vertexes = []
        for row in reader:
            vertexes.append([float(row[0]), float(row[1])])
            vertexes.append([float(row[2]), float(row[3])])
        vertexes2 = []
        for i in range(len(vertexes)):
            if i % 2 == 0:
                vertexes2.append(vertexes[i])
            if i == len(vertexes) - 3:
                vertexes2.append(vertexes[i])
    copy = vertexes2[len(vertexes2) - 2]
    return vertexes2

# Funzione che, dato un hpc, restituisce la posizione e la dimensione dell'oggetto nello spazio x,y,z
def getDimensionAndPosition(HPCObject):
    sizeObj = SIZE([1, 2, 3])(HPCObject)
    c = CUBOID([1, 1, 1])
    box = STRUCT([c, HPCObject])
    box = BOX([1, 2, 3])(box)
    distance = SIZE([1, 2, 3])(box)
    position = [(distance[0] - sizeObj[0]) * .03, (distance[1] - sizeObj[1]) * .03, (distance[2] - sizeObj[2]) * .03]
    dimAndPos = [sizeObj, position]
    return dimAndPos

# Funzione che restituisce il punto di intersezione di due rette
def linesIntersection(line1, line2):
    A = matrix([[line1[0], line1[1]], [line2[0], line2[1]]])
    b = array([line1[2], line2[2]])
    point = linalg.solve(A, b)
    return point

# Funzione che ridimensiona un oggetto hpc alle dimensioni x,y,z specificate
def resizeDim(HPCObject, x, y, z):
    dim = getDimensionAndPosition(HPCObject)[0]
    sX = x / dim[0]
    sY = y / dim[1]
    sZ = z / dim[2]
    resizeObj = STRUCT([S([1, 2, 3])([sX, sY, sZ]), HPCObject])
    return resizeObj