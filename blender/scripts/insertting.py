import bpy
import math
from utils import printf, start, end

def insert():
    C = bpy.context
    cl = C.scene.cursor_location
    start()
    x = math.trunc(cl[0])
    y = math.trunc(cl[1])
    printf("x")
    printf(x)
    printf(y)
    end()
# insert()
    


