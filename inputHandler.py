import pygame
class Input():
    def __init__(self):
        self.keys = None
        self.events = []
        self.keyboard = {
            "a":pygame.K_a,
            "b":pygame.K_b,
            "c":pygame.K_c,
            "d":pygame.K_d,
            "e":pygame.K_e,
            "f":pygame.K_f,
            "g":pygame.K_g,
            "h":pygame.K_h,
            "i":pygame.K_i,
            "j":pygame.K_j,
            "k":pygame.K_k,
            "l":pygame.K_l,
            "m":pygame.K_m,
            "n":pygame.K_n,
            "o":pygame.K_o,
            "p":pygame.K_p,
            "q":pygame.K_q,
            "r":pygame.K_r,
            "s":pygame.K_s,
            "t":pygame.K_t,
            "u":pygame.K_u,
            "v":pygame.K_v,
            "w":pygame.K_w,
            "x":pygame.K_x,
            "y":pygame.K_y,
            "z":pygame.K_z,
            "1":pygame.K_1,
            "2":pygame.K_2,
            "3":pygame.K_3,
            "4":pygame.K_4,
            "5":pygame.K_5,
            "6":pygame.K_6,
            "7":pygame.K_7,
            "8":pygame.K_8,
            "9":pygame.K_9,
            "0":pygame.K_0,
            "=":pygame.K_EQUALS,
            "-":pygame.K_MINUS,
            "space":pygame.K_SPACE,
            "lctrl":pygame.K_LCTRL,
            "rctrl":pygame.K_RCTRL,
            "lalt":pygame.K_LALT,
            "ralt":pygame.K_RALT,
            "lshift":pygame.K_LSHIFT,
            "rshift":pygame.K_RSHIFT,
            "tab":pygame.K_TAB
            }
        self.mouse = {
            "lclick":pygame.BUTTON_LEFT,
            "rclick":pygame.BUTTON_RIGHT,
            "mclick":pygame.BUTTON_MIDDLE}

    def update(self):
        self.events = pygame.event.get()
        self.keys = pygame.key.get_pressed()

    def isPressed(self, key):
        return self.keys[self.keyboard[key]]
    
    def justPressed(self,key):
        if key in self.mouse:
            for event in self.events: 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == self.mouse[key]:
                        return True
                
        if key in self.keyboard:
            for event in self.events: 
                if event.type == pygame.KEYDOWN:
                    if event.key == self.keyboard[key]:
                     return True     

    def justReleased(self,key):
        if key in self.mouse:
            for event in self.events: 
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == self.mouse[key]:
                        return True
                
        if key in self.keyboard:
            for event in self.events: 
                if event.type == pygame.KEYUP:
                    if event.key == self.keyboard[key]:
                     return True      
    
        return False
    def checkQuit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False
    
    def mousePos(self):
        return pygame.mouse.get_pos()