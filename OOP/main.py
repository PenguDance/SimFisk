import pygame as pygame
from pygame.locals import *
import random as r
from Library import Vector
from InheritanceFish import ClownFish,Sharks
from food import Food
windowSize = [800,600]
clock= pygame.time.Clock()
# Bredde og højde på vinduet
# Initialisering af Pygame
pygame.init()
fishSpawnEvent = 1
sharkFreezeEvent = 2
sharkUnfreezeEvent = 3
foodSpawnEvent = 4
hungerEvent = 5
screen = pygame.display.set_mode((windowSize[0],windowSize[1]))
pygame.display.set_caption('Flokkesimulation')
# Font til tekst i vinduet
font = pygame.font.SysFont("Arial", 36)
cfish = [0]*100
sharks = [0]*10
food = [0]
frozenSharks = [0]
time = clock.get_time()
def newFish():
    cfish.append(ClownFish([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(100,100,100),"Fisk",5,windowSize,5,200,50))
    print(f"Ny fisk :D {len(cfish)}")
def newShark():
    sharks.append(Sharks([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(255,10,50),"Haj",5,windowSize,1.5,300,150))
def newFood():
    if len(food) < 5:
        food.append(Food(windowSize))
def sharkFreeze():
    x = r.randint(0,len(sharks)-1)
    sharks[x].freeze()
    frozenSharks[0] = sharks[x]
    pygame.time.set_timer(sharkUnfreezeEvent,1000, loops = 1)
def sharkUnfreeze():
    frozenSharks[0].unfreeze()
    pygame.time.set_timer(sharkFreezeEvent, r.randint(500,4000), loops = 1)
    
def setup():
    for i in range(len(cfish)):
        cfish[i] = ClownFish([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(100,100,100),"Fisk",5,windowSize,5,200,50)
    for i in range(len(sharks)):
        sharks[i] = Sharks([r.randint(0,windowSize[0]),r.randint(0,windowSize[1])],[(r.randint(0,200)-100)/100,(r.randint(0,200)-100)/100],(255,10,50),"Haj",5,windowSize,1.5,300,150)
    food[0] = Food(windowSize)
pygame.time.set_timer(fishSpawnEvent, 1000)
pygame.time.set_timer(sharkFreezeEvent, r.randint(500,2000), loops = 1)
pygame.time.set_timer(foodSpawnEvent, 100, loops = 1)
pygame.time.set_timer(hungerEvent, 5000)
def draw():
    clock.tick(60)
    screen.fill((200, 200, 200))
    for i in range(len(cfish)):
        if i >= len(cfish):
            break
        if len(food) > 0:
            for j in range(len(food)):
                if cfish[i].checkCol(food[j]) == True:
                    cfish[i].size += 1
                    food.pop(j)
                    print("Yum")
                    break
        cfish[i].update(cfish,sharks,food)
        cfish[i].show(screen)
        for j in range(len(sharks)):
            if cfish[i].checkCol(sharks[j]) == True:
                cfish.pop(i)
                print("Yum")
                sharks[j].eat()
                break
        
    for i in range(len(sharks)):
        if sharks[i].frozen == False:
            sharks[i].update(cfish,sharks,food)
        sharks[i].show(screen)
    for i in range(len(food)):
        food[i].update()
        food[i].show(screen)
        #cfish[i].setVel(cfish)
#NB! bruger her dependency injection for at undgå circular import dependencies in other files.
#cfish1.swim()#MyVector(1,1)) #r.randint(-1,1),r.randint(-1,1)))
#cfish1.show(screen)
#shark1.swim(cfish1)
#shark1.show(screen)
# Vis vindhastighed og retning i vinduet
    text = f"amount of fishes = {len(cfish)}  amount  of sharks = {len(sharks)}"
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 50))
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