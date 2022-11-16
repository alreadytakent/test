"""
Created on Sat Nov 12 16:32:02 2022
"""

import pygame
from random import randint

pygame.font.init()

FPS = 60
DISPLAY = (1500, 700)
screen = pygame.display.set_mode(DISPLAY)
score_font = pygame.font.SysFont('Comic Sans MS', 30)
time_font = pygame.font.SysFont('Comic Sans MS', 30)
final_score_font_name = 'Comic Sans MS'
question_font_name = 'Comic Sans MS'
final_score_font_size = 50
question_font_size = 30
spawn_area = ((100, 900), (100, 600))
time_limit = 30 #seconds

Aim_trainer_mode = True

if Aim_trainer_mode:
    ball_lifetime = time_limit*FPS
    delta_v = 0
    r_max = 30
    r_min = 30
    minimal_points = 1
else:
    ball_lifetime = FPS*5
    time_delay = round(FPS*1)
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
WHITE = (255, 255, 255)
DARK_GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(spawn_area[0][0], spawn_area[0][1])
        self.y = randint(spawn_area[1][0], spawn_area[1][1])
        self.r = randint(r_min, r_max)
        self.vx = randint(-delta_v, delta_v)
        self.vy = randint(-delta_v, delta_v)
        if Aim_trainer_mode:
            self.value = minimal_points
        else:
            self.value = value(self.r/r_max, (self.vx**2 + self.vy**2)**0.5/delta_v)
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


def value(a, b):
    '''
    функция, рассчитывающая стоимость шарика по безрамерным параметрам:
    a - [0, 1] - относительный размер шарика (чем меньше, тем больше очков)
    b - [0, 1] - относительная скорость шарика (чем больше, тем больше очков)
    '''
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


class Button:
    '''
    Кнопка. Нужна, чтобы нарисовать прямоугольную кнопку. Функционал - подсвечивается, если
    на неё наведён курсор, сообщает о нажатии, если на неё нажали.
    '''
    def __init__(self, coord=(DISPLAY[0]//2, DISPLAY[1]//2), size=(200, 50), 
                 color0=DARK_GRAY, color1=LIGHT_GRAY):
        self.x = coord[0]
        self.y = coord[1]
        self.width = size[0]
        self.height = size[1]
        self.color0 = color0 # Дефолтеый цвет 
        self.color1 = color1 # Цвет, когда курсор над кнопкой
   
    def highlighted(self, x, y):
        '''Возвращает True, если курсор над кнопкой
        (x, y) - координаты курсора'''
        if  self.x - self.width//2 < x < self.x + self.width//2:
            if self.y - self.height//2 < y < self.y + self.height//2:
                return True
        return False
    
    def draw(self, pos):
        if self.highlighted(pos[0], pos[1]):
            color = self.color1
        else:
            color = self.color0
        pygame.draw.rect(screen, color, pygame.Rect((self.x-self.width//2, self.y-self.height//2), 
                                                    (self.width, self.height)))
        pygame.draw.rect(screen, BLACK, pygame.Rect((self.x-self.width//2, self.y-self.height//2), 
                                                    (self.width, self.height)), 2)

class Text:
    '''
    Текст. Нужен, чтобы вывести текст с данным шрифтом на нужных координатах.
    '''
    def __init__(self, text, coord=(DISPLAY[0]//2, DISPLAY[1]//2), 
                 font_name='Comic Sans MS', font_size=30, color=WHITE):
        self.x = coord[0]
        self.y = coord[1]
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        
    def draw(self):
        font = pygame.font.SysFont(self.font_name, self.font_size)
        text = font.render(self.text, False, self.color)
        screen.blit(text, (self.x - len(self.text)*self.font_size//4, self.y - self.font_size//2))

def hit(x0, y0):
    '''сообщает, попал ли клик в шарик'''
    for b in balls:
        if (b.x - x0)**2 + (b.y - y0)**2 <= b.r**2:
            return [True, b]
    return [False, 0]


def text(S, t):
    '''выводит на экран число очков'''
    S_line = 'Score ' + str(S)
    t_line = 'Time ' + str(int((time_limit - t)*10)/10)
    text_score = score_font.render(S_line, False, WHITE)
    text_time = time_font.render(t_line, False, WHITE)
    screen.blit(text_score, (0, 0))
    screen.blit(text_time, (DISPLAY[0]/2 - 60, 0))
    
    
def endgame():
    finished = False
    while not finished:
        screen.fill(BLACK)
        final_score = Text(str(S), (DISPLAY[0]//2, 
                                    (DISPLAY[1]-final_score_font_size-question_font_size)//2-100), 
                           final_score_font_name, final_score_font_size)
        question = Text('Do you want to save your score?', (DISPLAY[0]//2, DISPLAY[1]//2-80))
        yes_button = Button(((DISPLAY[0]-200)//2, DISPLAY[1]//2))
        no_button = Button(((DISPLAY[0]+200)//2, DISPLAY[1]//2))
        yes_text = Text('Yes', ((DISPLAY[0]-200)//2, (DISPLAY[1]-20)//2))
        no_text = Text('No', ((DISPLAY[0]+200)//2, (DISPLAY[1]-20)//2))
        final_score.draw()
        question.draw()
        yes_button.draw(pygame.mouse.get_pos())
        no_button.draw(pygame.mouse.get_pos())
        yes_text.draw()
        no_text.draw()
        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONUP: 
                if no_button.highlighted(event.pos[0], event.pos[1]):
                    print('clicked NO')
                    finished = True
                elif yes_button.highlighted(event.pos[0], event.pos[1]):
                    print('clicked YES')

    pass
    
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
text(S, 0)
new_ball = ball(screen)
balls.append(new_ball)

while not finished:
    screen.fill(BLACK)
    text(S, pygame.time.get_ticks()/1000)
    if not Aim_trainer_mode:
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
            closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            hitlist = hit(event.pos[0], event.pos[1])
            if hitlist[0]:
                hitlist[1].live = 0
                S += hitlist[1].value
                if Aim_trainer_mode:
                    new_ball = ball(screen)
                    balls.append(new_ball)
    
    if pygame.time.get_ticks()/1000 > time_limit:
        finished = True

if closed:
    pygame.quit()
else:
    endgame()
    pygame.quit()