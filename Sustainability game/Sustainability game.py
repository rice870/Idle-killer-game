'''
Sustainability game.py by Isaac Rice
Version 5 14/9/2020

'''

import pygame
import math
import random

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
    # Finds the relative angle of one obect to another. It is not used in my code, but I was planning on using it.
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
    # From https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame/42015712
    # By user usr2564301. It blits text over multiple lines.
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
    # This is the Game Sprite class, a parent to all my sprite classes. This makes it much easier to make new sprites and such.
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
        # Gets the sprite ready to draw
        self.image = pygame.image.load(self.picture).convert()
        self.image = pygame.transform.rotozoom(self.image, 0, self.size_change)
        self.image.set_colorkey(self.colour_key)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        # Blits the sprite
        rotated_image = pygame.transform.rotate(self.image, self.rot_change)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)

        surface.blit(rotated_image, new_rect.topleft)

    def update(self):
        # Update is a general method that is run every frame.
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


class Fishes(GameSprites):
    # This class is for displaying the fish after you've caught them.
    def __init__(self):
        super().__init__()
        # These are the fish and they're respective values
        self.fish_list = {'European Pilchard': 1, 'European Perch': 2, 'Red Snapper': 3, 'Atlantic Salmon': 4, 'Rainbow Trout': 5, 'Spotted Bass': 6, 'Northern Pike': 7}

        # This chooses a random fish, so it's not the same fish over and over.
        self.fish_type = random.choice(list(self.fish_list.keys()))
        self.picture = f'Images/{self.fish_type}.png'
        self.x = 420
        self.y = 270
        self.size_change = 4
        self.change_costume()

    def update(self):
        super().__init__()
        # Every frame it chooses a new type of fish. It's excessive, but easier than making it more efficiently choose a new fish when you need a new fish.
        self.fish_type = random.choice(list(self.fish_list.keys()))


