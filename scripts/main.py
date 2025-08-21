from direct.actor.Actor import Actor
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.title = "Walking Simulator"
window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

ground = Entity(model="plane", collider="box", scale=64, color=color.blue)

player = FirstPersonController(
    speed=8,
    position=(0, 0, 0),
    scale=1,
)
player.camera_pivot.x = 0
player.camera_pivot.z = -2
player.camera_pivot.y = 3

player.cursor.enabled = False

actor = Actor("../assets/Player.glb")
actor.reparent_to(player)
actor.setScale(1)
actor.setColor(color.peach)
actor.setHpr(180, 0, 0)

RandomCube = Entity(
    model="cube",
    position=(5,1,5),
    collider="box"
)

Sky()

interactText = Text(
    text="E To Interact",
    origin=(0,-15),
)

interactText.create_background()
#interactText.enabled = False


doingWalkingAnimation = False
isJumping = False

def reset_cube_color():
    RandomCube.color = color.white

def update():
    global doingWalkingAnimation
    global isJumping

    is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

    if is_moving and not doingWalkingAnimation:
        actor.loop("Walk_Loop")
        doingWalkingAnimation = True

    elif not is_moving and doingWalkingAnimation:
        actor.loop("Idle_Loop")
        doingWalkingAnimation = False

    if held_keys['space']:
        isJumping = True
        actor.stop()
        actor.play("Jump_Loop")

    if isJumping and player.grounded:
        isJumping = False
        actor.stop()
        actor.play("Idle_Loop")

    if distance(player.position, RandomCube.position) < 2:
        interactText.enabled = True
    else:
        interactText.enabled = False

    if interactText.enabled and held_keys['e']:
        RandomCube.color = color.red
        invoke(reset_cube_color, delay=2)

app.run()
