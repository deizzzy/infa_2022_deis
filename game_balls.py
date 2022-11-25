import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))
f_sys = pygame.font.SysFont('arial', 12)

a = []
i = 1

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

score = 0
o = 0

def append_fig(a, f):
    '''
    добавляет в массив данные нового объекта
    a - массив с данными объектов
    f - тип объекта, 1/2 соответственно круг/прямоуг
    '''
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    i = randint(1,255)
    j = randint(1,255)
    k = randint(1,255)
    phi = randint(1,360)
    a.append(x)
    a.append(y)
    a.append(r)
    a.append(i)
    a.append(j)
    a.append(k)
    a.append(phi)
    a.append(f)
    return a


def move(a, u, o):
    '''
    принимает массив с данными объектов a, индекс первого элемента объекта u, число о
    рисует существующий шар/прямоугольник в новом положении
    '''
    print(a)
    print(u)



    
    if a[u] + a[u+2] > 1195 or a[u] - a[u+2] < 5: 
        a[u+6] = 180 - a[u+6]
        if a[u] + a[u+2] > 1195:
            x = a[u] - 15
        else: x = a[u] + 15

    elif a[u+7] == 1:
        x = a[u] + 10*math.cos(a[u+6])
    else: x = a[u] + 20*math.cos(a[u+6])

    if a[u+1] + a[u+2] > 895 or a[u+1] - a[u+2] < 5: 
        a[u+6] = -a[u+6]
        if a[u+1] + a[u+2] > 895:
            y = a[u+1] - 15
        else: y = a[u+1] + 15
            

    elif a[u+7] == 1:
        y = a[u+1] + 10*math.sin(a[u+6])
    else: y = a[u+1] + 20*math.sin(a[u+6])


    print(a[u+3], a[u+4], a[u+5])

    
    if a[u+7] == 2:
        rect(screen, (a[u+3], a[u+4], a[u+5]), (x, y, a[u+2]*abs(math.cos(o))+10, a[u+2]*abs(math.sin(o))+10), 3)

        
    else:
        circle(screen, (a[u+3], a[u+4], a[u+5]), (x, y), a[u+2])

    
    a[u] = x
    a[u+1] = y
    return a
    
def click(a, event):
    '''принимает массив с данными объектов a и событие event - нажатие левой кнопки мыши
        

        возвращает количество попаданий мышкой за одну итерацию
        зануляет данные попавших под мышку объектов'''
    score = 0
    for i in range(0, len(a), 8):
        if ((event.pos[0]-a[i])**2)  + ((event.pos[1]-a[i+1])**2) <= a[i+2]**2:
            score+=1
            for f in range (i, i+8):
                a[f] = 0

    return a, score


def table(score):
    '''принимает число очков score

     выводит окошко со счетом'''

    f = pygame.font.SysFont('arial', 70)
    
    text = f.render(f"{score}", 1, BLACK, CYAN)
    screen.blit(text, (50, 50))
    


        

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a, score1 = click(a, event)
                score+=score1
    a = list(filter(lambda x: x != 0, a))

    if i%20 == 0:
        a = append_fig(a, 1)

    elif i%17 == 0:
        a = append_fig(a, 2)


    print(len(a))
    o+=0.1
    for u in range(0, len(a), 8):
        a = move(a, u, o)

    
        
    i+=1
    table(score)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
