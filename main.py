from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader
town = Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1, 2),
              x=random.uniform(-8,8),
              z=random.uniform(-8,8) + 8,
              collider='box',
              scale_y=random.uniform(2,3),
              color=color.hsv(0, 0, random.uniform(.9, 1))
              )


class Party(Entity):
    def __init__(self, unit_type, target, mission, **kwargs):
        type_colors = {'scout': color.olive,
                       'logistic': color.light_gray,
                       'war': color.black}
        super().__init__(model='cube', scale_y=0.3,
                         color=type_colors[unit_type], collider='box', **kwargs)
        self.position = player_army.position
        self.unit_type = unit_type
        self.target = target
        self.mission = mission
        self.target_reached = False
        self.mission_complete = False
        self.returned = False

    def update(self):
        dist = distance_xz(player_army.position, self.position)
        dist_to_target = distance_xz(self.target, self.position)
        # if dist > 15:
        #     self.visible = False
        #     return
        # else:
        #     self.visible = True
        if dist_to_target <= 1:
            self.target_reached = True
            self.mission_complete = True

        if self.target_reached and self.mission_complete:
            self.look_at_2d(player_army.position, 'y')
        else:
            self.look_at_2d(self.target, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        self.position += self.forward * time.dt * 2
        if self.target_reached and dist < 1:
            self.enabled = False


ground = Entity(model='plane', collider='box', scale=256, texture='grass', texture_scale=(4,4))

editor_camera = EditorCamera(enabled=True, ignore_paused=True)
player_army = FirstPersonController(model='cube', z=-10, color=color.blue, origin_y=-.5, speed=8, collider='box')
player_army.collider = BoxCollider(player_army, Vec3(0, 1, 0), Vec3(1, 2, 1))
player_army.strength = 1000
player_army.supplies = 1000
starting_party_count = {'scout': 1,
                        'war': 1,
                        'logistic': 1}
player_army.party_set = {'scout': [],
                         'war': [],
                         'logistic': []}
print(starting_party_count)
for key, value in starting_party_count.items():

    for i in range(value):
        player_army.party_set[key].append(Party(key, town.position, 1))

t = Text(str(len(player_army.party_set['logistic'])), color=color.light_gray)
e = Text(str(len(player_army.party_set['war'])), color=color.black)

def spawn_party(unit_type, target, mission):
    if True or len(player_army.party_set[unit_type]) >= 1:
        pass


def update():
    if held_keys['1']:
        spawn_party('logistic', town.position, 1)
    if held_keys['2']:
        spawn_party('scout', town.position, 1)
    if held_keys['3']:
        spawn_party('war', town.position, 1)


sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()