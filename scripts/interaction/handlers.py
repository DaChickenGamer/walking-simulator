from ursina import *
from scripts.dialogue.manager import dialogue_manager

def activate_dialogue(conversation_name):
    Audio("../../assets/sounds/ItemPickup.wav").play()
    mouse.locked = False
    dialogue_manager.start_conversation(conversation_name)

def deactivate_dialogue():
    mouse.locked = True
    dialogue_manager.end_conversation()