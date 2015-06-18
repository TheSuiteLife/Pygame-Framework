"""
Useful functions
"""

import pygame
import math
import numpy

BLACK = (0, 0, 0)
MAX_ALPHA = 255

class EffectsRenderer():
    def __init__(self):
        self.rendering = True
        self.resolution = (1280, 720)
        self.weight = 20
        self.linger = 200
        self.rendering_functions = set()
        self.fade_amount = 0
        self.fade_completion = 0
        self.last_direction = ''
        self.finish_actions = set()

    def finish_clip_actions(self):
        for func in self.finish_actions:
            func()
        self.finish_actions.clear()

    def calc_new_completion(self, fade_amount, milliseconds, direction, type):
        completion = 0
        if type == 'linear':
            if direction == 'in':
                completion = 1 - self.fade_amount * 1.0 / MAX_ALPHA
            elif direction == 'out':
                completion = (self.fade_amount * 1.0 / MAX_ALPHA)

        elif type == 'exponential':
            if direction == 'in':
                completion = math.log(2 -(self.fade_amount / MAX_ALPHA * 1.0)) / math.log(2)
            elif direction == 'out':
                completion = math.log((self.fade_amount * 1.0 / MAX_ALPHA + 1)) / math.log(2)
        if completion > 0.85:
            completion = 1 - completion
        return completion * milliseconds

    def reverse_effect(self, milliseconds, direction, type, infrastructure):
        self.rem_effects(infrastructure)
        if self.fade_completion > 0:
            time = self.calc_new_completion((255 - self.fade_amount), milliseconds, direction, type)
        else:
            time = 0
        return time

    def force_fade_linear(self, infrastructure, milliseconds, direction):
        self.rendering = True
        surface = pygame.Surface(self.resolution)
        surface.fill(BLACK)
        timer = [self.reverse_effect(milliseconds, direction, 'linear', infrastructure)]
        screen = infrastructure.view.screen

        def fading_linear(time):
            if self.rendering and timer[0] < milliseconds + self.linger:
                timer[0] += time
                completion = (timer[0] * 1.0 / milliseconds)
                self.fade_completion = completion
                if direction == 'in':
                    self.last_direction = 'in'
                    fade = MAX_ALPHA - completion * MAX_ALPHA
                elif direction == 'out':
                    self.last_direction = 'out'
                    fade = completion * MAX_ALPHA
                else:
                    fade = 0
                self.fade_amount = fade
                surface.set_alpha(fade)
                screen.blit(surface, (0, 0))
            else:
                self.fade_completion = 0
                if fading_linear in self.rendering_functions:
                    self.rendering_functions.remove(fading_linear)
                    infrastructure.view.remove_from_render(fading_linear, self.weight)
        self.rendering_functions.add(fading_linear)
        infrastructure.view.add_to_render(fading_linear, self.weight)

    def force_fade_exponential(self, infrastructure, milliseconds, direction):
        self.rendering = True
        surface = pygame.Surface(self.resolution)
        surface.fill(BLACK)
        timer = [self.reverse_effect(milliseconds, direction, 'exponential', infrastructure)]
        screen = infrastructure.view.screen

        def fading_exp(time):
            if self.rendering and timer[0] < milliseconds + self.linger:
                timer[0] += time
                completion = (timer[0] * 1.0 / milliseconds)
                self.fade_completion = completion
                if direction == 'in':
                    self.last_direction = 'in'
                    fade = MAX_ALPHA - (math.exp(math.log(2) * completion) - 1) * MAX_ALPHA
                elif direction == 'out':
                    self.last_direction = 'out'
                    fade = (math.exp(math.log(2) * completion) - 1) * MAX_ALPHA
                else:
                    fade = 0
                self.fade_amount = fade
                surface.set_alpha(fade)
                screen.blit(surface, (0, 0))
            else:
                self.fade_completion = 0
                if fading_exp in self.rendering_functions:
                    self.rendering_functions.remove(fading_exp)
                    infrastructure.view.remove_from_render(fading_exp, self.weight)
        self.rendering_functions.add(fading_exp)
        infrastructure.view.add_to_render(fading_exp, self.weight)

    def stop_effects(self, infrastructure):
        self.rendering = False
        self.rem_effects(infrastructure)

    def rem_effects(self, infrastructure):
        for func in self.rendering_functions.copy():
            infrastructure.view.remove_from_render(func, self.weight)
            self.rendering_functions.remove(func)

    def render_effect(self, time):
        pass

effects_renderer = EffectsRenderer()