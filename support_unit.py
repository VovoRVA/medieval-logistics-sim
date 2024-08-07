from ursina import *
from enum import Enum

from utils import CoreEntity, SupportStatus


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
        self.status = SupportStatus.READY

        self.behaviors = {
            SupportStatus.READY: self.idle,
            SupportStatus.ON_ROUTE: self.go_to_target,
            SupportStatus.EXECUTING_MISSION: self.execute_mission,
            SupportStatus.RETURNING_FROM_MISSION: self.return_back
        }
        self.get_allowed_actions(self.__class__)

    def idle(self):
        pass

    def go_to_target(self):
        dist_to_target = distance_xz(self.target.position, self.position)
        if dist_to_target <= 1:
            self.status = SupportStatus.EXECUTING_MISSION
        else:
            self.move(self.target.position)

    def execute_mission(self):
        if self.mission == 'supply run' and self.supplies < self.max_supplies:
            self.target.supplies -= 0.01
            self.supplies += 0.01
        else:
            self.status = SupportStatus.RETURNING_FROM_MISSION

    def return_back(self):
        dist = distance_xz(self.master_entity.position, self.position)
        if dist < 2:
            self.master_entity.supplies += self.supplies
            self.target = self.mission = None
            self.status = SupportStatus.READY
        else:
            self.move(self.master_entity.position)

    def execute_behavior(self):
        self.behaviors[self.status]()

    def chose_action(self):
        if self.status == SupportStatus.READY and self.target and self.mission:
            self.parent = None
            self.status = SupportStatus.ON_ROUTE
        self.execute_behavior()

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
