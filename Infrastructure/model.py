"""
Main frame of the game that will control states

Note that the controllers must have a pause and a run function
"""

from Resources.events import QuitEvent


def remove_from_dict(dict, value_to_remove):
    dict = {key: value for key, value in dict.items() if value is not value_to_remove}
    return dict


class Model():
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.controllers = {}
        self.perm_controllers = {}
        self.current = None

    def add_controller(self, name, controller):
        self.controllers[name] = controller

    def remove_controller(self, name, controller):
        self.controllers.pop(name, None)

    def add_perm_controller(self, name, controller):
        self.perm_controllers[name] = controller

    def remove_perm_controller(self, name, controller):
        self.controllers.pop(name, None)

    def pause_all(self):
        self.pause_current_controller()
        for controller in self.perm_controllers.keys(): self.pause_perm_controller(controller)

    def pause_current_controller(self):
        self.current.pause()
        self.current = None

    def pause_perm_controller(self, name):
        self.perm_controllers[name].pause()

    def load(self, name, controller=None, delete_current=False):
        if controller and controller not in self.controllers.values():
            self.add_controller(name, controller)
        if controller:
            controller.run()
        elif name in self.controllers:
            self.controllers[name].run()
        else:
            raise NoSuchControllerException("The controller does not exist in the model: " + name)
        if self.current:
            if delete_current:
                self.controllers = remove_from_dict(self.controllers, self.current)
                self.current.remove()
            else:
                self.current.pause()
        self.current = self.controllers[name]

    def load_perm(self, name, controller=None):
        if controller and controller not in self.perm_controllers.values():
            self.add_perm_controller(name, controller)
        elif name in self.perm_controllers:
            self.perm_controllers[name].run()
        else:
            raise NoSuchControllerException("The controller does not exist in the model: " + name)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            for controller_name in self.controllers.copy():
                self.controllers.pop(controller_name).remove()
            for controller_name in self.perm_controllers.copy():
                self.perm_controllers.pop(controller_name).remove()


class NoSuchControllerException(Exception):
    pass