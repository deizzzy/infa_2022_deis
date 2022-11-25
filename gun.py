from copy import deepcopy
from math import cos, sin, atan
from random import randint

import numpy as np
import pygame
from pygame.draw import *
from pygame.font import *
from screeninfo import get_monitors




def get_res():
    '''
    Получает параметры вашего монитора
    :return: Возвращает Tuple с координатами
    '''
    monitor = str(get_monitors()[0])[8:-1].split(', ')
    current_resolution = (int(monitor[2][6:]), int(monitor[3][7:]))
    return current_resolution


def collision_check(flying_obj, massive_obj):
    '''
    Проверяет, попал ли flying_obj в один из объектов massive_obj, проверяет их коллизии как круги
    :param flying_obj: летящий объект (пуля)
    :param massive_obj: Массив с объектами, с которыми может столкнуться пуля
    :return: Массив объектов - целей, булевская переменная, попала ли пуля в одну из целей
    '''
    hit = False
    for j in range(len(massive_obj) - 1, -1, -1):
        lenght = ((flying_obj.pos[0] - massive_obj[j].pos[0]) ** 2 +
                  (flying_obj.pos[1] - massive_obj[j].pos[1]) ** 2) ** 0.5
        if lenght <= flying_obj.radius + massive_obj[j].radius:
            global score
            score += massive_obj[j].score
            del massive_obj[j]
            hit = True
    return massive_obj, hit


res = get_res()
fps = 60
pygame.init()

# Вводим базовые цвета
m_color = (60, 60, 60)
s_color = (20, 20, 20)
g_color = (100, 100, 100)


