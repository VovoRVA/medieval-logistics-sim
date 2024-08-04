from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from action_manager import ActionsManager
from land import Castle, Town, Village
from main_force import MainForce
app = Ursina()

random.seed(0)
Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', collider='box', scale=256, texture='grass', texture_scale=(4,4))
editor_camera = EditorCamera(enabled=True, ignore_paused=True)
main_force = MainForce(camera=editor_camera)
# editor_camera.look_at_2d(main_force, axis='z')

# start_castle = Castle()
nearby_town = Town()
nearby_village = Village()
pause_handler = Entity(ignore_paused=True)
pause_text = Text('PAUSED', origin=(0,0), scale=2, enabled=False) # Make a Text saying "PAUSED" just to make it clear when it's paused.


def pause_handler_input(key):
    if key == 'escape':
        application.paused = not application.paused # Pause/unpause the game.
        pause_text.enabled = application.paused     # Also toggle "PAUSED" graphic.


pause_handler.input = pause_handler_input   # Assign the input function to the pause handler.


sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()
