"""
Abstract controller for the keyboard
"""
import pygame
from pygame.locals import QUIT, K_F4, KMOD_ALT

from Resources.events import TickEvent, QuitEvent


class MouseController():
    def __init__(self):
        self.left_down_actions = set()
        self.left_up_actions = set()
        self.middle_down_actions = set()
        self.middle_up_actions = set()
        self.right_down_actions = set()
        self.right_up_actions = set()
        self.scroll_up_actions = set()
        self.scroll_down_actions = set()
        self.mouse_move_actions = set()

class KeyboardController():
    def __init__(self):
        self.key_down = set()
        self.key_up = set()


class InputController():
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.quit_events = set()

    def add_key_down(self, pygame_key, action_func):
        self.keyboard.key_down.add((pygame_key, action_func))

    def rem_key_down(self, pygame_key, action_func):
        self.keyboard.key_down.remove((pygame_key, action_func))

    def add_key_up(self, pygame_key, action_func):
        self.keyboard.key_up.add((pygame_key, action_func))

    def rem_key_up(self, pygame_key, action_func):
        self.keyboard.key_up.remove((pygame_key, action_func))

    def add_mouse_move(self, func):
        self.mouse.mouse_move_actions.add(func)

    def rem_mouse_move(self, func):
        self.mouse.mouse_move_actions.remove(func)

    def add_ml_down(self, func):
        self.mouse.left_down_actions.add(func)

    def rem_ml_down(self, func):
        self.mouse.left_down_actions.remove(func)

    def add_mm_down(self, func):
        self.mouse.middle_down_actions.add(func)

    def rem_mm_down(self, func):
        self.mouse.middle_down_actions.remove(func)

    def add_mr_down(self, func):
        self.mouse.right_down_actions.add(func)

    def rem_mr_down(self, func):
        self.mouse.right_down_actions.remove(func)

    def add_ml_up(self, func):
        self.mouse.left_up_actions.add(func)

    def rem_ml_up(self, func):
        self.mouse.left_up_actions.remove(func)

    def add_mm_up(self, func):
        self.mouse.middle_up_actions.add(func)

    def rem_mm_up(self, func):
        self.mouse.middle_up_actions.remove(func)

    def add_mr_up(self, func):
        self.mouse.right_up_actions.add(func)

    def rem_mr_up(self, func):
        self.mouse.right_up_actions.remove(func)

    def add_scroll_up(self, func):
        self.mouse.scroll_up_actions.add(func)

    def rem_scroll_up(self, func):
        self.mouse.scroll_up_actions.remove(func)

    def add_scroll_down(self, func):
        self.mouse.scroll_down_actions.remove(func)

    def rem_scroll_down(self, func):
        self.mouse.scroll_down_actions.remove(func)

    def add_quit_event(self, func):
        self.quit_events.add(func)

    def rem_quit_event(self, func):
        self.quit_events.remove(func)

    def quit(self):
        for func in self.quit_events: func()
        self.event_manager.post(QuitEvent())

    def notify(self, event):
        if isinstance(event, TickEvent):
            ev = pygame.event.get()
            for event in ev:
                if event.type == QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        for func in self.mouse.left_down_actions.copy(): func(mouse_pos)
                    elif event.button == 2:
                        for func in self.mouse.middle_down_actions.copy(): func(mouse_pos)
                    elif event.button == 3:
                        for func in self.mouse.right_down_actions.copy(): func(mouse_pos)
                    elif event.button == 4:
                        for func in self.mouse.scroll_up_actions.copy(): func(mouse_pos)
                    elif event.button == 5:
                        for func in self.mouse.scroll_down_actions.copy(): func(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        for func in self.mouse.left_up_actions.copy(): func(mouse_pos)
                    elif event.button == 2:
                        for func in self.mouse.middle_up_actions.copy(): func(mouse_pos)
                    elif event.button == 3:
                        for func in self.mouse.right_up_actions.copy(): func(mouse_pos)
                    elif event.button == 4:
                        for func in self.mouse.scroll_up_actions.copy(): func(mouse_pos)
                    elif event.button == 5:
                        for func in self.mouse.scroll_down_actions.copy(): func(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for func in self.mouse.mouse_move_actions.copy(): func(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    key_press = event.key
                    for key in self.keyboard.key_down:
                        if key[0] == key_press:
                            key[1](key_press)
                            break
                    if event.key == K_F4 and bool(event.mod & KMOD_ALT):
                        self.quit()
                elif event.type == pygame.KEYUP:
                    key_press = event.key
                    for key in self.keyboard.key_up:
                        if key[0] == key_press:
                            key[1](key_press)
                            break
