import math
from vectors import *

def raycast(origin, direction, lines, end = 7000):
    if not isinstance(lines,list):
        lines = [lines]

    x1,y1 = origin
    x2 = origin[0] + end*math.cos(direction)
    y2 = origin[1] + end*math.sin(direction)
    
    closestPoint = (x2,y2)
    shortestDist = end
     
    
    for (x3,y3),(x4,y4) in lines:
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            continue
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            px = x1 + t * (x2 - x1)
            py = y1 + t * (y2 - y1)
            
            if( Vector2(px,py)-vector(origin)).magnitude() <= shortestDist:
                    shortestDist = ( Vector2(px,py)-vector(origin)).magnitude()
                    closestPoint = (px,py)
    return closestPoint
        
    