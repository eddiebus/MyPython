import pygame

class Window:
    def __init__(self, width=300, height=300, sizeable=False, fullscreen = False):
        self.sizeableWindow = sizeable
        self.fullScreen = False

        self._fullscreenMask = False
        self._sizeableMask = False
        if sizeable == True:
            self._sizeableMask = pygame.RESIZABLE

        if fullscreen == True:
            self._fullscreenMask = pygame.FULLSCREEN


        self.display = pygame.display.set_mode((width, height), (self._sizeableMask | self._fullscreenMask))
        self.surface = pygame.display.get_surface()
        self.focus = False
        self.events = []
        self.mousePressed = []
        self.mouseDown = []
        self.mousePos = ()
        self.keyPressed = []
        self.keyDown = []
        self.clock = pygame.time.Clock()
        self.deltaTime = 0;
        self.fps = 0;

    # Set the window title
    def setTitle(self, name):
        pygame.display.set_caption(name)

    def setIcon(self, iconSurface):
        pygame.display.set_icon(iconSurface)

    # Get events,deltaTime and key input
    def update(self, framerate=60):
        self.clock.tick(framerate)
        self.focus = pygame.key.get_focused()
        self.events = pygame.event.get()
        self.fps = int(self.clock.get_fps())
        self.deltaTime = self.clock.get_time() / 1000

        self.keyDown = []
        self.mouseDown = []
        self.keyPressed = pygame.key.get_pressed()
        self.mousePressed = pygame.mouse.get_pressed()

        for e in self.events:
            if e.type == pygame.KEYDOWN:
                self.keyDown.append(e.key)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.mouseDown = pygame.mouse.get_pressed()
            elif e.type == pygame.VIDEORESIZE:
                self.surface = pygame.display.set_mode(
                    (e.w, e.h),
                    (
                        self._sizeableMask|
                        self._fullscreenMask
                    )
                )

    def flip(self):
        pygame.display.flip()

    def checkKeyDown(self, keyCode):
        for k in self.keyDown:
            if k == keyCode:
                return True

        return False

    # Get the window surface
    def getSurface(self):
        return pygame.display.get_surface()

    def toggleFullscreen(self):#
        if self.fullScreen:
            self.fullScreen = False
        else:
            self.fullScreen = True

        if self.fullScreen:
            self._fullscreenMask = pygame.FULLSCREEN
        else:
            self._fullscreenMask = False

        self.surface = pygame.display.set_mode(
            (
                self.getSurface().get_width(),
                self.getSurface().get_height()
            ),
            ( self._fullscreenMask)
        )

    # Close pygame
    def __del__(self):
        pygame.quit()
