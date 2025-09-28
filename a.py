# Persiapan File dan Aset-aset
from pygame import*
from random import randint
window = display.set_mode((700, 500))
display.set_caption("Shooter")
bg = transform.scale(image.load("galaxy.jpg"), (700, 500))

#Musik
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

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
        pass

lost = 0 #jumlah musuh yang lewat
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - 80)
            lost = lost + 1

#Membuat monsters
monster1 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
monster2 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
monster3 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
monster4 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))
monster5 = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 5))

#Membuat group Monster
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

ship = Player('rocket.png', 5, 400, 80, 100, 10)

#Inisiasi font
font.init()
font2 = font.Font(None, 36)
score = 0 #jumlah musuh yang ditembak
clock = time.Clock()
FPS = 60
finish = False
# Loop Game
run = True
while run:
    clock.tick(FPS)
    # Mendeteksi Event
    for e in event.get():
        if e.type == QUIT:
            run = False
    # Meletakkan Aset dan Objek
    if not finish:
        #Membuat text jumlah yang miss
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_score = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(bg, (0,0))
        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        window.blit(text_lose, (10, 50)) #Menampilkan jumlah miss
        window.blit(text_score, (10, 20)) #Menampilkan jumlah score
    display.update()


