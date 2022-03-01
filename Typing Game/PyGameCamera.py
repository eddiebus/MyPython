import pygame


class Camera:
    def __init__(self, x=0, y=0, width=100, height=100):
        self.x = x
        self.y = y
        self._width = width
        self._height = height

        self._textureSurface = pygame.Surface((width, height), pygame.SRCALPHA)

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setCameraSize(self, width, height):
        self._width = width
        self._height = height

    def setSurfaceSize(self, width, height):
        self._textureSurface = pygame.Surface((width, height), pygame.SRCALPHA)

    def getCameraSize(self):
        return (self._width,self._height)

    def getSurfaceSize(self):
        return (
            self._textureSurface.get_width(),
            self._textureSurface.get_height()
        )

    def getSurface(self):
        return self._textureSurface

    def clearSurface(self):
        self._textureSurface.fill(
            pygame.Color(0,0,0)
        )

    def transformPoint(self,pointTuple = (0,0)):
        pointX = pointTuple[0]
        pointY = pointTuple[1]

        pointX -= self.x + -self._width/2
        pointY += self.y + self._height/2

        pointX = (pointX / self._width) * self._textureSurface.get_width()
        pointY = (pointY / self._height) * self._textureSurface.get_height()

        return (pointX,pointY)

    def transformRect(self, inputRect=pygame.Rect(0, 0, 0, 0)):
        """
        Transform a pygame rect to the projection of a camera.
        :param inputRect: The rect to transform
        :return: The result of transformation
        """
        rectX = inputRect.centerx
        rectY = inputRect.centery
        rectWidth = inputRect.width
        rectHeight = inputRect.height

        # translate rect
        rectX -= self.x + -self._width/2
        rectY += self.y + self._height/2

        rectX = (rectX / self._width) * self._textureSurface.get_width()
        rectY = (rectY / self._height) * self._textureSurface.get_height()

        # project rectangle width and height
        rectWidth = rectWidth / self._width
        rectHeight = rectHeight / self._height

        # scale projection to textureSize
        rectWidth *= self._textureSurface.get_width()
        rectHeight *= self._textureSurface.get_height()

        returnRect = pygame.Rect(
            rectX - rectWidth/2,
            rectY - rectHeight/2,
            rectWidth,
            rectHeight
        )

        return returnRect


