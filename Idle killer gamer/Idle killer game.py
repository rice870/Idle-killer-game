# This is the Idle killer game
# Idle killer game.py
# BETA v1.6 13/8/2020
# By Isaac Rice

'''
To do list:

Make player a sprite DONE 10/8/2020

Make bullet a sprite DONE 10/8/2020

Make enemies killable DONE 10/8/2020

Change Enemies look STARTED 11/8/2020

Make enemies spawn n times per second STARTED 11/8/2020 DONE 13/8/2020

Make enemies have and display health STARTED 13/8/2020 DONE 13/8/2020

Make money count appear STARTED 13/8/2020 DONE 08/18/2020

Make menu STARTED 18/08/2020

Do all comments
'''

import pygame
import random

# Colours that will be referenced later in the code.
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

        # Sets the background for my stickman
        self.image = pygame.Surface([12, 27])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = 50
        self.rect.y = 50
        self.x_change = 0
        self.y_change = 0
        self.last_x_change = 3
        self.last_y_change = 0

        self.draw()

    def move(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def moving(self):
        return self.x_change != 0 or self.y_change != 0

    def update_last_movement(self):
        if self.moving():
            self.last_x_change = self.x_change
            self.last_y_change = self.y_change

    def draw(self):
        # This function draws a stickman.
        pygame.draw.ellipse(self.image, BLACK, [1, 0, 10, 10], 0)

        # Legs
        pygame.draw.line(self.image, BLACK, [5, 17], [10, 27], 2)
        pygame.draw.line(self.image, BLACK, [5, 17], [0, 27], 2)

        # Body
        pygame.draw.line(self.image, RED, [5, 17], [5, 7], 2)

        # Arms
        pygame.draw.line(self.image, RED, [5, 7], [9, 17], 2)
        pygame.draw.line(self.image, RED, [5, 7], [1, 17], 2)

    def bounce(self):
        if self.rect.x + 12 > size[0]:
            self.x_change = 0
            self.rect.x -= 3
        elif self.rect.x < 0:
            self.x_change = 0
            self.rect.x += 3
        if self.rect.y + 27 > size[1]:
            self.y_change = 0
            self.rect.y -= 3
        elif self.rect.y < 50:
            self.y_change = 0
            self.rect.y += 3

    def update(self):
        self.move()
        self.bounce()
        self.update_last_movement()


class BulletClass(pygame.sprite.Sprite):
    # This class is for storing all the information regarding bullets
    def __init__(self, x, y, x_vel, y_vel):

        super().__init__()

        self.image = pygame.Surface([9, 9])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.score = 0

        self.rect.x = x
        self.rect.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

        self.draw()

    def draw(self):
        pygame.draw.line(self.image, RED, [4, 4], [self.x_vel + 3, self.y_vel + 3], 5)

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def update(self):
        self.move()
        bullet_enemy_collision = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in bullet_enemy_collision:
            enemy.health -= 1
            enemy.display_health()
            if enemy.health <= 0:
                enemy.kill()
            self.score += 1
        if self.rect.x > size[0] or self.rect.x < 0 or self.rect.y > size[1] or self.rect.y < 0:
            self.kill()

            return self.score


class Enemy(pygame.sprite.Sprite):
    def __init__(self):

        # Enemy is a child of Sprite, so I need to say that everything from pygame.sprite.Sprite's init attribute also needs to be in Enemy's (I don't want to
        # override the __init__ of pygame.sprite.Sprite)
        super().__init__()

        # I get the image band.png from my files within the same directory and convert it to a format pycharm can easily understand.
        self.image = pygame.image.load('Bad.png').convert()

        # This makes white colours transparent.
        self.image.set_colorkey(WHITE)

        # Helps with dimensioning and positioning the sprite
        self.rect = self.image.get_rect()

        self.max_health = random.randint(3, 6)
        self.health = self.max_health

        self.display_health()

    def pos_reset(self):
        self.rect.x = random.randrange(size[0]-33)
        self.rect.y = random.randrange(50, size[1]-47)

    def get_ready(self):
        self.pos_reset()
        enemy_list.add(self)
        sprite_list.add(self)

    def display_health(self):
        pygame.draw.line(self.image, BLACK, [0, 0], [33, 0], 2)
        pygame.draw.line(self.image, RED, [0, 0], [int(33 * (self.health/self.max_health)), 0], 2)

    def update(self, *args):
        self.display_health()
        if score > 10:
            self.image = pygame.image.load('meme.png').convert()
            self.image.set_colorkey(WHITE)


pygame.init()

# Set the width and height of the screen [width, height]
size = (500, 500)
screen = pygame.display.set_mode(size)

bullet_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
sprite_list = pygame.sprite.Group()

score = 0

enemy_spawns_per_second = 10
time_elapsed = 0

my_font = pygame.font.SysFont('adobedevanagaribolditalic', 30)

# Creates the list of enemies
for i in range(10):
    enemy = Enemy()
    enemy.get_ready()

player = Player()
sprite_list.add(player)

pygame.display.set_caption("Stickman game")

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
        elif event.type == pygame.KEYDOWN:
            # If you press WASD or arrow keys it changes velocity
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.x_change = -3
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.x_change = 3
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.y_change = -3
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.y_change = 3
            if event.key == pygame.K_SPACE:
                # If you click space a bullet is fired in the direction you're facing
                if player.x_change != 0 or player.y_change != 0:
                    bullet = BulletClass(player.rect.x, player.rect.y, player.x_change * 3, player.y_change * 3)
                    bullet_list.add(bullet)
                    sprite_list.add(bullet)
                else:
                    bullet = BulletClass(player.rect.x, player.rect.y, player.last_x_change * 3, player.last_y_change * 3)
                    bullet_list.add(bullet)
                    sprite_list.add(bullet)
        elif event.type == pygame.KEYUP:
            pygame.key.set_repeat(100, 0)
            # If you release WASD or arrow keys it resets velocity
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player.x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_w:
                player.y_change = 0

    # --- General game logic ----------------------------------------------------------------------------------------------------------------

    # Updates the players position and most recent movement (apart from no movement)
    for sprite in sprite_list:
        try:
            score += sprite.update()
        except TypeError:
            pass

    time_elapsed += clock.get_time()

    if time_elapsed >= 1000 / enemy_spawns_per_second:
        enemy = Enemy()
        enemy.get_ready()
        time_elapsed = 0

    # Clears the screen, makes the background white.
    screen.fill(WHITE)

    # This draws all sprites
    sprite_list.draw(screen)
    screen.blit(my_font.render(f'Money: {score}', False, BLACK), (0, 0))

    # Updates the screen
    pygame.display.flip()

    # Sets a frame limit to make the frame rate consistent
    clock.tick(60)

# Close the window and quit.
pygame.quit()
