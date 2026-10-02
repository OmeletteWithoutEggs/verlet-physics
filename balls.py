import sys
import time
import pygame
import random
from vectors import vector, Vector2
from verlet_solver import Solver
from verlet_object import VerletObject
from cameraUtils import Camera
from debugy import debug, timerModule
from inputHandler import Input

screen = pygame.display.set_mode((1900,1000))
camera = Camera(screen,(1900,1000),5,zoomspeed=5)
inputManager = Input()

physics = Solver()
physics.constraints.append((0,0,500))
random.seed(345)
for i in range(100):
    physics.add(VerletObject((random.randint(0,255),random.randint(0,255),random.randint(0,255)),(0,0), (random.randrange(-200,200)/10,random.randrange(-200,200)/10), 10,random.randint(10,40)))

physics.lines.append((Vector2(-100,0),Vector2(100,10)))
running = True

currentFrame = time.time()-0.1
frame = 0
clock = pygame.time.Clock()
average = 100
fps = [0 for _ in range(average)]
averageFPS = 0
timer = timerModule()

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
    camera.move(inputManager)
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
        physics.update(0.009)
    change = timer.read()
    timer.log()
    physics.drawAll(camera)
    
    debug(f"frame time {int(deltaTime*1000)}ms",10,10)
    debug(f"physics time {int(change)}ms",40)
    debug(f"min/avg/max {int(minimum)}/{int(averageFPS)}/{int(maximum)} fps",70)
    pygame.display.flip()
    #clock.tick(144)
    
