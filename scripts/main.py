from direct.actor.Actor import Actor
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# TODO Implement a dialog system
# TODO Make a textbox appear for the npcs text with text options that you can click mouse has to be unlocked
# TODO Add a character model to interact with

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

random_cube = Entity(
    model="cube",
    position=(5,1,5),
    collider="box"
)

Sky()

interact_text = Text(
    text="E To Interact",
    origin=(0,-15),
)

interact_text.create_background()
#interactText.enabled = False

death_text = Text(
    text="You Died",
    origin=(0,0),
)

death_text.create_background()
death_text.enabled = False

respawn_button = Button(
    text="Respawn",
    scale=(.15,.07),
    origin=(0,1.5),
)

respawn_button.enabled = False

doing_walking_animation = False
is_jumping = False
is_interacting = False

def reset_cube_color():
    global is_interacting
    random_cube.color = color.white
    is_interacting = False

def player_die():
    death_text.enabled = True
    respawn_button.enabled = True
    player.enabled = False
    player.cursor.enabled = True

def player_respawn():
    death_text.enabled = False
    respawn_button.enabled = False
    player.enabled = True
    player.cursor.enabled = False
    player.position = Vec3(0, 0, 0)

respawn_button.on_click = player_respawn

def update():
    global doing_walking_animation
    global is_jumping
    global is_interacting

    is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

    if is_moving and not doing_walking_animation:
        actor.loop("Walk_Loop")
        doing_walking_animation = True

    elif not is_moving and doing_walking_animation:
        actor.loop("Idle_Loop")
        doing_walking_animation = False

    if held_keys['space']:
        is_jumping = True
        actor.stop()
        actor.play("Jump_Loop")

    if is_jumping and player.grounded:
        is_jumping = False
        actor.stop()
        actor.play("Idle_Loop")

    if distance(player.position, random_cube.position) < 2:
        interact_text.enabled = True
    else:
        interact_text.enabled = False

    if interact_text.enabled and held_keys['e'] and not is_interacting:
        is_interacting = True
        random_cube.color = color.red
        invoke(reset_cube_color, delay=.3)

    if player.position.y_getter() < -10:
        player_die()

app.run()
