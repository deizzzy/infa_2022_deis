import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((200, 200, 200))




circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 2)
circle(screen, (255, 0, 0), (152, 180), 20)
circle(screen, (255, 0, 0), (248, 180), 15)
circle(screen, (0, 0, 0), (152, 180), 20, 2)
circle(screen, (0, 0, 0), (248, 180), 15, 2)
circle(screen, (0, 0, 0), (152, 180), 7)
circle(screen, (0, 0, 0), (248, 180), 7)
rect(screen, (0, 0, 0), (150, 245, 100, 17))
line(screen, (0, 0, 0), [100, 100], [170, 170], 15)
line(screen, (0, 0, 0), [300, 140], [230, 170], 13)





pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