class Game:
    # This is the main class. It is the majority of the game.
    def __init__(self):
        # These are the fonts I use in my game. They're all the same font, just different sizes, as you cannot change their size after declaring them.
        self.my_font = pygame.font.SysFont('adobedevanagaribolditalic', 30)
        self.huge_font = pygame.font.SysFont('adobedevanagaribolditalic', 50)
        self.small_font = pygame.font.SysFont('adobedevanagaribolditalic', 20)

        # This is a list of the sprites so it's easier to remove them all, have them each do a specific task (for example update or draw)
        self.sprite_list = pygame.sprite.Group()

        # This defines the screen
        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)

        # Done is a bool saying whether the entire game is done or not.
        self.done = False
        self.clock = pygame.time.Clock()

        # All of these instances of the menu class are general buttons to help navigation of this game
        self.fish = Menu('Images/fish.png', 569, 215, WHITE, 0, 1)
        self.bed = Menu('Images/Bed.png', 303, 215, WHITE, 0, 1)
        self.menu_bg = Menu('Images/Design.png', 0, 0, WHITE, 0, 1)
        self.leave_fishing_button = Menu('Images/Leave.png', 852, 362, WHITE, 0, 1)
        self.player = Player()
        self.fishy = Fishes()

        # Fade is a surface used for tranitions, specifically sleeping and leaving the game.
        self.fade = pygame.Surface(self.size)
        self.fade.fill(BLACK)

        # The phase dictates what part of the game is happening, because many parts repeat.
        self.phase = 'initial_screen'

        # This is the trxt you're given at the start of the game as explanation.
        self.initial_full_text = 'In this game you need to make as much money as you can.\n' \
                                 'Each day you can catch up to five fish. Be careful though,\n' \
                                 'you don\'t want to kill too many fish, as there is a maximum\n' \
                                 'of only 20 in total. Everyday they reproduce by 25%. Each day\n' \
                                 'you have the choice of whether you fish or not and how \n' \
                                 'many fish you want to catch, as long as you don\'t catch \n' \
                                 'more than 5. When fishing, wait until your person notices there \n' \
                                 'is a fish (an exclamation mark will appear above his head) and \n' \
                                 'then soon after click to catch the fish (a bar will appear and \n' \
                                 'you need to click before it runs out!) See how much money you can make \n' \
                                 'before your 10 days run out, but make sure you don\'t ruin the \n' \
                                 'ecosystem! Best of luck! (Left click to continue)'

        # Frame counter used to make the writing not too fast or slow.
        self.frames = 0

        # self explanatory counters
        self.day = 1
        self.money = 0
        self.fish_count = 20
        self.time_since_last_fish = 0

        # Finished dictates whether a phase is done or not.
        self.finished = False

        # Did you catch a fish?
        self.caught = False

    def selecting_bed(self):
        # Is the mouse hovering over the bed selection in the menu?
        x_in_range = self.bed.rect.x < pygame.mouse.get_pos()[0] < self.bed.rect.x + self.bed.rect.width
        y_in_range = self.bed.rect.y < pygame.mouse.get_pos()[1] < self.bed.rect.y + self.bed.rect.height
        return x_in_range and y_in_range

    def selecting_fish(self):
        # Is the mouse hovering over the fishing selection in the menu?
        x_in_range = self.fish.rect.x < pygame.mouse.get_pos()[0] < self.fish.rect.x + self.fish.rect.width
        y_in_range = self.fish.rect.y < pygame.mouse.get_pos()[1] < self.fish.rect.y + self.fish.rect.height
        return x_in_range and y_in_range

    def initial_screen(self):
        # The initial screen is the initial info you receive when you open up the game.
        self.finished = False
        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # This allows you to skip it
                    self.phase = 'menu'
                    self.finished = True

            self.screen.fill(0x0080ff)
            blit_text(self.screen, self.initial_full_text[:int(self.frames / 2)], (150, 50), self.my_font, WHITE)
            self.frames += 1

            pygame.display.flip()

            self.clock.tick(60)

    def menu_screen(self):
        # This function is the main menu screen.
        for sprite in self.sprite_list:
            # This deletes all sprites.
            sprite.kill()

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

            # Here we just make sure all our costumes are updated for our sprites.
            for sprite in self.sprite_list:
                sprite.update()

            # These if/else statements make the selection pop out when you hover over them to so you know you're going to click it or not.
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

            # General stats about the player. I prefer rendering text with anti-aliasing.
            self.screen.blit(self.my_font.render("Which will you choose?", True, BLACK), (375, 110))
            self.screen.blit(self.small_font.render("Sleep for the day", True, BLACK), (294, 186))
            self.screen.blit(self.small_font.render("Go fishing", True, BLACK), (554, 187))
            self.screen.blit(self.small_font.render(f"Money: ${self.money}", True, BLACK), (825, 15))
            self.screen.blit(self.small_font.render(f"Fish: {self.fish_count}", True, BLACK), (825, 45))
            self.screen.blit(self.small_font.render(f"Day: {self.day}", True, BLACK), (825, 75))
            self.screen.blit(self.small_font.render(f"Days left: {10 - self.day}", True, BLACK), (825, 105))

            pygame.display.flip()

            self.clock.tick(60)

    def sleep(self, text):
        # This function is used after you catch five fish or choose to go to sleep. It fades you out, whih turned out well

        self.finished = False
        while not self.finished and not self.done:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            # Clear the screen
            self.screen.fill(BLACK)

            # Changes the opacity to add the fading effect.
            for opacity in range(255):
                self.fade.set_alpha(opacity)
                self.screen.blit(self.huge_font.render(text, True, WHITE), (375, 110))
                self.screen.blit(self.fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)

            self.finished = True
            self.new_day()

    def new_day(self):
        # Updates any necessary information for the new day.

        # The fish breed, but their limit is 20
        self.fish_count = int(self.fish_count * 1.25)
        if self.fish_count > 20:
            self.fish_count = 20

        self.day += 1

        self.phase = 'menu'

    def fishing_minigame(self):
        # This is the little bit you need to win to catch the fish. My event loop doesn't include quitting the game.
        self.caught = False
        self.time_since_last_fish = 0
        for time in range(100):
            self.screen.fill(0x0080ff)
            self.screen.blit(self.huge_font.render("Click before it gets the end to catch the fish!", True, BLACK), (100, 100))
            pygame.draw.line(self.screen, 0xC32929, [200, 175], [700, 175], 5)

            # This draws the circle progressively along the line as your time runs out.
            pygame.draw.ellipse(self.screen, 0xE98787, [195 + time * 5, 170, 10, 10])
            for event in pygame.event.get():
                # If you click within the 100 frames you catch the fish.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.caught = True

            # If you have caught the fish, end the game.
            if self.caught:
                break
            print(time)
            pygame.display.flip()
            self.clock.tick(60)

    def fish_catch(self):
        # This function displays the caught fish
        self.finished = False
        self.time_since_last_fish = 0
        self.screen.fill(0x0080ff)

        # The box the fish is shown in
        pygame.draw.rect(self.screen, 0x971311, [300, 150, 300, 300])
        pygame.draw.rect(self.screen, 0xC32929, [320, 170, 260, 260])

        # Info for the audience.
        self.screen.blit(self.my_font.render(f"You caught a {self.fishy.fish_type}! Click to continue", True, BLACK), (200, 100))
        self.screen.blit(self.my_font.render(f"Worth: ${self.fishy.fish_list[self.fishy.fish_type]}!", True, BLACK), (400, 200))

        # Updates necessary stats
        self.money += self.fishy.fish_list[self.fishy.fish_type]
        self.fish_count -= 1

        # Draws the fish
        self.fishy.draw(self.screen)

        pygame.display.flip()
        while not self.finished:
            # This bit here allows you to either skip through the viewing of your fish, or wait till the timer runs out and you need to go back to fishing or sleeping.
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.finished = True
                    self.time_since_last_fish = 0
            self.time_since_last_fish += self.clock.get_time()
            if self.time_since_last_fish > 5000:
                self.finished = True
                self.time_since_last_fish = 0
            self.clock.tick(60)

    def leave_fishing_method(self):
        # The leave or "go back button" method allows you to go back after saying you want to fish.
        self.finished = True
        self.phase = 'menu'

    def fish_game(self):
        # This is the fishing game, (the thing that appears after you select fishing).
        for sprite in self.sprite_list:
            sprite.kill()

        self.sprite_list.add(self.player, self.leave_fishing_button)
        self.finished = False

        while not self.finished and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif self.leave_fishing_button.rect.x <= pygame.mouse.get_pos()[0] <= self.size[0] and self.leave_fishing_button.rect.y <= pygame.mouse.get_pos()[1] <= self.size[1] and event.type == pygame.MOUSEBUTTONDOWN:
                    # If you click leave, then you leave.
                    self.leave_fishing_method()
            for sprite in self.sprite_list:
                sprite.update()

            self.time_since_last_fish += self.clock.get_time()

            if self.player.fish_caught > 4:
                # If they've caught too many fish today they're forced to sleep.
                self.finished = True
                self.phase = 'too much fish'

            self.screen.fill(0x0080ff)

            for sprite in self.sprite_list:
                sprite.draw(self.screen)

            if self.time_since_last_fish > 5000:
                # Switches from sleepy to shocked person after 5 seconds (there is a fish)
                self.player.picture = 'Images/my character2.png'

            if self.time_since_last_fish > 5500:
                # This start the minigame, updates information, then changes the character back to sleeping.
                self.time_since_last_fish = 0
                self.fishing_minigame()
                if self.caught:
                    self.player.fish_caught += 1
                    self.fish_catch()
                    print(self.time_since_last_fish)
                self.time_since_last_fish = 0
                self.player.picture = 'Images/my character1.png'

            # Displayings stats for the user.
            self.screen.blit(self.small_font.render(f"Money: ${self.money}", True, BLACK), (825, 15))
            self.screen.blit(self.small_font.render(f"Day: {self.day}", True, BLACK), (825, 45))
            self.screen.blit(self.small_font.render(f"Days left: {10 - self.day}", True, BLACK), (825, 75))
            self.screen.blit(self.small_font.render(f"Fish caught today: {self.player.fish_caught}", True, BLACK), (825, 105))
            self.screen.blit(self.small_font.render(f"Fish: {self.fish_count}", True, BLACK), (825, 135))

            pygame.display.flip()

            self.clock.tick(60)

    def do(self):
        # Main function with each phase

        while not self.day > 10 and not self.done:
            if self.phase == 'initial_screen':
                self.initial_screen()
            elif self.phase == 'menu':
                self.menu_screen()
            elif self.phase == 'sleep':
                self.sleep('Goodnight!')
            elif self.phase == 'too much fish':
                self.sleep('That\'s enough fish for today!')
            elif self.phase == 'fish':
                self.fish_game()
            else:
                # If you complete tha game, it gives you a goal to do it better next time.
                self.screen.fill(BLACK)
                self.screen.blit(self.huge_font.render(f"Score to beat: ${self.money}", True, WHITE), (350, 150))
                pygame.display.update()
                pygame.time.delay(10000)
                break


pygame.init()

pygame.display.set_caption("Fishing Sim")

game = Game()

while not game.done:
    # This makes the game repeat when done
    game = Game()
    game.do()

# Fades you out and says see you next time when you alt-f4 or click the exit button. Pretty cool effect in my opinion
for opacity in range(255):
    game.fade.set_alpha(opacity)
    game.screen.blit(game.huge_font.render("See you next time!", False, WHITE), (375, 110))
    game.screen.blit(game.fade, (0, 0))
    pygame.display.update()
    pygame.time.delay(10)

# Close the window and quit.
pygame.quit()
