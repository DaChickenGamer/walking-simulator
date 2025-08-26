import os

from ursina.prefabs.conversation import Conversation

class DialogueManager():
    def __init__(self):
        self.dialogues = {}
        self.get_all_dialogues()
        self.active_dialogue = None

        self.conversation = Conversation()
        self.conversation.enabled = False

    def start_conversation(self, conversation_name):
        if not self.active_dialogue is None:
            print(self.active_dialogue + " has already started")
            return

        self.active_dialogue = conversation_name

        dialogue_text = self.dialogues.get(conversation_name)
        if dialogue_text is None:
            print(f"Dialogue '{conversation_name}' not found.")
            return

        self.conversation.enabled = True
        self.conversation.start_conversation(dialogue_text)

    def end_conversation(self):
        if not self.active_dialogue is None:
            print("No active dialogue to end.")
            return

        self.active_dialogue = None
        self.conversation.enabled = False
        self.conversation.end_conversation()

    def get_all_dialogues(self):
        self.dialogues.clear()

        for file in os.listdir("./scripts/dialogue/dialogues/"):
            if file.endswith(".txt"):
                with open("./scripts/dialogue/dialogues/" + file, "r") as f:
                    dialogue_text = f.read()
                    dialogue_name = os.path.splitext(file)[0]
                    self.dialogues[dialogue_name] = dialogue_text
        return self.dialogues

dialogue_manager = DialogueManager()