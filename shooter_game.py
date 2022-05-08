#Создай собственный Шутер!
from pygame import *
from random import randint
import time as t
font.init()
font2 = font.SysFont('Arial', 36)
#надписи выйгрыша и проигрыша
win = font2.render('ТЫ ВЫЙГРАЛ :)', 1, (255, 255, 255))
lose = font2.render('К СОЖЕЛЕНИЮ ТЫ ПРОИГРАЛ :(', 1, (255, 255, 255))


#создание библиотек
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, sizex, sizey):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullets(img_bullet, -5, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)
    

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > w_height:
            self.rect.x = randint(80, w_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullets(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > w_height:
            self.rect.x = randint(80, w_width - 80)
            self.rect.y = 0
            
#счетчики
score = 0
lost = 0
goal = 20
max_lost = 5

count_bullets = 5
time_reload = 3
hp = 3
#создание окна
window = display.set_mode((700, 500))
display.set_caption('shooter')

w_height = 500
w_width = 700
#картинки
img_back = 'galaxy.jpg'
img_rocket = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

bg = transform.scale(image.load(img_back), (w_width, w_height))
rocket = Player(img_rocket, 8, 400, 450, 65, 55)

finish = False
rel_fire = True

#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#создание группы монстров и астероидов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(1, 3), randint(80, w_width - 80), 80, 50, 50)
    monsters.add(monster) 

bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid(img_asteroid, 1, randint(80, w_width - 80), 80, 50, 50)
    asteroids.add(asteroid)
#игровой цикл
clock = time.Clock()
game = True
FPS = 20
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    #надписи счета очков, промахов и жизней
    if not finish:
        window.blit(bg, (0, 0))
        
        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        text_hp = font2.render('Жизни:' + str(hp), 1, (255, 255, 255))
        window.blit(text_hp, (10, 80))

        text_count_bullets = font2.render('Осталось пуль' + str(count_bullets) + '/ 5', 1, (255, 255, 255))
        window.blit(text_count_bullets, (10, 110))

        #столкновения
        if sprite.groupcollide(monsters, bullets, True, True):
            score = score + 1

        if sprite.spritecollide(rocket, asteroids, True) or sprite.spritecollide(rocket, monsters, True):
            hp = hp - 1
        

        #если в группе меньше штук чем обычно
        if len(monsters) < 5:
            monster = Enemy(img_enemy, randint(1, 3), randint(80, w_width - 80), 80, 50, 50)
            monsters.add(monster)

        if len(asteroids) < 3:
            asteroid = Asteroid(img_asteroid, randint(1, 3), randint(80, w_width - 80), 80, 50, 50)
            asteroids.add(asteroid)
        

        if count_bullets <= 0:
            time_reload.t()
            count_bullets = 5

        #условие проигрыша
        if hp == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        #условия выйгрыша
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        
  

        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        rocket.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        display.update()
    display.update()
    clock.tick(FPS)      