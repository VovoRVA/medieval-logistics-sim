from ursina import *

from ursina.prefabs.health_bar import HealthBar
from utils import CoreEntity, MainForceStatus


from support_unit import SupportUnit
STARTING_SETTINGS = {
    'SUPPORT_UNITS_AMOUNT': {'logistic': 1,
                             'scout': 1,
                             'war': 1}

}


class MainForce(CoreEntity):
    def __init__(self, camera, **kwargs):
        super().__init__(model='cube', z=-10, color=color.blue, origin_y=-.5, speed=1, collider='box', **kwargs)
        self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))
        self.camera = camera

        self.supplies_bar = HealthBar(max_value=self.max_supplies, value=self.supplies, color=color.yellow)

        self.action_map = {'order supply run': self.issue_logistic_order_to_support_unit,
                           'order a raid': self.issue_logistic_order_to_support_unit,
                           'march': None}
        self.main_units = []
        self.support_units = {'logistic': [],
                              'scout': [],
                              'war': []}

        self.speed = 0.01
        self.target_position = None
        self.status = MainForceStatus.READY
        self.behaviors = {
            MainForceStatus.READY: self.idle,
            MainForceStatus.MARCHING: self.march
        }

        self.get_allowed_actions(self.__class__)
        self.setup()

    def idle(self):
        pass

    def prepare_for_march(self):
        pass

    def set_up_camp(self):
        pass

    def march(self):
        self.go_to_target()

    def go_to_target(self):
        dist_to_target = distance_xz(self.target_position, self.position)
        if dist_to_target <= 1:
            self.status = MainForceStatus.READY
        else:
            self.move(self.target_position)

    def setup(self):
        for key, value in STARTING_SETTINGS['SUPPORT_UNITS_AMOUNT'].items():
            for i in range(value):
                self.support_units[key].append(SupportUnit(unit_type=key, master_entity=self))

    def issue_logistic_order_to_support_unit(self, target):
        mission = 'supply run'
        support_unit = None
        for unit in self.support_units['logistic']:
            if unit.status.value == 1:
                support_unit = unit
                break
        if not support_unit:
            print('all units are busy')
            return
        support_unit.visible = support_unit.on_route = True
        support_unit.target_reached = support_unit.mission_complete = False
        support_unit.target = target
        support_unit.mission = mission
        support_unit.go_to_target()

    def issue_attack_order_to_support_unit(self, target):
        mission = 'raid'
        support_unit = None
        for unit in self.support_units['logistic']:
            if unit.status.value == 1:
                support_unit = unit
                break
        if not support_unit:
            print('all units are busy')
            return
        support_unit.visible = support_unit.on_route = True
        support_unit.target_reached = support_unit.mission_complete = False
        support_unit.target = target
        support_unit.mission = mission
        support_unit.go_to_target()

    def chose_action(self):
        self.behaviors[self.status]()

    def input(self, key):
        if key == 'left mouse' or held_keys['left mouse']:
            target = mouse.hovered_entity
            if not isinstance(target, CoreEntity):
                self.target_position = Vec3(mouse.world_point[0], mouse.world_point[1], mouse.world_point[2])
                self.status = MainForceStatus.MARCHING
            else:
                target = mouse.hovered_entity
                self.create_action_buttons(target)

    def update(self):
        self.supplies_bar.value = int(self.supplies)
        self.chose_action()

