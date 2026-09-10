######### IMPORTS ###################################################


import random, math, pygame
from pygame.locals import *


counter = 0


    

######### MAIN #####################################################

def main():

    showstartscreen = 1
    
    while 1:
        ######## CONSTANTS
        WINSIZE = [800,600]
        WHITE = [255,255,255]
        #temporarily BLUE
        BLACK = [0,20,150]
        #temporarily ORANGE
        RED = [255,174,66]
        GREEN = [0,255,0]
        #temporarily RED
        BLUE = [255,0,0]
        BLOCKSIZE = [20,20]
        UP = 1
        DOWN = 3
        RIGHT = 2
        LEFT = 4
        SHIFT = 120
        MAXX = 360
        MINX = 140
        MAXY = 560
        MINY = 340
        SNAKESTEP = 20
        TRUE = 1
        FALSE = 0
        BRAKE = 1
        TRIES = 0
        

        ######## VARIABLES

        direction = RIGHT # 1=up,2=right,3=down,4=left
        snakexy = [300,400]
        snakelist = [[300,400],[280,400],[260,400]]
        counter = 0
        score = 0
        appleonscreen = 0
        #applexy = [0,0]
        newdirection = RIGHT
        snakedead = FALSE
        gameregulator = 6
        gamepaused = 0
        growsnake = 0  # added to grow tail by two each time 
        snakegrowunit = 2 # added to grow tail by two each time
        pyfont = "arial"
        
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('SNAKE')
        screen.fill(BLACK)

        #### show initial start screen
        
        if showstartscreen == TRUE:
            showstartscreen = FALSE

            s = [[180,120],[180,100],[160,100],[140,100],[120,100],[100,100],[100,120],[100,140],[100,160],[120,160],[140,160],[160,160],[180,160],[180,180],[180,200],[180,220],[160,220],[140,220],[120,220],[100,220],[100,200]]
            apple = [100,200]
            
            pygame.draw.rect(screen,GREEN,Rect(apple,BLOCKSIZE))
            pygame.display.flip()
            clock.tick(8)
            
            for e in s:
                pygame.draw.rect(screen,RED,Rect(e,BLOCKSIZE))
                pygame.display.flip()
                clock.tick(8)

            #print(pygame.font.get_fonts())
            font = pygame.font.SysFont(pyfont, 64)
            text_surface = font.render("NAKE", True, RED)
            screen.blit(text_surface, (220,180))
            font = pygame.font.SysFont(pyfont, 24)
            #text_surface = font.render("Move the snake with the arrow keys to eat the apples", True, RED)
            #screen.blit(text_surface, (50,300))
            #text_surface = font.render("Avoid the walls and yourself !", True, RED)
            #screen.blit(text_surface, (50,350))
            text_surface = font.render("Press [S] to start a new game - Press [Q] to quit at any time", True, RED)
            screen.blit(text_surface, (50,300))
            text_surface = font.render("Press [P] to pause and [R] to resume at any time", True, RED)
            screen.blit(text_surface, (50,350))
            #text_surface = font.render("Use [ARROW KEYS] to move", True, BLUE)
            #screen.blit(text_surface, (50,400))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: exit()
                if pressed_keys[K_s]: break

                clock.tick(10)


        while not snakedead:
            if TRIES >= 3:
                exit()
            ###### get input events  ####

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                    
            pressed_keys = pygame.key.get_pressed()
            
            if pressed_keys[K_LEFT]: newdirection = LEFT
            if pressed_keys[K_RIGHT]: newdirection = RIGHT
            if pressed_keys[K_UP]: newdirection = UP
            if pressed_keys[K_DOWN]: newdirection = DOWN
            if pressed_keys[K_q]: snakedead = TRUE
            if pressed_keys[K_p]: gamepaused = 1

            ### wait here if p key is pressed until p key is pressed again
            
            while gamepaused == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_r]:
                    gamepaused = 0 
                clock.tick(10)


            ### added gameregulator because setting a very low clock ticks
            ### caused the keyboard input to be hit and miss.  So I up the
            ### gameticks and the input and screen refresh is at this rate
            ### but the snake moving and all other logic is at the slower
            ### "regulated" speed

            
            if gameregulator == 6:

                ####### lets make sure we can't go back the reverse direction

                if newdirection == LEFT and not direction == RIGHT:
                    direction = newdirection

                elif newdirection == RIGHT and not direction == LEFT:
                    direction = newdirection

                elif newdirection == UP and not direction == DOWN:
                    direction = newdirection

                elif newdirection == DOWN and not direction == UP:
                    direction = newdirection
                    
                ##### now lets move the snake according to the direction
                ##### if we hit the wall the snake dies
                ##### need to make it less twitchy when you hit the walls
                    

                if direction == RIGHT:
                    snakexy[0] = snakexy[0] + SNAKESTEP
                    if snakexy[0] > MAXX:
                        snakedead = TRUE
                    
                elif direction == LEFT:
                    snakexy[0] = snakexy[0] - SNAKESTEP
                    if snakexy[0] < MINX:
                        snakedead = TRUE
                        
                elif direction == UP:
                    snakexy[1] = snakexy[1] - SNAKESTEP
                    if snakexy[1] < MINY:
                        snakedead = TRUE
                        
                elif direction == DOWN:
                    snakexy[1] = snakexy[1] + SNAKESTEP
                    if snakexy[1] > MAXY:
                        snakedead = TRUE

                ### is the snake crossing over itself
                ### had to put the > 1 test in there as I was
                ### initially matching on first pass otherwise - not sure why
                        
                if len(snakelist) > 3 and snakelist.count(snakexy) > 0: 
                    snakedead = TRUE
                

                        
                #### generate an apple at a random position if one is not on screen
                #### make sure apple never appears in snake position
                    
                if appleonscreen == 0:
                    good = FALSE
                    while good == FALSE:
                        x = random.randrange(7,18)
                        y = random.randrange(17,29)
                        #applexy = [int(x*(SNAKESTEP/BRAKE)),int(y*(SNAKESTEP/BRAKE))]
                        applexy = [int(x*(SNAKESTEP/BRAKE)),int(y*(SNAKESTEP/BRAKE))]
                        if snakelist.count(applexy) == 0:
                            good = TRUE
                    appleonscreen = 1

                #### add new position of snake head
                #### if we have eaten the apple don't pop the tail ( grow the snake )
                #### if we have not eaten an apple then pop the tail ( snake same size )

                snakelist.insert(0,list(snakexy))
                if snakexy[0] == applexy[0] and snakexy[1] == applexy[1]:
                    appleonscreen = 0
                    score = score + 1
                    growsnake = growsnake + 1
                elif growsnake > 0:
                    growsnake = growsnake + 1
                    if growsnake == snakegrowunit:
                        growsnake = 0
                else:
                    snakelist.pop()
                    
                

                gameregulator = 0


            ###### RENDER THE SCREEN ###############
            
            ###### Clear the screen
            screen.fill(BLACK)
            
            ###### Draw the screen borders
            ### horizontals
            #pygame.draw.line(screen,BLUE,(0,9),(799,9),20)
            #top
            pygame.draw.line(screen,BLUE,(0+SHIFT,330),(260+SHIFT,330),20)
            #bottom
            pygame.draw.line(screen,BLUE,(0+SHIFT,589),(260+SHIFT,589),20)
            #pygame.draw.line(screen,BLUE,(0,69),(799,69),20)
            ### verticals
            #left
            pygame.draw.line(screen,BLUE,(9+SHIFT,340),(9+SHIFT,599),20)
            #right
            pygame.draw.line(screen,BLUE,(269+SHIFT,321),(269+SHIFT,599),20)
            #pygame.draw.line(screen,BLUE,(789,0),(789,599),20)
            
            ###### Print the score
            font = pygame.font.SysFont(pyfont, 38)
            #score
            #text_surface = font.render("Score: " + str(score), True, BLUE)
            #screen.blit(text_surface, (10,50))
            #pygame.draw.line(screen,BLUE,(10,100),(160,100),5)
            ###### Output the array elements to the screen as rectangles ( the snake)
            for element in snakelist:
                pygame.draw.rect(screen,RED,Rect(element,BLOCKSIZE))

            ###### Draw the apple
            pygame.draw.rect(screen,GREEN,Rect(applexy,BLOCKSIZE))

            ###### Flip the screen to display everything we just changed
            pygame.display.flip()



            gameregulator = gameregulator + 1
            
            clock.tick(25)


        ##### if the snake is dead then it's game over
            
        if snakedead == TRUE:
            screen.fill(BLACK)
            font = pygame.font.SysFont(pyfont, 48)
            text_surface = font.render("GAME OVER", True, RED)
            screen.blit(text_surface, (250,200))
            text_surface = font.render("Your Score: " + str (score), True, RED)
            screen.blit(text_surface, (250,300))
            font = pygame.font.SysFont(pyfont, 24)
            text_surface = font.render("Press [Q] to quit", True, RED)
            screen.blit(text_surface, (300,400))
            text_surface = font.render("Press [N] to play again", True, RED)
            screen.blit(text_surface, (275,450))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: exit()
                if pressed_keys[K_n]: 
                    break

                clock.tick(10)
    
if __name__ == '__main__':
    main()


