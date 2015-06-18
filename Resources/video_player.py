"""
Handles playing videos
"""

import pygame
from Base.generics import GenericController, GenericModel, GenericView


class GenericVideoPlayerController(GenericController):
    def __init__(self, event_manager, infrastructure):
        model = GenericVideoPlayerModel(event_manager, infrastructure)
        view = GenericVideoPlayerView(event_manager, infrastructure)
        GenericController.__init__(self, event_manager, infrastructure, model, view)
        self.skippable = False
        self.ticker = pygame.time.Clock()
        self.timer = 0

    def load_video(self, filename, skip=False):
        self.view.load_video(filename)

    def pause_extra(self):
        if self.view.video:
            self.view.video.pause()

    def resume(self):
        if self.view.video:
            self.view.resume()

    def run(self):
        self.load_video(self.model.queue)

class GenericVideoPlayerModel(GenericModel):
    def __init__(self, event_manager, infrastructure):
        GenericModel.__init__(self, event_manager, infrastructure)
        self.queue = None


class GenericVideoPlayerView(GenericView):
    def __init__(self, event_manager, infrastructure):
        GenericView.__init__(self, event_manager, infrastructure)
        self.weight = 0
        self.surface = pygame.Surface(self.infrastructure.view.resolution)
        self.replay = True
        self.video = None

    def resume(self):
        if not self.video.get_busy():
            self.video.play()

    def rem_from_render(self, weight):
        if self.video:
            GenericView.rem_from_render(self, self.weight)

    def load_bg_color(self, color):
        self.surface.fill(color)
        self.render = self.render_bg_color
        self.add_to_render(self.weight)

    def render_bg_color(self, time):
        self.infrastructure.view.screen.blit(self.surface, (0, 0))

    def load_video(self, filename):
        self.video = pygame.movie.Movie(filename)
        self.video.set_display(self.surface)
        self.render = self.render_video
        self.add_to_render(self.weight)
        self.video.play()

    def render_video(self, time):
        if not self.video.get_busy():
            if self.replay:
                self.video.rewind()
                self.video.play()
            else:
                pass
        self.infrastructure.view.screen.blit(self.surface, (0, 0))