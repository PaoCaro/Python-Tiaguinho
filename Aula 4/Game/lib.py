import pygame

def load_png(name):
    """ Load image and return image object"""
    try:
        img = pygame.image.load(name)
    except:
        raise SystemExit('Cannot load image: %s' % name)

    if img.get_alpha() is None:
        img = img.convert() 
    else:
        img = img.convert_alpha()

    return img, img.get_rect()
