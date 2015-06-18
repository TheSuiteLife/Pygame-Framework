"""
Processes the view on the screen
"""

from bisect import insort

import pygame
from Resources.events import TickEvent


class View():
    def __init__(self, event_manager, resolution):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.render_list = []
        self.resolution = []
        pygame.init()
        self.update_window(resolution)
        self.screen = pygame.display.get_surface()

    def add_to_render(self, func, weight):
        """
        Adds a function to the render list
        :param func: must be capable of drawings onto the main screen
        :param weight: the order of the drawing, lower has more priority and goes first
        :return: None
        """
        insort(self.render_list, [weight, func])

    def remove_from_render(self, func, weight):
        if [weight, func] in self.render_list:
            self.render_list.remove([weight, func])
        else:
            print "Warning: render function not found in the render list"

    def print_functions(self):
        for weight, func in self.render_list:
            print weight, func

    def render(self):
        for weight, func in self.render_list:
            func()

    def update_window(self, resolution):
        pygame.display.set_mode(resolution)
        self.resolution = resolution

    def notify(self, event):
        if isinstance(event, TickEvent):
            for view in self.render_list:
                view[1](event.time)
            pygame.display.flip()