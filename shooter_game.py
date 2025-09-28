# Persiapan File dan Aset-aset
from pygame import*
from random import randint
import time as t

window = display.set_mode((700, 500))
display.set_caption("Shooter")
bg = transform.scale(image.load("galaxy.jpg"), (700, 500))

#Musik
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Kelas GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


lost = 0 #jumlah musuh yang lewat
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - 80)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -20
            self.rect.x = randint(0, 700)

#Membuat Grup Bullet
bullets = sprite.Group()

#Membuat monsters
monster1 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
monster2 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
monster3 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
monster4 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
monster5 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))

#Membuat group Monster
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

#Membuat asteroid
asteroid1 = Asteroid('asteroid.png', randint(0, 620), -40, 80, 50, 1)
asteroid2 = Asteroid('asteroid.png', randint(0, 620), -40, 80, 50, 1)

#Membaut grup asteroid
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)


ship = Player('rocket.png', 5, 400, 80, 100, 10)


ammo = 10
reloading = False
reload_time = 0

#Inisiasi font
font.init()
font2 = font.Font(None, 36)
score = 0 #jumlah musuh yang ditembak
clock = time.Clock()
FPS = 60
finish = False

health = 3
# Loop Game
run = True
while run:
    clock.tick(FPS)
    # Mendeteksi Event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo > 0 and reloading == False:
                    ship.fire()
                    fire_sound.play()
                    ammo -= 1
    # Meletakkan Aset dan Objek
    if not finish:
        #Mendeteksi tabrakan
        collides = sprite.groupcollide(monsters, bullets, True, True)
        if collides:
            monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            score += 1

        #Membuat text jumlah yang miss
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_score = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(bg, (0,0))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_lose, (10, 50)) #Menampilkan jumlah miss
        window.blit(text_score, (10, 20)) #Menampilkan jumlah score
        bullets.draw(window)
        bullets.update()
        #Deteksi kemenangan
        if score == 10:
            finish = True
            text_win = font2.render("Kamu Menang!", 1, (255, 255, 255))
            window.blit(text_win, (200, 200))
        #Deteksi tabrakan dengan asteroid
        if sprite.spritecollide(ship, asteroids, True):
            health -= 1
        #Deteksi kekalahan
        if lost > 3:
            finish = True
            text_lose = font2.render("Kamu Kalah!", 1, (255, 255, 255))
            window.blit(text_lose, (200, 200))
        #mekanisme reloading
        if ammo == 0:
            reloading = True
            start = t.time()
        if reloading:
            text_lose = font2.render("Reloading...!", 1, (255, 255, 255))
            window.blit(text_lose, (200, 200))
            reload_time = t.time() - start
            ammo = 5
        if reload_time > 2:
            reloading = False
        if health < 0:
            finish = True
            text_win = font2.render("Game over D;", 1, (255, 255, 255))
            window.blit(text_win, (200,200))


    display.update()



