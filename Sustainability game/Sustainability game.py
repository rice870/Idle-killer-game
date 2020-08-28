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

# Set the width and height of the screen [width, height]
size = (1000, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)

    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()