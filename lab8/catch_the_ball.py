"""
Created on Sat Nov 12 16:32:02 2022
"""

import pygame
from random import randint

pygame.font.init()

FPS = 60
DISPLAY = (1200, 700)
screen = pygame.display.set_mode(DISPLAY)
font = pygame.font.SysFont(None, 50)
spawn_area = ((100, 900), (100, 600))
time_limit = 10 #seconds

Aim_trainer_mode = True

if Aim_trainer_mode:
    ball_lifetime = time_limit*FPS
    delta_v = 0
    r_max = 30
    r_min = 30
else:
    ball_lifetime = FPS*5
    time_delay = round(FPS*0.5)
    delta_v = round(450/FPS)
    r_max = 45
    r_min = 20

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (190, 190, 190)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(spawn_area[0][0], spawn_area[0][1])
        self.y = randint(spawn_area[1][0], spawn_area[1][1])
        self.r = randint(r_min, r_max)
        self.vx = randint(-delta_v, delta_v)
        self.vy = randint(-delta_v, delta_v)
        self.color = COLORS[randint(0, 5)]
        self.live = ball_lifetime
    
    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.x > DISPLAY[0] - self.r or self.x < self.r:
            self.vx *= -1
        if self.y > DISPLAY[1] - self.r or self.y < self.r:
            self.vy *= -1
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def value(self):
        '''
        функция, рассчитывающая стоимость шарика по безрамерным параметрам:
        a - [0, 1] - относительный размер шарика (чем меньше, тем больше очков)
        b - [0, 1] - относительная скорость шарика (чем больше, тем больше очков)
        '''
        if Aim_trainer_mode:
            return 1
        a = self.r/r_max
        b = 2*(self.vx**2 + self.vy**2)**0.5/delta_v
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
        return round(r_bonus*v_bonus)


class Button:
    '''
    Кнопка. Нужна, чтобы нарисовать прямоугольную кнопку. Функционал - подсвечивается, если
    на неё наведён курсор, сообщает о нажатии, если на неё нажали.
    '''
    def __init__(self, rectangle, color0=DARK_GRAY, color1=LIGHT_GRAY):
        self.rectangle = rectangle
        self.color0 = color0 # Дефолтный цвет 
        self.color1 = color1 # Цвет, когда курсор над кнопкой
    
    def draw(self, pos):
        if self.rectangle.collidepoint(pos):
            pygame.draw.rect(screen, self.color1, self.rectangle)
        else:
            pygame.draw.rect(screen, self.color0, self.rectangle)

def hit(x0, y0):
    '''сообщает, попал ли клик в шарик'''
    for b in balls:
        if (b.x - x0)**2 + (b.y - y0)**2 <= b.r**2:
            return [True, b]
    return [False, 0]

def input_box():
    
    pass
    
def endgame():
    finished = False
    saving_score = False
    while not finished:
        screen.fill(BLACK)
        
        show_text(str(S), (DISPLAY[0]//2, DISPLAY[1]//2 - 160))
        show_text('Do you want to save your score?', (DISPLAY[0]//2, DISPLAY[1]//2-80))
        
        yes_button = Button(pygame.Rect((DISPLAY[0]//2-200, (DISPLAY[1]-50)//2), (200, 50)))
        no_button = Button(pygame.Rect((DISPLAY[0]//2, (DISPLAY[1]-50)//2), (200, 50)))
        
        yes_button.draw(pygame.mouse.get_pos())
        no_button.draw(pygame.mouse.get_pos())
        
        show_text('Yes', (DISPLAY[0]//2-100, DISPLAY[1]//2))
        show_text('Try again', (DISPLAY[0]//2+100, DISPLAY[1]//2))
        
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONUP: 
                if no_button.rectangle.collidepoint(event.pos):
                    finished = True
                elif yes_button.rectangle.collidepoint(event.pos):
                    finished = True
                    saving_score = True
    #if saving_score:
    #    while saving_score:
    #        pass
            
    pass

def show_text(text, coord=(DISPLAY[0]//2, DISPLAY[1]//2)):
    '''выводит текст на экран в центре заданных координат'''
    text = font.render(text, False, WHITE)
    text_rect = text.get_rect(center=coord)
    screen.blit(text, text_rect)
    
pygame.init()
pygame.font.init()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
closed = False

S = 0 #Число очков
frames_passed = 0
balls = []
screen.fill(BLACK)
show_text(str(S))
new_ball = Ball(screen)
balls.append(new_ball)

while not finished:
    screen.fill(BLACK)
    show_text('Score '+str(S), (80, 30))
    show_text('Time '+str(int((time_limit - pygame.time.get_ticks()/1000)*10)/10), 
              (DISPLAY[0]//2, 30))
    if not Aim_trainer_mode:
        if frames_passed/time_delay % 1 == 0:
            new_ball = Ball(screen)
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
            closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            hitlist = hit(event.pos[0], event.pos[1])
            if hitlist[0]:
                hitlist[1].live = 0
                S += hitlist[1].value()
                if Aim_trainer_mode:
                    new_ball = Ball(screen)
                    balls.append(new_ball)
    
    if pygame.time.get_ticks()/1000 > time_limit:
        finished = True

if closed:
    pygame.quit()
else:
    endgame()
    pygame.quit()