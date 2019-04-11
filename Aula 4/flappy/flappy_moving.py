import sys
import pygame
from pygame.locals import *
from random import randint
### COMO CRIAR UM ATRIBUTO
## self.QUALQUERCOISA

WIDTH = 500
HEIGHT = 350
TUBE_WIDTH = 80                 # width of the tube
TUBE_INTERVAL = 160               # spacing between each consecutive tube
TUBE_GAP = 80                   # height of the hole in the tube
TUBE_COLOUR = (34, 130, 127)    # colour of the tube
TUBE_BORDER_COLOUR = (44, 170, 160)  # colour of the border of the tube
FPS = 60


def load_image(name, transparent=False):
    """Function that handles image loading
    Returns the image and its Rect"""
    try:
        img = pygame.image.load(name)
    except pygame.error:
        raise SystemExit("Could not load image " + name)
    if not transparent:
        img = img.convert()
    img = img.convert_alpha()
    img_rect = img.get_rect()

    return img, img_rect


class ScrollingBackground(object):
    def __init__(self, surface, bg_image):
        self.surface = surface
        self.surface_width = self.surface.get_width()
        self.surface_height = self.surface.get_height()
        self.bg_image = bg_image
        self.bg_image_width = self.bg_image.get_width()
        self.offset = 0

    def scroll(self, px):
        """Scrolls px pixels forward; if px < 0, scrolls back"""
        self.offset += px
        self.offset %= self.bg_image_width

    def update(self):
        """Updates the scrolling background on the surface"""
        if self.offset + self.surface_width <= self.bg_image_width:
            # we can take one whole slice
            area = pygame.Rect(self.offset, 0,
                               self.surface_width, self.surface_height)
            self.surface.blit(self.bg_image, (0, 0), area)
        else:
            # we must take two slices
            fst_width = self.bg_image_width - self.offset
            area = pygame.Rect(self.offset, 0,
                               fst_width, self.surface_height)
            self.surface.blit(self.bg_image, (0, 0), area)
            area = pygame.Rect(0, 0,
                               self.surface_width - fst_width, self.surface_height)
            self.surface.blit(self.bg_image, (fst_width, 0), area)


class Duck(object):
    def __init__(self, surface, img, pos):
        self.surface = surface
        self.img = img
        self.pos = pygame.Rect(pos[0], pos[1],
                               #função
                               img.get_width(),
                               img.get_height())
        """CONSTRUIR O RETANGULO DE COLISAO"""
        self.collision_rect = pygame.Rect(
            self.pos.x, self.pos.y,
            img.get_width() * 0.8, img.get_height() * 0.8)
        self.a = 2
        self.v0 = -10
        self.x0 = pos[1]
        self.t = 0

    def update(self):
        x, y = self.pos.topleft
        p = [x, round(y)]
        self.surface.blit(self.img, p)

    def update_position(self):
        # every time we update the position, t increases 0.2
        self.t += 0.2
        """ATUALIZAR A POSICAO DO TOPO"""
        self.pos.top = 0.5 * self.a * self.t ** 2 + self.v0 * self.t + self.x0
        self.collision_rect.center = self.pos.center

    def press_bar(self):
        """REINICIAR A EQUACAO DA POSICAO"""
        self.t = 0
        self.x0 = self.pos.top


def draw_tube(surf, tube):
    top = tube[0]
    bot = tube[1]
    pygame.draw.rect(surf, TUBE_COLOUR, top)
    pygame.draw.rect(surf, TUBE_BORDER_COLOUR, top, 3)
    pygame.draw.rect(surf, TUBE_COLOUR, bot)
    pygame.draw.rect(surf, TUBE_BORDER_COLOUR, bot, 3)


screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg, _ = load_image("bin/background.png")
duck, _ = load_image("bin/duck2.png", True)
# scale the duck so its height is half the height of the gap
# find the scaling ratio
prop = TUBE_GAP//2 / duck.get_height()
duck = pygame.transform.scale(duck,
                              (round(prop*duck.get_width()), TUBE_GAP//2))

BG_manager = ScrollingBackground(screen, bg)
duck = Duck(screen, duck, [WIDTH//3, HEIGHT//2])
horizontal_speed = 2
tube_countdown = TUBE_INTERVAL
tubes = []
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        # VERIFICAR SE SE CARREGOU NO ESPACO
        elif ev.type == KEYDOWN:
            if ev.key == K_UP:
                duck.press_bar()

    BG_manager.scroll(horizontal_speed)
    BG_manager.update()

    tube_countdown -= horizontal_speed
    if tube_countdown <= 0:
        # create a new tube in the end of the screen
        # a tube is composed of two halfs, the top one and the bottom one
        # the two halfs are separated by TUBE_GAP pixels
        top_gap = randint(TUBE_GAP, HEIGHT-TUBE_GAP)    # bottom of top tube
        bot_gap = top_gap + TUBE_GAP                    # top of bottom tube
        top_half = pygame.Rect(WIDTH, 0, TUBE_WIDTH, top_gap)
        bot_half = pygame.Rect(WIDTH, bot_gap, TUBE_WIDTH, HEIGHT-bot_gap)
        tubes.append((top_half, bot_half))
        tube_countdown = TUBE_WIDTH + TUBE_INTERVAL
    i = 0
    while i < len(tubes):
        tubes[i][0].left -= horizontal_speed
        tubes[i][1].left -= horizontal_speed
        if tubes[i][0].right <= 0:
            tubes.pop(i)
        else:
            draw_tube(screen, tubes[i])
            """VERIFICAR SE O PATO CHOCA"""
            first_collision = duck.pos.collidelist(tubes[i])
            if first_collision > -1:
                pygame.quit()
                sys.exit()
            i += 1

    duck.update_position()
    duck.update()

    pygame.display.update()
