"""
Abstraction layer to communicate with the MVC infrastructure
"""

import pygame
from Resources.events import TickEvent
from Resources.render_effects import effects_renderer


class GenericModel():
    def __init__(self, event_manager, infrastructure):
        self.event_manager = event_manager
        self.infrastructure = infrastructure

    def subscribe_to_events(self):
        self.event_manager.register_listener(self)

    def unsubscribe_to_events(self):
        self.event_manager.unregister_listener(self)

    def remove(self):
        self.unsubscribe_to_events()
        del self

    def notify(self, event):
        if isinstance(event, TickEvent):
            # Do model event handling here
            pass


class GenericView():
    def __init__(self, event_manager, infrastructure):
        self.event_manager = event_manager
        self.infrastructure = infrastructure
        self.drawings = {}
        self.weight = 10

    def add_to_render(self, weight):
        self.infrastructure.view.add_to_render(self.render, weight)

    def rem_from_render(self, weight):
        self.infrastructure.view.remove_from_render(self.render, weight)

    def render(self, time):
        pass

    def remove(self):
        if [self.render, self.weight] in self.infrastructure.view.render_list:
            self.rem_from_render(self.weight)
        del self


class GenericController():
    def __init__(self, event_manager, infrastructure, model=None, view=None):
        self.event_manager = event_manager
        self.infrastructure = infrastructure
        self.effects_renderer = effects_renderer
        self.fade_time = 800
        if model:
            self.model = model
        else:
            self.model = GenericModel(event_manager, infrastructure)
        if view:
            self.view = view
        else:
            self.view = GenericView(event_manager, infrastructure)


    def run(self):
        self.model.subscribe_to_events()
        self.view.add_to_render(self.view.weight)
        self.run_extra()
        pass

    def pause(self):
        self.model.unsubscribe_to_events()
        self.view.rem_from_render(self.view.weight)
        self.pause_extra()

    def run_extra(self):
        pass

    def pause_extra(self):
        pass

    def remove(self):
        self.model.remove()
        self.view.remove()
        del self


class MouseClickActionPoster():
    """
    Click on something and an event happens
    """

    def __init__(self, mouse_button, infrastructure, rect=None):
        self.infrastructure = infrastructure
        self.mouse_button = mouse_button

        self.state = 0
        if rect:
            self.rect = rect

    def listen(self):
        if self.mouse_button == 'left':
            self.infrastructure.controller.add_ml_down(self.mouse_down_state)
            self.infrastructure.controller.add_ml_up(self.mouse_up_state)
        elif self.mouse_button == 'middle':
            self.infrastructure.controller.add_mm_down(self.mouse_down_state)
            self.infrastructure.controller.add_mm_up(self.mouse_up_state)
        elif self.mouse_button == 'right':
            self.infrastructure.controller.add_mr_down(self.mouse_down_state)
            self.infrastructure.controller.add_mr_up(self.mouse_up_state)
        else:
            raise ValueError('Parameter mouse_button does not equal \'left\', \'middle\', or \'right\'')

    def stop_listen(self):
        if self.mouse_button == 'left':
            self.infrastructure.controller.rem_ml_down(self.mouse_down_state)
            self.infrastructure.controller.rem_ml_up(self.mouse_up_state)
        elif self.mouse_button == 'middle':
            self.infrastructure.controller.rem_mm_down(self.mouse_down_state)
            self.infrastructure.controller.rem_mm_up(self.mouse_up_state)
        elif self.mouse_button == 'right':
            self.infrastructure.controller.rem_mr_down(self.mouse_down_state)
            self.infrastructure.controller.rem_mr_up(self.mouse_up_state)
        else:
            raise ValueError('Parameter mouse_button does not equal \'left\', \'middle\', or \'right\'')


    def mouse_down_state(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.down_action()
            self.state = 1

    def mouse_up_state(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.state == 1:
            self.post_action()
            self.up_action()
        else:
            self.up_action()
        self.state = 0

    def down_action(self):
        pass

    def up_action(self):
        pass

    def post_action(self):
        pass


class KeyPressActionPoster():
    def __init__(self, pygame_key, infrastructure):
        self.input_controller = infrastructure
        infrastructure.controller.add_key_down(pygame_key, self.key_down_state)
        infrastructure.controller.add_key_up(pygame_key, self.key_up_state)
        self.state = 0

    def key_down_state(self):
        self.down_action()
        self.state = 1

    def key_up_state(self):
        self.up_action()
        self.state = 0

    def down_action(self):
        pass

    def up_action(self):
        pass


class GenericImage():
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.rect = 0
        self.update_rect()

    def update_rect(self):
        width, height = self.image.get_rect().size
        left = self.position[0] - width / 2
        top = self.position[1] - height / 2
        self.rect = pygame.Rect(left, top, width, height)


class GenericSprite(pygame.sprite.Sprite, GenericImage):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        GenericImage.__init__(self, image, position)
        self.speed = 0

    def update(self, time):
        multiplier = time / 1000.0
        self.move(multiplier)
        self.update_rect()

    def move(self, multiplier):
        pass

    def remove(self):
        self.kill()
        del self


class GenericButton(MouseClickActionPoster, GenericSprite):
    def __init__(self, mouse_button, infrastructure, image, position):
        MouseClickActionPoster.__init__(self, mouse_button, infrastructure)
        GenericSprite.__init__(self, image, position)


class GenericTextDrawButton(MouseClickActionPoster):
    def __init__(self, mouse_button, infrastructure, rect, position, edge_color, fill_color, thickness):
        MouseClickActionPoster.__init__(self, mouse_button, infrastructure, rect)
        self.edge_color = edge_color
        self.fill_color = fill_color
        self.position = position
        self.thickness = thickness
        self.font = None
        self.text = None
        self.text_color = None
        self.surface = pygame.Surface((rect.width, rect.height))
        self.draw()

    def add_text(self, text, text_color, font, font_size):
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(font, font_size)
        self.font_size = font_size
        self.draw()

    def draw(self):
        self.surface.fill(self.fill_color)
        pygame.draw.rect(self.surface, self.edge_color, self.surface.get_rect(), self.thickness)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            self.surface.blit(text_surface, self.new_rect(self.surface.get_rect().center, text_surface))

    def new_rect(self, position, surface):
        width, height = surface.get_rect().size
        left = position[0] - width / 2
        top = position[1] - height / 2
        rect = pygame.Rect(left, top, width, height)
        return rect

    def center(self, surface):
        new_pos = surface.get_rect()


    def render(self):
        self.infrastructure.view.screen.blit(self.surface, self.new_rect(self.position, self.surface))

