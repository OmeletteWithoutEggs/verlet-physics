import keyboard
from vectors import vector, Vector2, tupl
from inputHandler import Input

class Camera():
    def __init__(self,screen,size,speed,zoomspeed = 0.01):
        self.speed = speed
        self.screen = screen
        self.zoomSpeed = zoomspeed
        self.size = vector(size)
        self.position = Vector2(0,0)
        self.center = self.size / 2
        self.zoom = 1

    def screenSpace(self,position):
        position = (((position - self.position)*self.zoom)+self.center)
        return tupl(position)  
    
    def worldSpace(self,screenPos):
        position = (screenPos-self.center)/self.zoom + self.position
        return position

    def move(self,input:Input,deltaTime = 1):
        if input.isPressed("w"):
            self.position.y -= self.speed * deltaTime
        if input.isPressed("s"):
            self.position.y += self.speed * deltaTime
        if input.isPressed("a"):
            self.position.x -= self.speed * deltaTime
        if input.isPressed("d"):
            self.position.x += self.speed * deltaTime

        if input.isPressed("="):
            self.zoom += self.zoomSpeed * self.zoom * deltaTime
        if input.isPressed("-"):
            self.zoom -= self.zoomSpeed * self.zoom * deltaTime
        



