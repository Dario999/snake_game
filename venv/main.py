import pygame
from random import randrange
import enum
from datetime import datetime
import time

pygame.init()
screen = pygame.display.set_mode((600,600))
playerImg = pygame.image.load('snake.png')
tailImg = pygame.image.load('snake1.png')
appleImg = pygame.image.load('apple.png')


snakeX = 60
snakeY = 0
tail = [(0,0)]
appleX = 60
appleY = 120
appleEaten = False
direction = 1
refreshTime = datetime.now().time()

def drawTail(tail):
    for temp in tail:
        screen.blit(tailImg,temp)


def moveInDirection(direction):
    time.sleep(0.5)
    global snakeX
    global snakeY
    global tail
    if direction == 1:
        snakeY += 60
    elif direction == 2:
        snakeY -= 60
    elif direction == 3:
        snakeX += 60
    elif direction == 4:
        snakeX -= 60
    tail.append((snakeX, snakeY))
    tail.pop(0)
    # drawTail(tail)


def drawSnake(x,y):
    screen.blit(playerImg,(x,y))

def drawApple(x,y):
    screen.blit(appleImg,(x,y))


def checkEaten():
    global snakeX
    global snakeY
    global appleX
    global appleY
    global appleEaten
    if snakeX == appleX and snakeY == appleY:
        appleEaten = True
    else:
        appleEaten = False

def moveUp():
    global snakeY
    global snakeX
    global tail
    snakeY -= 60
    tail.append((snakeX,snakeY))
    tail.pop(0)

def moveDown():
    global snakeY
    global snakeX
    global tail
    snakeY += 60
    tail.append((snakeX,snakeY))
    tail.pop(0)

def moveLeft():
    global snakeX
    global snakeY
    global tail
    snakeX -= 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def moveRight():
    global snakeX
    global snakeY
    global tail
    snakeX += 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def generateRandomApple():
    randomX = randrange(10)
    randomY = randrange(10)
    print(randomX)
    print(randomY)
    global appleX
    global appleY
    global tail
    while True:
        if randomX == 0:
            appleX = 0
        elif randomX == 1:
            appleX = 60
        elif randomX == 2:
            appleX = 120
        elif randomX == 3:
            appleX = 180
        elif randomX == 4:
            appleX = 240
        elif randomX == 5:
            appleX = 300
        elif randomX == 6:
            appleX = 360
        elif randomX == 7:
            appleX = 420
        elif randomX == 8:
            appleX = 480
        else:
            appleX = 540

        if randomY == 0:
            appleY = 0
        elif randomY == 1:
            appleY = 60
        elif randomY == 2:
            appleY = 120
        elif randomY == 3:
            appleY = 180
        elif randomY == 4:
            appleY = 240
        elif randomY == 5:
            appleY = 300
        elif randomY == 6:
            appleY = 360
        elif randomY == 7:
            appleY = 420
        elif randomY == 8:
            appleY = 480
        else:
            appleY = 540

        if (appleX,appleY) in tail:
            randomX = randrange(10)
            randomY = randrange(10)
        else:
            break


running = True
lastKey = pygame.K_RIGHT;
while running:
    screen.fill((192,192,192))

    moveInDirection(direction)

    time.sleep(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            lastKey = event.key;

            if lastKey == pygame.K_RIGHT:
                direction = 3
            if lastKey == pygame.K_LEFT:
                direction = 4
            if lastKey == pygame.K_UP:
                direction = 2
            if lastKey == pygame.K_DOWN:
                direction = 1

        # time.sleep(1)

    if appleEaten:
        generateRandomApple()

   #if len(tail) == 3:
    #    font = pygame.font.Font('freesansbold.ttf', 32)
     #   text = font.render('Game Over!', True, (255,255,255), (150,150,150))
      #  textRect = text.get_rect()
       # textRect.center = (630 // 2, 600 // 2)
        #screen.blit(text, textRect)
    #
    checkEaten()

    #time = datetime.now().time()
    #print(time.second)
    #if time.second - refreshTime.second > 1:
        #moveInDirection(direction)



    drawTail(tail)

    if appleEaten:
        tail.insert(0,tail.__getitem__(0))

    # print(snakeX)
    # print(snakeY)
    # print(tail)

    drawApple(appleX,appleY)
    drawSnake(snakeX,snakeY)
    pygame.display.update()
