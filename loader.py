import sys
import time
import pygame
from vectors import vector
from verlet_solver import Solver
from verlet_object import VerletObject
from verlet_link import Link
from cameraUtils import Camera
from debugy import debug, timerModule
from inputHandler import Input


inputManager = Input()
physics = Solver()
#physics.constraints.append((0,-100000,100000+500))
physics.load("saves/"+input("enter the save you would like to load (eg: 'save1','save2'): "))
screen = pygame.display.set_mode((1900,1000))
camera = Camera(screen,(1900,1000),500,zoomspeed=5)



timer = timerModule()
currentFrame = time.time()-0.1
frame = 0
clock = pygame.time.Clock()
average = 20
fps = [0 for _ in range(average)]
averageFPS = 0

addPos = pygame.mouse.get_pos()

running = False
while True:
    minimum = sys.maxsize
    maximum = 0
    frame += 1
    lastFrame = currentFrame
    currentFrame = time.time()
    deltaTime = currentFrame - lastFrame
    fps.insert(0,1/deltaTime)
    fps.pop(-1)
    for i in range(average):
        if fps[i] < minimum:
            minimum = fps[i]
        if fps[i] > maximum:
            maximum = fps[i]
        averageFPS += fps[i]
    averageFPS /= average

    inputManager.update()
    camera.move(inputManager,deltaTime)
    if inputManager.checkQuit():
        exit()
    if inputManager.justPressed("space"):
        running = not running
    if inputManager.justPressed("lclick"):
        mouseDownPos = vector(inputManager.mousePos())
        clickPos = camera.worldSpace(mouseDownPos)
        clicked = physics.pointCheck(clickPos)
    if inputManager.justReleased("lclick"):
        if clicked is None:
            velo = (mouseDownPos-inputManager.mousePos())
            velo *= velo.magnitude()/5
            physics.add(VerletObject("white",clickPos,velo,10,20))
        else:
            velo = (mouseDownPos-inputManager.mousePos())
            velo *= velo.magnitude()/5
            clicked.lastPosition -= (velo * deltaTime )/ clicked.mass


    screen.fill((0,0,50))
    timer.log()
    if running == 1:
        physics.update(deltaTime,itteration=1)
    change = timer.read()
    timer.log()
    physics.drawAll(camera)
    physics.drawLinks(camera)

    
    debug(f"frame time {int(deltaTime*1000)}ms",10,10)
    debug(f"physics time {int(change)}ms",40)
    debug(f"min/avg/max {int(minimum)}/{int(averageFPS)}/{int(maximum)} fps",70)
    pygame.display.flip()
    #clock.tick(144)
