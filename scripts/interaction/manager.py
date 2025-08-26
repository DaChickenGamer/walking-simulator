from ursina import *
from scripts.interaction.handlers import activate_dialogue, deactivate_dialogue

class Interaction:
    def __init__(self):
        self.interaction_text = self.init_text()
        self.targets = []
        self.is_interacting = False

    def update(self, player_position):
        target = interaction.get_nearby_target(player_position)

        if target and not interaction.is_interacting:
            interaction.show_prompt()
        else:
            interaction.hide_prompt()

        if held_keys['e'] and target and not interaction.is_interacting:
            interaction.start_interaction(activate_dialogue("test"))

        if interaction.is_interacting and not target:
            interaction.stop_interaction(deactivate_dialogue())

    def init_text(self):
        text = Text("E To Interact", origin=(0, -15))
        text.create_background()
        text.enabled = False
        return text

    def add_target(self, obj, interaction_range=2):
        self.targets.append((obj, interaction_range))

    def remove_target(self, obj):
        self.targets = [t for t in self.targets if t[0] != obj]

    def show_prompt(self):
        self.interaction_text.enabled = True

    def hide_prompt(self):
        self.interaction_text.enabled = False

    def is_prompt_visible(self):
        return self.interaction_text.enabled

    def get_nearby_target(self, player_position):
        for obj, r in self.targets:
            if distance(player_position, obj.position) < r:
                return obj
        return None

    def start_interaction(self, function=None):
        self.is_interacting = True
        self.hide_prompt()

        if function:
            function()


    def stop_interaction(self, function=None):
        self.is_interacting = False

        if function:
            function()

interaction = Interaction()