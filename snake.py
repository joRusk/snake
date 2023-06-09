# adapted from this code http://programarcadegames.com/python_examples/f.php?file=snake.py

import pygame
import random
import sys

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (73, 13, 107)

# Block Attributes
BLOCK_HEIGHT = 15
BLOCK_WIDTH = 15
BLOCK_MARGIN = 3
BLOCK_STEP = BLOCK_WIDTH + BLOCK_MARGIN

# Display Attributes
SCREEN_WIDTH = 810 # a multiple of BLOCK_STEP
SCREEN_HEIGHT = 594 # a multiple of BLOCK_STEP
GAME_WIDTH = SCREEN_WIDTH - (BLOCK_STEP*4)
GAME_HEIGHT = SCREEN_HEIGHT - (BLOCK_STEP*4)

GAME_TOP = (SCREEN_HEIGHT-GAME_HEIGHT)/2
GAME_LEFT = (SCREEN_WIDTH-GAME_WIDTH)/2

SCORE_INCREMENT = 50
SNAKE_INIT = 3

class Block(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super().__init__()
        
        # create an image of the block and fill it with colour
        # could also use an image loaded from memory
        self.image = pygame.Surface([BLOCK_WIDTH,BLOCK_HEIGHT])
        self.image.fill(colour)
        self.horizontal = False
        self.direction = 0
        self.previousCoords = None
        
        # fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
      
def isGameOver(goal,snakeSegs,allSpritesList):
    result = False
    player = snakeSegs[0]
    
    # check for out of bounds
    if (player.rect.x <= (GAME_LEFT) or player.rect.y <= (GAME_TOP)):
        result = True
    elif (player.rect.x >= (SCREEN_WIDTH-GAME_LEFT-BLOCK_STEP) or player.rect.y >= (SCREEN_HEIGHT-GAME_TOP-BLOCK_STEP)):
        result = True
    # check if hitting itself
    hitSnakeSegs = pygame.sprite.spritecollide(player,allSpritesList,False)
    for snake in hitSnakeSegs:
        if (snake != player and snake != goal):
            result = True
             
    return result
    
def placeGoal(snakeSegs):
    x = random.randrange(SCREEN_WIDTH-GAME_WIDTH,GAME_WIDTH)
    y = random.randrange(SCREEN_HEIGHT-GAME_HEIGHT,GAME_HEIGHT)
    
    # the goal block cannot occupy the same space as any of the snake segments
    done = False
    while not done:
        count = 0
        for seg in snakeSegs:
            if (x==seg.rect.x and y==seg.rect.y):
                x = random.randrange(GAME_LEFT+BLOCK_STEP,GAME_LEFT+GAME_WIDTH-BLOCK_STEP)
                y = random.randrange(GAME_TOP+BLOCK_STEP,GAME_TOP+GAME_HEIGHT-BLOCK_STEP)
                break
            else:
                count += 1
        if count == len(snakeSegs):
            done = True
            
    return Block(YELLOW, x, y)  
        
def main():
    pygame.init()
    
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    screen.fill(PURPLE)
    pygame.display.set_caption("Snake Example")
    # screen is purple but the actual playing surface is black
    # i.e., appears as a black rectangle with a purple border
    pygame.draw.rect(screen,BLACK,(GAME_LEFT,GAME_TOP,GAME_WIDTH,GAME_HEIGHT))
    pygame.display.flip()
    
    snakeSegs = []
    allSpritesList = pygame.sprite.Group()
    
    # create the initial snake segments
    for i in range(SNAKE_INIT):
        x = 234 - ((BLOCK_WIDTH+BLOCK_MARGIN)*i)
        y = 180
        snakeBlock = Block(WHITE, x, y)
        snakeSegs.append(snakeBlock)
        allSpritesList.add(snakeBlock)
    
    goal = placeGoal(snakeSegs)
    allSpritesList.add(goal)
    
    clock = pygame.time.Clock()
    
    x_change = 0
    y_change = 0
    firstMove = True
    done = False
    score = 0
    
    while not done:
        # set game to 15 FPS
        clock.tick(15)
        # initialize pygame font for displaying score
        font = pygame.font.Font(None, 28)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # check for player movements
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change = BLOCK_STEP * -1
                    y_change = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = BLOCK_STEP * 1
                    y_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    x_change = 0
                    y_change = BLOCK_STEP * -1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    x_change = 0
                    y_change = BLOCK_STEP * 1
        
        # the snake shouldn't move over itself
        # i.e., starting from rest, it can't move directly left
        if firstMove:
            if x_change < 0:
                x_change = 0
                y_change = 0
                
        # update snake segment locations if the player has moved them
        if not (x_change==0 and y_change==0):
            # prevent the 'head' of the snake from traveling over itself
            # i.e., cannot immediately reverse directions
            if ((snakeSegs[0].rect.x + x_change) == snakeSegs[1].rect.x and (snakeSegs[0].rect.y + y_change) == snakeSegs[1].rect.y):
                x_change = x_change*-1
                y_change = y_change*-1
                
            oldSeg = snakeSegs.pop()
            allSpritesList.remove(oldSeg)
            
            x = snakeSegs[0].rect.x + x_change
            y = snakeSegs[0].rect.y + y_change
            newSeg = Block(WHITE, x, y)
            
            snakeSegs.insert(0,newSeg)
            allSpritesList.add(newSeg)
            
            firstMove = False
            
        # check if the goal has been hit
        allSpritesList.remove(goal)
        hitGoal = pygame.sprite.spritecollide(goal,allSpritesList,False)
        if (len(hitGoal)!=0):
            # move the goal and add a new segment to the snake tail
            goal = placeGoal(snakeSegs)
            
            newSeg = Block(WHITE,snakeSegs[0].rect.x+x_change,snakeSegs[0].rect.y+y_change)
            snakeSegs.insert(len(snakeSegs),newSeg)
            allSpritesList.add(newSeg)
            
            score += SCORE_INCREMENT
            
        allSpritesList.add(goal)  
                  
        # wipe the screen            
        screen.fill(PURPLE)            
        pygame.draw.rect(screen,BLACK,(GAME_LEFT,GAME_TOP,GAME_WIDTH,GAME_HEIGHT))
        
        # draw all the sprites
        allSpritesList.draw(screen)
        
        # draw the score to the screen
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        
        # check for game over (out of bounds or snake hit itself)
        if isGameOver(goal,snakeSegs,allSpritesList):
            print("Game Over")
            done = True
    
    pygame.quit()
    sys.exit()
        
    
if __name__ == "__main__":
    main()
        