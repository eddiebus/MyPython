import pygame

#GamePad blueprint base
class GamePad:
    def __init__(self,GamePadObject = pygame.joystick.Joystick):
        self._GamePadObject = GamePadObject
        self._GamePadName =self._GamePadObject.get_name()
        self._PowerLevel = 0
        self._SlotID = 0
        self._ButtonCount = self._GamePadObject.get_numbuttons()
        self._AxisCount = self._GamePadObject.get_numaxes()
        self._HatCount = self._GamePadObject.get_numhats()

        self.update()

        self._ButtonPress = []
        self._ButtonUP = []
        self._ButtonDown = []
        self._AxisValue = []
        self._HatValue = []

    def getGamePadName(self):
        return self._GamePadName
    def getPowerLevel(self):
        return self._PowerLevel

    def quit(self):
        self._GamePadObject.quit()

    def getButtonCount(self):
        return self._ButtonCount
    def getAxisCount(self):
        return self._AxisCount
    def getHatCount(self):
        return self._HatCount

    def getButton(self):
        return self._ButtonPress

    def getButtonDown(self):
        return self._ButtonDown

    def getButtonUp(self):
        return self._ButtonUP

    def getAxis(self):
        return self._AxisValue

    def getHat(self):
        return self._HatValue

    def setRumble(self,lowIntensity,highIntensity,duration):
        return self._GamePadObject.rumble(lowIntensity,highIntensity,duration)

    def update(self, windowEvents = []):
        self._PowerLevel = self._GamePadObject.get_power_level()
        self._SlotID = self._GamePadObject.get_instance_id()

        self._ButtonPress = []
        for index in range(self._ButtonCount):
            if self._GamePadObject.get_button(index):
                self._ButtonPress.append(index)

        self._HatValue = []
        for hat in range(self._HatCount):
            self._HatValue.append(self._GamePadObject.get_hat(hat))

        self._AxisValue = []
        for axis in range(self._AxisCount):
            self._AxisValue.append(self._GamePadObject.get_axis(axis))

        self._ButtonDown = []
        self._ButtonUP = []

        for event in windowEvents:
            if event.type == pygame.JOYBUTTONDOWN:
                if self._SlotID == event.instance_id:
                    self._ButtonDown.append(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                if self._SlotID == event.instance_id:
                    self._ButtonUP.append(event.button)

class GamePad2XBox:
    def __init__(self,GamePadRef = GamePad):
        self.DPadUP = [False,False,False]
        self.DPadDown = [False,False,False]
        self.DPadLeft = [False,False,False]
        self.DPadRight = [False,False,False]

        self.ButtonA = [False,False,False]
        self.ButtonB = [False,False,False]
        self.ButtonX = [False,False,False]
        self.ButtonY = [False,False,False]

        self.LeftBumper = [False,False,False]
        self.RightBumper = [False,False,False]

        self.StartButton = [False,False,False]
        self.BackButton = [False,False,False]

        self.LeftStick = [0,0]
        self.RightStick = [0,0]

        self.LeftTrigger = 0
        self.RightTrigger = 0

        self.LeftStickButton = [False, False, False]
        self.RightStickButton = [False, False, False]
        # Button Holds
        for button in GamePadRef.getButton():
            if   button == 0:
                self.ButtonA[0] = True
            elif button == 1:
                self.ButtonB[0] = True
            elif button == 2:
                self.ButtonX[0] = True
            elif button == 3:
                self.ButtonY[0] = True
            elif button == 4:
                self.LeftBumper[0] = True
            elif button == 5:
                self.RightBumper[0] = True
            elif button == 6:
                self.BackButton[0] = True
            elif button == 7:
                self.StartButton[0] = True
            elif button == 8:
                self.LeftStickButton[0] = True
            elif button == 9:
                self.RightStickButton[0] = True
        # Button Press
        for button in GamePadRef.getButtonDown():
            if   button == 0:
                self.ButtonA[1] = True
            elif button == 1:
                self.ButtonB[1] = True
            elif button == 2:
                self.ButtonX[1] = True
            elif button == 3:
                self.ButtonY[1] = True
            elif button == 4:
                self.LeftBumper[1] = True
            elif button == 5:
                self.RightBumper[1] = True
            elif button == 6:
                self.BackButton[1] = True
            elif button == 7:
                self.StartButton[1] = True
            elif button == 8:
                self.LeftStickButton[1] = True
            elif button == 9:
                self.RightStickButton[1] = True
        # Button Release
        for button in GamePadRef.getButtonUp():
            if   button == 0:
                self.ButtonA[2] = True
            elif button == 1:
                self.ButtonB[2] = True
            elif button == 2:
                self.ButtonX[2] = True
            elif button == 3:
                self.ButtonY[2] = True
            elif button == 4:
                self.LeftBumper[2] = True
            elif button == 5:
                self.RightBumper[2] = True
            elif button == 6:
                self.BackButton[2] = True
            elif button == 7:
                self.StartButton[2] = True
            elif button == 8:
                self.LeftStickButton[2] = True
            elif button == 9:
                self.RightStickButton[2] = True

        if len(GamePadRef.getHat()) == 1:
            hat = GamePadRef.getHat()[0]
            if   hat[0] < 0:
                self.DPadLeft[0] = True
            elif hat[0] > 0:
                self.DPadRight[0] = True
            elif hat[1] < 0:
                self.DPadDown[0] = True
            elif hat[1] > 0:
                self.DPadUP[0] = True

        # Xbox GamePad has at 6 axis
        if len(GamePadRef.getAxis()) == 6:
            axisValue = GamePadRef.getAxis()
            # A Joystick can never perfectly align to 0,0
            deadZone = 0.1
            for stickAxis in range(4):
                if axisValue[stickAxis] > -deadZone and axisValue[stickAxis] < deadZone:
                    axisValue[stickAxis] = 0

            for stickAxis in range(2):
                axisValue[4 + stickAxis] += 1
                axisValue[4 + stickAxis] *= 0.5
                # Trigger may not be able to reach 1 exactly, so clamp it
                if axisValue[4 + stickAxis] > 0.99:
                    axisValue[4 + stickAxis] = 1

            self.LeftStick[0] = axisValue[0]
            self.LeftStick[1] = - axisValue[1]
            self.RightStick[0] = axisValue[2]
            self.RightStick[1] = - axisValue[3]

            self.LeftTrigger = axisValue[4]
            self.RightTrigger = axisValue[5]


    def getDebugString(self):
        debugString = "Xbox button and values:\n"
        debugString += F"Stick/Triggers:\n"
        debugString += F"LeftStick {self.LeftStick}\n"
        debugString += F"RightStick {self.RightStick}\n"
        debugString += F"LeftTrigger {self.LeftTrigger}\n"
        debugString += F"RightTrigger {self.RightTrigger}\n"

        return debugString

class GamePadMapper:
    def __init__(self):
        pygame.joystick.init()
        self._rumbleSupport = False
        self._gamepadCount = 0
        self._slotObject = []
        pygameVersion = pygame.version.SDL

        #Check pygame version for rumble support
        if pygameVersion[0] >= 2 and pygameVersion[2] >= 10:
            self._rumbleSupport = True

    def toXBoxLayout(self,slot):
        if self.checkSlot(slot):
            return GamePad2XBox(self._slotObject[slot])

    def update(self,windoweventList = []):
        self._gamepadCount = pygame.joystick.get_count()

        if len(self._slotObject) != self._gamepadCount:
            #disconnect existing gamepads
            for object in self._slotObject:
                self._slotObject[0].quit()

            self._slotObject = []

            for index in range(self._gamepadCount):
                NewGamePad = pygame.joystick.Joystick(index)
                self._slotObject.append(
                    GamePad(NewGamePad)
                )

        for object in self._slotObject:
            object.update(windoweventList)

    def getGamePadName(self, slot):
        if self.checkSlot(slot):
            return self._slotObject[slot].getGamePadName()

    def getPowerLevel(self,slot):
        if self.checkSlot(slot):
            return self._slotObject[slot].getPowerLevel()

    def startRumble(self, slot, lIntensity, hIntensity, duration):
        if self.checkSlot(slot) and self._rumbleSupport:
            self._slotObject[slot].setRumble(lIntensity, hIntensity, duration)

    # Check device is on slot
    def checkSlot(self,slot):
        if slot < len(self._slotObject):
            return True
        else:
            return False





