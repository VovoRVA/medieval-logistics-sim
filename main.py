from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

from main_force import MainForce
app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', collider='box', scale=256, texture='grass', texture_scale=(4,4))
editor_camera = EditorCamera(enabled=True, ignore_paused=True)
main_force = MainForce()

# editor_camera.look_at_2d(main_force, axis='z')

sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()
