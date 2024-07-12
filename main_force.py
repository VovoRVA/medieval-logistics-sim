from ursina import *

from ursina.prefabs.health_bar import HealthBar
from utils import CoreEntity


from land import Town
from support_unit import SupportUnit
STARTING_SETTINGS = {
    'SUPPORT_UNITS_AMOUNT': {'logistic': 1,
                             'scout': 0,
                             'war': 0}

}


class MainForce(CoreEntity):
    def __init__(self, camera, **kwargs):
        super().__init__(model='cube', z=-10, color=color.blue, origin_y=-.5, speed=1, collider='box', **kwargs)
        self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))
        self.camera = camera
        self.visibility = 30
        self.strength = 1000
        self.energy = 50
        self.supplies = 10
        self.water = 10
        self.max_energy = 100
        self.max_supplies = 100
        self.max_water = 50

        self.supplies_bar = HealthBar(max_value=self.max_supplies, value=self.supplies, color=color.yellow)

        self.action_map = {'order supply run': self.issue_logistic_order_to_support_unit,
                           'kill': self.issue_logistic_order_to_support_unit}
        self.origin_town = Town()
        self.main_units = []
        self.support_units = {'logistic': [],
                              'scout': [],
                              'war': []}
        self.get_allowed_actions(self.__class__)
        self.setup()

    def setup(self):
        for key, value in STARTING_SETTINGS['SUPPORT_UNITS_AMOUNT'].items():
            for i in range(value):
                self.support_units[key].append(SupportUnit(unit_type=key, master=self))

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

    def input(self, key):
        if key == 'left mouse' or held_keys['left mouse']:
            if not isinstance(mouse.hovered_entity, CoreEntity):
                pass
            else:
                target = mouse.hovered_entity
                master = self  # currently no support for dynamic master actions
                for action in target.subjective_action_set:
                    b = self.create_action_button(action.name)
                    print(action.name)
                    print(master.action_map[action.name])
                    b.on_click = Sequence(Wait(.5), Func(self.action_map[action.name], target))

    def update(self):
        self.supplies_bar.value = int(self.supplies)
