"""2 Player Pong"""
import pygame
import random
pygame.init()


print("Start!")

class App():
  level = None
  clock = pygame.time.Clock()
  clockspeed = 60
  loop = True
  display = pygame.display.set_mode((300,300),(pygame.HWSURFACE|pygame.RESIZABLE))
  displayWH = [display.get_width(),display.get_height()]

  surface = pygame.Surface((600,600),pygame.HWSURFACE)

  keys = pygame.key.get_pressed()
  events = pygame.event.get()
  bgColour = [100,100,100]
  font  = pygame.font.Font("Font/arial.ttf",100)

  def update():
    App.clock.tick(App.clockspeed)
    App.keys = pygame.key.get_pressed() 
    App.events = pygame.event.get()
    for e in App.events:
      if e.type == pygame.QUIT:
        App.loop = False
      if e.type == pygame.KEYUP:
        if e.key == pygame.K_ESCAPE:
          App.loop = False
      if e.type == pygame.VIDEORESIZE:
        App.display = pygame.display.set_mode((e.w,e.h),(pygame.HWSURFACE|pygame.RESIZABLE))
        App.displayWH = [App.display.get_width(),App.display.get_height()]
    
    if App.level:
      level.update()
  
  def paint():
    App.surface.fill((0,0,0))

    for i in range(0,len(App.bgColour)):
      if random.random() > 0.5:
        App.bgColour[i]  += 0.5
      else: App.bgColour[i] -= 0.5
      
      if App.bgColour[i] <   0: App.bgColour[i] = 0
      if App.bgColour[i] > 255: App.bgColour[i] = 255

    App.surface.fill(App.bgColour)

    if App.level:
      App.level.paint(App.surface)

      App.display.fill((0,0,0,0))
    
      App.display.blit(
       pygame.transform.scale(App.surface,App.displayWH), 
       (0,0)
        )
      
      pygame.display.flip()


class GameObject():
  def create():
    return 0
  def update():
    return 0
  
  def paint():
    return 0

class players(GameObject):
  vsCPU = False
  playArea = pygame.Rect(0,0,600,600)
  playing = True
  y =[0,0]
  defaultSpeed = 18
  speed = [defaultSpeed]*2
  score = [0,0]
  rect = [pygame.Rect(0,0,0,0)] * 2

  defaultSize = [20,120]
  xySize = [defaultSize] * 2
  sizeMod = [0]

  colour = [(0,0,255),(255,0,0)]
  margin = 5
  def create(playArea):
    xySize = players.xySize
    players.rect = [
      pygame.Rect(
        playArea.left, 
        playArea.centery - players.xySize[0][1]/2,
        players.xySize[0][0],
        players.xySize[0][1]
      ),
      pygame.Rect(
        playArea.right - players.xySize[1][0],
        playArea.centery - players.xySize[0][1]/2,
        players.xySize[1][0],
        players.xySize[1][1]
        )
      ]

  upKey = [pygame.K_w,pygame.K_UP]
  downKey = [pygame.K_s,pygame.K_DOWN]


  defaultRect = pygame.Rect(
    0,0,2,100
  )

  def update():
    for i in range(0,2):
      if   App.keys[players.upKey[i]]:
        players.rect[i] = players.rect[i].move(0,-players.speed[i])
      elif App.keys[players.downKey[i]]:
        players.rect[i] = players.rect[i].move(0, players.speed[i])
      
      playArea = players.playArea
      while players.rect[i].top    < playArea.top:
        players.rect[i] = players.rect[i].move(0,  1)
      while players.rect[i].bottom > playArea.bottom:
        players.rect[i] = players.rect[i].move(0, -1)
      
      players.y[i] = players.rect[i].centery
      
  def paint(surface):
      pygame.draw.rect(
        surface,
        players.colour[0],
        players.rect[0]
      )

      pygame.draw.rect(
        surface,
        players.colour[1],
        players.rect[1]
      )

