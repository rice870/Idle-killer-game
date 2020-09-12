'''
To do list

Make Initial classes STARTEd 25/08/2020

'''

import pygame
import math

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


def find_rel_angle(cx, cy, ox, oy):
    rx = ox - cx
    ry = oy - cy
    return (180 / math.pi) * -math.atan2(ry, rx)


def draw(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


def change_costume(object, picture, x, y, colourkey, rot_change, size_change):
    object.image = pygame.image.load(picture).convert()
    object.image = pygame.transform.rotozoom(object.image, rot_change, size_change)
    object.image.set_colorkey(colourkey)
    object.rect = object.image.get_rect()
    object.rect.x = x
    object.rect.y = y


def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class GameSprites(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.picture = 'Images/Design.png'
        self.x = 0
        self.y = 0
        self.colour_key = WHITE
        self.rot_change = 0
        self.size_change = 1
        self.original_x = self.x

    def change_costume(self):
        self.image = pygame.image.load(self.picture).convert()
        self.image = pygame.transform.rotozoom(self.image, 0, self.size_change)
        self.image.set_colorkey(self.colour_key)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.rot_change)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)

        surface.blit(rotated_image, new_rect.topleft)

    def update(self):
        self.change_costume()


class Player(GameSprites):
    def __init__(self):
        super().__init__()
        self.picture = 'Images/Bed.png'
        self.x = 10
        self.y = 10
        self.colour_key = WHITE
        self.rot_change = 0
        self.size_change = 0
        self.change_costume()


class Menu(GameSprites):
    def __init__(self, picture, x, y, colour_key, angle, zoom):
        super().__init__()
        self.picture = picture
        self.x = x
        self.y = y
        self.colour_key = colour_key
        self.rot_change = angle
        self.size_change = zoom
        self.original_x = self.x
        self.change_costume()


class Game:
    def __init__(self):
        self.my_font = pygame.font.SysFont('adobedevanagaribolditalic', 30)
        self.small_font = pygame.font.SysFont('adobedevanagaribolditalic', 20)
        self.sprite_list = pygame.sprite.Group()
        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)
        self.done = False
        self.clock = pygame.time.Clock()
        self.selected = False
        self.fish = Menu('Images/fish.png', 569, 215, WHITE, 0, 1)
        self.bed = Menu('Images/Bed.png', 303, 215, WHITE, 0, 1)
        self.menu_bg = Menu('Images/Design.png', 0, 0, WHITE, 0, 1)
        self.phase = 0
        self.initial_full_text = 'In this game you need to make as much money as you can.\n' \
                                 'Each day you can catch up to five fish. Be careful though,\n' \
                                 'as you don\'t want to kill too many fish, since there are\n' \
                                 'only 20 in total. Everyday they reproduce by 25%. Each day\n' \
                                 'you have the choice of whether you fish or not and how \n' \
                                 'many fish you want to catch, as long as you don\'t catch \n' \
                                 'more than 5. See how much money you can make before your \n' \
                                 '10 days run out, but make sure you don\'t ruin the ecosystem! \n' \
                                 'Best of luck!'
        self.frames = 0

    def selecting_bed(self):
        x_in_range = self.bed.rect.x < pygame.mouse.get_pos()[0] < self.bed.rect.x + self.bed.rect.width
        y_in_range = self.bed.rect.y < pygame.mouse.get_pos()[1] < self.bed.rect.y + self.bed.rect.height
        return x_in_range and y_in_range

    def selecting_fish(self):
        x_in_range = self.fish.rect.x < pygame.mouse.get_pos()[0] < self.fish.rect.x + self.fish.rect.width
        y_in_range = self.fish.rect.y < pygame.mouse.get_pos()[1] < self.fish.rect.y + self.fish.rect.height
        return x_in_range and y_in_range

    def initial_screen(self):
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.phase += 1

        self.screen.fill(0x0080ff)
        blit_text(self.screen, self.initial_full_text[:int(self.frames/2)], (150, 0), self.my_font, WHITE)
        self.frames += 1

        pygame.display.flip()

        self.clock.tick(60)

    def menu_screen(self):
        self.sprite_list.add(self.menu_bg, self.bed, self.fish)
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and (self.selecting_bed() or self.selecting_fish()):
                self.phase += 1

        # --- Game logic should go here
        bed_center_x = self.bed.rect.x + 0.5 * self.bed.rect.width
        bed_center_y = self.bed.rect.y + 0.5 * self.bed.rect.height
        angle = find_rel_angle(bed_center_x, bed_center_y, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # --- Screen-clearing code goes here
        for sprite in self.sprite_list:
            sprite.update()

        if self.selecting_bed():
            self.bed.size_change = 1.5
            self.bed.rect.x = self.bed.original_x - (self.bed.rect.width / 6)
        else:
            self.bed.size_change = 1
        if self.selecting_fish():
            self.fish.size_change = 1.3
        else:
            self.fish.size_change = 0.8

        # If you want a background image, replace this clear with blit'ing the background image.
        self.screen.fill(0x0080ff)

        # --- Drawing code should go here
        for sprite in self.sprite_list:
            sprite.draw(self.screen)

        self.screen.blit(self.my_font.render("Which will you choose?", False, BLACK), (350, 110))
        self.screen.blit(self.small_font.render("Sleep for the day", False, BLACK), (294, 186))
        self.screen.blit(self.small_font.render("Go fishing", False, BLACK), (554, 187))

        pygame.display.flip()

        self.clock.tick(60)

    def do(self):

        while not self.done and self.phase == 0:
            self.initial_screen()

        while not self.done and self.phase == 1:
            self.menu_screen()

        for sprite in self.sprite_list:
            sprite.kill()


pygame.init()

pygame.display.set_caption("My Game")

game = Game()

game.do()

# Close the window and quit.
pygame.quit()
