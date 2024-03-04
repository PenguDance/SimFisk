import numpy as np

class Vector():
    def __init__(self,pos,len,name):
        self.pos = pos
        self.len = len
        self.length = np.sqrt(len[0]**2 + len[1]**2)
        self.name = name    #String
    def __add__(self,other):
        return Vector(self.pos[0],self.pos[1],self.len[0]+other.len[0],self.len[1]+other.len[1],self.color,self.thickness,"Sumvektor")
    def __mul__(self,k):
        return Vector(self.pos[0],self.pos[1],(self.len[0]*k),(self.len[1]*k),self.color,self.thickness,self.name)
    def getX(self):
        return self.pos[0]    #Returns the X-coordinate of the vectors starting point
    def getY(self):
        return self.pos[1]    #Returns the Y-coordinate of the vectors starting point
    def getLenX(self):
        return self.len[0]    #Returns the X-vectorcoordinate (the X-length) of the vector
    def getLenY(self):
        return self.len[1]    #Returns the Y-vectorcoordinate (the Y-length) of the vector
    def getLen(self):
        return self.length    #Returns the length of the vector
    def setLen(self,len):
        self.len = len
    def __setLength(self,length):
        self.length = length      #Changes the length of the vector
    def getName(self):
        return self.name    #Returns the name of the vector
    def normalize(self):
        self.len = [self.len[0]/self.length,self.len[1]/self.length]
        self.__setLength(1)
    def negate(self):
        self.__setLenX(-self.lenX)
        self.__setLenY(-self.lenY)
    def getAngle(self,other):
        return (np.arccos(((self.lenX*other.lenX)+(self.lenY*other.lenY))/(self.len*other.len)))
    def getScalar(self,other):
        return ((self.lenX*other.lenY)-(self.lenY*other.lenX))
    def isParallel(self,other):
        if self.getScalar(other) == 0:
            return True
        else:
            return False
    def isPerpendicular(self,other):
        if self.getAngle(other) == np.pi/2 or self.getAngle(other) == 3*np.pi/2:
            return True
        else:
            return False
    def isOpposite(self,other):
        if self.getAngle(other) == np.pi:
            return True
        else: 
            return False
        