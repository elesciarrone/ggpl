from pyplasm import *

# Definizione delle coordinate della porta
XD = [.10, .40, .10]
YD = [.05]
ZD = [.10, .40, .10, .90, .10, .40, .10]
occupancyD = [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]]


# Funzione per la costruzione della porta
def createDoor(coordinateD, occupancyD):
    def param(dx, dy, dz):
        x = coordinateD[0]
        y = coordinateD[1]
        z = coordinateD[2]
        lunghezzaX = 0
        altezzaZ = 0
        dCorner = [y[0] * .5]
        dGlass = y[0] * .5
        for i in x:
            lunghezzaX = lunghezzaX + i
        for i in z:
            altezzaZ = altezzaZ + i
        if dx < (lunghezzaX * 2.):
            percent = dx / (lunghezzaX * 2.)
            for i in range(0, len(x)):
                x[i] = x[i] * percent
            lunghezzaX = lunghezzaX * percent
        if dy < y[0]:
            print y
            percent = dy / (y[0] * 1.)
            y[0] = y[0] * percent
        if dz < altezzaZ:
            print z
            percent = dx / (altezzaZ * 1.)
            for i in range(0, len(z)):
                z[i] = z[i] * percent
            altezzaZ = altezzaZ * percent
        door = []
        for i in range(0, 2):
            for iz in range(0, len(z)):
                vect = occupancyD[iz]
                cont = 0
                for ix in vect:
                    if ix == 1:
                        prodXY = PROD([QUOTE([x[cont]]), QUOTE(y)])
                        prod = PROD([prodXY, QUOTE([z[iz]])])
                        door.append(COLOR(BROWN))
                        door.append(prod)
                    if ix == 0:
                        # cornice
                        prodXY = PROD([QUOTE([x[cont] - .01]), QUOTE(dCorner)])
                        prod = PROD([prodXY, QUOTE([z[iz] - .01])])
                        door.append(T([1, 2, 3])([0, y[0] / 2. - dCorner[0] / 2 - .005, 0]))
                        door.append(COLOR(BROWN))
                        door.append(OFFSET([.01, .01, .01])(SKEL_1(prod)))
                        door.append(T([1, 2, 3])([0, -(y[0] / 2. - dCorner[0] / 2 - .005), 0]))
                        # vetro
                        prodXY = PROD([QUOTE([x[cont]]), QUOTE([dGlass])])
                        prod = PROD([prodXY, QUOTE([z[iz]])])
                        door.append(T([1, 2, 3])([0, y[0] / 2. - dGlass / 2, 0]))
                        door.append(COLOR([150. / 255., 225. / 255., 1, 1]))
                        door.append(prod)
                        door.append(T([1, 2, 3])([0, -(y[0] / 2. - dGlass / 2), 0]))
                    door.append(T([1, 2, 3])([x[cont], 0, 0]))
                    cont = cont + 1
                door.append(T([1, 2, 3])(
                    [-lunghezzaX, 0, z[iz]]))
            door.append(T([1, 2, 3])(
                [lunghezzaX + .005, 0, -altezzaZ]))
        maniglia = CUBOID([-.02, .02, .15])
        door.append(
            T([1, 2, 3])([-lunghezzaX - .005 - .005 - .03, y[0], altezzaZ * .5]))
        door.append(COLOR([1, 191. / 255., 0, 1]))
        door.append(maniglia)
        door.append(T([1, 2, 3])([.03 + .05 + .005, 0, 0]))
        door.append(maniglia)
        maniglia = CUBOID([-.02, .02, .15])

        door.append(T(2)(-2 * y[0]))
        door.append(COLOR([1, 191. / 255., 0, 1]))
        door.append(maniglia)
        door.append(T([1, 2, 3])([-(.03 + .05 + .005), 0, 0]))
        door.append(maniglia)

        return STRUCT(door)

    return param