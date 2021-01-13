import random

import pygame
import os
import sys


def load_sprite_sheet(sheetname, x, y, sx=-1, sy=-1, colorkey=None):
    fullname = os.path.join('img', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width / x
    sizey = sheet_rect.height / y
    for i in range(y):
        for j in range(x):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, 16384)
            if sx != -1 or sy != -1:
                image = pygame.transform.scale(image, (sx, sy))
            sprites.append(image)
    sprite_rect = sprites[0].get_rect()
    return (sprites, sprite_rect)


class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5),
                                                           -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = w * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = h * 0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, score):
        score_digits = [int(i) for i in str(score)]
        score_digits = [0] * (5 - len(score_digits)) + score_digits
        self.image.fill(background_color)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0


class Dino(pygame.sprite.Sprite):
    def __init__(self, field):
        pygame.sprite.Sprite.__init__(self)
        self.normal = pygame.image.load(os.path.join(img_folder, 'dino/normal.png'))
        self.normal1 = pygame.image.load(os.path.join(img_folder, 'dino/normal_one.png'))
        self.normal2 = pygame.image.load(os.path.join(img_folder, 'dino/normal_two.png'))
        self.hited = pygame.image.load(os.path.join(img_folder, 'dino/hited.png'))
        self.shift1 = pygame.image.load(os.path.join(img_folder, 'dino/shift_one.png'))
        self.shift2 = pygame.image.load(os.path.join(img_folder, 'dino/shift_two.png'))

        self.jump_sound = pygame.mixer.Sound('sound/jump.wav')

        self.image = self.normal

        self.default_rect = self.normal.get_rect()
        self.down_rect = self.shift1.get_rect()

        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.y = int(h / 2 - 18 * 2.2)
        self.rect.y = self.y
        self.field = field
        self.last = 0
        self.image_tick = 0
        self.counter = 0

        self.grav = 0.6
        self.default_jump_speed = -10.8
        self.vy = 0
        self.tick_of_btn_jump_pressed = 0
        self.isJump = False
        self.isDown = False
        self.isStart = False

    def jump(self):
        if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed(
        )[pygame.K_UP]) and not self.isJump and not self.isDown:
            self.tick_of_btn_jump_pressed += 1
            if self.tick_of_btn_jump_pressed >= 7:
                self.vy = self.default_jump_speed
                self.isJump = True
            else:
                self.vy = self.default_jump_speed * (self.tick_of_btn_jump_pressed / 7)
        else:
            if self.tick_of_btn_jump_pressed > 0:
                self.isJump = True
                self.tick_of_btn_jump_pressed = 0
                self.jump_sound.play()
                if self.vy >= -9:
                    self.vy = -9
            if self.isJump:
                self.rect.y += self.vy
                self.vy += self.grav * (3 if self.isDown else 1)
                if not self.isDown:
                    self.image_tick = 0
            if self.rect.y >= self.y:
                self.rect.y = self.y
                self.isJump = False

    def down(self):
        if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_DOWN]):
            self.isDown = True
            if self.counter % 5 == 0 and self.isDown:
                self.image_tick = (self.image_tick + 1) % 2 + 4
        else:
            self.isDown = False

    def update(self):
        self.jump()
        if self.isStart:
            self.down()
            self.change_sprite_tick()
            if self.counter % 5 == 0 and not self.isJump and not self.isDown:
                self.image_tick = (self.image_tick + 1) % 2 + 2
            self.counter += 1

    def draw(self):
        screen.blit(self.image, self.rect)

    def change_sprite_tick(self):
        if self.image_tick == 0:
            self.image = self.normal
        elif self.image_tick == 2:
            self.image = self.normal2
        elif self.image_tick == 3:
            self.image = self.normal1

        elif self.image_tick == 4:
            self.image = self.shift2
        elif self.image_tick == 5:
            self.image = self.shift1

        if self.image_tick in [0, 2, 3]:
            self.rect.width = self.default_rect.width
        elif self.image_tick in [4, 5]:
            self.rect.width = self.down_rect.width
        #pygame.draw.rect(self.field.screen, "black", self.rect)
        #pygame.display.flip()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self, self.group)
        self.images = [pygame.image.load(os.path.join(img_folder, 'Enemy/big_cactus_x1.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/big_cactus_x2.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/big_cactus_x3.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/small_cactus_x1.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/small_cactus_x2.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/small_cactus_x3.png'))]
        index = random.randrange(0, 6)
        self.image = self.images[index]
        self.rect = self.image.get_rect()
        self.rect.y = int(h / 2 - 18 * 2.2)
        if index > 2:
            self.rect.y -= 5
        self.rect.left = w + self.rect.width
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()


class Pterodactyl(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self, self.group)
        self.images = [pygame.image.load(os.path.join(img_folder, 'Enemy/harpy/harpy1.png')),
                       pygame.image.load(os.path.join(img_folder, 'Enemy/harpy/harpy2.png'))]
        self.rect = self.images[0].get_rect()
        self.harpy_h = [int(h / 2 - 14 * 2.2), int(h / 2 - 32 * 2.2), int(h / 2 - 44 * 2.2)]
        self.rect.y = self.harpy_h[random.randrange(0, 3)]
        self.rect.left = w + self.rect.width
        self.image = self.images[0]
        self.speed = speed
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect.x -= self.speed
        self.counter += 1
        if self.rect.right < 0:
            self.kill()


