import random

import pygame
import pygame.font
import pygame.gfxdraw
import PyGameObject
import PyGameWindow
import PyGameCamera

class TextLabel(PyGameObject.GameObject):
    def __init__(self, pygameFont = pygame.font.Font, text = ""):
        self.x = 0
        self.y = 0
        self._Font = pygameFont
        self._renderedTexture = None
        self._Height = 10
        self._Width = 0
        self._Colour = pygame.Color(255,255,255)
        self._Alpha = 1;
        self._Text = text

        self._updateTexture()

    def getWidth(self):
        return self._renderedTexture.get_width()

    def getHeight(self):
        return self._renderedTexture.get_height()

    def setHeight(self,newHeight):
        """
        Set the height of the label
        :param newHeight:
        :return:
        """
        self._Height = newHeight
        self._updateTexture()

    def _updateTexture(self):
        """
        Update the lables texture and update width property.
        :return: None
        """
        self._renderedTexture = self._Font.render(
            self._Text,
            True,
            self._Colour
        )

        initFontHeight = self._Font.get_height()
        scale = self._Height/initFontHeight

        renderSize = [
            self._renderedTexture.get_width(),
            self._renderedTexture.get_height()
        ]

        newSize = [
            int(renderSize[0] * scale),
            int(renderSize[1] * scale)
        ]

        self._renderedTexture = pygame.transform.scale(
            self._renderedTexture,
            (newSize[0],newSize[1])
        )

        self._Width = self._renderedTexture.get_width()

    def paint(self, targetSurface = pygame.Surface):
        copySurface = self._renderedTexture.copy()
        copySurface.set_alpha(int(255 * self._Alpha))

        targetSurface.blit(
            copySurface,
            (self.x,self.y)
        )

class WordDictionary:
    def __init__(self):
        WordsFile = open("words.txt")
        self._WordList = [""]
        for char in WordsFile.read():
            if char == '\n':
                self._WordList[-1] = self._WordList[-1].upper()
                self._WordList.append("")
            else:
                self._WordList[-1] = self._WordList[-1] + char

        copyList = self._WordList
        self._WordList = []

        for word in copyList:
            okWord = True
            for char in word:
                if not char.upper() or char == "'":
                    okWord = False
            if okWord:
                self._WordList.append(word)


    def GetRandomWord(self):
        index = int (random.random() * (len(self._WordList) - 1))
        return self._WordList[index]

class CharacterSprites:
    def __init__(self, fontFileAddress):
        self._minChar = 'A'
        self._maxChar = 'Z'
        font = pygame.font.Font(fontFileAddress,100)
        self.spriteTexture = []
        for i in range(ord(self._minChar) ,ord(self._maxChar) + 1):
            self.spriteTexture.append(
                pygame.surface.Surface(
                    (150,150)
                )
            )

            charRender = font.render(
                chr(i),
                True,
                pygame.Color(0,0,0)
            )

            renderWidth = charRender.get_width()
            renderHeight = charRender.get_height()

            spriteCenterX = self.spriteTexture[-1].get_width()/2
            spriteCenterY = self.spriteTexture[-1].get_height()/2

            self.spriteTexture[-1].fill(
                pygame.Color(100,100,100)
            )

            self.spriteTexture[-1].blit(
                charRender,
                (
                    spriteCenterX - renderWidth/2,
                    spriteCenterY - renderHeight/2
                )
            )

    def draw(self, targetSurface, character,point, size,alpha = 1):
        character = character.upper()
        charNumber = ord(character)

        # Check if a valid character is given
        if len(character) != 1:
            return
        elif (charNumber < ord(self._minChar)) or (charNumber > ord(self._maxChar)):
            return

        charNumber -= ord(self._minChar)
        spriteCopy = self.spriteTexture[charNumber].copy()

        spriteCopy = pygame.transform.scale(
            spriteCopy,
            (int(size),int(size))
        )

        targetSurface.blit(
            spriteCopy,
            point
        )

