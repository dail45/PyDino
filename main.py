import pygame
import os


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
            if self.isJump:
                self.rect.y += self.vy
                self.vy += self.grav * (2 if self.isDown else 1)
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
        if self.counter % 5 == 0:
            self.image_tick = (self.image_tick + 1) % 2 + 2

        self.jump()
        self.down()

        self.change_sprite_tick()
        self.counter += 1

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


if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    screen = pygame.display.set_mode((w, h))
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    sprites = pygame.sprite.Group()
    field = Field(screen)
    field.start()
    dino = Dino(field)
    sprites.add(field)
    sprites.add(dino)
    cactus = Enemy()
    sprites.add(cactus)
    v = 6
    fps = 60
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sprites.update()
        field.render()
        sprites.draw(screen)
        clock = pygame.time.Clock()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()