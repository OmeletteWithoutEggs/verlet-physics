from vectors import dot
from verlet_object import *
from verlet_link import *
import pygame
import time
import sys
import json

class Solver():
    def __init__(self):
        self.gravity = Vector2(0,1000)
        self.objects = []
        self.links = []
        self.constraints = []
        self.lines = []

    
    def add(self,obj):
        self.objects.append(obj)

    def update(self,deltaTime,itteration = 20):
        self.applyConstraints()
        self.solveCollisions()
        for i in range(itteration):
            self.solveLinks()
        self.applyGravity()
        self.updatePositions(deltaTime)
        

    def updatePositions(self,deltaTime):
        for obj in self.objects:
            obj.updatePosition(deltaTime)


    def applyGravity(self):
        for obj in self.objects:
            obj.accelerate(self.gravity)

    def applyConstraints(self):
        for constraint in self.constraints:
            center = vector(constraint[0:2])
            radius = constraint[2]
            for obj in self.objects:
                toObj = center-obj.position
                dist = toObj.magnitude()
                if dist > radius-obj.radius:
                    toObj.normalise()
                    obj.position = center - toObj * (radius - obj.radius)

        for line in self.lines:
            for obj in self.objects:
                closest = closestPointOnLine(obj.position,line[0],line[1])
                delta = obj.position - closest
                dist = delta.magnitude()
                norm = delta.normalised()
                if dist < obj.radius:
                    obj.position -= (dist - obj.radius) * norm
                """maxMove = (closest - obj.position)
                maxMove -= obj.radius * maxMove.normalised()
                velo = obj.position - obj.lastPosition
                mag = velo.magnitude()
                m2 = (velo - maxMove).magnitude()
                if m2 < mag:
                     exit()"""


    def solveLinks(self):
        for link in self.links:
            link.apply()

    def solveCollisions(self):
        
        for obj in self.objects:
            for obj2 in self.objects:
                collisionAxis = obj.position - obj2.position
                dist = collisionAxis.magnitude()
                if dist < obj2.radius + obj.radius:
                    norm = collisionAxis.normalised()
                    delta = (obj2.radius + obj.radius) - dist
                    obj.position += delta * norm * obj2.mass / (obj.mass+obj2.mass)
                    obj2.position -= delta * norm * obj.mass / (obj.mass+obj2.mass)

    def drawAll(self,camera):
        for constraint in self.constraints:
            screenPos = camera.screenSpace(vector(constraint[0:2]))
            pygame.draw.aacircle(camera.screen,"red",screenPos,constraint[2]*camera.zoom,3)
        for line in self.lines:
            screenPos1 = camera.screenSpace(line[1])
            screenPos2 = camera.screenSpace(line[0])
            pygame.draw.aaline(camera.screen,"red",screenPos1,screenPos2,3)

        
        for obj in self.objects:
            obj.draw(camera)

    def drawLinks(self,camera):
        for link in self.links:
            link.draw(camera)


    def pointCheck(self,position) -> VerletObject:
        for obj in self.objects:
            if (obj.position - position).magnitude() < obj.radius:
                return obj
        return None
    
    def load(self,path):
        with open(path+".json","r") as file:
            data = json.load(file)
        objects = data["objects"]
        links = data["links"]
        for obj in objects:
            self.add(VerletObject("red",obj["position"],(0,0),obj["mass"],obj["radius"],obj["grounded"]))

        for link in links:
            self.links.append(Link(self.objects[link["obj1"]],self.objects[link["obj2"]],link["length"],elasticity=0.1))

        for line in data["lines"]:
            self.lines.append((vector(line[0]),vector(line[1])))
        



def closestPointOnLine(particlePos, point1, point2):
        p1ToParticle = particlePos - point1
        line = point2 - point1
        t = max(0, min(1, p1ToParticle.dot(line) / line.magnitude()**2))
        return point1 + line * t
