import pygame
import pygame.draw as pgd

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

pgd.rect(screen, (255, 0, 255), (100, 100, 200, 200))
pgd.rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
pgd.polygon(screen, (255, 255, 0), [(100,100), (200,50),
                               (300,100), (100,100)])
pgd.polygon(screen, (0, 0, 255), [(100,100), (200,50),
                               (300,100), (100,100)], 5)
pgd.circle(screen, (0, 255, 0), (200, 175), 50)
pgd.circle(screen, (255, 255, 255), (200, 175), 50, 5)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()