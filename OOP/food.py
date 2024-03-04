import random as r
import numpy as np
import pygame
class Food():
    def __init__(self,windowSize):
        self.name = "Food"
        self.size = r.randint(2,10)
        self.pos = [r.randint(50,windowSize[0]-50),self.size/2]
        self.maxY = windowSize[1]
        self.theta = 0
        self.color = [r.randint(0,255),r.randint(0,255),r.randint(0,255)]
    def update(self):
        if self.pos[1] < self.maxY-self.size:
            self.setVel()
            self.move()
    def show(self,screen):
        pygame.draw.circle(screen,self.color,self.pos,self.size)
    def move(self):
        self.pos[1] += 1
        self.pos[0] += np.cos(self.theta)*3
        self.theta += 0.1
    def setVel(self):
        pass
        
