import pygame
import random

pygame.init()

      
    
class gameScene:
    def update(self):
        pass

    def paint(self,surface):
        surface.fill( (0,0,0) )

class gameObj:
    xy = [0,0]
    xySpeed = [0,0]
    rect = pygame.Rect(0,0,0,0)
    def update(self):
        pass

    def paint(self,surface):
        pass


class window:
    font = pygame.font.Font(None,50)
    clock = pygame.time.Clock()
    clockSpeed = 60
    fps = 0
    loop = True
    focus = True
    mouseXY =  [0,0]
    mouseButton3 = 0
    mouseWheel  = 0
    display = pygame.display.set_mode((600,600))
    events = pygame.event.get()


    scene = gameScene()


    def update():
        window.clock.tick(window.clockSpeed)
        window.fps = int(window.clock.get_fps())
        window.mouseWheel   = 0
        window.mouseButton3 = 0
        window.mouseXY = pygame.mouse.get_pos()
        window.focus = pygame.key.get_focused()
        window.events = pygame.event.get()

        for e in window.events:
            if e.type == pygame.QUIT:
                window.loop = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    window.mouseWheel += 1
                if e.button == 5:
                    window.mouseWheel -= 1
                if e.button == 3:
                    window.mouseButton3 = 1


        if window.focus:
            window.scene.update()

    def paint():
        if window.focus:
            window.scene.paint(window.display)

        """
        window.display.blit(
            window.font.render("FPS = {0}".format(window.fps),0,(255,0,0),None),
            (0,0)
            )
        """
        pygame.display.flip()


class bubble(gameObj):
    def __init__(self,x,y,Size):
        self.size = Size 
        self.xy = [x,y]
        Dir = [1,-1]
        self.xySpeed = [ random.randint(1,5) * Dir[random.randint(0,1)] , random.randint(1,5) * Dir[random.randint(0,1)] ] 
        self.rect = pygame.Rect(
            x - Size/2,
            y - Size/2,
            Size,
            Size
            )

        self.colour = [ random.randint(0,255), random.randint(0,255), random.randint(0,255)]

    def update(self):
        self.rect = self.rect.move( self.xySpeed[0],self.xySpeed[1] )
        self.xy = self.rect.center

    def paint(self,surface):
        pygame.draw.circle(surface,self.colour,self.xy, self.size,0)

class mainScene(gameScene):
    overlaySurface = pygame.Surface( (window.display.get_width() ,window.display.get_height()), pygame.HWSURFACE )
    overlaySurface.set_colorkey( (0,255,0) )
    bubbles = []

    viewSize = 100
    for i in range(0,50):
        width = window.display.get_width()
        height = window.display.get_height()
        bubbles.append(bubble( random.randint(0,width), random.randint(0,height), random.randint(50,100) ) )

    def update(self):
        self.viewSize += window.mouseWheel * 10
        if self.viewSize < 0 : self.viewSize = 0
        if window.mouseButton3:
            self.viewSize = 100
        for b in self.bubbles:
            b.update()
            if b.rect.left < 0:
                b.rect = pygame.Rect(
                    0,
                    b.rect.top,
                    b.rect.width,
                    b.rect.height
                    )
                b.xySpeed[0] = b.xySpeed[0] * -1
            if b.rect.right > window.display.get_width():
                b.rect = pygame.Rect(
                    window.display.get_width() - b.rect.width,
                    b.rect.top,
                    b.rect.width,
                    b.rect.height
                    )
                b.xySpeed[0] = b.xySpeed[0] * -1
            if b.rect.top < 0:
                b.rect = pygame.Rect(
                    b.rect.left,
                    0,
                    b.rect.width,
                    b.rect.height
                    )
                b.xySpeed[1] = b.xySpeed[1] * -1
            if b.rect.bottom > window.display.get_height():
                b.rect = pygame.Rect(
                    b.rect.left,
                    window.display.get_height() - b.rect.height,
                    b.rect.width,
                    b.rect.height
                    )
                b.xySpeed[1] = b.xySpeed[1] * -1

    def paint(self,surface):
        surface.fill( (255,255,255) )

        for b in self.bubbles:
            b.paint(surface)
            
        self.overlaySurface.fill( (0,0,0) )
        pygame.draw.circle(self.overlaySurface,( (0,255,0) ),window.mouseXY,self.viewSize,0)                                
        surface.blit( self.overlaySurface, (0,0) )
            
window.scene = mainScene()
while (window.loop):
    window.update()
    window.paint()



pygame.quit()

