from ursina import *


class Town(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1, 2),
                         x=random.uniform(-8,8),
                         z=random.uniform(-8,8) + 8,
                         collider='box',
                         scale_y=random.uniform(2,3),
                         color=color.hsv(0, 0, random.uniform(.9, 1)), **kwargs)
        self.supplies_production = 0.01
        self.supplies_type = 'food'
        self.supplies_storage_size = 300
        self.supplies = 20

    def update(self):
        if self.supplies <= self.supplies_storage_size:
            self.supplies += self.supplies_production
