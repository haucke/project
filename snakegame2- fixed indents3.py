import pygame,sys
import win32api,win32console,win32gui,codecs
import time,random
from pygame.sprite import Sprite

pygame.init()

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600
#game display
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snakey")
#game icons
icon=pygame.image.load("mouse.png")
pygame.display.set_icon(icon)

img=pygame.image.load("snake.png")
mouseimg=pygame.image.load("mouse.png")

clock = pygame.time.Clock()

MouseThickness=30
block_size = 20
FPS = 15

direction="right"
#fonts
smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)
#game sounds
pygame.mixer.init()
intro_sound=pygame.mixer.Sound("intro.wav")
lose_sound=pygame.mixer.Sound("lose.wav")

#game intro and definitions
def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)

        message_to_screen("Welcome to Snakey!",green,-100,"large")
        message_to_screen("The objective of the game is to catch and eat the mice!",black,-30)
        message_to_screen("The more mice you eat, the longer you will get.",black,10)
        message_to_screen("If you run into yourself or the edges, you lose!",black,50)
        message_to_screen("Press C to play, P to pause, or Q to quit",black,180)
        pygame.display.update()
        clock.tick(15)

def pause():

    paused=True

    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue or Q to quit",black,25)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_c:
                        paused=False
                    elif event.key==pygame.K_q:
                        pygame.quit()
                        quit()

                clock.tick(5)

def score(score):

    text=smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])

def randMouseGen():

    randMousex = round(random.randrange(0,display_width-MouseThickness))
    randMousey = round(random.randrange(0,display_height-MouseThickness))
    return randMousex,randMousey

def snake(block_size,snakeList):

    if direction=="right":
        head=pygame.transform.rotate(img,270)
    if direction=="left":
        head=pygame.transform.rotate(img,90)
    if direction=="up":
        head=img
    if direction=="down":
        head=pygame.transform.rotate(img,180)

    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, (XnY[0],XnY[1],block_size,block_size))

def text_objects(text,color,size):

    if size=="small":
        textSurface=smallfont.render(text,True,color)
    elif size=="medium":
        textSurface=medfont.render(text,True,color)
    elif size=="large":
        textSurface=largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):

    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def gameLoop():

    global direction

    direction="right"
    running = True
    gameOver= False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snakeList=[]
    snakeLength=1

    randMousex,randMousey = randMouseGen()

    while running:
        if gameOver==True:
            message_to_screen("Game Over",red,-50,size="large") #for when game is lost
            message_to_screen("Press C to play again or Q to quit",black,50,size="medium")
            pygame.display.update()

    while gameOver == True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameOver=False
                running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        running=False
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameLoop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:  #keys to press for gameplay direction changes
                    if event.key == pygame.K_LEFT:
                        direction="left"
                        lead_x_change = -block_size
                        lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction="right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction="up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction="down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key==pygame.K_p:
                    pause()
                    if lead_x>=display_width or lead_x<0 or lead_y<0 or lead_y>=display_height:
                        gameOver=True
                        lose_sound.play()
                        lead_x += lead_x_change
                        lead_y += lead_y_change
                        gameDisplay.fill(white)

                        gameDisplay.blit(mouseimg,(randMousex,randMousey))

                        snakeHead=[]
                        snakeHead.append(lead_x)
                        snakeHead.append(lead_y)
                        snakeList.append(snakeHead)

                if len(snakeList)>snakeLength:
                    del snakeList[0]
                for eachSegment in snakeList[:-1]:
                    if eachSegment==snakeHead:
                        gameOver=True
                        lose_sound.play()

                snakeHead=[]
                snakeHead.append(lead_x)
                snakeHead.append(lead_y)
                snakeList.append(snakeHead)
#what causes game loss
                if len(snakeList)>snakeLength:
                    del snakeList[0]
                for eachSegment in snakeList[:-1]:
                    if eachSegment==snakeHead:
                        gameOver=True
                lose_sound.play()

                snake(block_size,snakeList)

                score(snakeLength-1)


                pygame.display.update()

                if lead_x>randMousex and lead_x <randMousex+MouseThickness or lead_x+block_size>randMousex and lead_x+block_size<randMousex+MouseThickness:
                    if lead_y>randMousey and lead_y <randMousey+MouseThickness:
                        randMousex,randMousey=randMouseGen()
                        snakeLength+=1
                elif lead_y+block_size > randMousey and lead_y+block_size<randMousey+MouseThickness:
                    randMousex,randMousey=randMouseGen()
                    snakeLength+=1

                clock.tick(FPS)

    pygame.quit()
    quit()
intro_sound.play()  #game sounds
game_intro()
intro_sound.stop()
gameLoop()
