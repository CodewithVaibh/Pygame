
import random
import sys
import pygame
from pygame.locals import *

FPS=32
Screenwidth=300
Screenheight=700
Screen=pygame.display.set_mode((Screenwidth,Screenheight))
Ground=Screenheight*0.8
Sprites={}
Sounds={}
Player='fla.jpg'
Background='background.jpg'
Pipe='pipe ss.jpg'

def Welcome_Screen():
    Playerx=int(Screenwidth/2)
    Playery=int(Screenheight/3)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
               pygame.quit()
               sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_KP_ENTER):
               return
        
            else:
                 Screen.blit(Sprites['Background'], (0,0))
                 Screen.blit(Sprites['Message'], (0,0))
                 Screen.blit(Sprites['Player'], (Playerx,Playery))
                 Screen.blit(Sprites['Base'], (0,Ground))
                 pygame.display.update()
                 FPSclock.tick(FPS)
    


def getRandomPipe():
    pipeHeight = Sprites['Pipe'][0].get_height()
    offset = Screenheight/3
    y2 = offset + random.randrange(0, int(Screenheight - Sprites['Base'].get_height()  - 1.2 *offset))
    pipeX = Screenwidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

def mainGame():
    score = 0
    playerx = int(Screenwidth/5)
    playery = int(Screenwidth/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': Screenwidth+200, 'y':newPipe1[0]['y']},
        {'x': Screenwidth+200+(Screenwidth/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': Screenwidth+200, 'y':newPipe1[1]['y']},
        {'x': Screenwidth+200+(Screenwidth/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    Sounds['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + Sprites['Player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + Sprites['Pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                Sounds['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = Sprites['Player'].get_height()
        playery = playery + min(playerVelY, Ground - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -Sprites['Pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        Screen.blit(Sprites['Background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screen.blit(Sprites['Pipe'][0], (upperPipe['x'], upperPipe['y']))
            Screen.blit(Sprites['Pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        Screen.blit(Sprites['Base'], (basex, Ground))
        Screen.blit(Sprites['Player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Sprites['numbers'][digit].get_width()
        Xoffset = (Screenwidth - width)/2

        for digit in myDigits:
            Screen.blit(Sprites['numbers'][digit], (Xoffset, Screenheight*0.12))
            Xoffset += Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSclock.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> Ground - 25  or playery<0:
        Sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = Sprites['Pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < Sprites['Pipe'][0].get_width()):
            Sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + Sprites['Player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < Sprites['Pipe'][0].get_width():
            Sounds['hit'].play()
            return True

    return False    
    
if __name__== "__main__":
    pygame.init()
    FPSclock=pygame.time.Clock()
    pygame.display.set_caption('GAME BY VAIBHAV')
    Sprites['numbers']=(
        pygame.image.load('0 ss.jpg').convert_alpha(),
        pygame.image.load('1 ss.jpg').convert_alpha(),
        pygame.image.load('2 ss.jpg').convert_alpha(),
        pygame.image.load('3 ss.jpg').convert_alpha(),
        pygame.image.load('4 ss.jpg').convert_alpha(),
        pygame.image.load('5 ss.jpg').convert_alpha(),
        pygame.image.load('6 ss.jpg').convert_alpha(),
        pygame.image.load('7 ss.jpg').convert_alpha(),
        pygame.image.load('8 ss.jpg').convert_alpha(),
        pygame.image.load('9 ss.jpg').convert_alpha(),
    )
    
    Sprites['Message']=pygame.image.load('message ss.jpg')
    Sprites['Base']=pygame.image.load('base ss.jpg')
    Sprites['Background']=pygame.image.load(Background).convert()
    Sprites['Player']=pygame.image.load(Player).convert_alpha()
    Sprites['Pipe']=(pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(),180),
    pygame.image.load(Pipe).convert_alpha()
    )
    
    Sounds['die']=pygame.mixer.Sound('Everything\sfx_die.wav')
    Sounds['hit']=pygame.mixer.Sound('Everything\sfx_hit.wav')
    Sounds['point']=pygame.mixer.Sound('Everything\sfx_point.wav')
    Sounds['swooshing']=pygame.mixer.Sound('Everything\sfx_swooshing.wav')
    Sounds['wing']=pygame.mixer.Sound('Everything\sfx_wing.wav')
    
while True:
        Welcome_Screen()
        mainGame()
        
    
    
                     