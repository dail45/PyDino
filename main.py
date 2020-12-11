import pygame
import os


class Field(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = field_img
        self.rect = self.image.get_rect()
        self.rect.y = h / 2
        self.count = 0
        self.status = 0
        self.screen = screen
        self.time = 0
        self.last_time_up = 0

    def update(self):
        global fps
        if self.status:
            self.rect.x -= v
            if self.rect.x % 80 == 0:
                self.count += 1
                print(self.count)
            if fps <= 360 and self.count % 100 == 0 and self.last_time_up != self.count:
                fps += 10
                self.last_time_up = self.count
        if self.rect.left <= -2400:
            self.rect.left = 0

    def start(self):
        self.status = 1

    def stop(self):
        self.status = 0

    def day_and_night_switch(self):
        self.time = ~self.time
        print(self.time)

    def render(self):
        color = (22, 22, 22) if ~self.time else (255, 255, 255)
        self.screen.fill(color)


if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    screen = pygame.display.set_mode((w, h))
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    field_img = pygame.image.load(os.path.join(img_folder, 'Field.png'))
    sprites = pygame.sprite.Group()
    field = Field(screen)
    field.start()
    sprites.add(field)
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