class Field(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'Field.png'))
        self.checkPoint_sound = pygame.mixer.Sound('sound/checkPoint.wav')
        self.rect = self.image.get_rect()
        self.rect.y = h / 2
        self.count = 0
        self.tick_counter = 0
        self.status = 0
        self.screen = screen
        self.time = True
        self.last_speed_up = 0
        self.last_checkpoint = 0
        self.last_day_and_night_switch = 0

    def update(self):
        global v
        if self.status:
            self.rect.x -= v
            if -v < self.rect.x % 50 < v:
                self.count += 1
            if v < 10 and self.tick_counter % 700 == 699 and self.last_speed_up != self.tick_counter:
                self.last_speed_up = self.tick_counter
                v += 1
        if self.rect.left <= -1450:
            self.rect.left = 0
        if self.get_score() > 0 and self.get_score() % 100 == 0:
            self.day_and_night_switch()
        if self.get_score() % 100 == 0 and self.get_score() != self.last_checkpoint:
            self.last_checkpoint = self.get_score()
            self.checkPoint_sound.play()
        if v < 10:
            self.tick_counter += 1

    def start(self):
        self.status = 1

    def stop(self):
        self.status = 0

    def day_and_night_switch(self):
        if self.get_score() != self.last_day_and_night_switch:
            self.time = not self.time
            self.last_day_and_night_switch = self.get_score()

    def render(self):
        global background_color
        self.screen.fill(background_color)
        if self.time and background_color < [255, 255, 255]:
            background_color = [i + 2 for i in background_color]
            if background_color > [255, 255, 255]:
                background_color = [255, 255, 255]
        elif not self.time and background_color > [20, 20, 20]:
            background_color = [i - 2 for i in background_color]
            if background_color < [30, 30, 30]:
                background_color = [30, 30, 30]

    def get_score(self):
        return self.count

    def draw(self):
        screen.blit(self.image, self.rect)


class Hi_scoreboard():
    def __init__(self):
        #self.images, self.rect1 = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.image.load("img/HI.png")
        self.HI_rect = self.image.get_rect()
        self.HI_rect.top = h * 0.1
        self.HI_rect.left = w * 0.7
        self.HI_scoreboard = Scoreboard(int(w * 0.78))

    def draw(self):
        self.HI_scoreboard.draw()
        screen.blit(self.image, self.HI_rect)

    def update_score(self, score):
        self.HI_scoreboard.update(score)


if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    v = 5
    fps = 60
    hi_score = 0
    background_color = [255, 255, 255]
    screen = pygame.display.set_mode((w, h))
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    sprites = pygame.sprite.Group()
    die_sound = pygame.mixer.Sound('sound/die.wav')
    field = Field(screen)
    dino = Dino(field)
    sprites.add(field)
    sprites.add(dino)

    scoreboard = Scoreboard()
    hi_scoreboard = Hi_scoreboard()

    cactus_group = pygame.sprite.Group()
    Cactus.group = cactus_group
    harpys_group = pygame.sprite.Group()
    Pterodactyl.group = harpys_group
    obstacle = None


    clock = pygame.time.Clock()
    running = True
    game_start = False
    game_over = False

    while running:
        # Смерть дино
        while game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                    sprites = pygame.sprite.Group()
                    field = Field(screen)
                    dino = Dino(field)
                    sprites.add(field)
                    sprites.add(dino)
                    cactus_group = pygame.sprite.Group()
                    Cactus.group = cactus_group
                    harpys_group = pygame.sprite.Group()
                    Pterodactyl.group = harpys_group
                    scoreboard = Scoreboard()
                    obstacle = None
                    game_start = False
                    game_over = False
            clock.tick(fps)
            pygame.display.flip()

        # "Меню" игры
        while not game_start and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            field.render()
            field.update()
            field.draw()
            dino.update()
            dino.draw()

            cactus_group.draw(screen)
            harpys_group.draw(screen)

            clock.tick(fps)
            pygame.display.flip()
            if dino.isJump:
                dino.isStart = True
            if not dino.isJump and dino.isStart:
                game_start = True
                field.start()

        # обработка главных событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Менеджер препятствий
        if len(cactus_group) < 2:
            if len(cactus_group) != 0:
                if obstacle.rect.right < w * 0.7 and random.randrange(0, 50) == 1:
                    obstacle = Cactus(v)
                    sprites.add(obstacle)
            else:
                obstacle = Cactus(v)
                sprites.add(obstacle)
        if len(harpys_group) == 0 and random.randrange(0, 200) == 1 and field.get_score() > 600:
            if obstacle.rect.right < w * 0.7:
                obstacle = Pterodactyl(v)
                sprites.add(obstacle)

        # Проверка столкновений
        for i in [*cactus_group, *harpys_group]:
            if pygame.sprite.collide_mask(dino, i):
                game_over = True
                dino.isStart = False
                dino.isJump = False
                die_sound.play()
                field.stop()

        # Обновление счётчика рекордов
        if game_over:
            score = field.get_score()
            if score > hi_score:
                hi_score = score

        field.render()  # Заливка окна цветом
        sprites.update()  # Обновление основных спрайтов (Поле, дино, препятствия)
        sprites.draw(screen)  # Отрисовка основных спрайтов
        scoreboard.update(field.get_score())  # Обновление счётчика
        scoreboard.draw()  # Отрисовка счётчика

        # Отображение рекордов
        if hi_score > 0:
            hi_scoreboard.update_score(hi_score)
            hi_scoreboard.draw()

        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()