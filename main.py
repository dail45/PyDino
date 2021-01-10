import pygame
import os


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
    def __init__(self, width, height, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5),
                                                           -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
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
        self.die_sound = pygame.mixer.Sound('sound/die.wav')
        self.checkPoint_sound = pygame.mixer.Sound('sound/checkPoint.wav')

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
        self.default_jump_speed = -10.5
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
                self.image_tick = 0
            if self.rect.y >= self.y:
                self.rect.y = self.y
                self.isJump = False

    def down(self):
        if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_DOWN]):
            self.isDown = True
            self.image_tick = (self.image_tick + 1) % 2 + 4
        else:
            self.isDown = False

    def update(self):
        self.jump()
        self.down()
        if self.isStart:
            if self.counter % 5 == 0:
                self.image_tick = (self.image_tick + 1) % 2 + 2
            self.change_sprite_tick()
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'Enemy/big_cactus_x3.png'))
        self.rect = self.image.get_rect()
        self.rect.y = h / 2 - 40
        self.rect.x = 1200

    def update(self):
        self.rect.x -= v
        if self.rect.x <= -100:
            self.rect.x = 1200


class Field(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, 'Field.png'))
        self.rect = self.image.get_rect()
        self.rect.y = h / 2
        self.count = 0
        self.status = 0
        self.screen = screen
        self.time = True
        self.last_speed_up = 0

    def update(self):
        global fps
        if self.status:
            self.rect.x -= v
            if -v < self.rect.x % 50 < v:
                #print(self.rect.x % 50, self.rect.x)
                self.count += 1
                #print(self.count)
            if fps <= 360 and self.count % 100 == 0 and self.last_speed_up != self.count:
                fps += 10
                self.last_speed_up = self.count
        if self.rect.left <= -1450:
            self.rect.left = 0

    def start(self):
        self.status = 1

    def stop(self):
        self.status = 0

    def day_and_night_switch(self):
        self.time = not self.time
        #print(self.time)

    def render(self):
        color = (0, 0, 0) if not self.time else (255, 255, 255)
        self.screen.fill(color)

    def get_score(self):
        return self.count

    def draw(self):
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    background_color = (255, 255, 255)
    screen = pygame.display.set_mode((w, h))
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    sprites = pygame.sprite.Group()
    field = Field(screen)
    field.start()
    dino = Dino(field)
    sprites.add(field)
    sprites.add(dino)
    scoreboard = Scoreboard(w, h)
    hiscoreboard = Scoreboard(w, h, int(w * 0.78))
    cactus = Enemy()
    sprites.add(cactus)
    v = 6
    fps = 60
    clock = pygame.time.Clock()
    running = True
    game_start = False
    while running:
        while not game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            field.render()
            field.draw()
            dino.update()
            dino.draw()
            clock.tick(fps)
            pygame.display.flip()
            if dino.isJump:
                dino.isStart = True
            if not dino.isJump and dino.isStart:
                game_start = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sprites.update()
        field.render()
        sprites.draw(screen)
        scoreboard.update(field.get_score())
        scoreboard.draw()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()