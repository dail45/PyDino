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
        self.y = h / 2 - 30 * 2.2
        self.rect.y = self.y
        self.field = field
        self.last = 0

    def update(self):
        if self.field.rect.x % 64 == 0 and self.field.rect.x != self.last:
            self.change_sprite_tick()
            self.last = self.field.rect.x

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
            if self.rect.x % 80 == 0:
                self.count += 1
                print(self.count)
            if fps <= 360 and self.count % 100 == 0 and self.last_speed_up != self.count:
                fps += 10
                self.last_speed_up = self.count
        if self.rect.left <= -2400:
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
    v = 8
    fps = 100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
                    print(dino.rect.y)
        sprites.update()
        field.render()
        sprites.draw(screen)
        clock = pygame.time.Clock()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()