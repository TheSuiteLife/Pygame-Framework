import pygame, os
import ConfigParser


def get_resolution():
    return (1280, 720)


def load_image(image_name):
    # Loads an image and returns the pygame image
    pathname = os.path.join('resources', "Images", image_name)
    try:
        image = pygame.image.load(pathname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        raise
    return image


def sprite_resize(sprite, percent_size):
    new_width = get_resolution[0] * percent_size[0]
    new_height = get_resolution[1] * percent_size[1]
    sprite.image = pygame.transform.scale(sprite.image, (new_width, new_height))
    sprite.get_rect()


def image_resize(image, size):
    image = pygame.transform.scale(image, size)
    return image


def get_setting(path_to_config, header, option):
    """
    Finds the folder location of a specific resource given the config file
    """
    Config = ConfigParser.ConfigParser()
    Config.read(path_to_config)
    return Config.get(header, option)
