"""
Created on Sat Nov 12 16:32:02 2022
"""

import pygame
from random import randint

pygame.init()
pygame.font.init()

FPS = 60
screen = pygame.display.set_mode((1000, 700))
font = pygame.font.SysFont('Comic Sans MS', 30)
ball_lifetime = FPS*5
time_delay = round(FPS*1)
spawn_area = ((100, 900), (100, 600))
delta_v = round(450/FPS)
r_max = 45
r_min = 20
minimal_points = 1

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(spawn_area[0][0], spawn_area[0][1])
        self.y = randint(spawn_area[1][0], spawn_area[1][1])
        self.r = randint(r_min, r_max)
        self.vx = randint(-delta_v, delta_v+1)
        self.vy = randint(-delta_v, delta_v+1)
        self.value = value(self.r/r_max, (self.vx**2 + self.vy**2)**0.5/delta_v)
        self.color = COLORS[randint(0, 5)]
        self.live = ball_lifetime
    
    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x > 1000 - self.r or self.x < self.r:
            self.vx *= -1
        if self.y > 700 - self.r or self.y < self.r:
            self.vy *= -1
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

def value(a, b):
    if a < 0.1:
        r_bonus = 3
    elif a < 0.3:
        r_bonus = 2
    elif a < 0.5:
        r_bonus = 1.5
    else:
        r_bonus = 1
    if b > 0.8:
        v_bonus = 3
    elif b > 0.5:
        v_bonus = 1.5
    else:
        v_bonus = 1
    return int(minimal_points*r_bonus*v_bonus)

def hit(x0, y0):
    '''сообщает, попал ли клик в шарик'''
    for b in balls:
        if (b.x - x0)**2 + (b.y - y0)**2 <= b.r**2:
            return [True, b]
    return [False, 0]

def score(S):
    '''выводит на экран число очков'''
    line = 'Score: ' + str(S)
    text_surface = font.render(line, False, (255, 255, 255))
    screen.blit(text_surface, (0,0))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

S = 0 #Число очков
frames_passed = 0
balls = []

while not finished:
    screen.fill(BLACK)
    score(S)
    if frames_passed/time_delay % 1 == 0:
        new_ball = ball(screen)
        balls.append(new_ball)
    frames_passed += 1
    i = 0
    while i < len(balls):
        balls[i].move()
        if balls[i].live > 0:
            balls[i].draw()
            i += 1
        else:
            balls.pop(i)
    for b in balls:
        b.live -= 1
    pygame.display.update()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            hitlist = hit(event.pos[0], event.pos[1])
            if hitlist[0]:    
                hitlist[1].live = 0
                S += hitlist[1].value

pygame.quit()