class ball(GameObject):
  inactiveFrames = 0
  xy = [0,0]
  size  = 50
  rect = pygame.Rect(0,0,0,0)
  defSpeed = 5
  spawnDir = 1
  xySpeed = [0,0]

  colour = [0,255,0]

  def create(playArea):
    ball.inactiveFrames = 100
    ball.rect = pygame.Rect(
      playArea.centerx - ball.size/2,
      playArea.centery - ball.size/2,
      ball.size,
      ball.size )
    
    defSpeed = ball.defSpeed
    direct = [1,-1]
    ball.xySpeed = [ defSpeed * direct[random.randint(0,1)], defSpeed * direct[random.randint(0,1)] ]

  def reset(playArea,direction):
    """put ball in center of playArea, direction can be 1 or -1"""
    ball.inactiveFrames = 100
    ball.rect = pygame.Rect(
      playArea.centerx - ball.size/2,
      playArea.centery - ball.size/2,
      ball.size,
      ball.size )
    
    defSpeed = ball.defSpeed
    direct = [1,-1]
    ball.xySpeed = [ defSpeed * direction, defSpeed * direct[random.randint(0,1)] ]


  def update():
    if ball.inactiveFrames > 0:
      ball.inactiveFrames -= 1
    else:
      ball.rect  = ball.rect.move(ball.xySpeed[0],ball.xySpeed[1])
      ball.xy = [ball.rect.centerx,ball.rect.centery]
  def paint(surface):
    colourS = (abs(ball.xySpeed[0])-ball.defSpeed) / (ball.defSpeed*1.5)
    if colourS > 1: colourS = 1
    ball.colour = [255*colourS,255-255*colourS,0]
    pygame.draw.rect(surface,ball.colour,ball.rect)
    
class level():
  playArea = pygame.Rect(0,0,600,600)
  ball.create(playArea)
  players.create(playArea)
  def update():
    players.update()
    ball.update()

    if   ball.rect.top < level.playArea.top:
      ball.rect = pygame.Rect(
        ball.rect.left,
        level.playArea.top,
        ball.size,
        ball.size)
      ball.xySpeed[1] = ball.xySpeed[1] * -1
    elif ball.rect.bottom > level.playArea.bottom:
      ball.rect = pygame.Rect(
        ball.rect.left,
        level.playArea.bottom - ball.size,
        ball.size,
        ball.size)
      ball.xySpeed[1] = ball.xySpeed[1] * -1
    #Player 2 goal
    elif ball.rect.right < level.playArea.left:
      players.score[1] += 1
      ball.reset(level.playArea, -1)
    #player 1 goal
    elif ball.rect.left > level.playArea.right:
      players.score[0] += 1
      ball.reset(level.playArea, 1)
    
    #player collision
    for i in range(0,2):
      if ball.rect.colliderect(players.rect[i]):
        addOn = 0.5
        if ball.xySpeed[0] > 0:
          ball.xySpeed[0] += addOn
        else: 
          ball.xySpeed[0] -= addOn
        
        ball.xySpeed[0] = ball.xySpeed[0] * -1
      
      while ball.rect.colliderect(players.rect[i]):
        if i == 0:
          ball.rect = ball.rect.move(1,0)
        else:
          ball.rect = ball.rect.move(-1,0)
        
    
        
    
  def paint(surface):
    surface.fill((50,50,50))

    #Draw text
    textSurface = []
    string = [ str(players.score[0]),"-",str(players.score[1]) ]
    stringColour = [players.colour[0],(0,0,0),players.colour[1]]
    totalWidth  = 0
    totalHeight = 0
    for i in range(len(string)):
      textSurface.append(
        App.font.render(
          string[i],
          2,
          stringColour[i],
          None 
        )
      
      )

      totalWidth += int(textSurface[-1].get_width())
      totalHeight = int(textSurface[-1].get_height())
    

    rSurface = pygame.Surface((totalWidth,totalHeight),pygame.SRCALPHA,None)

    for i in range(len(textSurface)):
      spacing = 0
      if i > 0:
        for s in range(0,i):
          spacing += textSurface[s].get_width()
      
      rSurface.blit(
        textSurface[i],
        (spacing,0),
        None, 0
      )
    
    surface.blit(
      rSurface,
      (
        level.playArea.centerx - rSurface.get_width()/2,
        level.playArea.centery - rSurface.get_height()/2
      ),
      None,0
    )

    #Draw player and ball
    players.paint(surface)
    ball.paint(surface)


while App.loop:
  App.level = level
  App.update()
  App.paint()

pygame.quit()


print("End")
