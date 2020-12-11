import pygame
import os


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = field_img
        self.rect = self.image.get_rect()
        self.rect.y = h / 2

    def update(self):
        self.rect.x -= 3
        if self.rect.left <= -2400:
            self.rect.left = 0


if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    screen = pygame.display.set_mode((w, h))
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    field_img = pygame.image.load(os.path.join(img_folder, 'Field.png'))
    sprites = pygame.sprite.Group()
    field = Field()
    sprites.add(field)

    fps = 60
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sprites.update()
        screen.fill("white")
        sprites.draw(screen)
        clock = pygame.time.Clock()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()