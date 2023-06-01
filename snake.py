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

# Block Attributes
BLOCK_HEIGHT = 15
BLOCK_WIDTH = 15
BLOCK_MARGIN = 3

# Display Attributes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
        
    # def update(self):
    #     # print("here")
    #     # self.previousCoords = (self.rect.x,self.rect.y)
    #     if self.horizontal:
    #         self.rect.x = self.rect.x + self.direction
    #     else:
    #         self.rect.y = self.rect.y + self.direction
      
def isGameOver(goal,snakeSegs,allSpritesList):
    result = False
    player = snakeSegs[0]
    
    # check for out of bounds
    if (player.rect.x <= 0 or player.rect.y <= 0 or player.rect.x >= SCREEN_WIDTH or player.rect.y >= SCREEN_HEIGHT):
        result = True
    # check if hitting itself
    hitSnakeSegs = pygame.sprite.spritecollide(player,allSpritesList,False)
    for snake in hitSnakeSegs:
        if (snake != player and snake != goal):
            result = True
             
    return result
    
def placeGoal(snakeSegs):
    x = random.randrange(SCREEN_WIDTH)
    y = random.randrange(SCREEN_HEIGHT)
    
    # the goal block cannot occupy the same space as any of the snake segments
    done = False
    while not done:
        count = 0
        for seg in snakeSegs:
            if (x==seg.rect.x and y==seg.rect.y):
                x = random.randrange(SCREEN_WIDTH-BLOCK_MARGIN)
                y = random.randrange(SCREEN_HEIGHT-BLOCK_MARGIN)
                break
            else:
                count += 1
        if count == len(snakeSegs):
            done = True
            
    return Block(YELLOW, x, y)  
        
def main():
    pygame.init()
    
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Snake Example")
    
    snakeSegs = []
    allSpritesList = pygame.sprite.Group()
    
    for i in range(3):
        x = 250 - ((BLOCK_WIDTH + BLOCK_MARGIN)*i)
        y = 30
        snakeBlock = Block(WHITE, x, y)
        snakeSegs.append(snakeBlock)
        allSpritesList.add(snakeBlock)
    
    goal = placeGoal(snakeSegs)
    allSpritesList.add(goal)
    
    clock = pygame.time.Clock()
    x_change = 0
    y_change = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change = (BLOCK_WIDTH + BLOCK_MARGIN) * -1
                    y_change = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = (BLOCK_WIDTH + BLOCK_MARGIN) * 1
                    y_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    x_change = 0
                    y_change = (BLOCK_HEIGHT + BLOCK_MARGIN) * -1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    x_change = 0
                    y_change = (BLOCK_HEIGHT + BLOCK_MARGIN) * 1
        
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
        
        # check for game over (out of bounds or snake hit itself)
        if isGameOver(goal,snakeSegs,allSpritesList):
            print("Game Over")
            pygame.quit()
            sys.exit()
            
        # check if the goal has been hit
        allSpritesList.remove(goal)
        hitGoal = pygame.sprite.spritecollide(goal,allSpritesList,False)
        if (len(hitGoal)!=0):
            goal = placeGoal(snakeSegs)
            newSeg = Block(WHITE,snakeSegs[0].rect.x+x_change,snakeSegs[0].rect.y+y_change)
            snakeSegs.insert(len(snakeSegs),newSeg)
            allSpritesList.add(newSeg)
        allSpritesList.add(goal)  
                    
        screen.fill(BLACK)
        allSpritesList.draw(screen)
        # set game to 15 FPS
        clock.tick(15)
        pygame.display.flip()
        
    
if __name__ == "__main__":
    main()
        