from pyplasm import *
from larlib import *

# Perimetro
lines = lines2lines("./lines/perimeter.lines")
plan = STRUCT(AA(POLYLINE)(lines))
plan = OFFSET([10,10])(plan)
height = QUOTE([100])
perimeter = PROD([plan,height])

# Muri interni
lines = lines2lines("./lines/internal.lines")
plan = STRUCT(AA(POLYLINE)(lines))
plan = OFFSET([5,5])(plan)
height = QUOTE([100])
internal = PROD([plan,height])

# Porte
lines = lines2lines("./lines/doors.lines")#acquisizione dei punti dal file di interesse
plan = STRUCT(AA(POLYLINE)(lines))#costruzione 3d della struttura
plan = OFFSET([14,20])(plan)#funzione per migliorare le dimensioni x,y e la visualizzazione
height = QUOTE([90])#funzione utilizzata per alzare l'altezza della struttura
doors = PROD([plan,height])#oggetto 3d del box delle porte

# Finestre
lines = lines2lines("./lines/windows.lines")#acquisizione dei punti dal file di interesse
plan = STRUCT(AA(POLYLINE)(lines))#costruzione 3d della struttura
plan = OFFSET([45,12])(plan)#funzione per migliorare le dimensioni x,y e la visualizzazione
height = QUOTE([40])#funzione utilizzata per alzare l'altezza della struttura
windows = PROD([plan,height])#oggetto 3d dei box delle finestre
window = []#oggetto finestra
window.append(T([1,2,3])([0,0,40]))#traslazione dei box verso l'alto
window.append(plan3dWindow)#oggetto 3d del box delle finestre

# Pavimento
lines = lines2lines("./lines/floor.lines")
plan = STRUCT(AA(POLYLINE)(lines))
plan = OFFSET([10,10])(plan)
height = QUOTE([1])
floor = PROD([plan,height])

# Costruzione dei muri con alloggiamenti per porte e finestre
sub = STRUCT([STRUCT(window),doors])
externalStruct =DIFFERENCE([perimeter,sub])
internalStruct =DIFFERENCE([internal),sub])

# Definizione delle texture
EXT_WALL_TXT = "./textures/ext_wall_txt.jpg"
INT_WALL_TXT = "./textures/int_wall_txt.jpg"
FLOOR_TXT = "./textures/floor_txt.jpg"

# Vista della casa
VIEW(STRUCT([TEXTURE(EXT_WALL_TXT)(externalStruct),TEXTURE(FLOOR_TXT)(floor),TEXTURE(INT_WALL_TXT)(internalStruct)]))