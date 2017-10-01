from pyplasm import *

# Definizione dele texture
ROOF_TXT = "./textures/roof.jpg"
FLOOR_TXT = "./textures/floor.jpg"

par = 0.2

# Definizione delle coordinate
x = [1.0, 3.0, 9.0, 10.0, 12.0, 14.0, 16.0, 22.0, 24.0, 11.0]
y = [2.0, 3.0, 4.0, 6.0, 7.0, 9.0, 10.0, 12.0, 13.0, 16.0, 14.0]
z = [0.0, 2.0]

vertsStruct = [
  [x[0],y[1],z[0]],
  [x[0],y[7],z[0]],
  [x[2],y[7],z[0]],
  [x[2],y[9],z[0]],
  [x[8],y[9],z[0]],
  [x[8],y[0],z[0]],
  [x[5],y[0],z[0]],
  [x[5],y[4],z[0]],
  [x[1],y[3],z[1]],
  [x[1],y[6],z[1]],
  [x[9],y[6],z[1]],
  [x[9],y[10],z[1]],
  [x[7],y[10],z[1]],
  [x[7],y[2],z[1]],
  [x[6],y[2],z[1]],
  [x[6],y[6],z[1]],
]

cellsStruct = [
  [1,2,10,9],
  [2,3,11,10],
  [3,4,12,11],
  [4,5,13,12],
  [5,6,14,13],
  [6,7,15,14],
  [7,8,16,15],
  [8,9,1 ,16]
]

cellsStructBorder = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,1]]

# Definizione delle celle e delle coordinate del tetto
roof = MKPOL([vertsStruct, cellsStruct,[1]])
roof = TEXTURE([ROOF_TXT, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([par, par, par])(SKEL_2(roof)))

# Definizione della pavimentazione del tetto
floor = MKPOL([vertsStruct, [[9,10,16],[13,14,15,16],[11,12,13,16]],[1]])
floor = TEXTURE([FLOOR_TXT, TRUE, FALSE, 1, 1, 0, 6, 6])(OFFSET([par, par, par])(SKEL_2(floor)))

completeRoof = STRUCT([roof, floor])

VIEW(completeRoof)