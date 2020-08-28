'''
To do list

Make Initial classes STARTEd 25/08/2020

'''


import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 55, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)


class Game:
    def __init__(self):
        self.done = False
        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)
        self.done = False
        self.clock = pygame.time.Clock()

    def do(self):
        while not self.done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            # --- Game logic should go here

            # --- Screen-clearing code goes here

            # If you want a background image, replace this clear with blit'ing thebackground image.
            self.screen.fill(WHITE)

            # --- Drawing code should go here

            pygame.display.flip()

            self.clock.tick(60)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # I get the image bad.png from my files within the same directory and convert it to a format pycharm can easily understand.
        self.image = pygame.image.load('Design.png').convert()

        # This makes white colours transparent.
        self.image.set_colorkey(WHITE)

        # Helps with dimensioning and positioning the sprite
        self.rect = self.image.get_rect()


pygame.init()

pygame.display.set_caption("My Game")

game = Game()

game.do()

# Close the window and quit.
pygame.quit()