class Tank:
    # Класс объектов, с танком
    def __init__(self, current_scr):
        '''
        Задаёт базовые параметры класса танк
        :param current_scr: принимает текущую страницу, на которой необходимо будет рисовать танк
        '''
        self.scr = current_scr
        self.pos = np.array([res[0] // 2, res[1] - 50])
        self.speed = 0
        self.hp = 3
        self.power = 0
        self.gun_angle = 0
        self.gun_pos = np.array([0, 0])
        self.scl = 1

    def aiming(self):
        '''
        Отвечает за наведение орудия на место положения мыши на экране, так же вне простых положений мыши
        :return: ничего
        '''
        len1 = mouse_pos[0] - self.pos[0]
        len2 = mouse_pos[1] - self.pos[1]
        if (mouse_pos[1] > res[1] - 110) and (mouse_pos[0] > self.pos[0]):
            self.gun_angle = 180
        elif (mouse_pos[1] > res[1] - 110) and (mouse_pos[0] < self.pos[0]):
            self.gun_angle = 0
        elif len1 == 0:
            self.gun_angle = 0
        else:
            self.gun_angle = atan(len1 / len2) * 57.3 + 90

    def shoot(self):
        '''
        Отвечает за создание новой пули у орудия и добавления её в базу данных
        '''
        global bullet_massive
        bullet_massive.append(Bullet(self.gun_pos, self.power, self.gun_angle, self.scr))

    def draw(self):
        '''
        Рисует танк в текущем положении, вместе с пушкой
        '''
        circle(self.scr, g_color, self.pos, 25 * self.scl)
        cord1 = np.array([[100, 0], [80, 40], [-80, 40], [-100, 0]]) * self.scl
        otn_arr4 = np.array([[self.pos[0], self.pos[1]] * 4]).reshape(4, 2)
        polygon(self.scr, m_color, cord1 + otn_arr4)
        self.gun()

    def gun(self):
        '''
        Рисует орудие, и обновляет координаты конца пушки у объекта танк
        '''
        an = self.gun_angle / 57.3
        power_shoot = self.power
        cx = self.pos[0]
        cy = self.pos[1]
        otn_arr2 = np.array([[cx, cy] * 2]).reshape(2, 2)
        otn_arr4 = np.array([[cx, cy] * 4]).reshape(4, 2)

        gun_l_b = 20
        gun_l_mi = 70
        gun_l_ma = 150
        gun_r = 5

        gun_l = gun_l_mi + (gun_l_ma - gun_l_mi) * power_shoot / 100
        coord_shar = np.array([0, 0])
        otn_coord_shar = np.array([coord_shar] * 4).reshape(4, 2)
        otn_coord_shar2 = np.array([coord_shar] * 2).reshape(2, 2)

        coord_gun = np.array([[-gun_l_b * cos(an) + gun_r * sin(an), gun_l_b * sin(an) + gun_r * cos(an)],
                              [-gun_l_b * cos(an) - gun_r * sin(an), gun_l_b * sin(an) - gun_r * cos(an)],
                              [gun_l * cos(an) - gun_r * sin(an), -gun_l * sin(an) - gun_r * cos(an)],
                              [gun_l * cos(an) + gun_r * sin(an), -gun_l * sin(an) + gun_r * cos(an)]])

        coord_gun_start_bul = np.array([[gun_l * cos(an), -gun_l * sin(an)],
                                        [gun_l * cos(an), -gun_l * sin(an)]])

        coord_gun_it = ((coord_gun + otn_coord_shar) * self.scl + otn_arr4).astype(int)

        coord_gun_start_bul_it = ((coord_gun_start_bul + otn_coord_shar2) * self.scl + otn_arr2).astype(int)

        polygon(self.scr, m_color, coord_gun_it)
        aalines(self.scr, m_color, True, coord_gun_it)

        self.gun_pos = coord_gun_start_bul_it[0]

    def move(self):
        '''
        Отвечает за обновление координат танка, так же не даёт танку уйти за стенки
        '''
        self.pos[0] += self.speed
        if self.pos[0] <= 100:
            self.pos[0] = 100
        elif self.pos[0] >= res[0] - 100:
            self.pos[0] = res[0] - 100


class Bullet:
    '''
    Класс пуль, которыми стреляет танк
    '''

    def __init__(self, pos, power, ang, scr):
        '''
        Отвечает за передачу параметров пули при её создании
        :param pos: Позиция пули в начальный момент времени, она же координата конца орудия
        :param power: Мощность выстрела танка, необходима для рассчёта скорости
        :param ang: Угол вылета пули, отсчитывается от направления вправо, против часовой стрелки
        :param scr: Текущий лист, необходим для отрисовки
        '''
        max_speed = 50
        self.pos = pos
        self.speed = (power * max_speed) // 100
        self.angle = ang
        self.radius = 5
        self.scr = scr
        self.speed_x = self.speed * cos(self.angle / 57.3)
        self.speed_y = -self.speed * sin(self.angle / 57.3)

    def draw(self):
        '''
        Рисует пульку
        '''
        circle(self.scr, (255, 0, 0), self.pos, self.radius)

    def move(self):
        '''
        Отвечает за движение пули по параболе, использует внешний парамент gravity
        '''
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        self.speed_y += gravity


class Target:
    '''
    Класс мишеней
    '''

    def __init__(self, scr):
        '''
        Отвечает за задачу параметров мишени при создании
        :param scr: Текущий лист, на котором необходимо рисовать цели
        '''
        max_speed = 5
        self.pos = np.array([randint(100, res[0] - 100), randint(100, res[0] - 100)])
        self.radius = randint(20, 50)
        self.speed = randint(50, 100) / 100 * max_speed
        self.angle = randint(0, 359)
        self.speed_x = self.speed * cos(self.angle / 57.3)
        self.speed_y = -(self.speed * sin(self.angle / 57.3))
        self.scr = scr
        self.score = 5

    def move(self):
        '''
        Отвечат за движение мишеней по экрану, отражение их от стенок
        '''
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        if self.pos[0] < self.radius:
            self.speed_x = -self.speed_x
            self.pos[0] = self.radius
        if self.pos[0] > res[0] - self.radius:
            self.speed_x = -self.speed_x
            self.pos[0] = res[0] - self.radius
        if self.pos[1] < self.radius:
            self.speed_y = -self.speed_y
            self.pos[1] = self.radius
        if self.pos[1] > res[1] - self.radius - 200:
            self.speed_y = -self.speed_y
            self.pos[1] = res[1] - self.radius - 200

    def draw(self):
        '''
        Рисует мишени
        '''
        circle(self.scr, (255, 0, 0), self.pos, self.radius)


class Enemy:
    '''
    Класс врагов, которые бомбят игрока бомбами
    '''

    def __init__(self, scr):
        '''
        Отвечает за создание базовых параметров при генерации врагов, принимает файл, 
        обязательно добавить файл в папку с программой и поменять текущее название на название файла
        :param scr: Текущий экран, на котором необходимо отрисовать врагов
        '''
        self.surf = pygame.image.load("enemy.png")
        self.surf.set_colorkey((255, 255, 255))
        self.pos = np.array([randint(100, res[0] - 100), randint(100, res[1] - 100)])
        self.scr = scr
        self.speed = randint(-2, 2)
        self.radius = 50
        self.score = 10

    def move(self):
        '''
        Отвечает за обновление координат врагов, они движутся по горизонтали, по достижении стенок отражаются
        '''
        self.pos[0] += self.speed
        if self.pos[0] <= self.radius:
            self.speed = -self.speed
            self.pos[0] = self.radius
        elif self.pos[0] >= res[0] - self.radius:
            self.speed = -self.speed
            self.pos[0] = self.pos[0] - self.radius

    def attack(self):
        '''
        Метод создания бомб, вылетающих из врагов
        '''
        bomb_massive.append(Bomb(self.scr, self.pos, self.speed))

    def draw(self):
        '''
        Рисует врагов 
        '''
        self.scr.blit(self.surf, self.pos - np.array([50, 50]))


class Bomb:
    '''
    Класс падающих бомб
    '''

    def __init__(self, scr, pos, speed_x):
        '''
        Отвечает за базовые параметры бомбы
        :param scr: Текущий экран
        :param pos: Координаты бомбы, они же координаты ВРАГА который её сбросил
        :param speed_x: Скорость бомбы по горизонтали
        '''
        self.scr = scr
        self.pos = deepcopy(pos)
        self.speed_y = 0
        self.speed_x = speed_x
        self.radius = 10

    def move(self, index):
        '''
        Отвечает за движение бомбы и проверку её попадания в игрока
        :param index: Номер бомбы в базе данных
        :return: ничего
        '''
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        self.speed_y += gravity
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed_x = -self.speed_x
        elif self.pos[0] > res[0]:
            self.pos[0] = res[0]
            self.speed_x = -self.speed_x
        if self.pos[1] >= res[1] - 50:
            global tank_player, bomb_massive
            if (self.pos[0] >= tank_player.pos[0] - 100) and (self.pos[0] <= tank_player.pos[0] + 100):
                tank_player.hp -= 1
            del bomb_massive[index]

    def draw(self):
        '''
        Рисует бомбу
        '''
        circle(self.scr, (70, 70, 70), self.pos, self.radius)


screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

finished = False
charging = False

tank_player = Tank(screen)
mouse_pos = np.array((0, 0))

# Задаём переменные, которые будут хранить данные о сцене
tick = 0
bullet_massive = []
enemy_massive = []
target_massive = []
bomb_massive = []
score = 0

# Задаём константы
gravity = 1
tank_maxspeed = 5

while not finished:
    # Данным циклом пробегаем по текущим "происшествиям", совершаем ситуативные действия
    for event in pygame.event.get():
        # Останавливаем программу при закрытии окна
        if event.type == pygame.QUIT:
            finished = True
        # Останавливаем программу при нажатии кнопки "Esc"
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                finished = True
        # Обновляем координаты мыши в случае её движения
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            tank_player.aiming()
        # Начинаем зарядку орудия в случае нажания ЛКМ
        elif event.type == pygame.MOUSEBUTTONDOWN:
            charging = True
        # Выстреливаем по отпускании ЛКМ
        elif event.type == pygame.MOUSEBUTTONUP:
            charging = False
            tank_player.shoot()
            tank_player.power = 0

    # Блок отвечает за движение танка по горизонтали, keys[100] и keys[97] - "D" и "A" соответственно
    keys = pygame.key.get_pressed()
    if keys[100] and keys[97]:
        tank_player.speed = 0
    elif keys[100]:
        tank_player.speed = tank_maxspeed
    elif keys[97]:
        tank_player.speed = -tank_maxspeed
    else:
        tank_player.speed = 0

    # ПРоверяем, не умер ли игрок
    if tank_player.hp <= 0:
        finished = True
        print("GAME OVER")
        print("Your score is:", score)
    # Запускаем функцию движения танка
    tank_player.move()

    # Данная пачка циклов отвечает за движение всех объектов на сцене
    for i in range(len(target_massive) - 1, -1, -1):
        target_massive[i].move()
    for i in range(len(enemy_massive) - 1, -1, -1):
        enemy_massive[i].move()
    for i in range(len(bomb_massive) - 1, -1, -1):
        bomb_massive[i].move(i)
    for i in range(len(bullet_massive) - 1, -1, -1):
        bullet_massive[i].move()

    # Данная пачка циклов отвечает за проверку столкновений объектов
    for i in range(len(bullet_massive) - 1, -1, -1):
        target_massive, t = collision_check(bullet_massive[i], target_massive)
        if t:
            del bullet_massive[i]
    for i in range(len(bullet_massive) - 1, -1, -1):
        enemy_massive, t = collision_check(bullet_massive[i], enemy_massive)
        if t:
            del bullet_massive[i]

    # Данный блок отвечает за содание новых объектов через заданные промежутки времени
    if tick % (fps * 2) == 0:
        target_massive.append(Target(screen))
    if tick % (fps * 3) == 0:
        enemy_massive.append(Enemy(screen))

    # Отвечает за начало "Бомбардировок" у всех ВРАГОВ
    if tick % (fps * 5) == 0:
        for i in enemy_massive:
            i.attack()

    # Данный блок циклов отвечает за отрисовку все объектов на сцене
    for i in range(len(target_massive) - 1, -1, -1):
        target_massive[i].draw()
    for i in range(len(enemy_massive) - 1, -1, -1):
        enemy_massive[i].draw()
    for i in range(len(bomb_massive) - 1, -1, -1):
        bomb_massive[i].draw()
    for i in range(len(bullet_massive) - 1, -1, -1):
        bullet_massive[i].draw()

    # Отвечает за вывод текущего количества здоровья на экран
    font = pygame.font.Font(None, 40)
    text = font.render("HP:" + str(tank_player.hp), True, (255, 0, 0))
    place = text.get_rect(center=(150, 150))
    screen.blit(text, place)

    # Отвечает за вывод текущего счёта на экран
    font = pygame.font.Font(None, 40)
    text = font.render("SCORE:" + str(score), True, (0, 100, 255))
    place = text.get_rect(center=(150, 100))
    screen.blit(text, place)

    # Отвечает за увеличение мощи выстрела при удержинии кнопки мыши
    if charging:
        tank_player.power += 2
        if tank_player.power > 100:
            tank_player.power = 100

    clock.tick(fps)

    # Обновляет экран
    tank_player.draw()
    pygame.display.update()
    tick += 1
    screen.fill((255, 200, 255))
