import math

class Helper(object):
    # trouve le point à partir d'un point de départ, avec une distance 
    # et un angle
    def getAngledPoint(angle,longueur,cx,cy):
        x = (math.cos(angle)*longueur)+cx
        y = (math.sin(angle)*longueur)+cy
        return (x,y)
    getAngledPoint = staticmethod(getAngledPoint)
    
    #trouve l'angle entre deux points
    def calcAngle(x1,y1,x2,y2):
         dx = x2-x1
         dy = y2-y1
         #angle = (math.atan2(dy,dx) % (2*math.pi)) * (180/math.pi)
         angle = (math.atan2(dy,dx) ) #% (2*math.pi)) * (180/math.pi)
         return angle
    calcAngle = staticmethod(calcAngle)
    
    #trouve la distance entre deux points
    def calcDistance(x1,y1,x2,y2):
         dx = abs(x2-x1)**2
         dy = abs(y2-y1)**2
         distance=math.sqrt(dx+dy)
         return distance
    calcDistance = staticmethod(calcDistance)
