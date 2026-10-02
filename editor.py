import pygame
from inputHandler import Input
from debugy import debug, timerModule
from verlet_solver import Solver
from verlet_link import Link
from verlet_object import VerletObject
from cameraUtils import Camera

from vectors import vector,tupl
import json





def checkPoint(points):
    for point in points:
        distance = (point["position"] - vector(camera.worldSpace(inputManager.mousePos()))).magnitude()
        if distance < point["radius"]: 
            return point["id"]
    return None
                    



screen = pygame.display.set_mode((1900,1000))
camera = Camera(screen,(1900,1000),5,zoomspeed=5)
inputManager = Input()
points = []
links = []
lines = []

path = input()
if path:
    try:
        with open(path+".json","r") as file:
            data = json.load(file)
        points = data["objects"]
        links = data["links"]
        lines = data["lines"]
    except:
        print("file not found")
        exit()

mass = 10
radius = 5
grounded = False
connecting = False
lining = False

running = True
while True:
    inputManager.update()
    camera.move(inputManager,deltaTime=0.001)
    if inputManager.checkQuit() is True:
        pygame.quit()
        with open(input()+".json","w") as file:
            json.dump({"objects":points,"links":links,"lines":lines},file)
        exit()
    if inputManager.justPressed("lclick"):
        if connecting:
            obj2 = checkPoint(points)
            length = (vector(points[obj1]["position"]) - vector(points[obj2]["position"])).magnitude()
            links.append({
                "obj1":obj1,
                "obj2":obj2,
                "length":length})
            connecting = False
        else:
            obj1 = checkPoint(points)
            if obj1 is None:
                points.append({
                    "position":tupl(camera.worldSpace(inputManager.mousePos())),
                    "radius": radius,
                    "mass":mass,
                    "id":len(points),
                    "grounded":grounded
                    })
            else:
                connecting = True
        
    if inputManager.justPressed("rclick"):
        if lining:
            p2 = tupl(camera.worldSpace(inputManager.mousePos()))
            lines.append((p1,p2))
            lining = False
        else:
            lining = True
            p1 = tupl(camera.worldSpace(inputManager.mousePos()))

    
    
    if inputManager.justPressed("space"):
        grounded = not grounded  

    screen.fill((0,0,50))
    for point in points:
        screenPos = camera.screenSpace(point["position"])
        pygame.draw.circle(camera.screen,"red",screenPos,point["radius"])

    for link in links:
        pos1 = camera.screenSpace(points[link["obj1"]]["position"])
        pos2 = camera.screenSpace(points[link["obj2"]]["position"])
        pygame.draw.line(camera.screen,"white",pos1,pos2)

    for line in lines:
        pos1 = camera.screenSpace(line[0])
        pos2 = camera.screenSpace(line[1])
        pygame.draw.line(camera.screen,"red",pos1, pos2)

    debug("grounded : " + str(grounded),10,20)
    pygame.display.flip()
    #clock.tick(144)
    print(points)
