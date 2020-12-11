import pygame

if __name__ == '__main__':
    pygame.init()
    w, h = 800, 600
    screen = pygame.display.set_mode((w, h))
    running = True
    fps = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()