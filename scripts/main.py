from ursina import *
app = Ursina()

from save_manager import load_game_data
from interaction.manager import interaction
from dialogue.manager import dialogue_manager
from interaction.handlers import activate_dialogue, deactivate_dialogue
from world_manager import create_world
from player_manager import player

# TODO Add a character model to interact with


window.title = "Walking Simulator"
window.borderless = True
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

create_world()

load_game_data(player=player.player_object)


def update():
    player.update()
    interaction.update(player.player_object.position)

app.run()