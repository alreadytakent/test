"""
Created on Mon Nov 14 20:36:51 2022
"""
import math
from random import choice
from random import randint
import pygame

FPS = 60
g = 3

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
BORDERS = (800, 550)
GUN_POSITION = (50, 500)
TARGET_SPAWN_AREA = ((500, 800), (0, 550))

class Ball:
    def __init__(self, screen: pygame.Surface, vx=0, vy=0):
        """ 
        Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = GUN_POSITION[0]
        self.y = GUN_POSITION[1]
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.t = 0
        self.vy0 = (vy**2 + 2*g*(BORDERS[1]-GUN_POSITION[1]))**0.5
        self.t0 = - (self.vy + self.vy0)/g
        self.Ty = 2*self.vy0/g

    def reposition(self):
        """ 
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        t = self.t
        if self.vx != 0:
            Tx = (BORDERS[0] - GUN_POSITION[0])/self.vx
            if t > Tx:
                self.x = round(BORDERS[0] - GUN_POSITION[0] - self.vx*(t-Tx))
            else:
                self.x = round(GUN_POSITION[0] + self.vx*t)
        t = (self.t - self.t0) % self.Ty
        self.y = round(BORDERS[1] - self.vy0*t + g*t**2/2)
        
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if type(obj) == Target and (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 400
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        self.an = math.atan2((event.pos[1]-GUN_POSITION[1]), (event.pos[0]-GUN_POSITION[0]))
        new_ball = Ball(self.screen, (self.f2_power**0.5)*math.cos(self.an), (self.f2_power**0.5)*math.sin(self.an))
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 400

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-GUN_POSITION[1]), (event.pos[0]-GUN_POSITION[0]))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        length = round(self.f2_power**0.5)
        end_point = (GUN_POSITION[0] + length*math.cos(self.an), GUN_POSITION[1] + length*math.sin(self.an))
        pygame.draw.line(screen, BLACK, (GUN_POSITION[0], GUN_POSITION[1]), end_point, 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 4225:
                self.f2_power += 9750/FPS
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self):
        """ Инициализация новой цели. """
        self.x = randint(TARGET_SPAWN_AREA[0][0], TARGET_SPAWN_AREA[0][1])
        self.y = randint(TARGET_SPAWN_AREA[1][0], TARGET_SPAWN_AREA[1][1])
        self.r = randint(5, 50)
        self.color = RED
        self.live = 1

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)

bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
score = 0

while not finished:
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (0, BORDERS[1]), (WIDTH, BORDERS[1]))
    screen.blit(font.render(str(score), False, BLACK), [20, 20])
    gun.draw()
    if target.live:    
        target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.reposition()
        b.t += 30/FPS
        if b.hittest(target) and target.live:
            target.live = 0
            score += 1
            target = Target()
    gun.power_up()

pygame.quit()
