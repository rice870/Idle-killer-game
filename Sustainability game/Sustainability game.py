'''
To do list

Make Initial classes STARTEd 25/08/2020

'''


import pygame

# Define some colors
BLACK =     (  0,   0,   0)
WHITE =     (255, 255, 255)
RED =       (255,   0,   0)
GREEN =     (  0, 255,   0)
BLUE =      (  0,   0, 255)
YELLOW =    (255, 255,   0)
CYAN =      (  0,  55, 255)
MAGENTA =   (255,   0, 255)
SILVER =    (192, 192, 192)


def blit_rotate(surf, image, pos, originPos, angle):
    # from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame#:~
    # :text=Surface%20)%20can%20be%20rotated%20by,rotate%20.&text=This%20is%20cause%2C%20because%20the,by%20mult
    # iples%20of%2090%20degrees). By https://stackoverflow.com/users/5577765/rabbid76
    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)


def change_costume(object, picture, x, y, colourkey):
    object.image = pygame.image.load(picture).convert()
    object.image.set_colorkey(colourkey)
    object.rect = object.image.get_rect()
    object.rect.x = x
    object.rect.y = y


class Game:
    def __init__(self):
        self.sprite_list = pygame.sprite.Group()
        self.size = (1000, 500)
        self.screen = pygame.display.set_mode(self.size)
        self.done = False
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

    def do(self):
        menu_bg = Menu('Design.png')
        self.sprite_list.add(menu_bg)

        while not self.done:
            # --- Main event loop
            self.check_events()

            # --- Game logic should go here

            # --- Screen-clearing code goes here

            # If you want a background image, replace this clear with blit'ing the background image.
            self.screen.fill(0x0080ff)

            # --- Drawing code should go here
            self.sprite_list.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        for sprite in self.sprite_list:
            sprite.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        change_costume(self, 'Design.png', 10, 10, WHITE)


class Menu(pygame.sprite.Sprite):
    def __init__(self, picture):
        super().__init__()

        change_costume(self, picture, 0, 0, WHITE)


pygame.init()

pygame.display.set_caption("My Game")

game = Game()

game.do()

# Close the window and quit.
pygame.quit()
