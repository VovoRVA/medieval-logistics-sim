from ursina import *
from enum import Enum

from utils import CoreEntity


class Status(Enum):
    READY = 1
    ON_ROUTE = 2
    EXECUTING_MISSION = 3
    RETURNING_FROM_MISSION = 4


class UnitType(Enum):
    SCOUT = 1
    LOGISTIC = 2
    WAR = 3


class SupportUnit(CoreEntity):
    def __init__(self, unit_type, master_entity, **kwargs):
        types = {'scout': color.olive,
                 'logistic': color.light_gray,
                 'war': color.black}
        super().__init__(model='cube', scale_y=0.3,
                         color=types[unit_type], collider='box', **kwargs)
        self.master_entity = master_entity
        self.position = master_entity.position
        self.unit_type = unit_type
        self.supplies = 0
        self.max_supplies = 20
        self.target = None
        self.mission = None
        self.status = Status.READY


        self.behaviors = {
            'move_to_target': self.go_to_target,
            'execute_mission': self.execute_mission,
            'return_from_mission': self.return_back
        }
        self.get_allowed_actions(self.__class__)

    def move(self, speed=1):
        self.position += self.forward * time.dt * speed

    def go_to_target(self):
        dist_to_target = distance_xz(self.target.position, self.position)
        if dist_to_target <= 1:
            self.status = Status.EXECUTING_MISSION
        else:
            self.look_at_2d(self.target.position, 'y')
            self.move()

    def execute_mission(self):
        if self.mission == 'supply run' and self.supplies < self.max_supplies:
            self.target.supplies -= 0.01
            self.supplies += 0.01
        else:
            self.status = Status.RETURNING_FROM_MISSION

    def return_back(self):
        dist = distance_xz(self.master_entity.position, self.position)
        self.look_at_2d(self.master_entity.position, 'y')
        if dist < 2:
            self.master_entity.supplies += self.supplies
            self.target = self.mission = None
            self.status = Status.READY
        else:
            self.move()

    def execute_behavior(self, behavior, **kwargs):
        self.behaviors[behavior](**kwargs)

    def chose_action(self):
        if self.status == Status.READY and self.target and self.mission:
            self.parent = None
            self.status = Status.ON_ROUTE
            self.execute_behavior('move_to_target')
        if self.status == Status.ON_ROUTE:
            self.execute_behavior('move_to_target')
        if self.status == Status.EXECUTING_MISSION:
            self.execute_behavior('execute_mission')
        if self.status == Status.RETURNING_FROM_MISSION:
            self.execute_behavior('return_from_mission')

    def update(self):
        self.chose_action()
        if not self.master_entity:
            return
        dist = distance_xz(self.master_entity.position, self.position)
        if dist > self.master_entity.visibility:
            self.visible = False
            return
        else:
            self.visible = True
