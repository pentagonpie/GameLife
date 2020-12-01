import pygame


class selectable:
    def __init__(self, color,location,size,text,visible=True,interact=True):
        self.color = color
        self.location = location
        self.size = size
        self.text = text
        self.visible = visible
        self.interact = interact
        self.value = 1

    def changeColor(self,color):
        self.color=color

    def collidePoint(self,aPoint):
        if aPoint[0] > self.location[0] and aPoint[0] < self.location[0]+self.size[0]:
            if aPoint[1] > self.location[1] and aPoint[1] < self.location[1]+self.size[1]:
                return True
        return False

    def draw(self,screen):

        pygame.draw.rect(screen,self.color,[self.location[0], self.location[1], self.size[0],self.size[1]]) 
        # defining a font 
        smallfont = pygame.font.SysFont('Corbel',25) 
        textColor = (245,244,240)
        # rendering a text written in 
        # this font 
        textForm = smallfont.render(self.text , True , textColor) 
        # superimposing the text onto our button 
        offset = 9

        screen.blit(textForm, (self.location[0]+offset+3,self.location[1]+offset))


class button(selectable):
    def __init__(self, color,location,size,text,visible=True,interact=True):
        selectable.__init__(self,color,location,size,text,visible,interact)


    def on(self):
        self.visible = True
        self.interact = True

    def off(self):
        self.visible = False
        self.interact = False