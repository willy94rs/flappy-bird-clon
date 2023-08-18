
import pygame
from pygame.locals import * 
import random
import sys
import os

pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 706  
screen_height = 700

screen = pygame.display.set_mode ((screen_height, screen_width))
pygame.display.set_caption('Willy Flappy Owl')

#Variables
scroll = 0 
speed = 4
fly = False
game_over = False
gap = 150
frecuency = 1700 #millisecond
last_pipe = pygame.time.get_ticks() - frecuency
score = 0
pass_pipe = False 
white = (255, 255, 255)
font = pygame.font.SysFont('Calibri', 60)

#Images
bg = pygame.image.load('img/bg1.png')
base = pygame.image.load('img/base.png')
restart_btn = pygame.image.load('img/restart.png')


def draw_score(text, font, text_color, x,y):
    img = font.render(text,True,text_color)
    screen.blit(img, (x,y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_width/2)
    score = 0
    return score


class Bird (pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images =[]
        self.index = 0
        self.counter= 0
        for num in range(1,4):
            img = pygame.image.load(f'img/owl{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.down = 0
        self.click = False

    def update(self):        
        
        #bird down
        if fly == True:
            self.down += 0.2
            if self.down > 8:
               self.down = 8 
            if self.rect.bottom < 602:
               self.rect.y += int(self.down)
        
        if game_over == False:
            #bird up 
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                self.down = -5
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False

            #animation 
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter =0 
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0 
            self.image = self.images[self.index]

            #Rotate bird
            self.image = pygame.transform.rotate(self.images[self.index],self.down *-2)
        else:
           self.image = pygame.transform.rotate(self.images[self.index],-90) 
        
    
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1top -1bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft =[x,y - int(gap/2)]
        if position == -1:
            self.rect.topleft =[x,y + int(gap/2)]
    
    def update(self):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()
        


class button ():
    def __init__(self, x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    
    def draw (self):
        action = False
        #mouse posittion
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] ==1:
                action = True

        #draw button
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action

#BirdGroup
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_width/2))
bird_group.add(flappy)

#PipeGroup  
pipe_group = pygame.sprite.Group()

#InstanceButton
btn = button(screen_height//2-50, screen_width // 2, restart_btn)



#//////////////////////////////////////////////////////////////////////////////////////////////#
run = True
while run:

    clock.tick(fps)
    
    #background
    screen.blit(bg,(0,0))
    
    #bird background
    bird_group.draw(screen)
    bird_group.update()
    #pipes background
    pipe_group.draw(screen)

    #base
    screen.blit(base,(scroll,600))


    #check the score
    if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
                and pass_pipe == False:
                    pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    print(score)
                    pass_pipe = False

    draw_score(str(score), font, white, int(screen_width/2),20)
    
    
    #collision pipes
    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False) or flappy.rect.top<0:
        game_over=True

    #check hit ground 600=base
    if flappy.rect.bottom >= 600:
        game_over =True
        fly = False

    if game_over == False and fly ==True:
        #new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > frecuency:
            pipe_gap = random.randint(-100,100)
            button_pipe = Pipe(screen_height, int(screen_width/2) + pipe_gap,-1)
            top_pipe = Pipe(screen_height, int(screen_width/2)+ pipe_gap,1)
            #add to the group
            pipe_group.add(button_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        
        #ScrollBase
        scroll -= speed
        if abs(scroll) > 50:
            scroll = 0
        pipe_group.update()
    
    #GameOver
    if game_over == True:
       if  btn.draw() == True:
           game_over = False
           score = reset_game()
       
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and fly == False and game_over == False:
            fly =True
    pygame.display.update()
pygame.quit()