import pygame

import PyGameCamera
import PyGameObject
import GameScenes
import PyGameWindow
pygame.init()

AppWidth = 1280
AppHeight = 720

DebugFont = pygame.font.Font(
    "Font\\arial.ttf",
    50
)

typingString = ""
if __name__ == '__main__':
    MainWindow = PyGameWindow.Window(1280,720,False)
    Apploop = True

    Scene = GameScenes.MainScene()
    while Apploop:
        MainWindow.update(60)

        for event in MainWindow.events:
            if event.type == pygame.QUIT:
                Apploop = False

        Scene.update(MainWindow)
        if MainWindow.checkKeyDown(pygame.K_F10):
            MainWindow.toggleFullscreen()


        MainWindow.getSurface().fill(pygame.Color(50,50,50))
        Scene.paint(MainWindow)
        MainWindow.flip()
