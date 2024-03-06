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
        for i in range(len(cFishes)): # Går gennem alle fisk
            if cFishes[i] == self: # Hopper fisken over hvis det er den selv
                continue
            dx = cFishes[i].pos[0]-self.pos[0] 
            dy = cFishes[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            # Angiver x- og y-afstande  mellem fiskene
            dist = np.sqrt(dx**2 + dy**2)
            # Angiver den samlede afstand mellem fiskene
            if dist > self.vis + self.size + cFishes[i].size: # Hvis afstanden mellem fiskene er længere end fiskens synslængde sprænges fisken over
                continue

            if dist > self.near + self.size + cFishes[i].size: # Tjekker om den anden fisk er uden for fiskens personligezone
                for j in range(2):
                    self.avgFish[j] += dc[j]
                    # Lægger x- og y-afstandene til en liste, der indeholder alle x- og y-afstande
            if dist <= self.near + self.size + cFishes[i].size: # Hvis fisken er indenfor den anden fisks personlige zone
                for j in range(2):
                    self.avgFish[j] -= 5*dc[j]
                    # Trækker 5*gange x- og y-afstande fra de samlagte afstande

            self.nFish += 1 # Tæller op hvor mange fisk der er i nærheden
        if self.nFish != 0: # Hvis der er en eller flere fisk i nærheden
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/self.nFish    
                # Tager gennemsnittet af x- og y-afstandende mellem fisken og de andre fisk
            dist = np.sqrt(self.avgFish[0]**2 + self.avgFish[1]**2)
            # Finde den gennemsnitlige afstand
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/dist
            # Normaliserer x- og y-afstanden

        for i in range(len(sharks)): # Går gennem alle hajer
            dx = sharks[i].pos[0]-self.pos[0]
            dy = sharks[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            # Finder x- og y-afstanden fra fisken til en haj, samt den samlede afstand
            if dist-sharks[i].size > self.vis + self.size: # Tjekker om fisken er udenfor det synlige område
                continue
            for j in range(2):
                self.avgSharks[j] += dc[j]
                # Lægger x- og y-afstande til en samlet liste
            self.nSharks += 1
            # Tæller antallet af hajer i nærheden
        if self.nSharks != 0: # Hvis der er en eller flere hajer i nærheden
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/self.nSharks
                # Tager gennemsnittet af hajernes x- og y-afstande
            dist = np.sqrt(self.avgSharks[0]**2 + self.avgSharks[1]**2)
            # Finder den gennemsnitlige afstand
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/dist
                # Normaliserer x- og y-afstanden
            
            
        if len(food) > 0: # Tjekker om der er mad
            for i in range(len(food)):
                dx = food[i].pos[0]-self.pos[0]
                dy = food[i].pos[1]-self.pos[1]
                dist = np.sqrt(dx**2 + dy**2)
                # Finder x- og y afstanden til maden, samt den samlede afstand
                if dist > 2*self.vis + self.size: # Hvis maden er udenfor den dobbelte fiskesynslængde
                    continue
                if self.food == [0,0]: # Hvis der er ikke er valgt mad endnu
                    self.food = [dy,dx] # Angiver nærmeste mads x- og y-afstand
                    continue
                if dist < np.sqrt(self.food[0]**2 + self.food[1]**2):
                    # Tjekker om det nye mad er tættere på end den tidligere som var tættest på
                    for j in range(2):
                        self.food[j] = food[i].pos[j]-self.pos[j]
                        # Angiver det madens x- og y-afstand
            dist = np.sqrt(self.food[0]**2 + self.food[1]**2)
            # Finder den samlede afstand til nærmeste mad
            if dist != 0: # Hvis der er mad i nærheden
                for i in range(2):
                    self.food[i] = self.food[i]/dist
                    # Normaliserer x- og y-afstandene
        for j in range(2):
            speed[j] = (self.avgFish[j] - self.avgSharks[j]*2 + 3*self.food[j])
            # Lægger de 3 x- og y-afstande sammen i forholdet, 1:-2:3
        if speed != [0,0]:  # Hvis der er noget i nærheden
            for j in  range(2):
                speed[j] = speed[j]/np.sqrt(speed[0]**2 + speed[1]**2)
                # Normaliserer de nye x- og y-afstande
        for i in range(2):
            self.vel[i] = self.vel[i] + speed[i]*5
            # Lægger 5 gange den fundne hastighed til fiskens hastighed 
    def checkCol(self,other):
        dist = np.sqrt((self.pos[0]-other.pos[0])**2 + (self.pos[1]-other.pos[1])**2)
        # Finder afstanden til det andet objekt
        if dist <= self.size + other.size: # Hvis afstanden mellem objekterne er mindre end deres samlede størrelser
            if other.name == "Haj": # Tjekker om det er en haj
                del self # Sletter fisken
                return True
            else:
                # Hvis det ikke er en haj men derimod mad
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
        for i in range(len(cFishes)): # Går gennem alle fisk
            dx = cFishes[i].pos[0]-self.pos[0]
            dy = cFishes[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            # Finder x- og y-afstand og den samlede afstand til fisken
            if dist > self.vis + self.size + cFishes[i].size: # Tjekker om fisken er indenfor hajens synslængde
                continue
            for j in range(2):
                self.avgFish[j] += 5*dc[j] # Lægger 5 * fiskens x- og y-afstand til en liste
            self.nFish += 1 # Tæller antallet af fisk i nærheden
        if self.nFish != 0: # Hvis der er 1 eller flere fisk i nærheden
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/self.nFish   
                # Finder gennemsnittet af x- og y-afstanden 
            dist = np.sqrt(self.avgFish[0]**2 + self.avgFish[1]**2)
            # Finde den gennemsnitlige afstand
            for i in range(2):
                self.avgFish[i] = self.avgFish[i]/dist
                # Normaliserer x- og y-afstandene

        for i in range(len(sharks)): # Går gennem alle hajer
            if sharks[i] == self: # Tjekker om hajen er sig selv
                continue
            dx = sharks[i].pos[0]-self.pos[0]
            dy = sharks[i].pos[1]-self.pos[1]
            dc = [dx,dy]
            dist = np.sqrt(dx**2 + dy**2)
            # Finder x- og y-afstanden samt den samlede afstand
            if dist > self.near + self.size + sharks[i].size: # Hvis hajen er udenfor hajens personlige zone
                continue
            for j in range(2):
                self.avgSharks[j] += dc[j]
                # Lægger x- og y-afstanden til en liste
            self.nSharks += 1
            # Tæller antallet af hajer i nærheden
        if self.nSharks != 0: # Hvis der er 1 eller flere hajer i nærheden
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/self.nSharks
                # Finder gennemsnittet af x- og y-afstandene
            dist = np.sqrt(self.avgSharks[0]**2 + self.avgSharks[1]**2)
            # Finder den genenmsnitlige afstand
            for i in range(2):
                self.avgSharks[i] = self.avgSharks[i]/dist
                # Normaliserer x- og y-afstanden
            
        for j in range(2):
            speed[j] = self.avgFish[j] - 2*self.avgSharks[j]
            # Lægger fiske afstandene og haj afstandene sammen i forholdet 1:-2

        for i in range(2):
            self.vel[i] = self.vel[i] + speed[i]*5
            # Lægger 5 gange den fundne hastighed til hajens egen hastighed 
        
    def eat(self):
        self.size = self.size + 1
        # Gør hajen større
    def freeze(self):
        self.frozen = True
        # Angiver at hajen er frosset
    def unfreeze(self):
        self.frozen = False
        # Angiver at hajen er optøet
