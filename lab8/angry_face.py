"""
Created on Mon Nov  7 19:43:19 2022
"""

import pygame
import pygame.draw as pgd 

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

pgd.circle(screen, (255, 255, 0), [200, 200], 100)
pgd.circle(screen, (255, 0, 0), [150, 190], 25)
pgd.circle(screen, (255, 0, 0), [250, 190], 25)
pgd.circle(screen, (0, 0, 0), [150, 190], 10)
pgd.circle(screen, (0, 0, 0), [250, 190], 10)
pgd.line(screen, (0, 0, 0), [125, 155], [185, 180], 10)
pgd.line(screen, (0, 0, 0), [275, 155], [215, 180], 10)
pgd.arc(screen, (0, 0, 0), pygame.Rect([160, 250], (80, 80)), 0.524, 2.618, 7)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()