import pygame
import numpy
import math

def main():
    pygame.init()

    pygame.display.set_caption("Cube Art")
    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)

    white = pygame.Color(255, 255, 255)
    running = True
    while running:

        pygame.key.set_repeat(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   running = False

        ##rain.update(dt)
        
        screen.fill(white)
        ##rain.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()