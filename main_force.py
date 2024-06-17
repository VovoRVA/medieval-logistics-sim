from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from town import Town
from support_unit import SupportUnit
STARTING_SETTINGS = {
    'SUPPORT_UNITS_AMOUNT': {'logistic': 1,
                             'scout': 0,
                             'war': 0}

}


class MainForce(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(model='cube', z=-10, color=color.blue, origin_y=-.5, speed=1, collider='box', **kwargs)
        self.collider = BoxCollider(self, Vec3(0, 1, 0), Vec3(1, 2, 1))
        self.visibility = 30
        self.strength = 1000
        self.supplies = 100
        self.origin_town = Town()
        self.main_units = []
        self.support_units = {'logistic': [],
                              'scout': [],
                              'war': []}
        self.setup()

    def setup(self):
        for key, value in STARTING_SETTINGS['SUPPORT_UNITS_AMOUNT'].items():
            for i in range(value):
                self.support_units[key].append(SupportUnit(unit_type=key, main_force=self))

    def manage_support_units(self):
        for unit in self.support_units['logistic']:
            if not unit.status.value == 1:
                pass
            else:
                self.issue_order_to_support_unit(support_unit=unit, target=self.origin_town, mission='supply run')

    @staticmethod
    def issue_order_to_support_unit(support_unit, target, mission):
        if not support_unit.status.value == 1:
            print('Support unit is already busy with an order')
            return
        support_unit.visible = support_unit.on_route = True
        support_unit.target_reached = support_unit.mission_complete = False
        support_unit.target = target
        support_unit.mission = mission
        support_unit.go_to_target()

    def update(self):
        super(MainForce, self).update()
        self.manage_support_units()

