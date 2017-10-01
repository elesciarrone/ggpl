from pyplasm import *
from supportMethods import *
from doorMethods import *
from windowMethods import *
from stairsMethods import *
from roofMethods import *

import csv

# Definizione delle textures
MURI_TXT = "./textures/muri.jpg"
INTERNI_TXT = "./textures/interni.jpg"
PAVIMENTO_TXT = "./textures/parquet.jpg"
PAVIMENTO_BAGNO_TXT = "./textures/pavimentoBagno.jpg"
PAVIMENTO_GARAGE_TXT = "./textures/pavimentoGarage.jpg"
SCALE_TXT = "./textures/scale.jpg"
GARAGE_TXT = "./textures/serranda.jpg"

# Funzione che dati un file .lines e un tipo di elemento, restiruisce una lista di elementi con dimensione e posizione noti dal file
def building_element(filename, elementType):
    with open(filename, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        elementsList = []
        if elementType=="porte" or elementType=="finestre" or elementType=="pavimento" or elementType=="scale" or elementType=="serrande":
            cuboid = []
            acc = 0
            for row in reader:
                acc = acc + 1
                cuboid.append([float(row[1]),float(row[0])])
                if(acc == 4):
                    elementsList.append(MKPOL([cuboid,[[1,2,3,4]],None]))
                    cuboid = []
                    acc = 0
        if elementType=="perimetro" or elementType=="interni":
            for row in reader:
                elementsList.append(POLYLINE([[float(row[1]), float(row[0])],[float(row[3]), float(row[2])]]))
    elements = STRUCT(elementsList)
    if elementType=="perimetro":
        elements = OFFSET([6,6])(elements)
        elements = PROD([elements, Q(100)])
    elif elementType=="interni":
        elements = OFFSET([3,3])(elements)
        elements = PROD([elements, Q(99.9)])
    elif elementType=="porte":
        elements = PROD([elements, Q(70)])
    elif elementType=="serrande":
        elements = PROD([elements, Q(70)])
        dimAndPos = getDimensionAndPosition(elements)
        elements = T([1,2,3])([dimAndPos[1][0]*.03*2,dimAndPos[1][1]*.03*2,dimAndPos[1][2]*.03*2])(elements)
    elif elementType=="finestre":
        elements = OFFSET([3,3])(elements)
        elements = PROD([elements, Q(50)])
        elements = T(3)(25)(elements)
    elif elementType=="scale":
        elements = PROD([elements, Q(100)])
        dimAndPos = getDimensionAndPosition(elements)
        app = ggpl_building_stairs(6,3,6)
        app = resizeDim(app,dimAndPos[0][0],dimAndPos[0][1],dimAndPos[0][2])
        app = T([1,2,3])([dimAndPos[1][0]*(1/.03),dimAndPos[1][1]*(1/.03),dimAndPos[1][2]*(1/.03)])(app)
        elements = app
    return elements

# Funzione per la creazione di un intero piano di una casa
def drawPlans(npiano, walls, entries, floors, scale):
    perimetro = walls[0]
    interni = walls[1]
    porte = entries[0]
    serrande = entries[1]
    finestre = entries[2]
    pavimentoP = floors[0]
    pavimentoB = floors[1]
    pavimentoG = floors[2]
    externalWall = building_element(perimetro, "perimetro")
    internalWall = building_element(interni, "interni")
    doorBox = building_element(porte, "porte")
    if serrande!=None:
        garageBox = building_element(serrande, "porte")
    windowsBox = building_element(finestre, "finestre")
    wallsENoDoorEWindow=DIFFERENCE([externalWall,STRUCT([doorBox,windowsBox])])
    if serrande!=None:
        wallsENoDoorEWindow=DIFFERENCE([wallsENoDoorEWindow, garageBox])
    wallsENoDoorEWindow = TEXTURE([MURI_TXT,TRUE,FALSE,1,1,0,150,150])(wallsENoDoorEWindow)
    wallsINoDoor=DIFFERENCE([internalWall,doorBox])
    wallsINoDoor = TEXTURE([INTERNI_TXT,TRUE,FALSE,1,1,0,15,20])(wallsINoDoor)
    walls = STRUCT([wallsENoDoorEWindow,wallsINoDoor])
    floorP = building_element(pavimentoP,"pavimento")
    floorP = TEXTURE([PAVIMENTO_TXT,TRUE,FALSE,1,1,0,15,20])(floorP)
    floorB = building_element(pavimentoB,"pavimento")
    floorB = TEXTURE([PAVIMENTO_BAGNO_TXT,TRUE,FALSE,1,1,0,15,20])(floorB)
    if pavimentoG!=None:
        floorG = building_element(pavimentoG,"pavimento")
        floorG = TEXTURE([PAVIMENTO_GARAGE_TXT,TRUE,FALSE,1,1,0,15,20])(floorG)
        floor = STRUCT([floorP, floorG, floorB])
    else:
        floor = STRUCT([floorP, floorB])
    if scale != None:
        stairs = building_element(scale,"scale")
        stairs = TEXTURE([SCALE_TXT,TRUE,FALSE,1,1,0,1,1])(stairs)
    if npiano=="terra":
        principDoor = insertElement(porte,"porte",externalWall)
    doors = insertElement(porte,"porte",internalWall)
    windows = insertElement(finestre,"finestre",externalWall)
    if serrande!=None:
        garageDoor = building_element(serrande, "serrande")
        garageDoor = TEXTURE([GARAGE_TXT,TRUE,FALSE,1,1,0,1,1])(garageDoor)
    if scale != None and serrande!=None:
        plan = STRUCT([walls, floor, stairs, garageDoor])
    elif serrande!=None:
        plan = STRUCT([walls, floor, garageDoor])
    else:
        plan = STRUCT([walls, floor])
    plan = S([1,2,3])([.03,.03,.03])(plan)
    if npiano=="terra":
        plan = STRUCT([plan,doors,principDoor,windows])
    else:
        plan = STRUCT([plan,doors,windows])
    return plan

# Funzione che, dati un file .lines, un tipo di elemento e il muro di interesse, restituisce una lista di box per l'alloggio degli elementi
def positionElement(filename, elementType, wall):
    with open(filename, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        elementsList = []
        if elementType=="porte" or elementType=="finestre":
            cuboid = []
            acc = 0
            for row in reader:
                acc = acc + 1
                cuboid.append([float(row[1]),float(row[0])])
                if(acc == 4):
                    cub = STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
                    if elementType=="porte":
                        cub = PROD([cub,Q(70)])
                    elif elementType=="finestre":
                        cub = PROD([cub, Q(SIZE([3])(wall)[0]/2.)])
                        cub = T(3)(SIZE([3])(wall)[0]/4.)(cub)
                    elementsList.append(cub)
                    cuboid = []
                    acc = 0
    return elementsList

# Funzione che, dati in input un file .lines, un tipo di elemento e il muro di interesse, crea i suddetti elementi e li inserisce negli appositi spazi
def insertElement(fileName, elementType, wall):#fileName, elementType, wall
    dimAndPosElements = []
    if elementType=="porte" or elementType=="finestre":
        for elem in positionElement(fileName,elementType, wall):
            wall2 = DIFFERENCE([wall, elem])
            element = DIFFERENCE([wall, wall2])
            sizeElement = SIZE([1,2])(element)
            if sizeElement[0]!=0.0 and sizeElement[1]!=0.0:
                dimAndPosElements.append(getDimensionAndPosition(element))
        elements =[]
        for d in dimAndPosElements:
            if d[0][0]>d[0][1]:
                if elementType=="porte":
                    element = createDoor([XD,YD,ZD],occupancyD)(1.2,.05,2.1)
                    element = rotation(element,2)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
                elif elementType=="finestre":
                    element = createWindow([XW,YW,ZW],occupancyW)(3.6,.05,2.29)
                    element = rotation(element,2)
                    element = resizeDim(element,d[0][0]*.0315,d[0][1]*.03,d[0][2]*.03)
            else:
                if elementType=="porte":
                    element = createDoor([XD,YD,ZD],occupancyD)(1.2,.05,2.1)
                    element = rotation(element,1)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
                elif elementType=="finestre":
                    element = createWindow([XW,YW,ZW],occupancyW)(3.6,.05,2.29)
                    element = rotation(element,1)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.031,d[0][2]*.03)
            element = STRUCT([T([1,2,3])(d[1]),element])
            if elementType=="porte":
                if d[0][0]>d[0][1]:
                    element = STRUCT([T(2)(-YD[0]),element])
                else:
                    element = STRUCT([T(1)(-YD[0]),element])
            elif elementType=="finestre":
                if d[0][0]>d[0][1]:
                    element = STRUCT([T(2)(-6*YW[0]),element])
                else:
                    element = STRUCT([T(1)(-4*YW[0]),element])
            elements.append(element)
        return STRUCT(elements)

# Funzione per la costruzione della casa
def multistoreyHouse(elementsOfHouse):
    elementOfPlanT = elementsOfHouse[0]
    elementOfPlanP = elementsOfHouse[1]
    entriesT = elementsOfPlanT[0]
    floorsT = elementsOfPlanT[1]
    wallsT = elementsOfPlanT[2]
    entriesP = elementsOfPlanP[0]
    floorsP = elementsOfPlanP[1]
    wallsP = elementsOfPlanP[2]
    plan1 = drawPlans("terra",wallsT,entriesT,floorsT,"pianoTerra/scale.lines")
    plan2 = T(3)(3)(drawPlans("primo",wallsP,entriesP,floorsP, None))
    house = STRUCT([plan1,plan2])
    roofMeasure = getDimensionAndPosition(house)
    roof = T([1,2])([roofMeasure[1][0]/.03,roofMeasure[1][1]/.03])(myRoofTerrace(house,PI/5,3))
    house = STRUCT([house,T(3)(6)(roof)])
    return house

# Definizione dei parametri per la costruzione del piano terra
entriesT = ["pianoTerra/porte.lines","pianoTerra/serrande.lines","pianoTerra/finestre.lines"]
floorsT = ["pianoTerra/pavimentoP.lines","pianoTerra/pavimentoB.lines","pianoTerra/pavimentoG.lines"]
wallsT = ["pianoTerra/perimetro.lines","pianoTerra/interni.lines"]
elementsOfPlanT = [entriesT, floorsT, wallsT]

# Definizione dei parametri per la costruzione del primo piano
entriesP = ["primoPiano/porte.lines",None,"primoPiano/finestre.lines"]
floorsP = ["primoPiano/pavimentoP.lines","primoPiano/pavimentoB.lines",None]
wallsP = ["primoPiano/perimetro.lines","primoPiano/interni.lines"]
elementsOfPlanP = [entriesP, floorsP, wallsP]

elementsOfHouse = [elementsOfPlanT, elementsOfPlanP]
house = multistoreyHouse(elementsOfHouse)
VIEW(house)