class WordEnemy(PyGameObject.GameObject):
    def __init__(self,word):
        self._Word = word
        self._CurrentCharIndex = 0
        self._MissType = 0

        self._CursorX = 0

        self.Value = 0

        uniquechar = []
        for char in word:
            if char not in uniquechar:
                uniquechar.append(char)

        self.Value += len(uniquechar) * 10

    def getWord(self):
        return self._Word

    def update(self, gameWindow = PyGameWindow.Window()):
        # Player has already typed all characters
        if not self.CheckHP():
            return

        # check if character has been pressed
        currentChar = self._Word[self._CurrentCharIndex]

        for key in gameWindow.keyDown:
            keyName = pygame.key.name(key)
            keyName = keyName.upper()
            if keyName == currentChar:
                self._CurrentCharIndex += 1
            else:
                self._MissType += 1

        if self._CursorX < self._CurrentCharIndex:
            self._CursorX += gameWindow.deltaTime * 10
            if self._CursorX > self._CurrentCharIndex:
                self._CursorX = self._CurrentCharIndex

        elif self._CursorX > self._CurrentCharIndex:
            self._CursorX -= gameWindow.deltaTime * 10
            if self._CursorX < self._CurrentCharIndex:
                self._CursorX = self._CurrentCharIndex

    def CheckHP(self):
        return len(self._Word) - (self._CurrentCharIndex)

    def getMissTypes(self):
        return self._MissType


    def paint(self,targetCamera = PyGameCamera.Camera, size = 100, characterSprite = CharacterSprites):
        charCount = len(self._Word)
        renderWidth = charCount * size

        drawPoints = []
        for i in range(charCount):
            xOffset = size * (i - (charCount/2))
            drawPoints.append((xOffset,-size/2))

        tPoint = []
        for i in range(charCount):
            tPoint.append(targetCamera.transformPoint(drawPoints[i]))
            characterSprite.draw(
                targetCamera.getSurface(),
                self._Word[i],
                tPoint[i],
                size
            )

        CursorSize = size/2
        CursorPointX = size * (self._CursorX -(charCount/2))
        CursorPointX += size/2
        CursorPointY = -size * 1.1

        triRenderPoints = [
            (
                CursorPointX - CursorSize/2,
                CursorPointY - CursorSize/2,
            ),
            (
                CursorPointX + CursorSize/2,
                CursorPointY - CursorSize/2
            )
            ,
            (
                CursorPointX,
                CursorPointY + CursorSize/2
            )
        ]

        for i in range(len(triRenderPoints)):
            triRenderPoints[i] = targetCamera.transformPoint(triRenderPoints[i])

        cursorTPoint = targetCamera.transformPoint((CursorPointX,CursorPointY))

        pygame.gfxdraw.filled_polygon(
            targetCamera.getSurface(),
            triRenderPoints,
            pygame.Color(255,0,0)
        )

class ScoreCard(PyGameObject.GameObject):
    def __init__(self):
        self.Score = 0
        self._displayScore = 0

        self.renderText = ""

    def update(self, gameWindow):
        if self._displayScore < self.Score:
            self._displayScore += 120 * gameWindow.deltaTime
            if self._displayScore > self.Score:
                self._displayScore = self.Score
        elif self._displayScore > self.Score:
            self._displayScore -= 120 * gameWindow.deltaTime
            if self._displayScore < self.Score:
                self._displayScore = self.Score


    def paint(self,pygameFont = pygame.font.Font,camera = PyGameCamera.Camera):
        renderedText = pygameFont.render(
            F"{int(self._displayScore)}",
            True,
            pygame.Color(255,255,255)
        )

        renderedTextSize = (renderedText.get_width(),renderedText.get_height())

        cameraSurfaceSize = camera.getCameraSize()

        renderPoint = (
            (cameraSurfaceSize[0] / 2) - renderedTextSize[0]/2,
            0
        )

        camera.getSurface().blit(
            renderedText,
            renderPoint
        )

    def SetScore(self,newScore):
        self.Score = newScore

class StaminaCard(PyGameObject.GameObject):
    def __init__(self):
        self._HP = 100
        self._Width = 1000
        self._Height = 55

        self._HealStep = 10
        self._LossStep = 2
        self._HealFlash = 0

    def update(self,gameWindow):
        if self._HP > 0:
            self._HP -= gameWindow.deltaTime * self._LossStep
            if self._HP < 0:
                self._HP = 0

        self._HealFlash -= gameWindow.deltaTime
        if self._HealFlash < 0:
            self._HealFlash = 0

    def paint(self,testCamera = PyGameCamera.Camera):
        cameraSurface = testCamera.getSurface()
        cameraSurfaceSize = testCamera.getSurfaceSize()

        renderPoint = (
            (cameraSurfaceSize[0] / 2 ) - (self._Width * self._HP /100)/2,
            cameraSurfaceSize[1] * 0.8 - (self._Height/2)
        )

        renderRect = pygame.Rect(
            renderPoint,
            (
                self._Width * (self._HP / 100),
                self._Height
            )
        )


        green = int(255 * self._HealFlash)
        red = int(255 - (255 * self._HealFlash))
        pygame.draw.rect(
            cameraSurface,
            pygame.Color(red,green,0,255),
            renderRect
        )

    def heal(self):
        if not self._HP:
            return
        self._HP += self._HealStep
        if self._HP > 100:
            self._HP = 100

        self._HealFlash = 1

    def speedUP(self,gameWindow):
        self._LossStep += gameWindow.deltaTime * 65

    def getHP(self):
        return self._HP

