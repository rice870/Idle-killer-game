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
            word_surface = font.render(word, 1, color)
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
        self.picture = 'Images/my character1.png'
        self.x = 0
        self.y = 50
        self.colour_key = (0, 0, 1)
        self.rot_change = 0
        self.size_change = 1
        self.change_costume()
        self.fish_caught = 0


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
        self.huge_font = pygame.font.SysFont('adobedevanagaribolditalic', 50)
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
        self.fade = pygame.Surface(self.size)
        self.fade.fill(BLACK)
        self.phase = 'initial_screen'
        self.initial_full_text = 'In this game you need to make as much money as you can.\n' \
                                 'Each day you can catch up to five fish. Be careful though,\n' \
                                 'you don\'t want to kill too many fish, as there are\n' \
                                 'only 20 in total. Everyday they reproduce by 25%. Each day\n' \
                                 'you have the choice of whether you fish or not and how \n' \
                                 'many fish you want to catch, as long as you don\'t catch \n' \
                                 'more than 5. See how much money you can make before your \n' \
                                 '10 days run out, but make sure you don\'t ruin the ecosystem! \n' \
                                 'Best of luck! (Left click to continue)'
        self.frames = 0
        self.day = 1
        self.money = 0
        self.finished = False
        self.player = Player()
        self.fish_list = {'European Pilchard': 1, 'European Perch': 2, 'Red Snapper': 3, 'Atlantic Salmon': 4, 'Rainbow Trout': 5, 'Spotted Bass': 6, 'Northern Pike': 7}
        self.time_since_last_fish = 0

    def selecting_bed(self):
        x_in_range = self.bed.rect.x < pygame.mouse.get_pos()[0] < self.bed.rect.x + self.bed.rect.width
        y_in_range = self.bed.rect.y < pygame.mouse.get_pos()[1] < self.bed.rect.y + self.bed.rect.height
        return x_in_range and y_in_range

    def selecting_fish(self):
        x_in_range = self.fish.rect.x < pygame.mouse.get_pos()[0] < self.fish.rect.x + self.fish.rect.width
        y_in_range = self.fish.rect.y < pygame.mouse.get_pos()[1] < self.fish.rect.y + self.fish.rect.height
        return x_in_range and y_in_range

    def initial_screen(self):
        self.finished = False
        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.phase = 'menu'
                    self.finished = True

            self.screen.fill(0x0080ff)
            blit_text(self.screen, self.initial_full_text[:int(self.frames/2)], (150, 50), self.my_font, WHITE)
            self.frames += 1

            pygame.display.flip()

            self.clock.tick(60)

    def menu_screen(self):
        self.finished = False
        self.sprite_list.add(self.menu_bg, self.bed, self.fish)
        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.selecting_bed():
                    self.phase = 'sleep'
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self.selecting_fish():
                    self.phase = 'fish'
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())

            # --- Game logic should go here
            bed_center_x = self.bed.rect.x + 0.5 * self.bed.rect.width
            bed_center_y = self.bed.rect.y + 0.5 * self.bed.rect.height
            angle = find_rel_angle(bed_center_x, bed_center_y, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

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

            self.screen.blit(self.my_font.render("Which will you choose?", True, BLACK), (375, 110))
            self.screen.blit(self.small_font.render("Sleep for the day", True, BLACK), (294, 186))
            self.screen.blit(self.small_font.render("Go fishing", True, BLACK), (554, 187))
            self.screen.blit(self.small_font.render(f"Money: ${self.money}", True, BLACK), (825, 15))
            self.screen.blit(self.small_font.render(f"Day: {self.day}", True, BLACK), (825, 45))
            self.screen.blit(self.small_font.render(f"Days left: {10 - self.day}", True, BLACK), (825, 75))

            pygame.display.flip()

            self.clock.tick(60)

    def sleep(self):
        self.finished = False
        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.screen.fill(BLACK)
            for opacity in range(255):
                self.fade.set_alpha(opacity)
                self.screen.blit(self.huge_font.render("Goodnight!", False, WHITE), (375, 110))
                self.screen.blit(self.fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)
            self.phase = 'menu'
            self.day += 1
            self.finished = True

    def fishing_minigame(self):
        pygame.draw.ellipse(self.screen, BLACK, )

    def fish_game(self):
        for sprite in self.sprite_list:
            sprite.kill()
        self.sprite_list.add(self.player)
        self.finished = False
        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            for sprite in self.sprite_list:
                sprite.update()
            self.time_since_last_fish += self.clock.get_time()
            if self.time_since_last_fish > 1000:
                self.player.picture = 'Images/my character2.png'

            self.screen.fill(0x0080ff)

            for sprite in self.sprite_list:
                sprite.draw(self.screen)

            self.screen.blit(self.small_font.render(f"Money: ${self.money}", True, BLACK), (825, 15))
            self.screen.blit(self.small_font.render(f"Day: {self.day}", True, BLACK), (825, 45))
            self.screen.blit(self.small_font.render(f"Days left: {10 - self.day}", True, BLACK), (825, 75))
            self.screen.blit(self.small_font.render(f"Fish caught today: {self.player.fish_caught}", True, BLACK), (825, 105))

            pygame.display.flip()

            self.clock.tick(60)

    def do(self):

        while not self.done or self.day > 10:
            if self.phase == 'initial_screen':
                self.initial_screen()
            elif self.phase == 'menu':
                self.menu_screen()
            elif self.phase == 'sleep':
                self.sleep()
            elif self.phase == 'fish':
                self.fish_game()
            else:
                self.done = True

        for opacity in range(255):
            self.fade.set_alpha(opacity)
            self.screen.blit(self.huge_font.render("See you next time!", False, WHITE), (375, 110))
            self.screen.blit(self.fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)


pygame.init()

pygame.display.set_caption("Fishing Sim")

game = Game()

game.do()

# Close the window and quit.
pygame.quit()
