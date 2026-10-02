from vectors import *
import pygame

class Link():
    def __init__(self,obj1,obj2,targetLength,elasticity = 1 ):
        self.obj1 = obj1
        self.obj2 = obj2
        self.targetLength = targetLength
        self.elasticity = elasticity

    def apply(self,):
        axis = self.obj1.position - self.obj2.position
        distance = axis.magnitude()
        norm = axis.normalised()
        delta = self.targetLength - distance
        error = 0.5 * delta * norm * self.elasticity
        if not self.obj1.grounded:
            self.obj1.position += error
        if not self.obj2.grounded:
            self.obj2.position -= error


    def draw(self,camera):
        pos1 = camera.screenSpace(self.obj1.position)     
        pos2 = camera.screenSpace(self.obj2.position)    
        pygame.draw.line(camera.screen,"white",pos1,pos2)  