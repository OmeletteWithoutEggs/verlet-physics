import pygame
from debugy import debug
from vectors import vector,Vector2


        

class VerletObject():
    def __init__(self,colour,position,velocity,mass,radius,grounded = False ,forces = []):
        self.colour = colour
        self.position = vector(position)
        self.lastPosition = self.position
        self.acceleration = vector(velocity)
        self.radius = radius
        self.mass = mass
        self.velocity = 0
        self.grounded = grounded

    def setPosition(self,position):
        self.position = vector(position)
        self.lastPosition = vector(position)


    def updatePosition(self,deltaTime):
        if not self.grounded:
            self.velocity = self.position - self.lastPosition
            #save current position
            self.lastPosition = self.position.copy() #copies the vector to ensure that they are different objects
            #perform verlet integration
            #self.position = self.position + self.velocity + self.acceleration * (deltaTime**2)
            self.position += self.velocity + self.acceleration * (deltaTime**2)
            #reset acceleration
            self.acceleration = Vector2(0,0)
        else:
            self.position = self.lastPosition.copy()
        
    def accelerate(self,acceleration):
        self.acceleration += acceleration

    def addForce(self,force):
        self.acceleration += force/self.mass

    def applyConstraints(self,constraints):
        for item in constraints:
            center = vector(item[0])
            radius = item[1]
            axis = center-self.position
            dist = axis.magnitude()
            if dist > radius-self.radius:
                axis.normalise()
                
                self.position = center - axis * (radius - self.radius)
    
    def solveCollisions(self,objects):
        for obj in objects:
            collisionAxis = self.position - obj.position
            dist = collisionAxis.magnitude()
            if dist < obj.radius + self.radius:
                norm = collisionAxis.normalised()
                delta = (obj.radius + self.radius) - dist
                self.position += 0.5 * delta * norm
                obj.position -= 0.5 * delta * norm


    def addForce(self,force):
        self.acceleration += force / self.mass

        #self.forces.append(vect(force))

    def draw(self,camera):
        screenPos = camera.screenSpace(self.position)
        pygame.draw.aacircle(camera.screen,self.colour,screenPos,self.radius*camera.zoom)




