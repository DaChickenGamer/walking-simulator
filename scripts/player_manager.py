from direct.actor.Actor import Actor
from ursina import color, Text, Button, invoke, held_keys, Vec3
from ursina.prefabs.first_person_controller import FirstPersonController

from scripts.save_manager import save_game_data


class Player:
    def __init__(self):
        self.player_object = self.initialize_player()
        self.actor = self.create_actor()

        self.death_text = Text(
            text="You Died",
            origin=(0,0),
        )

        self.death_text.create_background()
        self.death_text.enabled = False

        self.respawn_button = Button(
            text="Respawn",
            scale=(.15, .07),
            origin=(0, 1.5),
        )

        self.respawn_button.enabled = False
        self.respawn_button.on_click = self.respawn

        self.is_jumping = False
        self.doing_walking_animation = False

    def initialize_player(self):
        player_object = FirstPersonController(
            speed=8,
            position=(0, 0, 0),
            scale=1,
        )
        player_object.camera_pivot.x = 0
        player_object.camera_pivot.z = -2
        player_object.camera_pivot.y = 3

        player_object.cursor.enabled = False

        return player_object

    def create_actor(self):
        actor = Actor("../assets/models/Player.glb")
        actor.reparent_to(self.player_object)
        actor.setScale(1)
        actor.setColor(color.peach)
        actor.setHpr(180, 0, 0)
        return actor

    def update(self):
        invoke(save_game_data, player.player_object, delay=10)

        is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
        if is_moving and not self.doing_walking_animation:
            self.actor.loop("Walk_Loop")
            self.doing_walking_animation = True

        elif not is_moving and self.doing_walking_animation:
            self.actor.loop("Idle_Loop")
            self.doing_walking_animation = False

        if held_keys['space']:
            self.is_jumping = True
            self.actor.stop()
            self.actor.play("Jump_Loop")

        if self.is_jumping and self.player_object.grounded:
            self.is_jumping = False
            self.actor.stop()
            self.actor.play("Idle_Loop")

        if self.player_object.position.y_getter() < -10:
            self.die()

    def die(self):
        self.death_text.enabled = True
        self.respawn_button.enabled = True
        self.player_object.enabled = False
        self.player_object.cursor.enabled = True

    def respawn(self):
        self.death_text.enabled = False
        self.respawn_button.enabled = False
        self.player_object.enabled = True
        self.player_object.cursor.enabled = False
        self.player_object.position = Vec3(0, 0, 0)

player = Player()