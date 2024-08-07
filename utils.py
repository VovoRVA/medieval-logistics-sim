from ursina import *
from enum import Enum

from action_manager import ActionsManager


class SupportStatus(Enum):
    READY = 1
    ON_ROUTE = 2
    EXECUTING_MISSION = 3
    RETURNING_FROM_MISSION = 4


class MainForceStatus(Enum):
    READY = 1
    PREPARING_FOR_MARCH = 2
    MARCHING = 3
    MARCHING_IN_FORCE = 4
    MASSING_FORCES = 5


class CoreEntity(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visibility = 30
        self.strength = 1000
        self.speed = 1

        self.energy = 50
        self.supplies = 50
        self.water = 50

        self.max_energy = 100
        self.max_supplies = 100
        self.max_water = 100

        self.supplies_production = 0

        self.objective_action_set = []
        self.subjective_action_set = []

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

    def move(self, target_position):
        self.look_at_2d(target_position, 'y')
        self.position += self.forward * time.dt * self.speed

    def get_allowed_actions(self, cls):
        entity_name = cls.__name__
        for action in self.allowed_actions:
            if not action.action_type == 'order':
                pass
            elif action.master == entity_name or action.actor == entity_name:
                self.objective_action_set.append(action)
            elif entity_name in action.targets:
                self.subjective_action_set.append(action)
        return self.objective_action_set

    def create_action_buttons(self, target):
        offset = 0
        buttons = []

        def destroy_buttons(buttons):
            for button in buttons:
                destroy(button)

        for action in target.subjective_action_set:
            print(action.name)
            b = Button(model='quad', scale=.05, x=-0.5, y=offset, color=color.olive, text=action.name, text_size=.5,
                       text_color=color.black)
            buttons.append(b)
            offset += 0.1
            b.fit_to_text(radius=.1, padding=Vec2(Text.size * 1.5, Text.size))
            b.on_click = Sequence(Wait(.5), Func(self.action_map[action.name], target),
                                  Func(destroy_buttons, buttons))



