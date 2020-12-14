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

        self.image = self.normal
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.y = int(h / 2 - 18 * 2.2)
        self.rect.y = self.y
        self.field = field
        self.last = 0
        self.jump_possible = 1
        self.t = 0
        self.v = 0
        self.g = 15

    def jump(self):
        if self.y + 10 >= self.rect.y >= self.y:
            self.jump_possible = 1
            self.rect.y = self.y
            self.t = 0
            self.v = 0
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.jump_possible:
                self.v += 130
            if not self.rect.y > self.y - 10:
                self.jump_possible = 0
        else:
            if self.rect.y != self.y:
                self.jump_possible = 0
        self.t += 1
        self.rect.y = self.y - (self.v * self.t - (self.g * self.t ** 2) / 2) / 100

    def update(self):
        if -v < self.field.rect.x % 50 <= v and self.field.rect.x != self.last:
            self.change_sprite_tick()
            self.last = self.field.rect.x
        self.jump()

    def change_sprite_tick(self):
        if self.image == self.normal1:
            self.image = self.normal2
        elif self.image == self.normal2:
            self.image = self.normal1
        elif self.image == self.shift1:
            self.image = self.shift2
        elif self.image == self.shift2:
            self.image = self.shift1
        elif self.image == self.normal:
            self.image = self.normal1


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
                print(self.rect.x % 50, self.rect.x)
                self.count += 1
                print(self.count)
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
        print(self.time)

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
    fps = 100
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