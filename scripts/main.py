from direct.actor.Actor import Actor
from ursina import *
from ursina.prefabs.conversation import Conversation
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

# TODO Add a character model to interact with

app = Ursina()

window.title = "Walking Simulator"
window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

ground = Entity(
    model="plane",
    collider="box",
    scale=64,
    #color=color.blue,
    texture="../assets/textures/Grass.png",
    texture_scale=(16,16))

player = FirstPersonController(
    speed=8,
    position=(0, 0, 0),
    scale=1,
)
player.camera_pivot.x = 0
player.camera_pivot.z = -2
player.camera_pivot.y = 3

player.cursor.enabled = False

actor = Actor("../assets/models/Player.glb")
actor.reparent_to(player)
actor.setScale(1)
actor.setColor(color.peach)
actor.setHpr(180, 0, 0)

random_cube = Entity(
    model="cube",
    position=(5,1,5),
    collider="box",
    texture="../assets/textures/WindowGlass.png"
)

Sky()

interact_text = Text(
    text="E To Interact",
    origin=(0,-15),
)

interact_text.create_background()

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

hasSaveFile = os.path.exists("../save_file.json")

save_data = {
    "player_position": [0, 0, 0]
}

if hasSaveFile:
    with open("../save_file.json", "r") as f:
        data = json.load(f)

        player.position = Vec3(data["player_position"][0], data["player_position"][1], data["player_position"][2])
else:
    with open('../save_file.json', 'w') as file:
        json.dump(save_data, file)

def save_game():
    with open("../save_file.json", "w") as f:
        save_data["player_position"] = list(player.position)

        json.dump(save_data, f)

respawn_button.on_click = player_respawn

test_convo = Conversation()
test_convo.enabled = False

convo = dedent('''
    On skibidi this is so sigma
    Oi oi oi baka what do you think?
        * On god this is so sigma
            Wow I can't believe you picked this
        * What are you talking about?
            Oi oi oi you are not a nonchalant sigma
''')

def update():
    global doing_walking_animation
    global is_jumping
    global is_interacting

    invoke(save_game, delay=10)

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

    if distance(player.position, random_cube.position) < 2 and not is_interacting:
        interact_text.enabled = True
    else:
        interact_text.enabled = False

    if interact_text.enabled and held_keys['e'] and not is_interacting:
        is_interacting = True
        Audio("../assets/sounds/ItemPickup.wav").play()
        mouse.locked = False
        test_convo.enabled = True
        test_convo.start_conversation(convo)
    if is_interacting and not test_convo.enabled:
        is_interacting = False
        mouse.locked = True
        test_convo.enabled = False

    if player.position.y_getter() < -10:
        player_die()

app.run()