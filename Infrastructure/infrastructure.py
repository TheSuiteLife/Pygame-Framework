"""
Abstraction layer to communicate with the infrastructure
"""

import pygame

from model import Model
from view import View
from Infrastructure.controller import InputController
from Resources.events import EventManager, TickEvent, QuitEvent


class Infrastructure():
    def __init__(self, resolution, frame_rate):
        self.frame_rate = frame_rate
        self.event_manager = EventManager()
        self.event_manager.register_listener(self)
        self.model = Model(self.event_manager)
        self.view = View(self.event_manager, resolution)
        self.controller = InputController(self.event_manager)
        self.main_loop = True

    def update_resolution(self, resolution):
        self.view.update_window(resolution)

    def update_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate

    def run_main(self):
        while self.main_loop:
            clock = pygame.time.Clock()
            milliseconds = clock.tick(self.frame_rate)
            self.event_manager.post(TickEvent(milliseconds))

    def get_event_manager(self):
        return self.event_manager

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.main_loop = False