class ReportCard(PyGameObject.GameObject):
    def __init__(self, pygameFont = pygame.font.Font):
        self._BackgroundBox = pygame.Surface((100,100))
        self._BackgroundSize = [0,0]
        self._BackgroundBox.fill(
            pygame.Color(0,0,0)
        )

        self._YFill = 0

        self._Font = pygameFont

        self._ScoreResult = 0
        self._DisplayScore = 0

        self._WordCountResult = 0
        self._DisplayWordCount = 0

        self._ResultLabel = TextLabel(pygameFont,"RESULTS")
        self._ResultLabel.setHeight(100)

    def update(self,gameWindow, targetCamera = PyGameCamera.Camera):
        targetSize = targetCamera.getCameraSize()

        self._BackgroundSize[0] = targetSize[0]

        if self._YFill < 1:
            self._YFill += gameWindow.deltaTime;

        if self._BackgroundSize[1] < targetSize[1]:
            self._BackgroundSize[1] += targetSize[1] * (gameWindow.deltaTime * 2)

    def paint(self,targetCamera = PyGameCamera.Camera):
        BackgroundBox = pygame.transform.scale(
            self._BackgroundBox,
            (int(self._BackgroundSize[0]),int(targetCamera.getSurfaceSize()[1] * self._YFill))
        )

        self._BackgroundSize[1] = BackgroundBox.get_size()[1]
        camSize = targetCamera.getCameraSize()

        renderPoint = [
            camSize[0]/2,
            camSize[1]/2
        ]

        renderPoint[0] -= self._BackgroundSize[0]/2
        renderPoint[1] -= self._BackgroundSize[1]/2

        targetCamera.getSurface().blit(
            BackgroundBox,
            (renderPoint[0],renderPoint[1])
        )

        self._ResultLabel.x = self._BackgroundSize[0]/2 - self._ResultLabel.getWidth()/2
        self._ResultLabel.y = (targetCamera.getSurface().get_height()/2) - self._BackgroundSize[1]/2

        if self._YFill >= 1:
            self._ResultLabel.paint(targetCamera.getSurface())

class MainScene(PyGameObject.GameObject):
    def __init__(self):
        self.TextFont = pygame.font.Font("Font\\arial.ttf",100)
        self._Dictionary = WordDictionary()
        self._SelectedWord = WordEnemy(
            self._Dictionary.GetRandomWord()
        )

        self._WordRenderHeight = 100
        self._letterSprites = CharacterSprites("Font\\arial.ttf")
        self._ScoreCard = ScoreCard()

        self._Camera = PyGameCamera.Camera()
        self._Camera.setSurfaceSize(1280,720)
        self._Camera.setCameraSize(1280,720)

        self._Score = 0
        self._CharsTyped = 0
        self._WordsTyped = 0
        self._Typos = 0
        self._StaminaCard = StaminaCard()


        self._GameReportCard = ReportCard(self.TextFont)

    def update(self, gameWindow):
        # Check the word
        self._SelectedWord.update(gameWindow)
        if self._SelectedWord.CheckHP() == 0:
            self._Score += self._SelectedWord.Value
            self._SelectedWord = WordEnemy(self._Dictionary.GetRandomWord())
            self._StaminaCard.heal()
            self._StaminaCard.speedUP(gameWindow)

            self._CharsTyped += len(self._SelectedWord.getWord())
            self._WordsTyped += 1

        self._Typos = self._SelectedWord.getMissTypes()
        print(F"TYpos = {self._Typos}")

        # Set scorecard
        self._ScoreCard.SetScore(self._Score)
        self._ScoreCard.update(gameWindow)

        # Decrease Stamina
        self._StaminaCard.update(gameWindow)

        if self._StaminaCard.getHP() <= 0:
            self._GameReportCard.update(gameWindow,self._Camera)


    def paint(self, gameWindow):
        targetSurface = gameWindow.getSurface()
        self._Camera.getSurface().fill(
            pygame.Color(51, 168, 181)
        )
        renderCharCount = len(self._SelectedWord._Word)
        if renderCharCount < 5:
            renderCharCount = 5
        targetRenderWidth = self._Camera.getCameraSize()[0] * 0.75
        targetRenderHeight = targetRenderWidth / renderCharCount

        # Word is being rendered too big
        if self._WordRenderHeight > targetRenderHeight:
            self._WordRenderHeight -= gameWindow.deltaTime * 300
            if self._WordRenderHeight < targetRenderHeight:
                self._WordRenderHeight = targetRenderHeight

        # Word is being rendered too small
        elif self._WordRenderHeight < targetRenderHeight:
            self._WordRenderHeight += gameWindow.deltaTime * 300
            if self._WordRenderHeight > targetRenderHeight:
                self._WordRenderHeight = targetRenderHeight

        self._SelectedWord.paint(
            self._Camera,
            self._WordRenderHeight,
            self._letterSprites
        )

        self._ScoreCard.paint(self.TextFont,self._Camera)
        self._StaminaCard.paint(self._Camera)

        if self._StaminaCard.getHP() == 0:
            self._GameReportCard.paint(self._Camera)

        targetSurface.blit(
            self._Camera.getSurface(),
            (0,0)
        )





