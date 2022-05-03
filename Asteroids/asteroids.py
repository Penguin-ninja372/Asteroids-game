# ASTEROIDS GAME
# Started: Dec 4 2021
# By Tom

import pygame
import math
import os
import random
pygame.init()
pygame.font.init()
os.chdir(os.path.dirname(__file__))

WIDTH = 1600
HEIGHT = 1200
win = pygame.display.set_mode((1200, 800), pygame.FULLSCREEN)
pygame.display.set_caption('Asteroids game')
W, H = win.get_size()

PI = 3.141592653589793
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (153, 0, 0)
GREEN = (0, 153, 0)
CYAN = (0, 153, 153)
NORMAL = (20, 20, 30)
FREEZE = (20, 35, 45)
POWER = (45, 20, 20)

x_move = 0
y_move = 0

freeze_img = pygame.transform.scale(pygame.image.load('freeze_bar.png'), (140, 30))
freeze_mode = False
freeze_count = 300
power_img = pygame.transform.scale(pygame.image.load('power_bar.png'), (140, 30))
power_mode = False
power_count = 420

class Space_ship():
    def __init__(self, rotation=90, vel=0, x=W/2, y=H/2):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.vel = vel
        self.img = pygame.transform.scale(pygame.image.load('Spaceship.png'), (80, 60))
        self.mask = pygame.mask.from_surface(self.img)
        self.moving_img = pygame.transform.scale(pygame.image.load('Movingship.png'), (80, 60))
        self.moving_mask = pygame.mask.from_surface(self.moving_img)
        self.health = 100
        self.health_bar = pygame.transform.scale(pygame.image.load('health.png'), (200, 50))

    def draw(self, win):
        win.blit(copy_img, (self.x - int(copy_img.get_width() / 2) - top_left_x, self.y - int(copy_img.get_height() / 2) - top_left_y))

class Bullet():
    def __init__(self):
        self.x = p1.x
        self.y = p1.y
        self.xvel = 10 * math.cos(radian)
        self.yvel = -1 * (10 * math.sin(radian))
        self.rotation = p1.rotation
        self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('bullet.png'), (40, 20)), self.rotation)
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x - top_left_x - self.img.get_width()//2, self.y - top_left_y - self.img.get_height()//2))

class Asteroid():
    def __init__(self, x, y, rotation, img):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = img[0]
        self.img = img[1]
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x - top_left_x - self.img.get_width()//2, self.y - top_left_y - self.img.get_height()//2))

