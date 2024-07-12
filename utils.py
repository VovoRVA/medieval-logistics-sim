from ursina import *

from action_manager import ActionsManager


class CoreEntity(Entity):
    @property
    def master(self):
        return None

    @master.setter
    def master(self, value):
        self.master = value

    @property
    def option_set(self):
        return {}

    @option_set.setter
    def option_set(self, value):
        self.option_set = value

    @property
    def button_set(self):
        return {}

    @button_set.setter
    def button_set(self, value):
        self.option_set = value

    @property
    def allowed_actions(self):
        return ActionsManager().allowed_actions

    def get_allowed_actions(self, cls):
        self.objective_action_set = []
        self.subjective_action_set = []
        entity_name = cls.__name__
        for action in self.allowed_actions:
            if not action.action_type == 'order':
                pass
            elif action.master == entity_name or action.actor == entity_name:
                self.objective_action_set.append(action)
            elif entity_name in action.targets:
                self.subjective_action_set.append(action)
        print(self.objective_action_set)

    def create_action_button(self, button_text):
        b = Button(model='quad', scale=.05, x=-.5, color=color.olive, text=button_text, text_size=.5,
                   text_color=color.black)
        b.text_size = .5
        b.fit_to_text(radius=.1, padding=Vec2(Text.size * 1.5, Text.size))
        return b
