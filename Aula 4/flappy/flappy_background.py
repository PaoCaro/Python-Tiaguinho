import sys
import pygame
from pygame.locals import *

WIDTH = 500
HEIGHT = 350
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
            # One slice
            area = pygame.Rect(self.offset, 0, self.surface_width, self.surface_height)
            self.surface.blit(self.bg_image, (0, 0), area)
        else:
            # Two slices
            first_width = self.bg_image_width - self.offset
            area = pygame.Rect(self.offset, 0, first_width, self.surface_height)
            self.surface.blit(self.bg_image, (0, 0), area)

            second_width = self.surface_width - first_width 
            area = pygame.Rect(0, 0, second_width, self.surface_height)
            self.surface.blit(self.bg_image, (first_width, 0), area)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg, _ = load_image("bin/background.png")
BG_manager = ScrollingBackground(screen, bg)
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()

    BG_manager.scroll(-3)
    BG_manager.update()
    pygame.display.update()