class Health_up():
    def __init__(self, x, y, rotation, value, used):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = 1
        self.value = value
        self.img = pygame.transform.scale(pygame.image.load('health_up.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.img)
        self.used = used

    def draw(self, win):
        win.blit(self.img, (self.x - top_left_x - self.img.get_width()//2, self.y - top_left_y - self.img.get_height()//2))

def reset_rotation(deg):
    if deg >= 360:
        deg -= 360
    if deg < 0:
        deg += 360

    return deg

def generate_asteroid(min, max):
    random_x, random_y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    random_rotation = random.randint(0, 360)

    SMALL = (3, pygame.image.load('small_asteroid.png'))
    MED = (2, pygame.image.load('med_asteroid.png'))
    BIG = (1, pygame.image.load('large_asteroid.png'))
    sizes = (SMALL, MED, BIG)
    size_index = random.randint(min, max)
    random_size = sizes[size_index]

    return random_x, random_y, random_rotation, random_size

def move_object(override, *args):
    for object in args[0]:
        object.rotation = reset_rotation(object.rotation)

        object_radian = deg2rad(object.rotation)

        object_x_vel = math.cos(object_radian)*object.speed
        object_y_vel = math.sin(object_radian)*object.speed

        if object.x <= 0 or object.x >= WIDTH:
            object.rotation = (object.rotation - 180) * -1

            object_radian = deg2rad(object.rotation)

            object_x_vel = math.cos(object_radian)*object.speed
            object_y_vel = math.sin(object_radian)*object.speed

        if object.y <= 0 or object.y >= HEIGHT:
            object.rotation *= -1

            object_radian = deg2rad(object.rotation)

            object_x_vel = math.cos(object_radian)*object.speed
            object_y_vel = math.sin(object_radian)*object.speed

        if freeze_mode == False or override == True:
            object.x += object_x_vel
            object.y += object_y_vel


def draw_window(win):
    win.fill(BLACK)

    if freeze_mode:
        bg_colour = FREEZE
    else:
        bg_colour = NORMAL

    pygame.draw.rect(win, bg_colour, (0 - top_left_x, 0 - top_left_y, WIDTH, HEIGHT))
    pygame.draw.rect(win, WHITE, (0 - top_left_x, 0 - top_left_y, WIDTH, HEIGHT), 3)

    if power_mode:
        pygame.draw.circle(win, POWER, (p1.x - top_left_x, p1.y - top_left_y), 50)

    for bullet in bullet_list:
        bullet.draw(win)

    for asteroid in asteroid_list:
        asteroid.draw(win)

    if level % 2 == 0 and health_plus.used == False:
        health_plus.draw(win)

    p1.draw(win)

    health_width = round(p1.health / 100 * 178)
    pygame.draw.rect(win, (180, 0, 0), (40, 40, 178, 27))
    pygame.draw.rect(win, (0, 180, 0), (40, 40, health_width, 27))
    win.blit(p1.health_bar, (30, 30))

    power_width = round(power_count / 420 * 125)
    freeze_width = round(freeze_count / 300 * 125)
    win.blit(power_img, (30, 90))
    pygame.draw.rect(win, (255, 100, 0), (37, 98, power_width, 10))
    win.blit(freeze_img, (30, 130))
    pygame.draw.rect(win, (0, 180, 220), (37, 138, freeze_width, 10))

    font = pygame.font.SysFont("comicsans", 60)
    text = font.render(str(score), True, CYAN)
    win.blit(text, (W//2 - text.get_width()//2, 30))

    if p1.health <= 0:
        win.fill(NORMAL)
        font = pygame.font.SysFont("comicsans", 110)
        font2 = pygame.font.SysFont("comicsans", 40)
        font3 = pygame.font.SysFont("comicsans", 65)
        text = font.render("GAME OVER", True, RED)
        text2 = font2.render("Press ESC to exit", True, GREEN)
        text3 = font3.render(f"Final Score - {str(score)}", True, CYAN)
        win.blit(text, (W//2 - text.get_width()//2, H//5))
        win.blit(text2, (W//2 - text2.get_width()//2, H//4 * 3))
        win.blit(text3, (W//2 - text3.get_width()//2, H//2))

    pygame.display.update()


deg2rad = lambda deg: deg*PI/180

p1 = Space_ship()
copy_img = p1.img
radian = deg2rad(p1.rotation)

asteroid_list = []
bullet_list = []
level = 0
score = 0
clock = pygame.time.Clock()
top_left_x = 0
top_left_y = 0

run = True
while run:
    clock.tick(60)

    if len(asteroid_list) == 0:
        level += 1

        for i in range(48):
            X, Y, R, S = generate_asteroid(0, 2)
            asteroid_list.append(Asteroid(X, Y, R, S))

        if level % 2 == 0:
            health_plus = Health_up(random.randint(1, WIDTH), random.randint(1, HEIGHT), random.randint(1, 360), 30, False)

    if level % 2 == 0 and health_plus.used == False:
        offset = (round((health_plus.x - health_plus.img.get_width()//2) - (p1.x - p1.moving_img.get_width()//2)), round((health_plus.y - health_plus.img.get_height()//2) - (p1.y - p1.moving_img.get_height()//2)))

        check_hit = p1.moving_mask.overlap(health_plus.mask, offset)
        if check_hit:
            p1.health += health_plus.value
            health_plus.used = True

        move_object(False, [health_plus])

    if freeze_mode:
        freeze_count -= 1
        if freeze_count <= 0:
            freeze_mode = False
    if freeze_mode == False:
        if freeze_count < 300:
            freeze_count += 0.5

    if power_mode:
        for bullet in bullet_list:
            bullet.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('power_bullet.png'), (40, 20)), bullet.rotation)
        power_count -= 1
        if power_count <= 0:
            for bullet in bullet_list:
                bullet.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('bullet.png'), (40, 20)), bullet.rotation)
            power_mode = False
    if power_mode == False:
        if power_count <= 420:
            power_count += 0.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(bullet_list) < 3:
                    bullet_list.append(Bullet())

            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_x:
                freeze_mode = True

            if event.key == pygame.K_c:
                power_mode = True

    for bullet in bullet_list:
        bullet.x += bullet.xvel
        bullet.y += bullet.yvel

        if bullet.x <= 0 or bullet.x >= WIDTH or bullet.y <= 0 or bullet.y >= HEIGHT:
            try:
                bullet_list.remove(bullet)
            except:
                pass

        for bullet in bullet_list:
            for asteroid in asteroid_list:
                offset = (round((asteroid.x - asteroid.img.get_width()//2) - (bullet.x - bullet.img.get_width()//2)), round((asteroid.y - asteroid.img.get_height()//2) - (bullet.y - bullet.img.get_height()//2)))

                check_hit = bullet.mask.overlap(asteroid.mask, offset)
                if check_hit:
                    bullet_list.remove(bullet)

                    if asteroid.speed == 1:
                        score += 15
                    elif asteroid.speed == 2:
                        score += 10
                    elif asteroid.speed == 3:
                        score += 5

                    if power_mode == False:
                        new_asteroid_speed = asteroid.speed + 1
                        if new_asteroid_speed == 2:
                            for _ in range(2):
                                new_asteroid = Asteroid(asteroid.x, asteroid.y, random.randint(0, 360), (2, pygame.image.load('med_asteroid.png')))
                                asteroid_list.append(new_asteroid)
                                for _ in range(6):
                                    move_object(True, [new_asteroid])
                                    pygame.display.update()
                        if new_asteroid_speed == 3:
                            for _ in range(2):
                                new_asteroid = Asteroid(asteroid.x, asteroid.y, random.randint(0, 360), (3, pygame.image.load('small_asteroid.png')))
                                asteroid_list.append(new_asteroid)
                                for _ in range(6):
                                    move_object(True, [new_asteroid])
                                    pygame.display.update()

                    asteroid_list.remove(asteroid)
                    break

        draw_window(win)

    move_object(False, asteroid_list)

    p1.rotation = reset_rotation(p1.rotation)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if p1.vel < 4:
            p1.vel += 0.4

        radian = deg2rad(p1.rotation)
        x_move = p1.vel * math.cos(radian)
        y_move = p1.vel * math.sin(radian)

        p1.x += round(x_move)
        p1.y -= round(y_move)

        top_left_x += round(x_move)
        top_left_y -= round(y_move)

        if p1.x < 0 or p1.x > WIDTH:
            p1.x -= round(x_move)
            top_left_x -= round(x_move)
        if p1.y < 0 or p1.y > HEIGHT:
            p1.y += round(y_move)
            top_left_y += round(y_move)

        copy_img = p1.moving_img
        copy_img = pygame.transform.rotate(copy_img, p1.rotation)

        for asteroid in asteroid_list:
            offset = (round((asteroid.x - asteroid.img.get_width()//2) - (p1.x - p1.moving_img.get_width()//2)), round((asteroid.y - asteroid.img.get_height()//2) - (p1.y - p1.moving_img.get_height()//2)))

            check_hit = p1.moving_mask.overlap(asteroid.mask, offset)
            if check_hit:
                if asteroid.speed == 3:
                    p1.health -= 5
                if asteroid.speed == 2:
                    p1.health -= 10
                if asteroid.speed == 1:
                    p1.health -= 15

                asteroid_list.remove(asteroid)

    else:
        if p1.vel > 0:
            p1.vel -= 0.1

        radian = deg2rad(p1.rotation)
        x_move = p1.vel * math.cos(radian)
        y_move = p1.vel * math.sin(radian)

        p1.x += round(x_move)
        p1.y -= round(y_move)

        top_left_x += round(x_move)
        top_left_y -= round(y_move)

        if p1.x < 0 or p1.x > WIDTH:
            p1.x -= round(x_move)
            top_left_x -= round(x_move)
        if p1.y < 0 or p1.y > HEIGHT:
            p1.y += round(y_move)
            top_left_y += round(y_move)

        copy_img = p1.img
        copy_img = pygame.transform.rotate(copy_img, p1.rotation)

        for asteroid in asteroid_list:
            offset = (round((asteroid.x - asteroid.img.get_width()//2) - (p1.x - p1.img.get_width()//2)), round((asteroid.y - asteroid.img.get_height()//2) - (p1.y - p1.img.get_height()//2)))

            check_hit = p1.mask.overlap(asteroid.mask, offset)
            if check_hit:
                if asteroid.speed == 3:
                    p1.health -= 3
                if asteroid.speed == 2:
                    p1.health -= 6
                if asteroid.speed == 1:
                    p1.health -= 10

                asteroid_list.remove(asteroid)

    if keys[pygame.K_RIGHT]:
        if keys[pygame.K_UP]:
            copy_img = p1.moving_img
        else:
            copy_img = p1.img

        p1.rotation -= 3
        copy_img = pygame.transform.rotate(copy_img, p1.rotation)

    if keys[pygame.K_LEFT]:
        if keys[pygame.K_UP]:
            copy_img = p1.moving_img
        else:
            copy_img = p1.img

        p1.rotation += 3
        copy_img = pygame.transform.rotate(copy_img, p1.rotation)

    draw_window(win)

pygame.quit()
