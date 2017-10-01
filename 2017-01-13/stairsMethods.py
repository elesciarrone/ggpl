from pyplasm import *
from larlib import *

# Funzione per la costruzione delle scale
def ggpl_building_stairs(dx, dy, dz):

    # Definizione delle caratteristiche della scala
    platformX = 1
    platformY = dy
    idealTread = .29
    idealRiser = .17
    treadWidth = DIV([dy, 2])
    halfDz = DIV([dz, 2])
    treadTot = dx - platformX
    steps = modf(treadTot / idealTread)[1]
    tread = DIV([treadTot, steps])
    riser = DIV([halfDz, steps + .5])

    stairs = []
    diagonal = []
    vertex = [[tread, 0, 0], [tread, 0, riser], [2 * tread, 0, riser], [tread, treadWidth, 0],
              [tread, treadWidth, riser], [2 * tread, treadWidth, riser]]
    cells = [1, 2, 3, 4, 5, 6]
    diagonal.append(MKPOL([vertex, [cells], None]))

    for x in range(0, int(steps)):
        stairs.append(CUBOID([tread, treadWidth, riser]))
        stairs.append(T([1, 2, 3])([tread, 0, riser]))
        diagonal.append(MKPOL([vertex, [cells], None]))
        diagonal.append(T([1, 2, 3])([tread, 0, riser]))
    stairs.append(CUBOID([platformX, platformY, riser]))
    stairs.append(R([1, 2])(PI))
    stairs.append(
        T([1, 2, 3])([0, -2 * treadWidth, riser]))
    diagonal.append(R([1, 2])(PI))
    diagonal.append(
        T([1, 2, 3])([0, -2 * treadWidth, riser]))

    for x in range(0, int(steps)):
        stairs.append(CUBOID([tread, treadWidth, riser]))
        stairs.append(T([1, 2, 3])([tread, 0, riser]))
        if (x < (steps - 1)):
            diagonal.append(MKPOL([vertex, [cells], None]))
            diagonal.append(T([1, 2, 3])([tread, 0, riser]))
    stairs.append(R([1, 2])(PI))

    return STRUCT([STRUCT(diagonal), STRUCT(stairs)])