"""
Basic ui elements with their functionality

Note that image means the elements function by having an image passed to them
"""

import pygame
from numpy import array

from Macros.functions import image_resize
from Base.generics import MouseClickActionPoster
from generics import MouseClickActionPoster



class Button(MouseClickActionPoster):
    """
    Button object
    """
    def __init__(self, mouse_button, input_controller, image, position):
        MouseClickActionPoster.__init__(self, mouse_button, input_controller)
        self.image = image
        self.rect = image.get_rect()


class Container():
    """
    Object that will house other ui elements relatively in it
    """

    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.contained_objects = set()

    def move_position(self, position):
        dx = self.position[0] - position[0]
        dy = self.position[1] - position[1]
        self.position = position
        for object in self.contained_objects:
            object.position = [position[0] + dx, position[1] + dy]

    def resize(self, multiplier):
        # This function will need work
        self.size *= multiplier
        for object in self.contained_objects:
            object.resize(multiplier)

    def add(self, object, position):
        """
        Position is based off of top left of container
        """
        self.contained_objects.add(object)
        object_x = self.position[0] - (self.size[0] / 2) + position[0]
        object_y = self.position[1] - (self.size[1] / 2) + position[1]
        object.position = [object_x, object_y]

    def remove(self, object):
        self.contained_objects.remove(object)


class ImageButton(pygame.sprite.Sprite, MouseClickActionPoster):
    """
    You need the position and an image for this
    """

    def __init__(self, event_manager, position, image, mouse_button, input_controller):
        pygame.sprite.Sprite.__init__(self)
        MouseClickActionPoster.__init__(self, mouse_button, input_controller)
        self.event_manager = event_manager
        self.position = position
        self.image = image
        self.image_copy = image
        self.image_array = array(pygame.surfarray.pixels3d(image))
        self.rect = self.get_rect()

    def get_rect(self):
        size = self.image.get_rect().size
        left = self.position[0] - size[0] / 2
        top = self.position[1] - size[1] / 2
        return pygame.Rect(left, top, size[0], size[1])

    def resize(self, multiplier):
        size = self.image.get_rect().size
        new_size = [dimension * multiplier for dimension in size]
        self.image = image_resize(self.image, new_size)
        self.get_rect()

    def down_action(self):
        """
        Some sort of action should result that will trigger something in the model
        """
        pass

    def on_hover(self):
        """
        Perform something while the mouse is over this
        """
        pass

    def off_hover(self):
        """
        Perform something while the mouse isn't over this
        """
        pass

    def remove(self):
        self.kill()
        del self


class Menu():
    pass