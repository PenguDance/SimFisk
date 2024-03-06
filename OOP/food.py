import random as r
import numpy as np
import pygame
class Food():
    def __init__(self,windowSize):
        self.name = "Food"
        self.size = r.randint(5,8)
        self.pos = [r.randint(50,windowSize[0]-50),self.size/2]
        self.maxY = windowSize[1]
        self.theta = 0
        self.color = [r.randint(0,255),r.randint(0,255),r.randint(0,255)]
    def update(self):
        if self.pos[1] < self.maxY-self.size: # Tjekker om maden har ramt bunden
            self.setVel()
            self.move()
    def show(self,screen):
        pygame.draw.circle(screen,self.color,self.pos,self.size)
        # Tegner maden
    def move(self):
        self.pos[1] += 1
        # Rykker maden en pixel ned
        self.pos[0] += np.cos(self.theta)*3
        # Rykker maden fra side til side
        self.theta += 0.1
        # øger vinklen hvorved x-værdien findes fra
    def setVel(self):
        pass
        
