import pygame as pygame
from pygame.locals import *
import random as r
from Library import Vector
from InheritanceFish import ClownFish,Sharks
from food import Food
windowSize = [800,600] # Bredde og højde på vinduet
pygame.init() # Initialisering af Pygame
clock = pygame.time.Clock() # Tidssytem til spillet
fishSpawnEvent = 1
sharkFreezeEvent = 2
sharkUnfreezeEvent = 3
foodSpawnEvent = 4
hungerEvent = 5
# Events til spillet
screen = pygame.display.set_mode((windowSize[0],windowSize[1])) # Laver kanvas
pygame.display.set_caption('Flokkesimulation') # Navngiver programnavn
font = pygame.font.SysFont("Arial", 36) # Font til tekst i vinduet
cfish = [0]*100 # Start array til fisk
sharks = [0]*4 # Start array til hajer
food = [0]      # Start array til mad
frozenSharks = [0]
def newFish():
    cfish.append(ClownFish([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(100,100,100),"Fisk",5,windowSize,5,200,50))
    # Laver en ny fisk med værdierne ([x,y],[x-has,y-has],(r,g,b),"navn",størrelse, [vindue-x,vindue-y], synslængde, personligzone)
    print(f"Ny fisk :D {len(cfish)}")
def newShark():
    sharks.append(Sharks([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(255,10,50),"Haj",5,windowSize,1.5,300,150))
     # Laver en ny haj med værdierne ([x,y],[x-has,y-has],(r,g,b),"navn",størrelse, [vindue-x,vindue-y], synslængde, personligzone)
def newFood():
    if len(food) < 5:
        food.append(Food(windowSize))
    # Laver mere mad, hvis der er mindre end 5 stykker mad    
def sharkFreeze():
    x = r.randint(0,len(sharks)-1) # Finder en tilfældig haj
    sharks[x].freeze() # Fryser hajen
    frozenSharks[0] = sharks[x] # Angiver frozenSharks[0] som den frozne haj
    pygame.time.set_timer(sharkUnfreezeEvent,1000, loops = 1) # Starter en timer på 1 sekund
def sharkUnfreeze():
    frozenSharks[0].unfreeze() # optøer hajen
    pygame.time.set_timer(sharkFreezeEvent, r.randint(500,4000), loops = 1) # Start en timer til at fryse en ny haj
    
def setup():
    for i in range(len(cfish)):
        cfish[i] = ClownFish([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(100,100,100),"Fisk",5,windowSize,5,200,50)
    for i in range(len(sharks)):
        sharks[i] = Sharks([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(255,10,50),"Haj",5,windowSize,1.5,300,150)
    food[0] = Food(windowSize)
    # Laver start fisk, hajer og mad
pygame.time.set_timer(fishSpawnEvent, 1000)
pygame.time.set_timer(sharkFreezeEvent, r.randint(500,2000), loops = 1)
pygame.time.set_timer(foodSpawnEvent, 100, loops = 1)
pygame.time.set_timer(hungerEvent, 5000)
# Timere til simulationen
def draw():
    clock.tick(60) # sætter tickrate til 60 tps
    screen.fill((200, 200, 200)) # Farver skærmen lysegrå
    for i in range(len(cfish)): # Går gennem alle fisk
        if i >= len(cfish): # I tilfælde af at en fisk er slettet, sørger det for at programmet ikke crasher
            break
        if len(food) > 0: # Tjekker om der er mad
            for j in range(len(food)): # Går gennem alt maden
                if cfish[i].checkCol(food[j]) == True: # Tjekker om fisken kolliderer med maden
                    cfish[i].size += 1 # Gør fisken større
                    food.pop(j) # Fjerner maden
                    print("Yum")
                    break
        cfish[i].update(cfish,sharks,food)
        cfish[i].show(screen)
        # Opdaterer og viser fisken
        for j in range(len(sharks)): # Går gennem alle hajer
            if cfish[i].checkCol(sharks[j]) == True: # Tjekker om fisken kolliderer med en haj
                cfish.pop(i) # Fjerner fisken
                print("Yum")
                sharks[j].eat() # Kører hajens spise funktion
                break
        
    for i in range(len(sharks)): # Går gennem alle hajer
        if sharks[i].frozen == False: # Tjekker om hajen ikke er frosen
            sharks[i].update(cfish,sharks,food) # Opdaterer hajen
        sharks[i].show(screen) # Viser hajen
    for i in range(len(food)): # Går gennem alt mad
        food[i].update()
        food[i].show(screen) # Opdaterer og viser maden
    text = f"amount of fishes = {len(cfish)}  amount  of sharks = {len(sharks)}"
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 50))
    # Tekst der viser antallet af fisk og hajer
    pygame.display.update()
setup()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == fishSpawnEvent:
            newFish()
        elif event.type == sharkFreezeEvent:
            sharkFreeze()
        elif event.type == sharkUnfreezeEvent:
            sharkUnfreeze()
        elif event.type == foodSpawnEvent:
            newFood()
            pygame.time.set_timer(foodSpawnEvent,r.randint(1000,3000), loops = 1)
        elif event.type == hungerEvent:
            for i in range(len(sharks)):
                sharks[i].size -= 1
                if sharks[i].size == 0:
                    sharks.pop(i)
                    break
            if len(sharks) == 1:
                newShark()
    draw()

if __name__ == "__main__":
    pass
pygame.quit()