import numpy as np
import pygame 
from pygame.locals import *
import random as r
from Library import Vector
class Fish():
    def __init__(self,pos,len,color,name,size,windowSize,speed,vis,near):
        self.vectors = Vector(pos,len,name)
        self.pos = self.vectors.pos
        self.vel = self.vectors.len
        self.color = color
        self.size = size
        self.windowSize = windowSize
        self.speed = speed
        self.vis = vis
        self.near = near
    def move(self):
        self.length = np.sqrt(self.vel[0]**2 + self.vel[1]**2)
        for i in range(2):
            self.vel[i] = self.speed*self.vel[i]/self.length
            if self.pos[i] + self.vel[i] <= 0 or self.pos[i] + self.vel[i] >= self.windowSize[i]:
                self.vel[i] = self.vel[i] * (-1)
            self.pos[i] = self.pos[i] + self.vel[i]
        #print(f"x: {self.vel[0]}  y: {self.vel[1]}  L: {np.sqrt(self.vel[0]**2 + self.vel[1]**2)}  name: {self.vectors.name}")
    def update(self,cFishes,sharks,food):
        self.setVel(cFishes,sharks,food)
        self.move()
    def show(self,screen):
        pygame.draw.circle(screen,self.color,self.pos,self.size)

class ClownFish(Fish):
    def __init__(self, pos, len, color, name, size, windowSize,speed,vis,near):
        super().__init__(pos, len, color, name, size, windowSize,speed, vis, near)
    def setVel(self,cFishes,sharks,food):
        speed = [0,0]
        self.avgFish = [0,0]
        self.nFish = 0
        self.avgSharks = [0,0]
        self.nSharks = 0
        self.food = [0,0]
        for i in range(len(cFishes)):
            if cFishes[i] == self:
                continue
            dx = cFishes[i].pos[0]-self.pos[0]
            dy = cFishes[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            if dist > self.vis:
                continue

            if dist > self.near:
                for j in range(2):
                    self.avgFish[j] += dc[j]
            if dist <= self.near:
                for j in range(2):
                    self.avgFish[j] -= 5*dc[j]
            self.nFish += 1
        if self.nFish != 0:
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/self.nFish    
            dist = np.sqrt(self.avgFish[0]**2 + self.avgFish[1]**2)
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/dist

        for i in range(len(sharks)):
            dx = sharks[i].pos[0]-self.pos[0]
            dy = sharks[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            if dist-sharks[i].size > self.vis:
                continue
            for j in range(2):
                self.avgSharks[j] += dc[j]
            self.nSharks += 1
        if self.nSharks != 0:
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/self.nSharks
            dist = np.sqrt(self.avgSharks[0]**2 + self.avgSharks[1]**2)
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/dist
            
            
        if len(food) > 0:
            for i in range(len(food)):
                dx = food[i].pos[0]-self.pos[0]
                dy = food[i].pos[1]-self.pos[1]
                dist = np.sqrt(dx**2 + dy**2)
                if dist > 2*self.vis:
                    continue
                if self.food == [0,0]:
                    self.food = [dy,dx]
                    continue
                if dist < np.sqrt(self.food[0]**2 + self.food[1]**2):
                    for j in range(2):
                        self.food[j] = food[i].pos[j]-self.pos[j]
            dist = np.sqrt(self.food[0]**2 + self.food[1]**2)
            if dist != 0:
                for i in range(2):
                    self.food[i] = self.food[i]/dist
        for j in range(2):
            speed[j] = (self.avgFish[j] - self.avgSharks[j]*2 + 3*self.food[j])
        if speed != [0,0]:
            for j in  range(2):
                speed[j] = speed[j]/np.sqrt(speed[0]**2 + speed[1]**2)
        for i in range(2):
            self.vel[i] = self.vel[i] + speed[i]*5
    def checkCol(self,other):
        dist = np.sqrt((self.pos[0]-other.pos[0])**2 + (self.pos[1]-other.pos[1])**2)
        if dist <= self.size + other.size:
            if other.name == "Haj":
                del self
                return True
            else:
                return True
class Sharks(Fish):
    def __init__(self, pos, len, color, name, size, windowSize, speed, vis, near):
        super().__init__(pos, len, color, name, size, windowSize, speed, vis, near)
        self.name = name
        self.frozen = False
    def setVel(self,cFishes,sharks,food):
        speed = [0,0]
        self.avgFish = [0,0]
        self.nFish = 0
        self.avgSharks = [0,0]
        self.nSharks = 0
        for i in range(len(cFishes)):
            dx = cFishes[i].pos[0]-self.pos[0]
            dy = cFishes[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            if dist > self.vis:
                continue
            for j in range(2):
                self.avgFish[j] += 5*dc[j]
            self.nFish += 1
        if self.nFish != 0:
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/self.nFish    
            dist = np.sqrt(self.avgFish[0]**2 + self.avgFish[1]**2)
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/dist

        for i in range(len(sharks)):
            if sharks[i] == self:
                continue
            dx = sharks[i].pos[0]-self.pos[0]
            dy = sharks[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            if dist > self.near:
                continue
            for j in range(2):
                self.avgSharks[j] += dc[j]
            self.nSharks += 1
        if self.nSharks != 0:
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/self.nSharks
            dist = np.sqrt(self.avgSharks[0]**2 + self.avgSharks[1]**2)
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/dist
            
        for j in range(2):
            speed[j] = self.avgFish[j] - self.avgSharks[j]
            

        for i in range(2):
            self.vel[i] = self.vel[i] + speed[i]*5
        
    def eat(self):
        self.size = self.size + 1
    def freeze(self):
        self.frozen = True
    def unfreeze(self):
        self.frozen = False
