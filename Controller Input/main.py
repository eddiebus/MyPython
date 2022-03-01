import pygame
import PyGameWindow
import PyGameGamePad


MainWindow = PyGameWindow.Window(1280,720)
AppLoop = True

GamePadManager = PyGameGamePad.GamePadMapper()

while AppLoop:
    MainWindow.update(0)
    GamePadManager.update(MainWindow.events)
    xboxLayout = GamePadManager.toXBoxLayout(0)
    if xboxLayout:
        print(xboxLayout.getDebugString())
        print(F"GamePadName = {GamePadManager.getGamePadName(0)}")





    for e in MainWindow.events:
        if e.type == pygame.QUIT:
            AppLoop = False

    MainWindow.getSurface().fill(
        pygame.Color(0,0,0)
    )
    MainWindow.flip()





