import sys
import time
import pygame
from vectors import vector, Vector2
from verlet_solver import Solver
from verlet_object import VerletObject
from verlet_link import Link
from cameraUtils import Camera
from debugy import debug, timerModule
from inputHandler import Input

screen = pygame.display.set_mode((1900,1000))
camera = Camera(screen,(1900,1000),500,zoomspeed=5)
inputManager = Input()

physics = Solver()
physics.objects.append(VerletObject("red",(0,0),(1,1),10,5,grounded=True))
for i in range(100):
    physics.objects.append(VerletObject("red",(0,-200),(1,1),1,5))
for i in range(100):
    physics.links.append(Link(physics.objects[i],physics.objects[i+1],10,elasticity=1))

physics.objects[100].grounded = True
physics.objects[100].setPosition((900,0))
physics.objects[100].radius = 5
running = True

currentFrame = time.time()-0.1
frame = 0
clock = pygame.time.Clock()
average = 20
fps = [0 for _ in range(average)]
averageFPS = 0
timer = timerModule()

mouseDownPos = pygame.mouse.get_pos()
addPos = pygame.mouse.get_pos()
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
    camera.move(inputManager,deltaTime=deltaTime)
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
        physics.update(0.009,itteration = 1)
    change = timer.read()
    timer.log()
    physics.drawAll(camera)

    
    debug(f"frame time {int(deltaTime*1000)}ms",10,10)
    debug(f"physics time {int(change)}ms",40)
    debug(f"min/avg/max {int(minimum)}/{int(averageFPS)}/{int(maximum)} fps",70)
    pygame.display.flip()
    #clock.tick(144)

